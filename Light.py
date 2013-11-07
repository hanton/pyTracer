import math
from Utility import Vector, Color, Ray

class Light:
    def get_direction(self):
        pass

    def L(self, shading_point):
        pass

class AmbientLight(Light):
    def __init__(self, ls, color):
        self.ls    = ls
        self.color = color

    def get_direction(self):
        return Vector(0.0, 0.0, 0.0)

    def L(self, shading_point):
        return self.ls * self.color


class AmbientOcclusion(Light):
    def __init__(self, ls, color, min_amount, sampler):
        self.ls          = ls
        self.color       = color
        self.min_amount  = min_amount
        self.sampler     = sampler
        
        self.sampler.map_samples_to_hemisphere(1)
        self.u, self.v, self.w = Vector(0.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0)

    def get_direction(self):
        sample = self.sampler.sample_hemisphere()
        return (sample.x * self.u + sample.y * self.v + sample.z * self.w)

    def L(self, shading_point):
        self.w = shading_point.normal
        # jitter the up vector
        up     = Vector(0.005, 1.0, 0.005)
        self.v = self.w.cross(up)
        self.v = self.v.normalize()
        self.u = self.v.cross(self.w)

        shadow_ray = Ray(shading_point.hit_point, self.get_direction())

        if self.in_shadow(shadow_ray, shading_point):
            return self.ls * self.color * self.min_amount
        else:
            return self.ls * self.color

    def in_shadow(self, ray, shading_point): 
        for shape in shading_point.scene.shapes:
            if shape.shadow_hit(ray):
                    return True

        return False


class PointLight(Light):
    def __init__(self, ls, color, location, cast_shadow):
        self.ls          = ls
        self.color       = color
        self.location    = location
        self.cast_shadow = cast_shadow

    def get_direction(self, shading_point):
        self.distance = (shading_point.hit_point - self.location).length()
        return shading_point.hit_point - self.location

    def L(self):
        return self.ls * self.color  / (self.distance * self.distance)

    def in_shadow(self, ray, shading_point):
        for shape in shading_point.scene.shapes:
            if shape.shadow_hit(ray):
                if shape.shadow_t < (self.location - shading_point.hit_point).length():
                    return True

        return False


class DirectionalLight(Light):
    def __init__(self, ls, color, direction, cast_shadow):
        self.ls          = ls
        self.color       = color
        self.direction   = direction
        self.cast_shadow = cast_shadow

    def get_direction(self, shading_point):
        return self.direction

    def L(self):
        return self.ls * self.color

    def in_shadow(self, ray, shading_point): 
        for shape in shading_point.scene.shapes:
            if shape.shadow_hit(ray):
                return True

        return False


class AreaLight(Light):
    def __init__(self, shape, cast_shadow):
        self.shape       = shape
        self.cast_shadow = cast_shadow

        self.sample       = Vector(0.0, 0.0, 0.0)
        self.light_normal = Vector(0.0, 0.0, 0.0)
        self.wi           = Vector(0.0, 0.0, 0.0)

    def get_direction(self, shading_point):
        self.sample = self.shape.sample()
        self.light_normal = self.shape.normal
        self.wi = self.sample - shading_point.hit_point
        self.wi = self.wi.normalize()
        return -1.0 * self.wi

    def in_shadow(self, ray, shading_point):
        ts = (self.sample - ray.origin) * ray.direction
        for shape in shading_point.scene.shapes:
            if shape.shadow_hit(ray) and shape.shadow_t < ts:
                return True

        return False

    def L(self):
        ndotd = -1.0 * self.wi * self.light_normal

        if ndotd > 0.0:
            return self.shape.material.Le()
        else:
            return Color(0.0, 0.0, 0.0)

    def G(self, shading_point):
        ndotd = -1.0 * self.light_normal * self.wi
        d2    = self.sample.distance(shading_point.hit_point)
        d2    = d2 * d2
        return ndotd / d2

    def pdf(self, shading_point):
        return self.shape.pdf()


class EnvironmentLight(Light):
    def __init__(self, material, sampler, cast_shadow):
        self.material    = material
        self.sampler     = sampler
        self.cast_shadow = cast_shadow
        
        self.sampler.map_samples_to_hemisphere(1)
        self.u, self.v, self.w = Vector(0.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0)
        self.wi = Vector(0.0, 0.0, 0.0)

    def get_direction(self, shading_point):
        self.w = shading_point.normal
        up     = Vector(0.003, 1.0, 0.007)
        self.v = up.cross(self.w)
        self.v = self.v.normalize()
        self.u = self.v.cross(self.w)
        sp = self.sampler.sample_hemisphere()
        self.wi = self.u.scalar(sp.x) + self.v.scalar(sp.y) + self.w.scalar(sp.z)
        return self.wi.scalar(-1.0)

    def in_shadow(self, ray, shading_point):
        for shape in shading_point.scene.shapes:
            if shape.shadow_hit(ray):
                return True

        return False

    def L(self):
        return self.material.Le()

    def G(self, shading_point):
        return 1.0

    def pdf(self, shading_point):
        return shading_point.normal.dot(self.wi) / math.pi
