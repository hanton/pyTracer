#from PIL import Image

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

#        self.tracer = RayCast(self)        
#        self.diffuse_specular_texture_directionlight_shadow()
#        self.ambient_occlusion(num_samples, num_sets)
        
        self.tracer = AreaLighting(self)
        self.area_lighting(num_samples, num_sets)

#        self.tracer = Whitted(self)
#        self.perfect_specular(num_samples, num_sets)

#        self.tracer = PathTracer(self)
#        self.path_tracing(num_samples, num_sets)

    def hit_objects(self, ray_origin, ray_direction):
        ray = Ray(ray_origin, ray_direction)
        shading_point = ShadingPoint(self)
        tmin = 1e6  # default max distance

        for shape in self.shapes:
            if shape.hit(ray) and shape.t < tmin:
                shading_point.hit_an_object = True
                shading_point.material = shape.material
                shading_point.hit_point = ray.origin + (shape.t * ray.direction)
                shading_point.normal = shape.hit_point_normal
                shading_point.local_hit_point = shape.local_hit_point
                tmin = shape.t                                

        return shading_point

    # Cornell Box
    def cornell_box(self):
        height = 100.0
        width  = 100.0
        depth  = 100.0
        origin = Point(0.0, height / 2.0, 0.0)

        # Ceiling
        ka    = 0.0
        kd    = 1.0
        color = Color(1.0, 1.0, 0.0)
        constant_color = ConstantColor(color)
        sampler     = None #MultiJittered(num_samples, num_sets)
        matte = Matte(ka, kd, constant_color, sampler)
        p0          = Point(origin.x - width / 2.0, origin.y + height / 2.0, origin.z - depth / 2.0)
        a           = Vector(width, 0.0, 0.0)
        b           = Vector(0.0, 0.0, depth)
        sampler     = None #MultiJittered(num_samples, num_sets)
        block_light = True
        rectangle = Rectangle(p0, a, b, matte, sampler, block_light)
        self.add_shape(rectangle)

        # Ground
        ka    = 0.0
        kd    = 1.0
        color = Color(0.0, 1.0, 1.0)
        constant_color = ConstantColor(color)
        sampler     = None #MultiJittered(num_samples, num_sets)
        matte = Matte(ka, kd, constant_color, sampler)
        p0          = Point(origin.x - width / 2.0, origin.y - height / 2.0, origin.z + depth / 2.0)
        a           = Vector(width, 0.0, 0.0)
        b           = Vector(0.0, 0.0, -depth)
        sampler     = None #MultiJittered(num_samples, num_sets)
        block_light = True
        rectangle = Rectangle(p0, a, b, matte, sampler, block_light)
        self.add_shape(rectangle)

        # Left
        ka    = 0.0
        kd    = 1.0
        color = Color(1.0, 0.0, 0.0)
        constant_color = ConstantColor(color)
        sampler     = None #MultiJittered(num_samples, num_sets)
        matte = Matte(ka, kd, constant_color, sampler)
        p0          = Point(origin.x - width / 2.0, origin.y - height / 2.0, origin.z + depth / 2.0)
        a           = Vector(0.0, 0.0, -depth)
        b           = Vector(0.0, height, 0.0)
        sampler     = None #MultiJittered(num_samples, num_sets)
        block_light = True
        rectangle = Rectangle(p0, a, b, matte, sampler, block_light)
        self.add_shape(rectangle)

        # Right
        ka    = 0.0
        kd    = 1.0
        color = Color(0.0, 1.0, 0.0)
        constant_color = ConstantColor(color)
        sampler     = None #MultiJittered(num_samples, num_sets)
        matte = Matte(ka, kd, constant_color, sampler)
        p0          = Point(origin.x + width / 2.0, origin.y - height / 2.0, origin.z - depth / 2.0)
        a           = Vector(0.0, 0.0, depth)
        b           = Vector(0.0, height, 0.0)
        sampler     = None #MultiJittered(num_samples, num_sets)
        block_light = True
        rectangle = Rectangle(p0, a, b, matte, sampler, block_light)
        self.add_shape(rectangle)

        # Back
        ka    = 0.0
        kd    = 1.0
        color = Color(3.0, 3.0, 3.0)
        constant_color = ConstantColor(color)
        sampler     = None #MultiJittered(num_samples, num_sets)
        matte = Matte(ka, kd, constant_color, sampler)
        p0          = Point(origin.x - width / 2.0, origin.y - height / 2.0, origin.z - depth / 2.0)
        a           = Vector(width, 0.0, 0.0)
        b           = Vector(0.0, height, 0.0)
        sampler     = None #MultiJittered(num_samples, num_sets)
        block_light = True
        rectangle = Rectangle(p0, a, b, matte, sampler, block_light)
        self.add_shape(rectangle)

    def diffuse_specular_texture_directionlight_shadow(self):
        # 1280 * 720
        self.view_plane.pixel_size    = 0.09

