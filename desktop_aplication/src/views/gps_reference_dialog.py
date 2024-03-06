import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from screeninfo import get_monitors

class GPSReferenceDialog(ctk.CTkToplevel):
    def __init__(self, image_array=None, call=None):
        super().__init__()
        self.monitor = [m for m in get_monitors() if m.is_primary][0]
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
        self.canvas = self.display_image(self.image_array)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        # Scrollbars that operate on the canvas
        self.v_scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.h_scrollbar = tk.Scrollbar(self.canvas, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill="x")

        # Button to load and display an image
        self.set_coords_button = ctk.CTkButton(self, text="Save Coordinates", command=self.prepare_and_accept)
        self.set_coords_button.pack(pady=10)
        
        # Bind mouse click event to the canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.canvas.config(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # selected points label
        self.coords_label = ctk.CTkLabel(self, text="Selected Points: ")
        self.coords_label.pack(pady=2, padx=10, anchor="w")
        self.coords_label.configure(font=("Roboto", 12))

    def display_image(self, image_array=None):
        if image_array is not None:
            original_image = Image.fromarray(image_array)
            
            # Get image dimensions
            self.img_width, self.img_height = original_image.size

            # Get maximum canvas dimensions based on the screen size
            max_width = self.monitor.width
            max_height = self.monitor.height

            print(max_width, max_height)

            # Calculate scaling factors for width and height
            self.scale_width = max_width / self.img_width
            self.scale_height = max_height / self.img_height

            # Use the smaller scaling factor to ensure the image fits within the canvas and maintains aspect ratio
            self.scale_factor = min(self.scale_width, self.scale_height)

            # Calculate new image dimensions
            self.new_width = int(self.img_width * self.scale_factor)
            self.new_height = int(self.img_height * self.scale_factor)

            # Resize the image with the new dimensions
            resized_image = original_image.resize((self.new_width, self.new_height), Image.Resampling.LANCZOS)

            # Convert the resized image for Tkinter
            self.tk_image = ImageTk.PhotoImage(resized_image)

            # Ensure the canvas is big enough for the resized image or fits within maximum dimensions
            canvas_width = min(self.new_width, max_width)
            canvas_height = min(self.new_height, max_height)

            # Create or update the canvas to fit the resized image
            canvas = tk.Canvas(self.container, bg="gray", cursor="arrow", width=canvas_width, height=canvas_height)
            canvas.pack(side=tk.LEFT, expand=True, anchor="center", fill=tk.BOTH)

            # Display the resized image centered in the canvas
            self.image_on_canvas = canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.tk_image, anchor="center")

            return canvas
        
    def convert_scaled_to_original_coords(self, scaled_x, scaled_y):
        # Calculate the original coordinates
        original_x = scaled_x / self.scale_factor
        original_y = scaled_y / self.scale_factor

        return original_x, original_y

    def on_canvas_configure(self, event):
        # Update the scroll region and re-center the image
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


    def on_canvas_click(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        print(f"Clicked at: {x}, {y}")

        
        original_x, original_y = self.convert_scaled_to_original_coords(x,y)
        original_x, original_y = round(original_x, 2), round(original_y, 2)

        color = self.colors[self.current_color_index]
        radius = 2*self.scale_factor
        # Draw a circle with the current color
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)
        # Add a text label near the click location with the coordinates
        self.canvas.create_text(
            x + 10, y, text=f"({original_x}, {original_y})", 
            anchor="w", font=("Roboto", int(14*self.scale_factor))
            )

        self.current_color_index = (self.current_color_index + 1) % len(self.colors)

        self.selected_points.append((original_x, original_y, color))
        coords_text = ", ".join([f"({x}, {y}, {color})" for x, y, color in self.selected_points])

        self.coords_label.configure(text=f"Selected Points: {coords_text}")

        self.add_gps_entry(coords_text=str((original_x, original_y, color)))

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
