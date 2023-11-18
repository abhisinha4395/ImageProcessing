from abc import ABC, abstractmethod

class ProcessingStrategy(ABC):
    
    @abstractmethod
    def open(self, path):
        raise NotImplementedError

    @abstractmethod
    def find_size(self):
        raise NotImplementedError
    
    @abstractmethod
    def resize(self):
        raise NotImplementedError
    
    @abstractmethod
    def save_image(self, img, name):
        raise NotImplementedError