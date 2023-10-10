import sys
from PyQt5.QtWidgets import QApplication
from alignment import OrbAligner
from trajectory_extraction import SupervisionDetector
from video_processor import VideoProcessor
from controllers import VideoProcessorController
from views import VideoProcessorView
from filters import FilterChain, MovingAverageFilter

def main():
    # Instantiate the aligner, trajectory extractor and filters
    aligner_filters = [MovingAverageFilter()] # You can add more filters
    trajectory_extractor_filters = [MovingAverageFilter()] # You can add more filters
    aligner = OrbAligner()
    trajectory_extractor = SupervisionDetector()
    filter_chain = FilterChain()

    # Instantiate VideoProcessor
    video_processor = VideoProcessor(aligner, trajectory_extractor, aligner_filters, trajectory_extractor_filters, filter_chain)

    app = QApplication(sys.argv)

    # Instantiate the GUI view
    gui_view = VideoProcessorView()

    # Instantiate VideoProcessorController and associate it with the VideoProcessor and the GUI view
    ui_controller = VideoProcessorController(gui_view, video_processor)

    # Show the GUI and enter the application loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
