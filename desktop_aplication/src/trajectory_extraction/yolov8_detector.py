from .detector_strategy import DetectorStrategy
from ultralytics import YOLO

class YOLOv8Detector(DetectorStrategy):
    def __init__(self, source_weights_path="../../../models/cutom_dota.pt", detection_threshold=0.8):
        super().__init__(source_weights_path, detection_threshold)
        self.model = YOLO(source_weights_path)

    def detect(self, input_video, video_fps):
        self.fps = video_fps
        results = self.model.track(source=input_video.get_video_path(), verbose=False, conf=self.detection_threshold, iou=0.8, show=True, tracker="bytetrack.yaml", imgsz=1280)
        video_detections = []
        for result_i in range(len(results)):
            detections = {}
            for r in results[result_i].boxes.data.tolist():
                x1, y1, x2, y2, track_id, score, class_id = r
                track_id = int(track_id)
                class_id = int(class_id)
                if score > self.detection_threshold:
                    detections[track_id] = {
                        "bbox": [x1, y1, x2, y2],
                        "class": results[result_i].names[class_id],
                        "score": round(score, 2),
                        "frame": result_i
                    }
            video_detections.append(detections)

        return video_detections
    
    def get_trajectories(self, detections):
        trajectories = {}
        for i in range(len(detections)):
            for track_id in detections[i].keys():
                if track_id not in trajectories.keys():
                    trajectories[track_id] = {
                                            "x_trajectory": [], 
                                            "y_trajectory": [], 
                                            "class": detections[i][track_id]["class"], 
                                            "frames": [], 
                                            "time": []
                                             }

                x, y = self.calculate_tracking_point(detections[i][track_id]["bbox"])
                trajectories[track_id]["x_trajectory"].append(x)
                trajectories[track_id]["y_trajectory"].append(y)
                trajectories[track_id]["frames"].append(detections[i][track_id]["frame"])
                trajectories[track_id]["time"].append(i/self.fps)
        return trajectories
    
    def calculate_tracking_point(self, bbox):
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) / 2, (y1 + y2) / 2)


    
    def __str__(self):
        return "YOLOv8 + ByteTrack"

if __name__ == "__main__":
    detector = YOLOv8Detector()
    
    video_path = "../../../videos/video1_30s_sift_estabilizado_filtrado.mp4"

    detections = detector.detect(video_path, 30)
    trajectories = detector.get_trajectories(detections)


