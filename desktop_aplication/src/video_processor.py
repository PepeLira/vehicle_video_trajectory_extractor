import csv

class VideoProcessor:
    def __init__(self, aligner_filter_chain, trajectory_filter_chain):
        self.aligner_filter_chain = aligner_filter_chain
        self.trajectory_filter_chain = trajectory_filter_chain
        self.aligner = None
        self.detector = None
    
    def process_video(self, video_path):
        # Implements the flow processing the video
        if self.aligner is None and self.detector is None:
            raise ValueError("Aligner and detector must be set before processing video")
        
        if self.aligner != None:
            # TODO Apply aligner
            # TODO Apply filters to the aligner
            pass

        if self.detector != None:
            detections = self.detector.detect(video_path)
            trajectories = self.detector.get_trajectories(detections)
            
            # Filter trajectories
            trajectories = self.filter_trajectories(trajectories)

            # Record results
            self.record_csv_results(trajectories)

    def filter_trajectories(self, trajectories):
        for trajectory in trajectories.keys():
            trajectories[trajectory]["x_trajectory"] = self.trajectory_filter_chain.apply_filters(trajectories[trajectory]["x_trajectory"])
            trajectories[trajectory]["y_trajectory"] = self.trajectory_filter_chain.apply_filters(trajectories[trajectory]["y_trajectory"])
        return trajectories

    def set_aligner(self, aligner):
        self.aligner = aligner
    
    def set_detector(self, detector):
        self.detector = detector

    def add_aligner_filter(self, aligner_filter):
        self.aligner_filter_chain.add_filter(aligner_filter)
    
    def add_trajectory_extractor_filter(self, trajectory_extractor_filter):
        self.trajectory_filter_chain.add_filter(trajectory_extractor_filter)

    def record_csv_results(self, trajectories, output_path="trajectories.csv"):
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
            for vehicle_id, data in trajectories.items():
                x_trajectory = data['x_trajectory']
                y_trajectory = data['y_trajectory']
                vehicle_class = data['class']
                frames = data['frames']
                
                for i, (x, y, frame) in enumerate(zip(x_trajectory, y_trajectory, frames)):
                    writer.writerow([vehicle_id, vehicle_class, frame, x, y])
    
