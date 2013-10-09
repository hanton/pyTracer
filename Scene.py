from PIL import Image

from ViewPlane import ViewPlane
from Utility import Color, Point, Vector, Ray
from Shape import Sphere

class Scene:
    def __init__(self):
        self.shapes = []
        #self.lights = []

        width  = 600
        height = 600
        pixel_size = 1.0
        gamma = 1.0
        self.view_plane = ViewPlane(width, height, pixel_size, gamma)


    def add_shape(self, shape):
        self.shapes.append(shape)

    def build(self):
        #print("%s begin.", self)
        
        center = Point(0, 0, -2)
        radius = 10.0
        color = Color(255, 0, 0)
        sphere = Sphere(center, radius, color)
        self.add_shape(sphere)
        #print("%s %s end." % self.__name__, self.func_name)

    def render(self):
        #print("%s %s begin." % self.__name__, self.func_name)
        width  = self.view_plane.get_width()
        height = self.view_plane.get_height()
        picture = Image.new('RGB', (width, height))
        pixels = picture.load()
        
        for i in range(0, width):
            for j in range(0, height):
                ray = self.view_plane.get_ray(i, j)
                for shape in self.shapes:
                    if shape.hit(ray):
                        r, g, b = shape.get_color() 
                        pixels[i, j] = (r, g, b)
        picture.show()
        #print("%s %s end." % self.__name__, self.func_name)
