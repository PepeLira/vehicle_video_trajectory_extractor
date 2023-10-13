class VideoProcessorController:
    def __init__(self, ui_view, video_processor):
        self._ui_view = ui_view
        self._video_processor = video_processor
        self._event_listener()
    
    def start_processing(self):
        self.set_parameters()
        
        if self._video_processor.aligner is None and self._video_processor.detector is None:
            raise ValueError("An aligner or a detector must be set before processing video")
        if self._ui_view.input_video_path is None:
            raise ValueError("Input video must be set before processing video")
        
        self._video_processor.process_video(self._ui_view.input_video_path)

    def set_parameters(self):
        parameters = self._ui_view.get_user_input()
        if parameters["aligner"] != None:
            self._video_processor.set_aligner(parameters["aligner"])
            self._video_processor.add_aligner_filter(parameters["aligner_filter"])
        if parameters["detector"] != None:
            self._video_processor.set_detector(parameters["detector"])
            self._video_processor.add_trajectory_extractor_filter(parameters["trajectory_filter"])

    def _event_listener(self):
        self._ui_view.process_video_button.clicked.connect(self.start_processing)