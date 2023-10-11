from detector_strategy import DetectorStrategy
import cv2
import pdb
from ultralytics import YOLO

class YOLOv8Detector(DetectorStrategy):
    def __init__(self, source_weights_path="../../../models/custom_yolov8.pt", detection_threshold=0.3):
        self.model = YOLO(source_weights_path)
        self.detection_threshold = detection_threshold

    def detect(self, video):
        results = self.model.track(source = video, verbose=False, conf=0.3, iou=0.6, show=True)
        for result in results:
            detections = []
            for r in result.boxes.data.tolist():
                x1, y1, x2, y2, track_id, score, class_id = r
                x1 = int(x1)
                x2 = int(x2)
                y1 = int(y1)
                y2 = int(y2)
                track_id = int(track_id)
                class_id = int(class_id)
                if score > self.detection_threshold:
                    detections.append([x1, y1, x2, y2, result.names[class_id], track_id, score])
        
        return video, detections

if __name__ == "__main__":
    detector = YOLOv8Detector()
    detector.detect('../../../videos/video1_30s_sift_estabilizado_filtrado.mp4')


