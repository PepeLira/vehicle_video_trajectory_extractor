import cv2

class InputVideo:
    def __init__(self, video_path):
        self.video_path = video_path

    def get_video_path(self):
        return self.video_path
    
    def get_frames(self):
        video = cv2.VideoCapture(self.video_path)
        while True:
            ret, frame = video.read()
            if ret:
                yield frame
            else:
                break
        video.release()

    def get_video_fps(self):
        video = cv2.VideoCapture(self.video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        video.release()
        return fps

    def display_frames(self, frame):
        for frame in self.get_frames():
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def get_reference_frame(self):
        video = cv2.VideoCapture(self.video_path)
        ret, frame = video.read()
        video.release()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if ret:
            return frame
        else:
            return None

    def __str__(self):
        return self.video_path
        

if __name__ == "__main__":
    input_video = InputVideo("../../../videos/video1_30s_sift_estabilizado_filtrado.mp4")
    frame = input_video.get_frames()
    input_video.display_frames(frame)
    