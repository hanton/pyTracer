from ViewPlane import ViewPlane
from Utility import Color, Point, Vector, Ray
from Shape import Sphere
from Tracer import RayCast
from Camera import PinholeCamera
from Light import DirectionalLight
from ShadingPoint import ShadingPoint
from Material import Matte

class Scene:
    def __init__(self):
        self.shapes = []
        self.lights = []

    def add_light(self, light):
        self.lights.append(light)

    def add_shape(self, shape):
        self.shapes.append(shape)

    def build(self):
        width  = 600
        height = 600
        pixel_size = 1.0
        gamma = 1.0
        self.view_plane = ViewPlane(width, height, pixel_size, gamma)

        self.tracer = RayCast(self)
        self.background_color = Color(0, 0, 0)

        eye = Point(0, 0, 50)
        lookat = Point(0, 0, -1)
        up = Vector(0, 1, 0)
        viewplane_distance = 40
        self.camera = PinholeCamera(eye, lookat, up, viewplane_distance)
        self.camera.compute_uvw()

        blue = Color(0, 0, 255)
        kd   = 0.8
        matte = Matte(kd, blue)

        center = Point(0, 0, -10)
        radius = 100.0
        sphere = Sphere(center, radius, matte)
        self.add_shape(sphere)
        
        light_direction = Vector(0, 0, -1)
        light_color = Color(255, 255, 255)
        direction_light = DirectionalLight(3.0, light_color, light_direction)
        self.add_light(direction_light)

    def hit_objects(self, ray_origin, ray_direction):
        ray = Ray(ray_origin, ray_direction)
        shading_point = ShadingPoint(self)
        tmin = 1e6  # default max distance

        for shape in self.shapes:
            if shape.hit(ray) and shape.t < tmin:
                shading_point.hit_an_object = True
                shading_point.material = shape.get_material()
                shading_point.hit_point = ray.origin.move(ray.direction.scalar(shape.t))
                shading_point.normal = (ray.origin.substract(shape.center) + ray.direction.scalar(shape.t)).scalar(1.0 / shape.radius)       
                shading_point.local_hit_point = ray.origin.move(ray.direction.scalar(shape.t))
                tmin = shape.t                                

        return shading_point
