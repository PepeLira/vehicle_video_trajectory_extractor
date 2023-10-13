from .filter_chain import Filter

class MovingAverageFilter(Filter):
    def __init__(self, window_size=3):
        self.window_size = window_size
    
    def apply(self, data):
        if self.window_size <= 0:
            raise ValueError("Window size must be a positive integer")
        
        if self.window_size > len(data):
            raise ValueError("Window size must be less than or equal to the size of data")
        
        moving_averages = []
        for i in range(len(data) - self.window_size + 1):
            window = data[i:i + self.window_size]
            average = sum(window) / self.window_size
            moving_averages.append(average)
        
        return moving_averages
    
    def __str__(self):
        return f"Moving Average Filter (window_size={self.window_size})"
