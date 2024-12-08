## Wind Analysis Application

### Overview
The Wind Analysis Application is a Python-based tool designed to analyze wind data and generate various visualizations, including wind rose plots, scatter plots, and cumulative probability plots. The application reads wind data from CSV files, processes the data, and generates visualizations to help understand wind patterns and distributions.

### Features
Wind Rose Plot: Visualizes the distribution of wind speeds and directions.
Scatter Plot: Displays wind speed data on a polar plot.
Cumulative Probability Plot: Shows the cumulative probability of wind velocities.
Data Cleaning: Excludes specified wind values and filters data based on direction ranges.
CSV Export: Saves the results of the analysis to CSV files.

### Project Structure

Wind_Analysis_Application/
    Wind_App.py
    Wind_Function.py
    WindData/
        clean_data_results.csv
        More_wind_data/
        Probability_results.csv
        Wind_Data.csv
    .gitattributes

### Installation

1. Clone the repository:

git clone (https://github.com/shahinfa9999/Wind_Application.git)
cd Wind_Analysis_Application

2. Install the required dependencies:
pip install -r requirements.txt

### Usage

1. Run the application:
python Wind_App.py

2. Use the GUI to select the directory containing the wind data CSV files and specify the analysis parameters:

Directory Path: Path to the directory containing the wind data files.
Station Name: Name of the station to filter the files.
Speed Bins: Number of bins for wind speed in the wind rose plot.
Direction Bins: Number of bins for wind direction in the wind rose plot.
Max Direction: Maximum direction value to include in the analysis.
Min Direction: Minimum direction value to include in the analysis.
Wind Values to Exclude: Comma-separated list of wind values to exclude from the analysis.

3. Click "Run Analysis" to perform the analysis and generate the visualizations. The results will be saved as CSV files in the specified directory.

### Functions
Wind_App.py
WindApp: Main application class that initializes the GUI and handles user interactions.
browse_directory: Opens a file dialog to select the directory containing wind data files.
run_analysis: Runs the wind data analysis using the specified parameters.
Wind_Function.py
read_wind_data: Reads wind data from CSV files in the specified directory.
clean_data: Cleans the wind data by excluding specified values and filtering by direction range.
plot_wind_rose: Generates a wind rose plot.
plot_wind_scatter: Generates a scatter plot of wind data.
Plot_wind_probability: Generates a cumulative probability plot of wind velocities.
csv_writer: Writes the analysis results to a CSV file.
csv_writer_cleandata: Writes the cleaned wind data to a CSV file.
WindRose: Main function that orchestrates the wind data analysis and visualization.

### Acknowledgements
Matplotlib
Pandas
NumPy