import numpy as np
import cv2
from ultralytics import YOLO
from sort import Sort

def resize_frame(frame, max_width=1920, max_height=1080):
    h, w = frame.shape[:2]
    scale = min(max_width / w, max_height / h)
    new_w, new_h = int(w * scale), int(h * scale)
    return cv2.resize(frame, (new_w, new_h))

if __name__ == '__main__':
    cap = cv2.VideoCapture("D:/Titulo/Github/vehicle_video_trajectory_extractor/videos/video_sim_30s_movement_estabilizado_filtrado.mp4")
    model = YOLO("D:/Titulo/Github/vehicle_video_trajectory_extractor/models/cutom_dota.pt")
    tracker = Sort()

    while cap.isOpened():
        status, frame = cap.read()
        if not status:
            break

        results = model(frame, stream=True)
        for res in results:
            filtered_indices = np.where(res.boxes.conf.cpu().numpy() > 0.5)[0]
            boxes = res.boxes.xyxy.cpu().numpy()[filtered_indices].astype(int)
            tracks = tracker.update(boxes)
            tracks = tracks.astype(int)
            
            for xmin, ymin, xmax, ymax, track_id in tracks:
                cv2.putText(img=frame, text=f"Id: {track_id}", org=(xmin, ymin-10), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(0,255,0), thickness=2)
                cv2.rectangle(img=frame, pt1=(xmin, ymin), pt2=(xmax, ymax), color=(0, 255, 0), thickness=2)

        resized_frame = resize_frame(frame)
        cv2.imshow("frame", resized_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

