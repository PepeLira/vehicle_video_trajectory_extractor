import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from .gps_reference_dialog import GPSReferenceDialog
from .custom_file_dialog import CustomFileDialog
import numpy as np
import cv2

def get_dpi_scaling():
    root = tk.Tk()
    scaling_factor = root.winfo_fpixels('1i') / 72 
    root.destroy()
    return scaling_factor

class VideoProcessorView(ctk.CTk):

    APP_NAME = "RastreoAéreo: Video Processor"
    WIDTH = 1000
    HEIGHT = 800

    def __init__(self, aligners, detectors, aligner_filters, trajectory_filters):
        super().__init__()

        self.geometry(f"{VideoProcessorView.WIDTH}x{VideoProcessorView.HEIGHT}")
        self.font = 'Roboto'
        
        self.scaling_factor = get_dpi_scaling()
        ctk.set_widget_scaling(self.scaling_factor*0.8)

        self.aligners = aligners
        self.detectors = detectors
        self.aligner_filters = aligner_filters
        self.trajectory_filters = trajectory_filters
        self.input_video = None
        self.reference_points = []
        self.progress = 0
        self.image_array = None
        self.input_video_path = None

        self.setup_ui()


    def setup_ui(self):
        ctk.set_appearance_mode("dark")  
        ctk.set_default_color_theme("blue") 

        self.title(VideoProcessorView.APP_NAME)

        # Layout Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ============ Frame Setup ============
        # Frame for buttons and dropdowns
        self.frame_left = ctk.CTkFrame(master=self, width=200, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.frame_left.grid_propagate(False)

        # Frame for image display
        self.frame_right = ctk.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame_right.grid_rowconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(0, weight=1)

        # Frame for some text or additional controls
        self.frame_bottom = ctk.CTkFrame(master=self, height=100, corner_radius=0)
        self.frame_bottom.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.frame_bottom.grid_propagate(False)

        # ============ Frame Left Components ============
        self.add_top_left_widgets(self.frame_left)

        # ============ Frame Right Components ============
        self.add_top_right_widgets(self.frame_right)

        # ============ Frame Bottom Components ============
        self.add_bottom_widgets(self.frame_bottom)
    
    def add_top_left_widgets(self, frame):
        self.select_video_button = ctk.CTkButton(frame, text="Select Video")
        self.select_video_button.pack(pady=5 , fill="x", padx=(20, 20))

        self.select_points_button = ctk.CTkButton(frame, text="Select Coordinates for Reference")
        self.select_points_button.pack(pady=5 , fill="x", padx=(20, 20))
        self.select_points_button.configure(command=self.select_points_on_image)

        self.aligner_dropdown_title, self.aligner_dropdown = self.configure_dropdown(
            frame, self.aligners, title="Select Aligner:"
        )
        self.aligner_dropdown_title.pack(pady=(10, 0), padx=(20, 20), anchor="w")
        self.aligner_dropdown.pack(pady=2, padx=(20, 20), fill="x")

        self.aligner_filter_title, self.aligner_filter_dropdown = self.configure_dropdown(
            frame, self.aligner_filters, title="Select Aligner Filter:"
        )
        self.aligner_filter_title.pack(pady=(10, 0), padx=(20, 20), anchor="w")
        self.aligner_filter_dropdown.pack(pady=2, padx=(20, 20), fill="x")

        self.detector_dropdown_title, self.detector_dropdown = self.configure_dropdown(
            frame, self.detectors, title="Select Trajectory Extractor:"
        )
        self.detector_dropdown_title.pack(pady=(10, 0), padx=(20, 20), anchor="w")
        self.detector_dropdown.pack(pady=2, padx=(20, 20), fill="x")

        self.trajectory_filter_title, self.trajectory_filter_dropdown = self.configure_dropdown(
            frame, self.trajectory_filters, title="Select Trajectory Extractor Filter:"
        )
        self.trajectory_filter_title.pack(pady=(10, 0), padx=(20, 20), anchor="w")
        self.trajectory_filter_dropdown.pack(pady=2, padx=(20, 20), fill="x")

        self.process_video_button = ctk.CTkButton(frame, text="Process Video")
        self.process_video_button.pack(pady=5 , fill="x", padx=(20, 20))

        self.save_transformations_button = ctk.CTkButton(frame, text="Export Video Transformations")
        self.save_transformations_button.pack(pady=5 , fill="x", padx=(20, 20))
        self.save_transformations_button.configure(state=ctk.DISABLED)

        self.save_trajectories_button = ctk.CTkButton(frame, text="Export Trajectories")
        self.save_trajectories_button.pack(pady=5 , fill="x", padx=(20, 20))
        self.save_trajectories_button.configure(state=ctk.DISABLED)

        self.save_video_button = ctk.CTkButton(frame, text="Save Video with Results")
        self.save_video_button.pack(pady=5 , fill="x", padx=(20, 20))
        self.save_video_button.configure(state=ctk.DISABLED)
    
    def add_top_right_widgets(self, frame):
        self.image_container = tk.Canvas(frame) 
        self.image_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, anchor="center")

        # Scrollbars that operate on the canvas
        self.v_scrollbar = tk.Scrollbar(self.image_container, orient="vertical", command=self.image_container.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.h_scrollbar = tk.Scrollbar(self.image_container, orient="horizontal", command=self.image_container.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill="x")

        self.image_container.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.image_container.bind("<Configure>", self.on_canvas_configure)

    def add_bottom_widgets(self, frame):
        self.selected_video_label = ctk.CTkLabel(frame, text="No video selected", anchor="w")
        self.selected_video_label.pack(pady=5, padx=10)

        self.progress_var = tk.StringVar()
        self.progress_label = ctk.CTkLabel(frame, text="Progress: 0%", textvariable= self.progress_var, anchor="w")
        self.progress_label.pack(pady=5, padx=10)

    def on_canvas_configure(self, event):
        # Update the scroll region and re-center the image
        self.image_container.config(scrollregion=self.image_container.bbox("all"))

    def configure_dropdown(self, frame, options, title="Select Option:"):
        title = ctk.CTkLabel(frame, text=title, font=(self.font, 15))
        dropdown_options = ["None"] + self.parse_to_string(options)
        dropdown = ctk.CTkOptionMenu(frame, values=dropdown_options)

        return title, dropdown
    
    def parse_to_string(self, elements):
        return list(map(str, elements))
    
    def get_user_input(self):
        selected_aligner = self.get_selected_object(self.aligners, self.aligner_dropdown.get())
        selected_detector = self.get_selected_object(self.detectors, self.detector_dropdown.get())
        selected_aligner_filter = self.get_selected_object(self.aligner_filters, self.aligner_filter_dropdown.get())
        selected_trajectory_filter = self.get_selected_object(self.trajectory_filters, self.trajectory_filter_dropdown.get())
        
        return {
            "aligner": selected_aligner,
            "detector": selected_detector,
            "aligner_filter": selected_aligner_filter,
            "trajectory_filter": selected_trajectory_filter
        }
    
    def get_selected_object(self, objects_list, selected_object_name):
        if selected_object_name == "None":
            return None
        else:
            return self.find_object_by_name(objects_list, selected_object_name)

    def find_object_by_name(self, objects_list, object_name):
        for obj in objects_list:
            if str(obj) == object_name:
                return obj
        return None
    
    def select_points_on_image(self):
        if self.input_video is None:
            self.show_error_dialog("No video selected")
            return

        reference_image = self.input_video.get_reference_frame()

        dialog = GPSReferenceDialog(image_array = reference_image, call= self.set_reference_points)
        dialog.grab_set()

    def set_reference_points(self, reference_points):
        self.reference_points = reference_points
        print(self.reference_points)
    
    def enable_save_results(self):
        self.save_transformations_button.configure(state=ctk.NORMAL)
        self.save_trajectories_button.configure(state=ctk.NORMAL)
        self.save_video_button.configure(state=ctk.NORMAL)
        self.process_video_button.configure(state=ctk.NORMAL)
        self.select_points_button.configure(state=ctk.NORMAL)
        self.select_video_button.configure(state=ctk.NORMAL)

    def disable_save_results(self):
        self.save_transformations_button.configure(state=ctk.DISABLED)
        self.save_trajectories_button.configure(state=ctk.DISABLED)
        self.save_video_button.configure(state=ctk.DISABLED)
        self.process_video_button.configure(state=ctk.DISABLED)
        self.select_points_button.configure(state=ctk.DISABLED)
        self.select_video_button.configure(state=ctk.DISABLED)

    def update_progress(self, progress, stage):
        self.progress_var.set(f"Progress: {progress}% - {stage}")
    
    def update_image(self):
        if not self.input_video.frames_queue.empty():
            image_array = self.input_video.frames_queue.get()
            image_array = Image.fromarray(image_array)
            image_array = ImageTk.PhotoImage(image_array)

            img_width = image_array.width()
            img_height = image_array.height()

            max_width = self.winfo_screenwidth()
            max_height = self.winfo_screenheight()
            window_width = min(img_width, max_width)
            window_height = min(img_height, max_height)

            self.image_container.create_image(0,0, image = image_array, anchor="nw")
            self.image_container.image = image_array  # Keep a reference! dont ask just do it or else >:( (3 days of debugging to find this out)

            self.image_container.config(scrollregion=self.image_container.bbox("all"))
        self.after(30, self.update_image)  # Adjust delay as needed

    def update_image_position(self):
        # Calculate the center position
        self.image_container.config
        canvas_width = self.image_container.winfo_width()
        canvas_height = self.image_container.winfo_height()
        img_width = self.tk_image.width()
        img_height = self.tk_image.height()
        x = (canvas_width - img_width) // 2
        y = (canvas_height - img_height) // 2

        # Move the image to the center
        self.image_container.coords(self.image_on_canvas, x, y)
        

    def select_video(self, set_input_video):
        self.set_input_video = set_input_video
        open_file_dialog = CustomFileDialog(
            title = "Select Video",
            file_types = [".mp4", ".avi"],
            mode = "open",
            on_close=self.open_filedialog_call,
            scale_factor=self.scaling_factor
        )
        open_file_dialog.grab_set()

    def export_csv_dialog(self, format, file_name="results"):
        self.format = format
        save_file_dialog = CustomFileDialog(
            mode="save",
            file_types =[".csv"],
            title ="Export CSV file",
            initialfile = file_name,
            on_close=self.save_filedialog_call,
            scale_factor=self.scaling_factor
        )
        save_file_dialog.grab_set()

    def save_video_dialog(self, format, file_name="tracked_video"):
        self.format = format
        save_file_dialog = CustomFileDialog(
            mode="save",
            file_types =[".mp4 "],
            title ="Save Video File",
            initialfile = file_name,
            on_close=self.save_filedialog_call,
            scale_factor=self.scaling_factor
        )
        save_file_dialog.grab_set()
    
    def clear_dropdowns(self):
        self.aligner_dropdown.set("None")
        self.aligner_filter_dropdown.set("None")
        self.detector_dropdown.set("None")
        self.trajectory_filter_dropdown.set("None")

    def open_filedialog_call(self, file_path):
        self.input_video_path = file_path
        
        if self.input_video_path:
            self.selected_video_label.configure(text = f"Selected Video: {self.input_video_path}")
            self.input_video = self.set_input_video(self.input_video_path)

    def save_filedialog_call(self, file_path):
        self.output_file_path = file_path
        
        if self.output_file_path:
            file_path = self.output_file_path
            self.format(output_path = file_path)

    
    def show_error_dialog(self, text):
        messagebox.showerror("An error occurred", text)

if __name__ == "__main__":
    app = VideoProcessorView()
    app.mainloop()