#        # 640 * 320
#        self.view_plane.pixel_size    = 0.2

        # Camera
        eye = Point(0, 50, 200)
        lookat = Point(0, 50, 50)
        up = Vector(0, 1, 0)
        viewplane_distance = 100
        self.camera = PinholeCamera(eye, lookat, up, viewplane_distance)
        self.camera.compute_uvw()

        self.cornell_box()

#        image             = Image.open("earthmap1k.jpg")
#        texels            = image.load()
#        image_width, image_height = image.size
#        spherical_mapping = SphericalMapping()
#        texture           = ImageTexture(texels, spherical_mapping, image_width, image_height)
#        ka                = 0.0
#        kd                = 1.0
#        matte             = Matte(ka, kd, texture)
#        radius = 20.0
#        center = Point(25.0, radius, -20.0)
#        block_light = True        
#        sphere = Sphere(center, radius, matte, block_light)
#        self.add_shape(sphere)

        ka    = 0.0
        kd    = 1.0
        color = Color(0.0, 0.0, 1.0)
        constant_color = ConstantColor(color)
        matte = Matte(ka, kd, constant_color)
        radius = 15.0
        center = Point(-25.0, radius, 0.0)
        block_light = True
        sphere = Sphere(center, radius, matte, block_light)
        self.add_shape(sphere)

        ka    = 0.0
        kd    = 0.7
        ks    = 0.3
        color = Color(0.0, 1.0, 0.0)
        constant_color = ConstantColor(color)
        exp   = 80.0
        phong = Phong(ka, kd, ks, constant_color, exp)
        radius = 10.0
        center = Point(10.0, radius, 20.0)
        block_light = True
        sphere = Sphere(center, radius, phong, block_light)
        self.add_shape(sphere)

        light_color     = Color(1.0, 1.0, 1.0)
        light_intensity    = 0.0
        self.ambient_light = AmbientLight(light_intensity, light_color)

#        light_color     = Color(1.0, 1.0, 1.0)
#        light_direction = Vector(0.1, -1.0, -1.0)
#        light_intensity = 0.05
#        cast_shadow     = True
#        direction_light = DirectionalLight(light_intensity, light_color, light_direction, cast_shadow)
#        self.add_light(direction_light)

        light_color     = Color(1.0, 1.0, 1.0)
        light_location = Vector(0.0, 50.0, 40.0)
        light_intensity = 0.95 * 3000
        cast_shadow     = True
        point_light= PointLight(light_intensity, light_color, light_location, cast_shadow)
        self.add_light(point_light)

    def ambient_occlusion(self, num_samples, num_sets):
        # 1280 * 720
        self.view_plane.pixel_size    = 1.0

