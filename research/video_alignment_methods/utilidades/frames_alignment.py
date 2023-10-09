import cv2
import numpy as np

def align_images(image1, image2):
    # Detect keypoints and compute descriptors
    orb = cv2.ORB_create()
    keypoints1, descriptors1 = orb.detectAndCompute(image1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(image2, None)

    # Match features
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = matcher.match(descriptors1, descriptors2)

    # Select top matches
    num_matches = int(len(matches) * 0.2)  # Adjust the ratio of selected matches as needed
    print(f"Number of matches: {len(matches)}")
    print(f"Number of matches after ratio: {num_matches}")
    matches = sorted(matches, key=lambda x: x.distance)[:num_matches]

    # Get matching keypoints
    src_pts = np.float32([keypoints1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # Estimate affine transformation matrix
    affine_matrix, _ = cv2.estimateAffinePartial2D(src_pts, dst_pts)

    # Warp image1 using the affine matrix
    aligned_image = cv2.warpAffine(image1, affine_matrix, (image2.shape[1], image2.shape[0]))

    return aligned_image

def process_video(input_path, output_path):
    # Open the video file for reading
    video_capture = cv2.VideoCapture(input_path)

    # Get video properties
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Read the reference frame
    for i in range(20):
      ret, first_frame = video_capture.read()

    frame_count = 0
    while True:
        # Read a frame from the video
        ret, frame = video_capture.read()
        if not ret:
            break

        # Process the frame (add red frame)
        frame_processed = align_images(frame, first_frame)

        # Write the processed frame to the output video file
        video_writer.write(frame_processed)

        # Display the processed frame
        cv2.imshow("Processed Frame", frame_processed)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1
        print(f"Processed frame {frame_count}/{total_frames}")

    # Release the video capture and writer objects
    video_capture.release()
    video_writer.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()

# Example usage
input_video_path = "video.mp4"
output_video_path = "output_video.mp4"

process_video(input_video_path, output_video_path)
