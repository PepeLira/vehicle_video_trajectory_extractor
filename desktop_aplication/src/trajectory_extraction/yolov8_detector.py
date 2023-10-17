from .detector_strategy import DetectorStrategy
from ultralytics import YOLO

class YOLOv8Detector(DetectorStrategy):
    def __init__(self, source_weights_path="../../../models/custom_yolov8.pt", detection_threshold=0.3):
        super().__init__(source_weights_path, detection_threshold)
        self.model = YOLO(source_weights_path)

    def detect(self, video):
        results = self.model.track(source = video, verbose=False, conf=0.3, iou=0.6, show=True)
        video_detections = []
        for result in results:
            detections = {}
            for r in result.boxes.data.tolist():
                x1, y1, x2, y2, track_id, score, class_id = r
                track_id = int(track_id)
                class_id = int(class_id)
                if score > self.detection_threshold:
                    detections[track_id] = {
                                            "bbox" : [x1, y1, x2, y2], 
                                            "class" : result.names[class_id], 
                                            "score": round(score, 2)
                                            }
                video_detections.append(detections)
        
        return video_detections
    
    def get_trajectories(self, detections):
        trajectories = {}
        for i in range(len(detections)):
            for track_id in detections[i].keys():
                if track_id not in trajectories.keys():
                    trajectories[track_id] = {"x_trajectory": [], "y_trajectory": [], "class": detections[i][track_id]["class"], "frames": []}
                x, y = self.calculate_tracking_point(detections[i][track_id]["bbox"])
                trajectories[track_id]["x_trajectory"].append(x)
                trajectories[track_id]["y_trajectory"].append(y)
                trajectories[track_id]["frames"].append(i)
        return trajectories
    
    def calculate_tracking_point(self, bbox):
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) / 2, (y1 + y2) / 2)


    
    def __str__(self):
        return "YOLOv8 Detector"

if __name__ == "__main__":
    detector = YOLOv8Detector()
    detector.detect('../../../videos/video1_30s_sift_estabilizado_filtrado.mp4')


