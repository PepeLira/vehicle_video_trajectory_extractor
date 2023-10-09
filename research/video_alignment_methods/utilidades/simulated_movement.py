import cv2
import numpy as np
import matplotlib.pyplot as plt

def reformat_affine_parameters(parameters_array):
  inverse_transformed_array = []
  
  for params in parameters_array:
    theta = params[0]
    s = params[1]
    tx = params[2]
    ty = params[3]
    
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    
    matrix = np.matrix([
      [cos_theta * s, -sin_theta * s, tx],
      [sin_theta * s, cos_theta * s, ty]
    ])
    
    inverse_transformed_array.append(matrix)
  
  return inverse_transformed_array

def plot_line_graph(array, title=None, x_label="frames"):
    x = range(len(array))
    y = array

    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.title(title)
    plt.show()

def process_video(input_path, output_path, window_height, window_width, angle, dx, dy):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Arreglos de movimiento para cada frame
    rotations = [angle*(1 + i) for i in range(total_frames)]
    plot_line_graph(rotations, 'Rotations', 'Frame')
    x_translations = [dx*(1 + i) for i in range(total_frames)]
    plot_line_graph(x_translations, 'X Translations', 'Frame')
    y_translations = [dy*(1 + i) for i in range(total_frames)]
    plot_line_graph(y_translations, 'Y Translations', 'Frame')
    
    n, amplitude, frequency, phase = total_frames, 0.0035, 1.5, np.pi
    scalings = amplitude * np.sin(np.linspace(0, 2 * np.pi * frequency, n) + phase)+1
    plot_line_graph(scalings, 'Scaling', 'Frame')

    parameters = [np.array([rotations[i], scalings[i], x_translations[i], y_translations[i]]) for i in range(len(rotations))]
    
    movement_matrices = reformat_affine_parameters(parameters)

    # Create output video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (window_width, window_height))

    frame_count = 0
    while True:
      ret, frame = cap.read()
      if not ret:
        break
      
      # Aplicar transformaciones 
      translated_rotated_frame = cv2.warpAffine(frame, movement_matrices[frame_count], (width, height))

      # Calculate the window coordinates
      window_x = int((width - window_width)/2)
      window_y = int((height - window_height)/2) 

      # Extract the window
      window = translated_rotated_frame[window_y:window_y + window_height, window_x:window_x + window_width]

      # Write the window to the output video
      out.write(window)

      cv2.imshow('Processed Video', window)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
      if frame_count%100 == 0:
        print(f"Frame: {frame_count} of {total_frames}")

      frame_count += 1

    print("Done!")
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Example usage
input_video = "video_sim_30s.mp4"
output_video = "video_sim_30s_movement.mp4"
window_width = 2880
window_height = 1620
angle = 0.000035  # Rotation angle in degrees
dx = 0.1      # Translation in x-direction
dy = -0.1      # Translation in y-direction

process_video(input_video, output_video, window_height, window_width, angle, dx, dy)
