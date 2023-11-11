from filters import FilterChain
import numpy as np

class VideoProcessor:
    def __init__(self, aligner_filter_chain: FilterChain, trajectory_filter_chain: FilterChain):
        self.aligner_filter_chain = aligner_filter_chain
        self.trajectory_filter_chain = trajectory_filter_chain
        self.aligner = None
        self.detector = None
    
    def process_video(self, input_video):
        # Implements the video processing pipeline
        if self.aligner is None and self.detector is None:
            raise ValueError("Aligner and detector must be set before processing video")
        
        filtered_affine_transformations = None
        filtered_trajectories = None
        
        if self.aligner != None:
            affine_transformations = self.aligner.set_affine_transformations(input_video)
            filtered_affine_transformations = self.filter_affine_transformations(affine_transformations)

        if self.detector != None:
            detections = self.detector.detect(input_video.get_video_path(), input_video.get_video_fps())
            trajectories = self.detector.get_trajectories(detections)
            
            # Filter trajectories
            filtered_trajectories = self.filter_trajectories(trajectories)

        return filtered_trajectories, filtered_affine_transformations

    def filter_trajectories(self, trajectories):
        for trajectory in trajectories.keys():
            trajectories[trajectory]["x_trajectory"] = self.trajectory_filter_chain.apply_filters(trajectories[trajectory]["x_trajectory"])
            trajectories[trajectory]["y_trajectory"] = self.trajectory_filter_chain.apply_filters(trajectories[trajectory]["y_trajectory"])
        return trajectories
    
    def filter_affine_transformations(self, affine_transformations):
        affine_transformations = np.array(affine_transformations)
        for i in range(len(affine_transformations[0])):
            affine_transformations[:, i] = np.array(self.aligner_filter_chain.apply_filters(list(affine_transformations[:, i])))
        return affine_transformations.tolist()

    def set_aligner(self, aligner):
        self.aligner = aligner
    
    def set_detector(self, detector):
        self.detector = detector

    def add_aligner_filter(self, aligner_filter):
        self.aligner_filter_chain.add_filter(aligner_filter)
    
    def add_trajectory_extractor_filter(self, trajectory_extractor_filter):
        self.trajectory_filter_chain.add_filter(trajectory_extractor_filter)
    
