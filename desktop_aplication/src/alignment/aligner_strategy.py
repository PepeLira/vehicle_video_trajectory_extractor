from abc import ABC, abstractmethod

class AlignerStrategy(ABC):
    @abstractmethod
    def align(self, frame, frame_index, affine_transformations=None):
        pass
