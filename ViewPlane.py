from Utility import Point, Vector, Ray

class ViewPlane:
    def __init__(self, width, height, pixel_size, gamma):
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        self.gamma = gamma
        
        self.position = Point(0,0,0)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height
