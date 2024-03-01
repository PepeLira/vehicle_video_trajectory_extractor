import cv2
from PyQt5.QtCore import QCoreApplication

def resize_frame(frame, max_width=1440, max_height=810):
    h, w = frame.shape[:2]
    scale = min(max_width / w, max_height / h)
    new_w, new_h = int(w * scale), int(h * scale)
    return cv2.resize(frame, (new_w, new_h))

class InputVideo:
    def __init__(self, video_path):
        self.video_path = video_path
        self.aligner = None
        self.detector = None
        self.progress = 0
        self.stage = ''

    def set_aligner(self, aligner):
        self.aligner = aligner
    
    def set_detector(self, detector):
        self.detector = detector
    
    def is_aligned(self):
        return self.aligner is not None
    
    def is_detected(self):
        return self.detector is not None
    
    def get_frames(self, stage=""):
        self.stage = stage
        if self.is_aligned():
            return self.get_aligned_frames()
        else:
            return self.stream_frames()

    def get_video_path(self):
        return self.video_path

    def get_aligned_frames(self):
        frame_count = 0
        for frame in self.stream_frames():
            yield self.aligner.align(frame, frame_count)
            frame_count += 1

    def reorganize_trajectories(self):
        self.stage = '"reorganize trajectories"'
        frame_trajectories = {}
        self.progress = 0
        step = 100/len(self.detector.trajectories.items())

        for id, data in self.detector.trajectories.items():
            for x, y, frame in zip(data["x_trajectory"], data["y_trajectory"], data["frames"]):
                if frame not in frame_trajectories:
                    frame_trajectories[frame] = {"x": [], "y": [], "class": data["class"], "ids": []}
                frame_trajectories[frame]["x"].append(int(x))
                frame_trajectories[frame]["y"].append(int(y))
                frame_trajectories[frame]["ids"].append(id)

            self.progress += step
            self.progress_call(round(self.progress, 2), self.stage)
            QCoreApplication.processEvents()
        return frame_trajectories

    def get_video_fps(self):
        video = cv2.VideoCapture(self.video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        video.release()
        return fps
    
    def get_video_width(self):
        video = cv2.VideoCapture(self.video_path)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        video.release()
        return width
    
    def get_video_frame_count(self):
        video = cv2.VideoCapture(self.video_path)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        video.release()
        return frame_count

    def get_reference_frame(self):
        video = cv2.VideoCapture(self.video_path)
        ret, frame = video.read()
        video.release()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if ret:
            return frame
        else:
            return None
        
    def display_frame(self, frame):
        # frame = resize_frame(frame)
        self.display_frame_call(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def stream_frames(self):
        self.progress = 0
        step = 100/self.get_video_frame_count()
        video = cv2.VideoCapture(self.video_path)
        while True:
            ret, frame = video.read()
            if ret:
                yield frame
            else:
                break
            self.progress += step
            self.progress_call(round(self.progress, 2), self.stage)
            QCoreApplication.processEvents()
        
        video.release()

    def save_processed_video(self, output_path="tracked_video.mp4"):
        self.stage = '"Video Saving"'
        video = cv2.VideoCapture(self.video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
        if self.is_detected():
            rt = self.reorganize_trajectories() # rt = reorganized_trajectories
        frame_count = 0
        for frame in self.get_frames( stage='"Saving Video"'):
            if self.is_detected():
                for x, y, id in zip(rt[frame_count]["x"], rt[frame_count]["y"], rt[frame_count]["ids"]):
                    cv2.putText(img=frame, text=f"{id}", org=(x, y-6), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(0,255,0), thickness=2)
                    cv2.circle(img=frame, center=(x,y), radius=0, color=(0, 0, 255), thickness=5)
            out.write(frame)
            frame_count += 1
        out.release()
        video.release()
        
    def update_progress(self, call):
        self.progress_call = call

    def display_frame_call(self, call):
        self.display_frame_call = call

    def __str__(self):
        return self.video_path
        

if __name__ == "__main__":
    input_video = InputVideo("../../../videos/video1_30s_sift_estabilizado_filtrado.mp4")
    frame = input_video.get_frames()
    input_video.display_frames(frame)
    