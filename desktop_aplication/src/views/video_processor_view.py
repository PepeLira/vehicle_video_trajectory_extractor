from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QFileDialog, QLabel
from .gps_reference_dialog import GPSReferenceDialog

class VideoProcessorView(QWidget):
    def __init__(self, aligners, detectors, aligner_filters, trajectory_filters):
        super().__init__()

        self.aligners = aligners
        self.detectors = detectors
        self.aligner_filters = aligner_filters
        self.trajectory_filters = trajectory_filters
        self.input_video = None
        self.reference_points = None

        self.initUI()

    def initUI(self):
        # Layout
        layout = QVBoxLayout(self)

        self.input_video_path = None
        self.setGeometry(300, 100, 400, 400)
        
        self.select_video_button = QPushButton("Select Video", self)
        layout.addWidget(self.select_video_button)

        self.select_points_button = QPushButton("Select Coordinates for Reference", self)
        self.select_points_button.clicked.connect(self.select_points_on_image)
        layout.addWidget(self.select_points_button)

        self.aligner_dropdown = QComboBox(self)
        self.aligner_dropdown.addItems(["None"] + self.parse_to_string(self.aligners))
        layout.addWidget(QLabel("Select Aligner:"))
        layout.addWidget(self.aligner_dropdown)

        self.aligner_filter_dropdown = QComboBox(self)
        self.aligner_filter_dropdown.addItems(["None"] + self.parse_to_string(self.aligner_filters))
        layout.addWidget(QLabel("Select Aligner Filter:"))
        layout.addWidget(self.aligner_filter_dropdown)

        self.detector_dropdown = QComboBox(self)
        self.detector_dropdown.addItems(["None"] + self.parse_to_string(self.detectors))
        layout.addWidget(QLabel("Select Detector:"))
        layout.addWidget(self.detector_dropdown)

        self.trajectory_filter_dropdown = QComboBox(self)
        self.trajectory_filter_dropdown.addItems(["None"] + self.parse_to_string(self.trajectory_filters))
        layout.addWidget(QLabel("Select Trajectory Extractor Filter:"))
        layout.addWidget(self.trajectory_filter_dropdown)

        self.process_video_button = QPushButton("Process Video", self)
        layout.addWidget(self.process_video_button)

        self.save_transformations_button = QPushButton("Export Video Transformations", self)
        layout.addWidget(self.save_transformations_button)

        self.save_trajectories_button = QPushButton("Export Trajectories", self)
        layout.addWidget(self.save_trajectories_button)

        self.selected_video_label = QLabel("No video selected", self)
        layout.addWidget(self.selected_video_label)

        self.progress_label = QLabel("Progress: 0%", self)
        layout.addWidget(self.progress_label)
        
        self.setLayout(layout)
        self.setWindowTitle("Video Processor")
        self.show()

    def get_user_input(self):
        selected_aligner = self.get_selected_object(self.aligners, self.aligner_dropdown.currentText())
        selected_detector = self.get_selected_object(self.detectors, self.detector_dropdown.currentText())
        selected_aligner_filter = self.get_selected_object(self.aligner_filters, self.aligner_filter_dropdown.currentText())
        selected_trajectory_filter = self.get_selected_object(self.trajectory_filters, self.trajectory_filter_dropdown.currentText())
        
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
        # Raise an error if no video is selected
        if self.input_video is None:
            raise ValueError("No video selected")

        reference_image = self.input_video.get_reference_frame()

        dialog = GPSReferenceDialog(image_array = reference_image)
        dialog.exec_()

        if not dialog.coordinates_mapping_is_empty():
            self.reference_points = dialog.get_coordinates_mapping()
            print(self.reference_points)

    def update_progress(self, progress):
        self.progress_label.setText(f"Progress: {progress}%")

    def display_results(self, results):
        self.results_label.setText(f"Results: {results}")

    def select_video(self, set_input_video):
        self.input_video_path, _ = QFileDialog.getOpenFileName(self, "Select Video", "", "Video Files (*.mp4 *.avi)")
        if self.input_video_path:
            self.selected_video_label.setText(self.input_video_path)
            self.input_video = set_input_video(self.input_video_path)
    
    def export_csv_dialog(self, format):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export CSV file", "", "CSV Files (*.csv)")
        if file_path:
            format(output_path = file_path)

    def parse_to_string(self, elements):
        return list(map(str, elements))
    
    
