import cv2

def process_video(input_path, output_path, start_frame, end_frame):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Check if start_frame and end_frame are within valid range
    start_frame = max(0, min(start_frame, total_frames - 1))
    end_frame = max(start_frame, min(end_frame, total_frames - 1))
    
    # Create output video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count < start_frame:
            frame_count += 1
            continue
        elif frame_count > end_frame:
            break
        
        # Write the frame to the output video
        out.write(frame)
        
        cv2.imshow('Processed Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_count += 1
    
    print("Done!")
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Example usage
input_video = "video_sim.mp4"
output_video = "video_sim_30s.mp4"
start_frame = 420  # Start frame to keep
end_frame = 2220    # End frame to keep

process_video(input_video, output_video, start_frame, end_frame)
