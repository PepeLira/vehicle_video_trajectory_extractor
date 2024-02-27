import cv2
import csv
import random
import numpy as np

# Global variables
drawing = False  # True if the mouse is pressed
ix, iy = -1, -1  # Initial x, y coordinates
img = None  # Image on which we draw
current_rectangle = None  # Store the current rectangle coordinates

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, img, current_rectangle
    if current_rectangle == None:
      if event == cv2.EVENT_LBUTTONDOWN:
          if not drawing:  # Start drawing only if not already drawing
              drawing = True
              ix, iy = x, y

      elif event == cv2.EVENT_MOUSEMOVE:
          if drawing:
              temp_img = img.copy()
              cv2.rectangle(temp_img, (ix, iy), (x, y), (0, 255, 0), 2)
              cv2.imshow('Frame', temp_img)

      elif event == cv2.EVENT_LBUTTONUP:
          if drawing:
              drawing = False
              current_rectangle = (ix, iy, x - ix, y - iy)  # Store rectangle dimensions
              if np.abs(current_rectangle[2]) < 10 or np.abs(current_rectangle[3]) < 10:
                  current_rectangle = None  # Ignore small rectangles
              cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)

def assign_colors(ids):
    return {id: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for id in ids}

def get_frame(cap, frame_number):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    if not ret:
        return None
    return frame

def read_annotations(file_path):
    annotations = {}
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                frame_number = int(row[0])
                object_id = row[1]
                bbox = tuple(map(float, row[2:6]))
                annotations.setdefault(frame_number, []).append((object_id, bbox))
    except FileNotFoundError:
        pass
    return annotations

def draw_annotations(frame, annotations, colors, frame_number):
    for object_id, bbox in annotations.get(frame_number, []):
        bb_left, bb_top, bb_width, bb_height = bbox
        top_left = (int(bb_left), int(bb_top))
        bottom_right = (int(bb_left + bb_width), int(bb_top + bb_height))
        cv2.rectangle(frame, top_left, bottom_right, colors[object_id], 2)
        cv2.putText(frame, str(object_id), (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, colors[object_id], 2)

def update_annotation_file(file_path, new_data):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for data in new_data:
            writer.writerow(data)
    print(f'Annotations saved to {file_path}')

def annotate_video(video_path, txt_file_path):
  global drawing, img, current_rectangle
  annotations = read_annotations(txt_file_path)
  cap = cv2.VideoCapture(video_path)
  unique_ids = {obj_id for frame_annots in annotations.values() for obj_id, _ in frame_annots}
  colors = assign_colors(unique_ids)
  new_id = max(map(int, unique_ids)) + 1 if unique_ids else 0
  new_annotations = []

  if not cap.isOpened():
      print("Error: Could not open video.")
      exit()

  cv2.namedWindow('Frame')
  cv2.setMouseCallback('Frame', draw_rectangle)

  frame_num = 0

  while True:
      img = get_frame(cap, frame_num)
      draw_annotations(img, annotations, colors, frame_num)
      if img is None:
          break
      cv2.putText(img, f'Frame {frame_num}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
      cv2.imshow('Frame', img)
      
      k = cv2.waitKey(0) & 0xFF

      if k == ord('n'):  # Press 'n' to go to the next frame
          if current_rectangle is not None:
            bb_left, bb_top, bb_width, bb_height = current_rectangle
            new_annotations.append([frame_num, new_id, bb_left, bb_top, bb_width, bb_height, 0.9, -1, -1, -1])
          current_rectangle = None  # Reset the rectangle for the new frame
          frame_num += 1
      elif k == 27 or k == ord('q'):  # Press 'ESC' to exit
          break

  cap.release()
  cv2.destroyAllWindows()
  if len(new_annotations) > 0:
    update_annotation_file(txt_file_path, new_annotations)



# Example usage
video_path = 'D:/Titulo/Github/vehicle_video_trajectory_extractor/research/tracking_methods/video_reference/vid_1_[180,220][00,99]_2_ss_cvat1.1/video_sift_estabilizado_filtrado.mp4'
annotation_file = 'D:/Titulo/Github/vehicle_video_trajectory_extractor/research/tracking_methods/video_reference/bounding_boxes_to_correct.csv'
annotate_video(video_path, annotation_file)
