from abc import ABC, abstractmethod

class DetectorStrategy(ABC):
    @abstractmethod
    def __init__(self, source_weights_path, detection_threshold):
        self.source_weights_path = source_weights_path
        self.detection_threshold = detection_threshold
        pass

    @abstractmethod
    def detect(self, video_path, video_fps):
        pass

    @abstractmethod
    def get_trajectories(self, detections):
        pass