#        # 640 * 320
#        self.view_plane.pixel_size    = 0.2

        # Camera
        eye = Point(0, 50, 150)
        lookat = Point(0, 15, 0)
        up = Vector(0, 1, 0)
        viewplane_distance = 100
        self.camera = PinholeCamera(eye, lookat, up, viewplane_distance)
        self.camera.compute_uvw()

        ka    = 0.5
        kd    = 0.5
        color = Color(1.0, 1.0, 1.0)
        constant_color = ConstantColor(color)
        matte = Matte(ka, kd, constant_color)
        radius = 100.0
        center = Point(0.0, radius, 0.0)
        block_light = True
        sphere = Sphere(center, radius, matte, block_light)
        self.add_shape(sphere)

        ka    = 0.5
        kd    = 0.5
        color = Color(0.6, 0.6, 0.6)
        constant_color = ConstantColor(color)        
        matte = Matte(ka, kd, constant_color)
        center = Point(0.0, 0.0, 0.0)
        normal = Vector(0.0, 1.0, 0.0)
        block_light = True
        plane = Plane(center, normal, matte, block_light)
        self.add_shape(plane)

        light_color     = Color(1.0, 1.0, 1.0)
        light_intensity = 1.0
        min_amount      = 0.0
        sampler         = MultiJittered(num_samples, num_sets)
        self.ambient_light = AmbientOcclusion(light_intensity, light_color, min_amount, sampler)

    def area_light_box(self, num_samples, num_sets):
        height = 2.0
        width  = 35.0
        depth  = 35.0
        origin = Point(0.0, 100.0 - height / 2.0, 0.0)

        # Front
        intensity = 10.0
        color     = Color(1.0, 1.0, 1.0)
        emissive  = Emissive(intensity, color)
        p0          = Point(origin.x + width / 2.0, origin.y + height / 2.0, origin.z + depth / 2.0)
        a           = Vector(-width, 0.0, 0.0)
        b           = Vector(0.0, -height, 0.0)
        sampler     = MultiJittered(num_samples, num_sets)
        block_light = False
        rectangle = Rectangle(p0, a, b, emissive, sampler, block_light)
        self.add_shape(rectangle)
        cast_shadow = True
        area_light = AreaLight(rectangle, cast_shadow)
        self.add_light(area_light)

        # Ground
        intensity = 10.0
        color     = Color(1.0, 1.0, 1.0)
        emissive  = Emissive(intensity, color)
        p0          = Point(origin.x - width / 2.0, origin.y - height / 2.0, origin.z - depth / 2.0)
        a           = Vector(width, 0.0, 0.0)
        b           = Vector(0.0, 0.0, depth)
        sampler     = MultiJittered(num_samples, num_sets)
        block_light = False
        rectangle = Rectangle(p0, a, b, emissive, sampler, block_light)
        self.add_shape(rectangle)
        cast_shadow = True
        area_light = AreaLight(rectangle, cast_shadow)
        self.add_light(area_light)

        # Left
        intensity = 10.0
        color     = Color(1.0, 1.0, 1.0)
        emissive  = Emissive(intensity, color)
        p0          = Point(origin.x - width / 2.0, origin.y - height / 2.0, origin.z - depth / 2.0)
        a           = Vector(0.0, 0.0, depth)
        b           = Vector(0.0, height, 0.0)
        sampler     = MultiJittered(num_samples, num_sets)
        block_light = False
        rectangle = Rectangle(p0, a, b, emissive, sampler, block_light)
        self.add_shape(rectangle)
        cast_shadow = True
        area_light = AreaLight(rectangle, cast_shadow)
        self.add_light(area_light)

        # Right
        intensity = 10.0
        color     = Color(1.0, 1.0, 1.0)
        emissive  = Emissive(intensity, color)
        p0          = Point(origin.x + width / 2.0, origin.y + height / 2.0, origin.z - depth / 2.0)
        a           = Vector(0.0, 0.0, depth)
        b           = Vector(0.0, -height, 0.0)
        sampler     = MultiJittered(num_samples, num_sets)
        block_light = False
        rectangle = Rectangle(p0, a, b, emissive, sampler, block_light)
        self.add_shape(rectangle)
        cast_shadow = True
        area_light = AreaLight(rectangle, cast_shadow)
        self.add_light(area_light)

        # Back
        intensity = 10.0
        color     = Color(1.0, 1.0, 1.0)
        emissive  = Emissive(intensity, color)
        p0          = Point(origin.x + width / 2.0, origin.y - height / 2.0, origin.z - depth / 2.0)
        a           = Vector(-width, 0.0, 0.0)
        b           = Vector(0.0, height, 0.0)
        sampler     = MultiJittered(num_samples, num_sets)
        block_light = False
        rectangle = Rectangle(p0, a, b, emissive, sampler, block_light)
        self.add_shape(rectangle)
        cast_shadow = True
        area_light = AreaLight(rectangle, cast_shadow)
        self.add_light(area_light)

    def area_lighting(self, num_samples, num_sets):
        # 740 * 740
        self.view_plane.pixel_size    = 0.09

