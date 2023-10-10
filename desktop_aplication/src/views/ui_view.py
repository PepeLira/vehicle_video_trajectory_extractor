from abc import ABC, abstractmethod

class UIView(ABC):
    @abstractmethod
    def get_user_input(self):
        pass
    
    @abstractmethod
    def update_progress(self, progress):
        pass
    
    @abstractmethod
    def display_results(self, results):
        pass