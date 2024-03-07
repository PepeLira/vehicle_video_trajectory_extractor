from .filter_chain import Filter

class MovingAverageFilter(Filter):
    def __init__(self, window_size=5):
        if window_size <= 0:
            raise ValueError("Window size must be a positive integer")
        self.window_size = window_size

    def apply(self, data):
        n = len(data)
        if self.window_size > n:
            return data

        moving_averages = []
        for i in range(n - self.window_size + 1):
            window = data[i:i + self.window_size]
            average = sum(window) / self.window_size
            moving_averages.append(average)
        
        pad_start = (self.window_size - 1) // 2
        pad_end = self.window_size // 2
        
        for _ in range(pad_start):
            moving_averages.insert(0, moving_averages[0])
        
        for _ in range(pad_end):
            moving_averages.append(moving_averages[-1])

        return moving_averages

    def __str__(self):
        return f"Moving Average Filter (window_size={self.window_size})"

if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    filter = MovingAverageFilter(4)
    print(filter.apply(data))