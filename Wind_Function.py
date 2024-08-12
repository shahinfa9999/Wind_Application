import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
import csv
def read_wind_data(dir_path, station_name):
    wind_data = []
    direction_data = []
 
    for filename in os.listdir(dir_path):
        if station_name in filename:
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path):
                try:
                    df = pd.read_csv(file_path)
                    for index, row in df.iterrows():
                        try:
                            wind_value = float(row['speed'])
                            dir_value = float(row['direction'])
 
                            wind_data.append(wind_value)
                            direction_data.append(dir_value)
                        except ValueError:
                            continue
                except Exception as e:
                    print(f"An error occurred while processing file {file_path}: {e}")
    return wind_data, direction_data
 
def clean_data(wind_data, direction_data, wind_values_exclude, dir_high_range, dir_low_range):
    if len(wind_values_exclude)>0:
        try:
            wind_values_exclude = [float(num) for num in wind_values_exclude.strip().split(',')]
        except ValueError:
            wind_values_exclude = -1
            print ("No wind values excluded")
            pass
    else:
        wind_values_exclude = -1
    clean_wind = []
    clean_dir = []
    for wind, direction in zip(wind_data, direction_data):
        if wind not in wind_values_exclude:
            if direction<= dir_high_range and direction>=dir_low_range:
                clean_wind.append(wind)
                clean_dir.append(direction)
    return clean_wind, clean_dir
 
def plot_wind_rose(wind_data, direction_data, speed_bins, direction_bins):
    wind_directions_rad = np.deg2rad(direction_data)
    quantilesS = np.linspace(0, 1, speed_bins + 1)
    speed_bins = np.quantile(wind_data, quantilesS)
    speed_bins[-1] = np.inf
    speed_bins[0] = 0
    num_bins = len(speed_bins) - 1
 
    num_dir_bins = direction_bins
    quantilesD = np.linspace(0, 1, num_dir_bins + 1)
    dir_bins = np.quantile(wind_data, quantilesD)
    num_dir_bins = len(dir_bins) - 1
    direction_bin_edges = np.linspace(0, 2 * np.pi, num_dir_bins + 1)
 
    hist = np.zeros((num_dir_bins, num_bins))
    for speed, direction in zip(wind_data, wind_directions_rad):
        speed_bin = np.digitize(speed, speed_bins) - 1
        direction_bin = np.digitize(direction, direction_bin_edges) - 1
        if speed_bin < num_bins and direction_bin < num_dir_bins:
            hist[direction_bin, speed_bin] += 1
 
    max_frequency = np.max(hist)
    rticks = np.linspace(0, max_frequency*2, num=5)[1:]
   
    fig, ax = plt.subplots(figsize=(15, 15), subplot_kw={'projection': 'polar'})
    colors = plt.cm.viridis(np.linspace(0, 1, num_bins))
 
    for i in range(num_bins):
        ax.bar(direction_bin_edges[:-1], hist[:, i], width=np.diff(direction_bin_edges),
               bottom=np.sum(hist[:, :i], axis=1), color=colors[i], edgecolor='k', alpha=0.7, label=f'{speed_bins[i]}-{speed_bins[i+1]} mph')
 
    ax.set_yticklabels([])
    labels = [f'{speed_bins[i]}-{speed_bins[i+1]}' if speed_bins[i+1] != np.inf else f'{speed_bins[i]}+ mph' for i in range(num_bins)]
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.arange(0, 360, 45), labels=['0°', '45°', '90°', '135°', '180°', '225°', '270°', '315°'])
 
    for r in rticks:
        ax.text(np.deg2rad(80), r, f'{int(r)}', ha='center', va='center', fontsize=10,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))
    ax.set_yticks(rticks)
    ax.set_title('Wind Rose Plot', pad=15)
 
    plt.legend(labels, title='Wind Speed (mph)', loc='upper right', bbox_to_anchor=(1.1, 1.1))
    plt.show()
 
def plot_wind_scatter(wind_data, direction_data):
    wind_directions_rad = np.deg2rad(direction_data)
   
    fig, ax = plt.subplots(figsize=(15, 15), subplot_kw={'projection': 'polar'})
    sc = ax.scatter(wind_directions_rad, wind_data, c=wind_data, cmap='viridis', alpha=0.7, edgecolors='k')
 
    cbar = plt.colorbar(sc, ax=ax, orientation='vertical', pad=0.1)
    cbar.set_label('Wind Speed (mph)')
 
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.arange(0, 360, 45), labels=['0°', '45°', '90°', '135°', '180°', '225°', '270°', '315°'])
    ax.set_title('Wind Rose Scatter Plot', pad=20)
 
    dfw = pd.Series(wind_data)
    min_value = dfw.min()
    max_value = dfw.max()
    radial_ticks = np.linspace(min_value, max_value, num=5)
    ax.set_yticklabels([])  # Clear default labels
    for r in radial_ticks:
        ax.text(np.deg2rad(23), r, f"{r:.2f} mph", ha='center', va='center', fontsize=8,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))
    ax.set_yticks(radial_ticks)
   
 
    plt.show()
 
