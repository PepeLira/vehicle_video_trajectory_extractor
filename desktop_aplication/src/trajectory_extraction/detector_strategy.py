from abc import ABC, abstractmethod

class DetectorStrategy(ABC):
    @abstractmethod
    def detect(self, video):
        pass