from abc import ABC, abstractmethod

class Filter(ABC):
    @abstractmethod
    def apply(self, data):
        # data: lista de listas o arrays, 
        # donde cada lista/array interna tiene la misma longitud y unidad
        pass

class FilterChain:
    def __init__(self):
        self.filters: list[Filter] = []
    
    def add_filter(self, filter: Filter):
        self.filters.append(filter)
    
    def apply_filters(self, data):
        if len(self.filters) == 0:
            return data
        for filter in self.filters:
            data = filter.apply(data)
        return data
    
    def clear_filters(self):
        self.filters = []
