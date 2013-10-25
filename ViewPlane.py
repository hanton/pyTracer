from Utility import Point, Vector, Ray
from Sampler import MultiJittered, Regular

class ViewPlane:
    def __init__(self, width, height, pixel_size, gamma, max_ray_depth, num_samples, num_sets):
        self.width      = width
        self.height     = height
        self.pixel_size = pixel_size
        self.gamma      = gamma
        self.max_ray_depth  = max_ray_depth
       
        if num_samples > 1:
            self.sampler = MultiJittered(num_samples, num_sets)
        else:
            self.sampler = Regular(1, num_sets)

        self.position = Point(0,0,0)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height
