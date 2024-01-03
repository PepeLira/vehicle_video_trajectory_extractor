import argparse
import cv2
import numpy as np
from tqdm import tqdm
from ultralytics import YOLO
import supervision as sv
import random

class BoxAnnotator:
    def annotate(self, frame: np.ndarray, detections: any, labels: list, colors: list = None) -> np.ndarray:
        """
        Annotates the frame with bounding boxes and labels.
        
        Args:
            frame (np.ndarray): The frame to annotate.
            detections (any): The detections to annotate the frame with.
            labels (list): The labels corresponding to the detections.
            colors (list, optional): List of colors for each bounding box. Defaults to None.

        Returns:
            np.ndarray: The annotated frame.
        """
        
        # Loop through the detections and draw the bounding boxes
        for i, detection in enumerate(detections):
            top_left = (int(detection.xmin), int(detection.ymin))
            bottom_right = (int(detection.xmax), int(detection.ymax))
            
            # Choose color for the bounding box
            if colors and len(colors) > i:
                box_color = colors[i]
            else:
                box_color = (0, 255, 0)  # Default color: green
            
            # Draw bounding box
            cv2.rectangle(frame, top_left, bottom_right, box_color, 2)
            
            # Draw label (if provided)
            if labels and len(labels) > i:
                cv2.putText(frame, labels[i], (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)
        
        return frame

class VideoProcessor:
    def __init__(
        self,
        source_weights_path: str,
        source_video_path: str,
        target_video_path: str = None,
        confidence_threshold: float = 0.3,
        iou_threshold: float = 0.7,
    ) -> None:
        self.conf_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.source_video_path = source_video_path
        self.target_video_path = target_video_path

        self.model = YOLO(source_weights_path)
        self.tracker = sv.ByteTrack()

        # Random color generator for each tracker ID
        self.color_mapping = {}

        self.box_annotator = sv.BoxAnnotator()  # We will handle colors within process_frame
        self.trace_annotator = sv.TraceAnnotator()  # Added this

    def process_video(self):
      frame_generator = sv.get_video_frames_generator(
        source_path=self.source_video_path
      )

      if self.target_video_path:
          video_info = sv.VideoInfo.from_video_path(self.source_video_path)
          with sv.VideoSink(self.target_video_path, video_info) as sink:
              for frame in tqdm(frame_generator, total=video_info.total_frames):
                  annotated_frame = self.process_frame(frame)
                  sink.write_frame(annotated_frame)
      else:
          for frame in tqdm(frame_generator):
              annotated_frame = self.process_frame(frame)
              cv2.imshow("Processed Video", annotated_frame)
              if cv2.waitKey(1) & 0xFF == ord("q"):
                  break
          cv2.destroyAllWindows()

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
      results = self.model(
        frame, verbose=False, conf=self.conf_threshold, iou=self.iou_threshold
      )[0]
      detections = sv.Detections.from_ultralytics(results)
      detections = self.tracker.update_with_detections(detections)

      # Create a random color for each tracker ID
      # for tracker_id in detections.tracker_id:
      #   if tracker_id not in self.color_mapping:
      #     self.color_mapping[tracker_id] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
          
      labels = [f"#{tracker_id}" for tracker_id in detections.tracker_id]
      
      # Annotate frame with traces
      annotated_frame = self.trace_annotator.annotate(frame, detections)
      
      # Annotate the frame with bounding boxes and labels
      annotated_frame = self.box_annotator.annotate(annotated_frame, detections, labels)

      return annotated_frame

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Car Detection and Tracking with YOLO and ByteTrack"
    )

    parser.add_argument(
        "--source_weights_path",
        required=True,
        help="Path to the source weights file",
        type=str,
    )
    parser.add_argument(
        "--source_video_path",
        required=True,
        help="Path to the source video file",
        type=str,
    )
    parser.add_argument(
        "--target_video_path",
        default=None,
        help="Path to the target video file (output)",
        type=str,
    )
    parser.add_argument(
        "--confidence_threshold",
        default=0.3,
        help="Confidence threshold for the model",
        type=float,
    )
    parser.add_argument(
        "--iou_threshold", default=0.7, help="IOU threshold for the model", type=float
    )

    args = parser.parse_args()
    processor = VideoProcessor(
        source_weights_path=args.source_weights_path,
        source_video_path=args.source_video_path,
        target_video_path=args.target_video_path,
        confidence_threshold=args.confidence_threshold,
        iou_threshold=args.iou_threshold,
    )
    processor.process_video()
