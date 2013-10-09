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

    def get_ray(self, i, j):
        x = self.pixel_size * (i - self.width/2 + 0.5)
        y = self.pixel_size * (j - self.height/2 + 0.5)
        z = -1  # hard core
        
        ray_origin = Point(x, y, 0)
        ray_direction = Vector(0, 0, z)
        return Ray(ray_origin, ray_direction)
