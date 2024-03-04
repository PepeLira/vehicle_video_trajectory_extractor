import sys
from alignment import OrbAligner
from trajectory_extraction import YOLOv8ByteTrackDetector, YOLOv8SortDetector
from video_processor import VideoProcessor
from controllers import VideoProcessorController
from views import VideoProcessorView
from filters import FilterChain, MovingAverageFilter

def main():
    # Instantiate the aligner, trajectory extractor and filters
    aligner_filters = [MovingAverageFilter()] # You can add more filters
    trajectory_extractor_filters = [MovingAverageFilter()] # You can add more filters
    aligners = [OrbAligner()]
    detectors = [YOLOv8ByteTrackDetector(), YOLOv8SortDetector()]
    aligner_filter_chain = FilterChain()
    trajectory_filter_chain = FilterChain()
    
    # Instantiate the GUI view
    gui_view = VideoProcessorView(aligners, detectors, aligner_filters, trajectory_extractor_filters)
    video_processor = VideoProcessor(aligner_filter_chain, trajectory_filter_chain)

    # Instantiate VideoProcessorController and associate it with the VideoProcessor and the GUI view
    ui_controller = VideoProcessorController(gui_view, video_processor)

    gui_view.mainloop()
    

if __name__ == "__main__":
    main()
