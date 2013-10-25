from PIL import Image

from ViewPlane import * 
from Utility import *
from Shape import *
from Tracer import *
from Camera import *
from Light import *
from ShadingPoint import *
from Material import *
from Sampler import *

class Scene:
    def __init__(self):
        self.shapes = []
        self.lights = []

    def add_light(self, light):
        self.lights.append(light)

    def add_shape(self, shape):
        self.shapes.append(shape)

    def build(self, width, height, samples):
        num_samples    = samples
        num_sets       = 83  # default vaule
        pixel_size     = 1.0
        gamma          = 1.0
        max_ray_depth  = 0
        self.view_plane = ViewPlane(width, height, pixel_size, gamma, max_ray_depth, num_samples, num_sets)
        self.background_color = Color(0.0, 0.0, 0.0)

        eye = Point(-900, 900, 900)
        lookat = Point(0, 0, 1)
        up = Vector(0, 1, 0)
        viewplane_distance = 300
        self.camera = PinholeCamera(eye, lookat, up, viewplane_distance)
        self.camera.compute_uvw()

        #self.tracer = RayCast(self)        
        #self.diffuse_specular_texture_directionlight_shadow()
        #self.ambient_occlusion(num_samples, num_sets)
        
        #self.tracer = AreaLighting(self)
        #self.area_lighting(num_samples, num_sets)

        self.tracer = Whitted(self)
        self.perfect_specular(num_samples, num_sets)

    def hit_objects(self, ray_origin, ray_direction):
        ray = Ray(ray_origin, ray_direction)
        shading_point = ShadingPoint(self)
        tmin = 1e6  # default max distance

        for shape in self.shapes:
            if shape.hit(ray) and shape.t < tmin:
                shading_point.hit_an_object = True
                shading_point.material = shape.material
                shading_point.hit_point = ray.origin.move(ray.direction.scalar(shape.t))
                shading_point.normal = shape.hit_point_normal
                shading_point.local_hit_point = shape.local_hit_point
                tmin = shape.t                                

        return shading_point

    def diffuse_specular_texture_directionlight_shadow(self):
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
        block_light = True        
        sphere = Sphere(center, radius, matte, block_light)
        self.add_shape(sphere)

        ka    = 0.0
        kd    = 1.0
        color = Color(0.0, 0.0, 1.0)
        constant_color = ConstantColor(color)
        matte = Matte(ka, kd, constant_color)
        center = Point(300.0, 0.0, -100.0)
        radius = 100.0
        block_light = True
        sphere = Sphere(center, radius, matte, block_light)
        self.add_shape(sphere)

        ka    = 0.0
        kd    = 1.0
        color = Color(0.6, 0.6, 0.6)
        constant_color = ConstantColor(color)        
        matte = Matte(ka, kd, constant_color)
        center = Point(0.0, -100.0, 0.0)
        normal = Vector(0.0, 1.0, 0.0)
        block_light = True
        plane = Plane(center, normal, matte, block_light)
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
        block_light = True
        sphere = Sphere(center, radius, phong, block_light)
        self.add_shape(sphere)

        light_color     = Color(1.0, 1.0, 1.0)
        light_intensity    = 0.0
        self.ambient_light = AmbientLight(light_intensity, light_color)

        light_color     = Color(1.0, 1.0, 1.0)
        light_direction = Vector(1, -1, 1)
        light_intensity = 3.0
        cast_shadow     = True
        direction_light = DirectionalLight(light_intensity, light_color, light_direction, cast_shadow)
        self.add_light(direction_light)

    def ambient_occlusion(self, num_samples, num_sets):
        ka    = 0.5
        kd    = 0.5
        color = Color(0.0, 1.0, 0.0)
        constant_color = ConstantColor(color)
        matte = Matte(ka, kd, constant_color)
        center = Point(0.0, 0.0, -100.0)
        radius = 100.0
        sphere = Sphere(center, radius, matte)
        self.add_shape(sphere)

        ka    = 0.5
        kd    = 0.5
        color = Color(0.6, 0.6, 0.6)
        constant_color = ConstantColor(color)        
        matte = Matte(ka, kd, constant_color)
        center = Point(0.0, -100.0, 0.0)
        normal = Vector(0.0, 1.0, 0.0)
        plane = Plane(center, normal, matte)
        self.add_shape(plane)

        light_color     = Color(1.0, 1.0, 1.0)
        light_intensity = 1.0
        min_amount      = 0.0
        sampler         = MultiJittered(num_samples, num_sets)
        self.ambient_light = AmbientOcclusion(light_intensity, light_color, min_amount, sampler)

    def area_lighting(self, num_samples, num_sets):
        ka    = 0.0
        kd    = 1.0
        color = Color(0.0, 1.0, 0.0)
        constant_color = ConstantColor(color)
        matte = Matte(ka, kd, constant_color)
        center = Point(0.0, 0.0, -100.0)
        radius = 100.0
        block_light = True
        sphere = Sphere(center, radius, matte, block_light)
        self.add_shape(sphere)

        ka    = 0.0
        kd    = 1.0
        color = Color(0.6, 0.6, 0.6)
        constant_color = ConstantColor(color)        
        matte = Matte(ka, kd, constant_color)
        center = Point(0.0, -100.0, 0.0)
        normal = Vector(0.0, 1.0, 0.0)
        block_light = True
        plane = Plane(center, normal, matte, block_light)
        self.add_shape(plane)

        intensity = 40.0
        color     = Color(1.0, 1.0, 1.0)
        emissive  = Emissive(intensity, color)
        p0          = Point(-400.0, 120.0, 0.0)
        a           = Vector(0.0, 0.0, -100.0)
        b           = Vector(50.0, 100.0, 0.0)
        sampler     = MultiJittered(num_samples, num_sets)
        block_light = False
        rectangle = Rectangle(p0, a, b, emissive, sampler, block_light)
        self.add_shape(rectangle)
        cast_shadow = True
        area_light = AreaLight(rectangle, cast_shadow)
        self.add_light(area_light)

        intensity   = 0.3
        color       = Color(1.0, 1.0, 0.5)
        emissive    = Emissive(intensity, color)
        material    = emissive
        sampler     = MultiJittered(num_samples, num_sets)
        cast_shadow = True
        environment_light = EnvironmentLight(emissive, sampler, cast_shadow)
        #self.add_light(environment_light)

        light_color     = Color(1.0, 1.0, 1.0)
        light_intensity    = 0.0
        self.ambient_light = AmbientLight(light_intensity, light_color)        

    def perfect_specular(self, num_samples, num_sets):
        self.view_plane.max_ray_depth = 3
        self.view_plane.pixel_size    = 0.2

        ka    = 0.0
        kd    = 0.6
        ks    = 0.15
        color = Color(1.0, 0.0, 0.0)
        constant_color = ConstantColor(color)
        exp   = 100.0
        kr = 0.75
        kc = Color(1.0, 1.0, 1.0)
        reflective = Reflective(ka, kd, ks, constant_color, exp, kr, kc)
        center = Point(-300.0, 0.0, -100.0)
        radius = 100.0
        block_light = True        
        sphere = Sphere(center, radius, reflective, block_light)
        self.add_shape(sphere)

        ka    = 0.0
        kd    = 0.6
        ks    = 0.15
        color = Color(0.0, 1.0, 0.0)
        constant_color = ConstantColor(color)
        exp   = 100.0
        kr = 0.75
        kc = Color(1.0, 1.0, 1.0)
        reflective = Reflective(ka, kd, ks, constant_color, exp, kr, kc)
        center = Point(0.0, 0.0, -100.0)
        radius = 100.0
        block_light = True        
        sphere = Sphere(center, radius, reflective, block_light)
        self.add_shape(sphere)

        ka    = 0.0
        kd    = 0.6
        ks    = 0.15
        color = Color(0.0, 0.0, 1.0)
        constant_color = ConstantColor(color)
        exp   = 100.0
        kr = 0.75
        kc = Color(1.0, 1.0, 1.0)
        reflective = Reflective(ka, kd, ks, constant_color, exp, kr, kc)
        center = Point(-150.0, 0.0, 100.0)
        radius = 100.0
        block_light = True                
        sphere = Sphere(center, radius, reflective, block_light)
        self.add_shape(sphere)

        ka    = 0.0
        kd    = 1.0
        color = Color(0.6, 0.6, 0.6)
        constant_color = ConstantColor(color)        
        matte = Matte(ka, kd, constant_color)
        center = Point(0.0, -100.0, 0.0)
        normal = Vector(0.0, 1.0, 0.0)
        block_light = True        
        plane = Plane(center, normal, matte, block_light)
        self.add_shape(plane)

        light_color     = Color(1.0, 1.0, 1.0)
        light_intensity    = 0.0
        self.ambient_light = AmbientLight(light_intensity, light_color)        

        light_color     = Color(1.0, 1.0, 1.0)
        light_direction = Vector(-1.0, -2.0, -3.0)
        light_intensity = 3.0
        cast_shadow     = True
        direction_light = DirectionalLight(light_intensity, light_color, light_direction, cast_shadow)
        self.add_light(direction_light)
