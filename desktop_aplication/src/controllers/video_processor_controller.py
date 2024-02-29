from models.input_video import InputVideo
from .controller_helper import ControllerHelper
import csv

class VideoProcessorController:
    def __init__(self, ui_view, video_processor):
        self._ui_view = ui_view
        self._video_processor = video_processor
        self.input_video = None
        self._ui_view.progress_changed.connect(self._ui_view.update_progress)
        self.event_listener()

    def event_listener(self):
        self._ui_view.select_video_button.clicked.connect(self.select_video)
        self._ui_view.process_video_button.clicked.connect(self.start_processing)
        self._ui_view.save_transformations_button.clicked.connect(self.export_transformations_csv)
        self._ui_view.save_trajectories_button.clicked.connect(self.export_trajectories_csv)
        self._ui_view.save_video_button.clicked.connect(self.save_video)
    
    def start_processing(self):
        self.set_parameters()
        
        if self._video_processor.aligner is None and self._video_processor.detector is None:
            raise ValueError("An aligner or a detector must be set before processing video")
        if self._ui_view.input_video_path is None:
            raise ValueError("Input video must be set before processing video")
        
        self.trajectories, self.affine_transformations = self._video_processor.process_video(self.input_video)
        reference_points = self._ui_view.reference_points

        if len(reference_points) >= 3:
            self.trajectories = ControllerHelper.add_meters_2_trajectory(reference_points, self.trajectories)
        

        self._ui_view.enable_save_results() # Processing Finished, enable save results buttons

    def set_parameters(self):
        parameters = self._ui_view.get_user_input()
        if parameters["aligner"] != None:
            self._video_processor.set_aligner(parameters["aligner"])
            if parameters["aligner_filter"] != None:
                self._video_processor.add_aligner_filter(parameters["aligner_filter"])
        if parameters["detector"] != None:
            self._video_processor.set_detector(parameters["detector"])
            if parameters["trajectory_filter"] != None:
                self._video_processor.add_trajectory_extractor_filter(parameters["trajectory_filter"])

    def select_video(self):
        self._ui_view.select_video(self.set_input_video)

    def export_transformations_csv(self):
        self._ui_view.export_csv_dialog(self.record_affine_transformations_csv, file_name="affine_transformations")

    def export_trajectories_csv(self):
        self._ui_view.export_csv_dialog(self.record_trajectories_csv, file_name="trajectories")
    
    def save_video(self):
        self._ui_view.save_video_dialog(self.input_video.save_processed_video, file_name="tracked_video")
    
    def set_input_video(self, input_video_path):
        self.input_video = InputVideo(input_video_path)
        self.input_video.update_progress(self._ui_view.update_progress)
        self.input_video.display_frame_call(self._ui_view.update_image)
        return self.input_video
        
    def record_trajectories_csv(self, output_path="trajectories.csv"):
        '''
        Input: 
        trajectories = {
            1: {"x_trajectory": [10, 11], "y_trajectory": [20, 21], "class": "car", "frames": [1, 2]},
            2: {"x_trajectory": [20], "y_trajectory": [40], "class": "car", "frames": [1]}
        }

        Output CSV format:
        | id de vehículo | class | número de frame | posición en i | posición en j |
        | ---            | ---   | ---             | ---           | ---          |
        | 1              | car   | 1               | 10            | 20           |
        | 1              | car   | 2               | 11            | 21           |
        | 2              | car   | 1               | 20            | 40           |
        '''

        with open(output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(['id de vehículo', 'class', 
                             'número de frame', 
                             'posición en i', 
                             'posición en j', 
                             'posición en x (metros)', 
                             'posición en y (metros)',  
                             'tiempo', 
                             'velocidad x (metros)',  
                             'velocidad y (metros)'])
            
            for vehicle_id, data in self.trajectories.items():
                x_trajectory = data['x_trajectory']
                y_trajectory = data['y_trajectory']
                vehicle_class = data['class']
                frames = data['frames'] 
                time = data['time']

                if 'speed_x' in data.keys():
                    x_speeds = data['speed_x']
                    y_speeds = data['speed_y']
                    m_coords_x = data['x_m_trajectory']
                    m_coords_y = data['y_m_trajectory']
                
                    for i, (x, y, frame, t, x_m, y_m, x_s, y_s) in enumerate(zip(x_trajectory, y_trajectory, 
                                                             frames, 
                                                             time, 
                                                             m_coords_x, m_coords_y, 
                                                             x_speeds, y_speeds)):
                        writer.writerow([vehicle_id, vehicle_class, frame, x, y,
                                        x_m, y_m, t, 
                                        x_s, y_s])
                else:
                    for i, (x, y, frame, t) in enumerate(zip(x_trajectory, y_trajectory, frames, time)):
                        writer.writerow([vehicle_id, vehicle_class, frame, x, y, 0, 0, t, 0, 0])


    def record_affine_transformations_csv(self, output_path="affine_transformations.csv"):
        '''
        Input: 
        affine_transformations = [
            [theta, s, tx, ty],
            [theta, s, tx, ty],
            ...
        ] 
        len(affine_transformations) = frame number
        Output:
        | número de frame | theta |  s  | tx  | ty  |
        | ---             | ---   | --- | --- | --- |
        | 1               | 0.0   | 0.0 | 0.0 | 0.0 | #first frame is the reference frame
        | 2               | 0.2   | 0.3 | 0.4 | 0.5 |
        '''

        with open(output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(['número de frame', 'theta', 's', 'tx', 'ty'])
            
            # Write data
            for frame_number, affine_transformation in enumerate(self.affine_transformations):
                theta, s, tx, ty = affine_transformation
                writer.writerow([frame_number, theta, s, tx, ty])
    