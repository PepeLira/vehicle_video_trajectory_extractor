from .detector_strategy import DetectorStrategy, resize_frame
from ultralytics import YOLO
import cv2

class YOLOv8ByteTrackDetector(DetectorStrategy):
    def __init__(self, source_weights_path="../../../models/cutom_dota.pt", detection_threshold=0.8):
        super().__init__(source_weights_path, detection_threshold)
        self.model = YOLO(source_weights_path)

    def detect(self, input_video, video_fps):
        self.fps = video_fps
        self.byte_track(input_video)
        video_detections = []
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
    
    def byte_track(self, input_video):
        self.results = []
        frame_count = 0
        for frame in input_video.get_frames():
            results = self.model.track(frame, persist=True, imgsz=1280, show_labels=False, show_conf=False, show_boxes=False, tracker="bytetrack.yaml", verbose=False)
            
            # Get the boxes, track IDs and confidences
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            confidences = results[0].boxes.conf.cpu().tolist()
            class_ids = results[0].boxes.cls.cpu().tolist()
            new_data = []
            # Write tracking info to the output file
            for box, track_id, confidence, class_id in zip(boxes, track_ids, confidences, class_ids):
                x, y, w, h = box
                x_min = x - w / 2
                y_min = y - h / 2
                x_max = x + w / 2
                y_max = y + h / 2
                xmin, ymin, xmax, ymax = int(x_min), int(y_min), int(x_max), int(y_max)
                new_data.append([xmin, ymin, xmax, ymax, confidence, class_id, track_id])
                cv2.putText(img=frame, text=f"Id: {track_id}", org=(xmin, ymin-10), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(0,255,0), thickness=2)
                cv2.rectangle(img=frame, pt1=(xmin, ymin), pt2=(xmax, ymax), color=(0, 255, 0), thickness=2)
                cv2.circle(img=frame, center=(int((xmin + xmax) / 2), int((ymin + ymax) / 2)), radius=0, color=(0, 0, 255), thickness=2)
            resized_frame = resize_frame(frame)
            cv2.imshow("frame", resized_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break  # Add a delay (0 means wait indefinitely)
            self.results.append(new_data)
            frame_count += 1
        cv2.destroyAllWindows()

    
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
    detector = YOLOv8ByteTrackDetector()
    
    video_path = "../../../videos/video1_30s_sift_estabilizado_filtrado.mp4"

    detections = detector.detect(video_path, 30)
    trajectories = detector.get_trajectories(detections)


