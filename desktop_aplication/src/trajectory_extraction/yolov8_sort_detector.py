from .detector_strategy import DetectorStrategy
from ultralytics import YOLO
import numpy as np
import cv2
from .extensions.sort import Sort

def resize_frame(frame, max_width=1440, max_height=810):
    h, w = frame.shape[:2]
    scale = min(max_width / w, max_height / h)
    new_w, new_h = int(w * scale), int(h * scale)
    return cv2.resize(frame, (new_w, new_h))

class YOLOv8SortDetector(DetectorStrategy):
    def __init__(self, source_weights_path="../../../models/cutom_dota.pt", detection_threshold=0.5):
        super().__init__(source_weights_path, detection_threshold)
        self.model = YOLO(source_weights_path)

    def detect(self, video_path, video_fps):
        self.fps = video_fps
        self.track_by_sort(video_path)
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
    
    def track_by_sort(self, video_path):
        cap = cv2.VideoCapture(video_path)
        tracker = Sort()
        self.results = []
        while cap.isOpened():
            status, frame = cap.read()
            if not status:
                break

            results = self.model(frame, stream=True, verbose=False, imgsz=1920)
            for res in results:
                filtered_indices = np.where(res.boxes.conf.cpu().numpy() > self.detection_threshold)[0]
                boxes = res.boxes.xyxy.cpu().numpy()[filtered_indices].astype(int)
                data = res.boxes.data.cpu().numpy()[filtered_indices].tolist()
                tracks = tracker.update(boxes)
                tracks = tracks.astype(int)
                new_data = []
                for i in range(len(tracks)):
                    xmin, ymin, xmax, ymax, track_id = tracks[i]
                    data[i][5] = res.names[data[i][5]]  # Add class name to boxes array \
                    data[i].append(track_id)  # Add track ID to boxes array
                    new_data.append(data[i])
                    cv2.putText(img=frame, text=f"Id: {track_id}", org=(xmin, ymin-10), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(0,255,0), thickness=2)
                    cv2.rectangle(img=frame, pt1=(xmin, ymin), pt2=(xmax, ymax), color=(0, 255, 0), thickness=2)
            resized_frame = resize_frame(frame)
            cv2.imshow("frame", resized_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break  # Add a delay (0 means wait indefinitely)    
            self.results.append(new_data)

        cap.release()
        cv2.destroyAllWindows()



    
    def __str__(self):
        return "YOLOv8 + Sort Tracker"

if __name__ == "__main__":
    detector = YOLOv8SortDetector()
    
    video_path = "../../../videos/video1_30s_sift_estabilizado_filtrado.mp4"

    detections = detector.detect(video_path, 30)
    trajectories = detector.get_trajectories(detections)


