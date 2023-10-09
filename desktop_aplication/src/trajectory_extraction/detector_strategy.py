from abc import ABC, abstractmethod

class DetectorStrategy(ABC):
    @abstractmethod
    def detect(self, frames):
        pass