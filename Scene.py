from PIL import Image
from ViewPlane import ViewPlane
from Utility import Color, Point, Vector, Ray
from Shape import Sphere, Plane
from Tracer import RayCast
from Camera import PinholeCamera
from Light import AmbientLight, DirectionalLight
from ShadingPoint import ShadingPoint
from Material import Matte, Phong, ConstantColor, ImageTexture, SphericalMapping

class Scene:
    def __init__(self):
        self.shapes = []
        self.lights = []

    def add_light(self, light):
        self.lights.append(light)

    def add_shape(self, shape):
        self.shapes.append(shape)

    def build(self, width, height):
        num_samples    = 16
        num_sets       = 83
        pixel_size = 1.0
        gamma      = 1.0
        self.view_plane = ViewPlane(width, height, pixel_size, gamma, num_samples, num_sets)

        self.tracer = RayCast(self)
        self.background_color = Color(0.0, 0.0, 0.0)

        eye = Point(0, 0, -700)
        lookat = Point(0, 0, 1)
        up = Vector(0, 1, 0)
        viewplane_distance = 400
        self.camera = PinholeCamera(eye, lookat, up, viewplane_distance)
        self.camera.compute_uvw()

        image             = Image.open("earthmap1k.jpg")
        texels            = image.load()
        image_width, image_height = image.size
        spherical_mapping = SphericalMapping()
        texture           = ImageTexture(texels, spherical_mapping, image_width, image_height)
        ka                = 0.0
        kd                = 1.0
        matte             = Matte(ka, kd, texture)

        center = Point(0.0, 0.0, -100.0)
        radius = 100.0
        sphere = Sphere(center, radius, matte)
        self.add_shape(sphere)

        ka    = 0.0
        kd    = 1.0
        color = Color(0.0, 0.0, 1.0)
        constant_color = ConstantColor(color)
        matte = Matte(ka, kd, constant_color)

        center = Point(300.0, 0.0, -100.0)
        radius = 100.0
        sphere = Sphere(center, radius, matte)
        self.add_shape(sphere)

        ka    = 0.0
        kd    = 1.0
        color = Color(0.6, 0.6, 0.6)
        constant_color = ConstantColor(color)        
        matte = Matte(ka, kd, constant_color)
        center = Point(0.0, -100.0, 0.0)
        normal = Vector(0.0, 1.0, 0.0)
        plane = Plane(center, normal, matte)
        self.add_shape(plane)
        
        ka    = 0.0
        kd    = 0.5
        ks    = 0.5
        color = Color(0.0, 1.0, 0.0)
        constant_color = ConstantColor(color)
        exp   = 5.0
        phong = Phong(ka, kd, ks, constant_color, exp)

        center = Point(-300.0, 0.0, -100.0)
        radius = 100.0
        sphere = Sphere(center, radius, phong)
        self.add_shape(sphere)
        
        light_color     = Color(1.0, 1.0, 1.0)
        light_direction = Vector(1, -1, 1)
        light_intensity = 3.0
        cast_shadow     = True
        direction_light = DirectionalLight(light_intensity, light_color, light_direction, cast_shadow)
        self.add_light(direction_light)
        light_intensity    = 0.0
        self.ambient_light = AmbientLight(light_intensity, light_color)

    def hit_objects(self, ray_origin, ray_direction):
        ray = Ray(ray_origin, ray_direction)
        shading_point = ShadingPoint(self)
        tmin = 1e6  # default max distance

        for shape in self.shapes:
            if shape.hit(ray) and shape.t < tmin:
                shading_point.hit_an_object = True
                shading_point.material = shape.get_material()
                shading_point.hit_point = ray.origin.move(ray.direction.scalar(shape.t))
                shading_point.normal = shape.hit_point_normal
                shading_point.local_hit_point = shape.local_hit_point
                tmin = shape.t                                

        return shading_point
