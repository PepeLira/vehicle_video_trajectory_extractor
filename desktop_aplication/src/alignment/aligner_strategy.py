from abc import ABC, abstractmethod

class AlignerStrategy(ABC):
    @abstractmethod
    def align(self, frames):
        pass