#        # 640 * 320
#        self.view_plane.pixel_size    = 0.2

        # Camera
        eye = Point(0, 50, 200)
        lookat = Point(0, 50, 50)
        up = Vector(0, 1, 0)
        viewplane_distance = 100
        self.camera = PinholeCamera(eye, lookat, up, viewplane_distance)
        self.camera.compute_uvw()

        self.cornell_box()
        self.area_light_box(num_samples, num_sets)


#        image             = Image.open("earthmap1k.jpg")
#        texels            = image.load()
#        image_width, image_height = image.size
#        spherical_mapping = SphericalMapping()
#        texture           = ImageTexture(texels, spherical_mapping, image_width, image_height)
#        ka                = 0.0
#        kd                = 1.0
#        matte             = Matte(ka, kd, texture)
#        radius = 20.0
#        center = Point(25.0, radius, -20.0)
#        block_light = True        
#        sphere = Sphere(center, radius, matte, block_light)
#        self.add_shape(sphere)

        ka    = 0.0
        kd    = 1.0
        color = Color(0.0, 0.0, 1.0)
        constant_color = ConstantColor(color)
        matte = Matte(ka, kd, constant_color)
        radius = 15.0
        center = Point(-25.0, radius, 0.0)
        block_light = True
        sphere = Sphere(center, radius, matte, block_light)
        self.add_shape(sphere)

        ka    = 0.0
        kd    = 0.7
        ks    = 0.3
        color = Color(0.0, 1.0, 0.0)
        constant_color = ConstantColor(color)
        exp   = 80.0
        phong = Phong(ka, kd, ks, constant_color, exp)
        radius = 10.0
        center = Point(10.0, radius, 20.0)
        block_light = True
        sphere = Sphere(center, radius, phong, block_light)
        self.add_shape(sphere)

#        intensity   = 0.3
#        color       = Color(1.0, 1.0, 0.5)
#        emissive    = Emissive(intensity, color)
#        material    = emissive
#        sampler     = MultiJittered(num_samples, num_sets)
#        cast_shadow = True
#        environment_light = EnvironmentLight(emissive, sampler, cast_shadow)
#        self.add_light(environment_light)

        light_color     = Color(1.0, 1.0, 1.0)
        light_intensity    = 0.0
        self.ambient_light = AmbientLight(light_intensity, light_color)        

    def perfect_specular(self, num_samples, num_sets):
        self.view_plane.max_ray_depth = 2
        self.view_plane.pixel_size    = 0.13

        # Camera
        eye = Point(0, 100, 150)
        lookat = Point(0, 0, -100)
        up = Vector(0, 1, 0)
        viewplane_distance = 100
        self.camera = PinholeCamera(eye, lookat, up, viewplane_distance)
        self.camera.compute_uvw()

         # ks = kr
#        ka    = 0.0
#        kd    = 0.25
#        ks    = 0.75
#        color = Color(1.0, 0.0, 0.0)
#        constant_color = ConstantColor(color)
#        exp   = 100.0
#        kr = 0.75
#        kc = Color(1.0, 1.0, 1.0)
#        reflective = Reflective(ka, kd, ks, constant_color, exp, kr, kc)
#        center = Point(-300.0, 0.0, -100.0)
#        radius = 100.0
#        block_light = True        
#        sphere = Sphere(center, radius, reflective, block_light)
#        self.add_shape(sphere)

        # Middle Diffuse Sphere
        ka    = 0.0
        kd    = 1.0
        color = Color(0.0, 1.0, 0.0)
        constant_color = ConstantColor(color)
        matte = Matte(ka, kd, constant_color)
        center = Point(0.0, 10.0, -10.0)
        radius = 10.0
        block_light = True
        sphere = Sphere(center, radius, matte, block_light)
        self.add_shape(sphere)

        # Ground Diffuse Plane
        ka    = 0.0
        kd    = 1.0
        color = Color(0.6, 0.6, 0.6)
        constant_color = ConstantColor(color)
        matte = Matte(ka, kd, constant_color)
        center = Point(0.0, 0.0, 0.0)
        normal = Vector(0.0, 1.0, 0.0)
        block_light = True        
        plane = Plane(center, normal, matte, block_light)
        self.add_shape(plane)
        
