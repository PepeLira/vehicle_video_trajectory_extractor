import csv

class VideoProcessorController:
    def __init__(self, ui_view, video_processor):
        self._ui_view = ui_view
        self._video_processor = video_processor
        self._event_listener()
    
    def start_processing(self):
        self.set_parameters()
        
        if self._video_processor.aligner is None and self._video_processor.detector is None:
            raise ValueError("An aligner or a detector must be set before processing video")
        if self._ui_view.input_video_path is None:
            raise ValueError("Input video must be set before processing video")
        
        self.trajectories, self.affine_transformations = self._video_processor.process_video(self._ui_view.input_video_path)
        print("Processing finished")

    def set_parameters(self):
        parameters = self._ui_view.get_user_input()
        if parameters["aligner"] != None:
            self._video_processor.set_aligner(parameters["aligner"])
            self._video_processor.add_aligner_filter(parameters["aligner_filter"])
        if parameters["detector"] != None:
            self._video_processor.set_detector(parameters["detector"])
            self._video_processor.add_trajectory_extractor_filter(parameters["trajectory_filter"])

    def _event_listener(self):
        self._ui_view.process_video_button.clicked.connect(self.start_processing)
        self._ui_view.save_transformations_button.clicked.connect(self.export_transformations_csv)
        self._ui_view.save_trajectories_button.clicked.connect(self.export_trajectories_csv)

    def export_transformations_csv(self):
        self._ui_view.export_csv_dialog(self.record_affine_transformations_csv)

    def export_trajectories_csv(self):
        self._ui_view.export_csv_dialog(self.record_trajectories_csv)

    def record_trajectories_csv(self, output_path="trajectories.csv"):
        '''
        Input: 
        trajectories = {
            1: {"x_trajectory": [10, 11], "y_trajectory": [20, 21], "class": "car", "frames": [1, 2]},
            2: {"x_trajectory": [20, 21], "y_trajectory": [40, 41], "class": "car", "frames": [1]}
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
            writer.writerow(['id de vehículo', 'class', 'número de frame', 'posición en i', 'posición en j'])
            
            # Write data
            for vehicle_id, data in self.trajectories.items():
                x_trajectory = data['x_trajectory']
                y_trajectory = data['y_trajectory']
                vehicle_class = data['class']
                frames = data['frames']
                
                for i, (x, y, frame) in enumerate(zip(x_trajectory, y_trajectory, frames)):
                    writer.writerow([vehicle_id, vehicle_class, frame, x, y])

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