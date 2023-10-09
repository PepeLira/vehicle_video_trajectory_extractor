import cv2

def reduce_frame_rate(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    reduced_fps = fps / 2  # Reduce frame rate to half

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, reduced_fps, (width, height))
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count%2 == 0:

            out.write(frame)

        frame_count += 1
        cv2.imshow('Reduced Frame Rate Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Example usage
input_video = "video_sim_30s.mp4"
output_video = "video_sim_30s_fps.mp4"

reduce_frame_rate(input_video, output_video)
