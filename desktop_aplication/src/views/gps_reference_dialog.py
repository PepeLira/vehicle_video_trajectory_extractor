import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk

class GPSReferenceDialog(ctk.CTkToplevel):
    def __init__(self, image_array=None, call=None):
        super().__init__()
        self.title("Image Coordinate Picker")
        self.image_array = image_array
        self.colors = ['red', 'blue', 'green', 'yellow', 'purple']  # List of colors to cycle through
        self.current_color_index = 0  # Index of the current color
        self.call = call
        self.selected_points = []
        self.gps_entries = []
        self.coordinates_mapping = {}

        self.initUI()

    def initUI(self):
        # Container frame for the canvas and scrollbars
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas for displaying the image
        self.canvas = tk.Canvas(self.container, bg="gray", cursor="arrow")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, anchor="center")
        # Scrollbars that operate on the canvas
        self.v_scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.h_scrollbar = tk.Scrollbar(self.canvas, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill="x")

        self.canvas.config(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Button to load and display an image
        self.set_coords_button = ctk.CTkButton(self, text="Save Coordinates", command=self.prepare_and_accept)
        self.set_coords_button.pack(pady=10)

        # Bind mouse click event to the canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.display_image(self.image_array)

        # selected points label
        self.coords_label = ctk.CTkLabel(self, text="Selected Points: ")
        self.coords_label.pack(pady=2, padx=10, anchor="w")
        self.coords_label.configure(font=("Roboto", 12))

    def display_image(self, image_array=None):
        if image_array is not None:
            self.image = Image.fromarray(image_array)
            self.tk_image = ImageTk.PhotoImage(self.image)
            
        # else:
        #     self.image = Image.open(file_path)
        #     self.tk_image = ImageTk.PhotoImage(self.image)

            # Get image dimensions
            img_width = self.tk_image.width()
            img_height = self.tk_image.height()

            # Optionally, set a maximum window size to ensure the window isn't too large
            max_width = self.winfo_screenwidth()
            max_height = self.winfo_screenheight()
            window_width = min(img_width, max_width)
            window_height = min(img_height, max_height)

            # Set window size based on the image size (or maximum size)
            self.geometry(f"{window_width}x{window_height}")

            self.image_on_canvas = self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")
            self.update_image_position()

            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def update_image_position(self):
        # Calculate the center position
        self.canvas.config
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_width = self.tk_image.width()
        img_height = self.tk_image.height()
        x = (canvas_width - img_width) // 2
        y = (canvas_height - img_height) // 2

        # Move the image to the center
        self.canvas.coords(self.image_on_canvas, x, y)

    def on_canvas_configure(self, event):
        # Update the scroll region and re-center the image
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


    def on_canvas_click(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        print(f"Clicked at: {x}, {y}")

        color = self.colors[self.current_color_index]
        radius = 2
        # Draw a circle with the current color
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)
        # Add a text label near the click location with the coordinates
        self.canvas.create_text(x + 10, y, text=f"({x}, {y})", anchor="w")

        self.current_color_index = (self.current_color_index + 1) % len(self.colors)

        self.selected_points.append((x, y, color))
        coords_text = ", ".join([f"({x}, {y}, {color})" for x, y, color in self.selected_points])

        self.coords_label.configure(text=f"Selected Points: {coords_text}")

        self.add_gps_entry(coords_text=str((x, y, color)))

    def add_gps_entry(self, coords_text=""):
        gps_entry = ctk.CTkEntry(self, placeholder_text=f"Enter GPS coordinates for: {coords_text}")
        gps_entry.pack(pady=2, padx=10, fill="x")
        self.gps_entries.append(gps_entry)

    def accept(self):
        self.call(self.coordinates_mapping)
        self.destroy()

    def prepare_and_accept(self):
        if len(self.selected_points) >= 3 and len(self.gps_entries)>= 3:
            if len(self.selected_points) != len(self.gps_entries):
                print("You must enter the GPS coordinates for each selected point")
                self.show_error_dialog("You must enter the GPS coordinates for each selected point")
            else:
                for point, entry in zip(self.selected_points, self.gps_entries):
                    x, y, color = point
                    gps_coords = list(map(float,entry.get().split(",")))
                    self.coordinates_mapping[(x, y)] = gps_coords
        else:
            print("You must select at least 3 points and enter the GPS coordinates for each one")
            self.show_error_dialog("You must select at least 3 points and enter the GPS coordinates for each one")
        self.accept()


    def show_error_dialog(self, text):
        messagebox.showerror("An error occurred", text)

if __name__ == "__main__":
    app = GPSReferenceDialog()
    app.mainloop()
