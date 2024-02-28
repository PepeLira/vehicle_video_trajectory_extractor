from abc import ABC, abstractmethod
import cv2

def resize_frame(frame, max_width=1440, max_height=810):
    h, w = frame.shape[:2]
    scale = min(max_width / w, max_height / h)
    new_w, new_h = int(w * scale), int(h * scale)
    return cv2.resize(frame, (new_w, new_h))

class DetectorStrategy(ABC):
    @abstractmethod
    def __init__(self, source_weights_path, detection_threshold):
        self.source_weights_path = source_weights_path
        self.detection_threshold = detection_threshold

    @abstractmethod
    def detect(self, video_path, video_fps):
        """
        Detects objects in a video using the specified detector strategy.

        Args:
            video_path (str): The path to the video file.
            video_fps (int): The frames per second of the video.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the detected objects.
                Each dictionary contains the following keys:
                - 'class_id' (int): The class ID of the detected object.
                - 'class_name' (str): The class name of the detected object.
                - 'confidence' (float): The confidence score of the detection.
                - 'bbox' (Tuple[int, int, int, int]): The bounding box coordinates of the detection
                    in the format (x_min, y_min, width, height).
                - 'trajectory' (List[Tuple[int, int]]): The trajectory of the detected object,
                    represented as a list of (x, y) coordinates.
        """
        raise NotImplementedError("The detect method must be implemented")

    @abstractmethod
    def get_trajectories(self, detections):
        """
        Extracts the trajectories of the detected objects.

        Args:
            detections (List[Dict[str, Any]]): A list of dictionaries representing the detected objects.
                Each dictionary contains the following keys:
                - 'class_id' (int): The class ID of the detected object.
                - 'class_name' (str): The class name of the detected object.
                - 'confidence' (float): The confidence score of the detection.
                - 'bbox' (Tuple[int, int, int, int]): The bounding box coordinates of the detection
                    in the format (x_min, y_min, width, height).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the trajectories of the detected objects.
                Each dictionary contains the following keys:
                - 'class_id' (int): The class ID of the detected object.
                - 'class_name' (str): The class name of the detected object.
                - 'trajectory' (List[Tuple[int, int]]): The trajectory of the detected object,
                    represented as a list of (x, y) coordinates.
        """
        raise NotImplementedError("The get_trajectories method must be implemented")