from PIL import Image

from processingstrategy import ProcessingStrategy

class PillowStrategy(ProcessingStrategy):
    
    def __init__(self) -> None:
        super().__init__()
        
    def open(self, path):
        return Image.open(path)
    
    def find_size(self, img):
        return img.size
    
    def resize(self, img):
        return img.resize((600, 480))
    
    def save_image(self, img, name):
        img.save(name)
        