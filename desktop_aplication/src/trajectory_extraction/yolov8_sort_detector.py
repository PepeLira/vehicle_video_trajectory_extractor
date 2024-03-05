from .detector_strategy import DetectorStrategy
from ultralytics import YOLO
import cv2
from .extensions.sort import Sort
import os

MODEL_PATH = os.path.join( "..", "..", "models/custom_dota.pt")

class YOLOv8SortDetector(DetectorStrategy):
    def __init__(self, source_weights_path=MODEL_PATH, detection_threshold=0.3):
        super().__init__(source_weights_path, detection_threshold)
        self.model = YOLO(source_weights_path)
        self.trajectories = {}

    def detect(self, input_video, video_fps):
        self.fps = video_fps
        self.track_by_sort(input_video)
        video_detections = []
        for result_i in range(len(self.results)):
            detections = {}
            for r in self.results[result_i]:
                x1, y1, x2, y2, score, class_, track_id = r
                track_id = int(track_id)
                if score > self.detection_threshold:
                    detections[track_id] = {
                        "bbox": [x1, y1, x2, y2],
                        "class": class_,
                        "score": round(score, 2),
                        "frame": result_i
                    }
            video_detections.append(detections)

        return video_detections
    
    def get_trajectories(self, detections):
        for i in range(len(detections)):
            for track_id in detections[i].keys():
                if track_id not in self.trajectories.keys():
                    self.trajectories[track_id] = {
                                            "x_trajectory": [], 
                                            "y_trajectory": [], 
                                            "class": detections[i][track_id]["class"], 
                                            "frames": [], 
                                            "time": []
                                             }

                x, y = self.calculate_tracking_point(detections[i][track_id]["bbox"])
                self.trajectories[track_id]["x_trajectory"].append(x)
                self.trajectories[track_id]["y_trajectory"].append(y)
                self.trajectories[track_id]["frames"].append(detections[i][track_id]["frame"])
                self.trajectories[track_id]["time"].append(i/self.fps)
        return self.trajectories
    
    def calculate_tracking_point(self, bbox):
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) / 2, (y1 + y2) / 2)
    
    def track_by_sort(self, input_video):
        tracker = Sort(max_age=15)
        self.results = []
        frame_count = 0
        for frame in input_video.get_frames(stage="Tracking"):
            results = self.model(frame, stream=True, verbose=False, imgsz=input_video.get_video_width())
            for res in results:
                # filtered_indices = np.where(res.boxes.conf.cpu().numpy() > 0.3)[0]
                data = res.boxes.data.cpu().numpy()
                tracks = tracker.update(data)
                new_data = []
                for i in range(len(tracks)):
                    xmin, ymin, xmax, ymax, conf, class_id, track_id = tracks[i]
                    xmin, ymin, xmax, ymax, track_id = int(xmin), int(ymin), int(xmax), int(ymax), int(track_id)
                    class_name = res.names[int(class_id)]
                    new_data.append([xmin, ymin, xmax, ymax, conf, class_name, track_id])
                    cv2.putText(img=frame, text=f"Id: {track_id}", org=(xmin, ymin-10), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(0,255,0), thickness=2)
                    cv2.rectangle(img=frame, pt1=(xmin, ymin), pt2=(xmax, ymax), color=(0, 255, 0), thickness=2)
                    cv2.circle(img=frame, center=(int((xmin + xmax) / 2), int((ymin + ymax) / 2)), radius=0, color=(0, 0, 255), thickness=2)
            input_video.display_frame(frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break  # Add a delay (0 means wait indefinitely)    
            self.results.append(new_data)
            frame_count += 1
            
        cv2.destroyAllWindows()
    
    def __str__(self):
        return "YOLOv8 + Sort Tracker"

if __name__ == "__main__":
    detector = YOLOv8SortDetector()
    
    video_path = "../../../videos/video1_30s_sift_estabilizado_filtrado.mp4"

    detections = detector.detect(video_path, 30)
    trajectories = detector.get_trajectories(detections)
