import tkinter as tk
from tkinter import filedialog, messagebox
from Wind_Function import WindRose  # Import your WindRose function
 
class WindApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wind Data Analysis")
        self.root.configure(bg="#333333")
 
        # Create a sizable frame
        self.main_frame = tk.Frame(root, bg="#333333")
       
        # Configure the main window to be resizable
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
 
        # Make the frame resizable
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)  # Left padding column
        self.main_frame.grid_columnconfigure(1, weight=3)  # Main content column
        self.main_frame.grid_columnconfigure(2, weight=1)  # Right padding column
 
        # Directory Path
        self.dir_path = tk.StringVar()
        tk.Label(self.main_frame, text="Select Directory:", bg="#333333", fg="#FFFFFF").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(self.main_frame, textvariable=self.dir_path, width=50).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        tk.Button(self.main_frame, text="Browse", command=self.browse_directory, bg="#333333", fg="#FFFFFF").grid(row=0, column=2, padx=10, pady=10, sticky="ew")
 
        # Station Name
        self.station_name = tk.StringVar()
        tk.Label(self.main_frame, text="Station Name:", bg="#333333", fg="#FFFFFF").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(self.main_frame, textvariable=self.station_name).grid(row=1, column=1, padx=10, pady=10, sticky="ew")
 
        # Speed Bins
        self.speed_bins = tk.IntVar(value=6)
        tk.Label(self.main_frame, text="Speed Bins:", bg="#333333", fg="#FFFFFF").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(self.main_frame, textvariable=self.speed_bins).grid(row=2, column=1, padx=10, pady=10, sticky="ew")
 
        # Direction Bins
        self.direction_bins = tk.IntVar(value=20)
        tk.Label(self.main_frame, text="Direction Bins:", bg="#333333", fg="#FFFFFF").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(self.main_frame, textvariable=self.direction_bins).grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Max direction
        self.Max_Direction = tk.IntVar(value=360)
        tk.Label(self.main_frame, text="Highest direction value to include:", bg="#333333", fg="#FFFFFF").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(self.main_frame, textvariable=self.Max_Direction).grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Min direction
        self.Min_direction = tk.IntVar(value=0)
        tk.Label(self.main_frame, text="lowest direction value to include:", bg="#333333", fg="#FFFFFF").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(self.main_frame, textvariable=self.Min_direction).grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        # wind numbers to exclude 
        self.wind_exclude = tk.StringVar(value="9999,-9999")
        tk.Label(self.main_frame, text="Enter wind values to exclude (comma seperated):", bg="#333333", fg="#FFFFFF").grid(row=6, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(self.main_frame, textvariable=self.wind_exclude).grid(row=6, column=1, padx=10, pady=10, sticky="ew")
 
        # Run Button
        tk.Button(self.main_frame, text="Run Analysis", bg="#333333", fg="#FFFFFF", command=self.run_analysis).grid(row=7, column=1, pady=20, sticky="ew")
 
        self.main_frame.pack()
 
    def browse_directory(self):
        folder_selected = filedialog.askdirectory()
        self.dir_path.set(folder_selected)
 
    def run_analysis(self):
        dir_path = self.dir_path.get()
        station_name = self.station_name.get()
        speed_bins = self.speed_bins.get()
        direction_bins = self.direction_bins.get()
        min_direction=  self.Min_direction.get()
        max_direction = self.Max_Direction.get()
        wind_rmv = self.wind_exclude.get()

       
        if not dir_path or not station_name:
            messagebox.showerror("Error", "Directory path and station name are required!")
            return
 
        try:
            WindRose(dir_path, speed_bins, direction_bins, station_name, wind_rmv, max_direction, min_direction)  # Call your function
            messagebox.showinfo("Success", "Analysis completed and results saved!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
 
if __name__ == "__main__":
    root = tk.Tk()
    app = WindApp(root)
    root.mainloop()
 