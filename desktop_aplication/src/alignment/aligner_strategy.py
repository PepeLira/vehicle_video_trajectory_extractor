from abc import ABC, abstractmethod

class AlignerStrategy(ABC):
    @abstractmethod
    def __init__(self):
        """ The strategies must be initialized with at least the following attributes:
            - self.affine_transformations = None list of affine transformations for each frame
        """
        raise NotImplementedError("The aligner strategy must be initialized with at least the affine_transformations attribute")
    @abstractmethod
    def align(self, frame, frame_index, affine_transformations=None):
        """ Aligns one frame given the affine transformations for each frame
            - frame: frame to align
            - frame_index: the index of the frame to align (0 is the first frame)
            - affine_transformations: list of affine transformations for each frame (eg: [theta, s, tx, ty])
        """
        raise NotImplementedError("The align method must be implemented")
    @abstractmethod
    def update_affine_transformations(self, affine_transformations):
        """ Updates the affine transformations for each frame
            - affine_transformations: list of affine transformations for each frame (eg: [theta, s, tx, ty])
        """
        raise NotImplementedError("The update_affine_transformations method must be implemented")