def vlookup_interpolated(df, lookup_value, column_to_search, column_to_return):
    x = df[column_to_search]
    y = df[column_to_return]
    return float(np.interp(lookup_value, x, y))
 
def Plot_wind_probability (wind_data):
    wind_overwater_df = pd.DataFrame({
    'speed_mph': [1.98, 1.75, 1.5, 1.25, 1.1, 1.0, 0.98, 0.95, 0.925, 0.90, 0.895,0.89],
    'Uw/Ui': [2, 5, 9.5, 17, 25.5, 34, 37.5, 43, 48, 60, 64,100]
    })
    wind_clean_overwater=[]
    for num in wind_data:
        if num<150:
            conv=vlookup_interpolated(wind_overwater_df,num,"Uw/Ui","speed_mph")
            wind_clean_overwater.append(num*conv)
 
    wind_speeds = wind_clean_overwater
 
    # Sort the wind velocities
    sorted_wind_velocities_overwater = np.sort(wind_speeds)
    # Calculate the cumulative frequencies
    cumulative_frequencies_overwater = np.arange(1, len(sorted_wind_velocities_overwater) + 1) / len(sorted_wind_velocities_overwater)
    cumulative_frequencies_overwater =[1-cumulative_frequencies_overwater[i] for i in range(len(cumulative_frequencies_overwater))]
    # Sort the wind velocities
    sorted_wind_velocities_overland = np.sort(wind_data)
    # Calculate the cumulative frequencies
    cumulative_frequencies_overland = np.arange(1, len(sorted_wind_velocities_overland) + 1) / len(sorted_wind_velocities_overland)
    cumulative_frequencies_overland =[1.000-cumulative_frequencies_overland[i] for i in range(len(cumulative_frequencies_overland))]
    # Create the plot
    plt.plot(sorted_wind_velocities_overwater, cumulative_frequencies_overwater, label="Over Water Windspeed")
    plt.plot(sorted_wind_velocities_overland, cumulative_frequencies_overland,label="Over Land Windspeed")
    plt.yscale('log')
    plt.title('Cumulative Probability of Wind Velocities')
    plt.xlabel('Wind Velocity (mph)')
    plt.ylabel('Cumulative Probability')
    plt.legend()
    plt.grid(True, which='both')
    plt.show()
    return sorted_wind_velocities_overwater, cumulative_frequencies_overwater,sorted_wind_velocities_overland,cumulative_frequencies_overland
 
def csv_writer (dir, col1_name, col2_name,col3_name, col4_name, col1_data, col2_data,col3_data, col4_data):
    file_path = os.path.join(dir, "Probability_results.csv")
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([col1_name, col2_name,col3_name,col4_name])
        writer.writerows(zip(col1_data, col2_data,col3_data,col4_data ))

def csv_writer_cleandata (dir, col1_name, col2_name, col1_data, col2_data):
    file_path = os.path.join(dir, "clean_data_results.csv")
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([col1_name, col2_name])
        writer.writerows(zip(col1_data, col2_data))
 
def WindRose(diri, speed_bins, direction_bins_input, name, wind_values_exclude, dir_high_range, dir_low_range):
    wind_data, direction_data = read_wind_data(diri, name)
    wind_data, direction_data = clean_data(wind_data, direction_data, wind_values_exclude, dir_high_range, dir_low_range)
   
    print("Wind data count:", len(wind_data))
    print("Direction data count:", len(direction_data))
    print("Max wind speed:", max(wind_data))
    print("Max wind direction:", max(direction_data))
 
    plot_wind_rose(wind_data, direction_data, speed_bins, direction_bins_input)
    plot_wind_scatter(wind_data, direction_data)
    sorted_wind_velocities_overwater, cumulative_frequencies_overwater,sorted_wind_velocities_overland,cumulative_frequencies_overland=Plot_wind_probability(wind_data)
    col1,col2,col3,col4='Over Water Wind Velocity (mph)', 'Over Water cumulative frequencies', "Over Land Wind Velocity (mph)","Over Land cumulative frequencies"
    csv_writer(diri,col1,col2,col3,col4,sorted_wind_velocities_overwater, cumulative_frequencies_overwater,sorted_wind_velocities_overland,cumulative_frequencies_overland)
    csv_writer_cleandata(diri,"wind_speed" , "wind_direction",wind_data,direction_data)

 