#        # Left Rectangle
#        ka    = 0.0
#        kd    = 0.5
#        ks    = 0.25
#        color = Color(0.0, 0.0, 1.0)
#        constant_color = ConstantColor(color)
#        exp   = 100.0
#        kr = 0.75
#        kc = Color(1.0, 1.0, 1.0)
#        reflective = Reflective(ka, kd, ks, constant_color, exp, kr, kc)
#        p0          = Point(0.0, 0.0, -60.0)
#        a           = Vector(-50.0, 0.0, 50.0)
#        b           = Vector(0.0, 50.0, 0.0)
#        sampler     = MultiJittered(num_samples, num_sets)
#        block_light = True
#        left_rectangle = Rectangle(p0, a, b, reflective, sampler, block_light)
#        self.add_shape(left_rectangle)
#
#        # Right Rectangle
#        ka    = 0.0
#        kd    = 0.5
#        ks    = 0.25
#        color = Color(0.0, 0.0, 1.0)
#        constant_color = ConstantColor(color)
#        exp   = 100.0
#        kr = 0.75
#        kc = Color(1.0, 1.0, 1.0)
#        reflective = Reflective(ka, kd, ks, constant_color, exp, kr, kc)
#        p0          = Point(0.0, 0.0, -60.0)
#        a           = Vector(50.0, 0.0, 50.0)
#        b           = Vector(0.0, 50.0, 0.0)
#        sampler     = MultiJittered(num_samples, num_sets)
#        block_light = True
#        right_rectangle = Rectangle(p0, a, b, reflective, sampler, block_light)
#        self.add_shape(right_rectangle)

        # Ambient Light
        light_color     = Color(1.0, 1.0, 1.0)
        light_intensity    = 0.0
        self.ambient_light = AmbientLight(light_intensity, light_color)

        # Direction Light
        light_color     = Color(1.0, 1.0, 1.0)
        light_direction = Vector(-1.0, -2.0, -3.0)
        light_intensity = 1.0
        cast_shadow     = True
        direction_light = DirectionalLight(light_intensity, light_color, light_direction, cast_shadow)
        self.add_light(direction_light)

        # Second Direction Light
        light_color     = Color(1.0, 1.0, 1.0)
        light_direction = Vector(1.0, -1.0, 0.0)
        light_intensity = 0.6
        cast_shadow     = True
        direction_light = DirectionalLight(light_intensity, light_color, light_direction, cast_shadow)
        self.add_light(direction_light)

    def path_tracing(self, num_samples, num_sets):
        self.view_plane.pixel_size    = 0.1
        self.view_plane.max_ray_depth = 1

        # Camera
        eye = Point(0, 5, 150)
        lookat = Point(0, 0, 0)
        up = Vector(0, 1, 0)
        viewplane_distance = 100
        self.camera = PinholeCamera(eye, lookat, up, viewplane_distance)
        self.camera.compute_uvw()

        ka    = 0.0
        kd    = 1.0
        color = Color(0.0, 0.0, 1.0)
        constant_color = ConstantColor(color)
        sampler     = MultiJittered(num_samples, num_sets)
        matte = Matte(ka, kd, constant_color, sampler)
        center = Point(0.0, 0.0, -10.0)
        radius = 10.0
        block_light = True
        sphere = Sphere(center, radius, matte, block_light)
        self.add_shape(sphere)

        ka    = 0.0
        kd    = 1.0
        color = Color(0.6, 0.6, 0.6)
        constant_color = ConstantColor(color)
        sampler     = MultiJittered(num_samples, num_sets)
        matte = Matte(ka, kd, constant_color, sampler)
        center = Point(0.0, -10.0, 0.0)
        normal = Vector(0.0, 1.0, 0.0)
        block_light = True
        plane = Plane(center, normal, matte, block_light)
        self.add_shape(plane)
        
        intensity = 1.0
        color     = Color(1.0, 1.0, 1.0)
        emissive  = Emissive(intensity, color)
        p0          = Point(-40.0, 12.0, 0.0)
        a           = Vector(0.0, 0.0, -10.0)
        b           = Vector(5.0, 10.0, 0.0)
        sampler     = MultiJittered(num_samples, num_sets)
        block_light = False
        rectangle = Rectangle(p0, a, b, emissive, sampler, block_light)
        self.add_shape(rectangle)
        cast_shadow = True
        area_light = AreaLight(rectangle, cast_shadow)
        self.add_light(area_light)
