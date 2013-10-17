import math
from Utility import Color, Ray

class Material:
    def shade(self, shading_point):
        pass


class Matte(Material):
    def __init__(self, ka, kd, cd):
        self.ambient_brdf = Lambertian(ka, cd)
        self.diffuse_brdf = Lambertian(kd, cd)
        
    def shade(self, shading_point):
        L = self.ambient_brdf.rho(shading_point) * shading_point.scene.ambient_light.L()
        for light in shading_point.scene.lights:
            wi = light.get_direction().scalar(-1.0)
            wi = wi.normalize()
            ndotwi = shading_point.normal.dot(wi)
            if ndotwi > 0.0:
                in_shadow = False

                if light.cast_shadow:
                    shadow_ray = Ray(shading_point.hit_point, wi)
                    in_shadow = light.in_shadow(shadow_ray, shading_point)
                if not in_shadow:
                    L = L + self.diffuse_brdf.f(shading_point) * light.L()
                    L = L.scalar(ndotwi)

        return L


class Phong(Material):
    def __init__(self, ka, kd, ks, cd, exp):
        self.ambient_brdf = Lambertian(ka, cd)
        self.diffuse_brdf = Lambertian(kd, cd)
        self.specular_brdf = GlossySpecular(ks, exp, cd)
        
    def shade(self, shading_point):
        wo = shading_point.ray.direction.scalar(-1.0)
        wo = wo.normalize()
        L = self.ambient_brdf.rho(shading_point) * shading_point.scene.ambient_light.L()
        for light in shading_point.scene.lights:
            wi = light.get_direction().scalar(-1.0)
            wi = wi.normalize()
            ndotwi = shading_point.normal.dot(wi)
            if ndotwi > 0.0:
                in_shadow = False

                if light.cast_shadow:
                    shadow_ray = Ray(shading_point.hit_point, wi)
                    in_shadow = light.in_shadow(shadow_ray, shading_point)
                if not in_shadow:
                    L = L + (self.diffuse_brdf.f(shading_point) + self.specular_brdf.f(shading_point, wo, wi)) * light.L()
                    L = L.scalar(ndotwi)

        return L


class BRDF:
    def f(self):
        pass


class Lambertian(BRDF):
    def __init__(self, kd, cd):
        self.kd = kd
        self.cd = cd

    def rho(self, shading_point):
        return self.cd.get_color(shading_point).scalar(self.kd)
    
    def f(self, shading_point):
        return self.cd.get_color(shading_point).scalar(self.kd / math.pi)


class GlossySpecular(BRDF):
    def __init__(self, ks, exp, cd):
        self.ks  = ks
        self.exp = exp
        self.cd  = cd

    def f(self, shading_point, wo, wi):
        ndotwi = shading_point.normal.dot(wi)
        r = wi.scalar(-1.0) + shading_point.normal.scalar(2.0 * ndotwi)
        rdotwo = r.dot(wo)

        if rdotwo > 0.0:
            return self.cd.get_color(shading_point).scalar(self.ks * pow(rdotwo, self.exp))
        else:
            return Color(0.0, 0.0, 0.0)


class Surface:
    def get_color(self, shading_point):
        pass


class ConstantColor(Surface):
    def __init__(self, color):
        self.color = color

    def get_color(self, shading_point):
        return self.color


class ImageTexture(Surface):
    def __init__(self, texels, mapping, image_width, image_height):
        self.texels  = texels
        self.mapping = mapping
        self.hres    = image_width
        self.vres    = image_height

    def get_color(self, shading_point):
        self.mapping.get_texel_coordinates(shading_point.local_hit_point, self.hres, self.vres)
        column  = self.mapping.column
        row     = self.mapping.row
        r, g, b = self.texels[column, row]
        return Color(r / 255.0, g / 255.0, b / 255.0)


class Mapping:
    def get_texel_coordinates(self, local_hit_point, hres, vres):
        pass


class SphericalMapping(Mapping):
    def __init__(self):
        self.column = 0
        self.row    = 0

    def get_texel_coordinates(self, local_hit_point, hres, vres):
        theta = math.acos(local_hit_point.y)
        phi   = math.atan2(local_hit_point.x, local_hit_point.z)
        pi    = math.pi
        
        if phi < 0.0:
            phi += 2.0 * pi
         
        u = phi * (1.0 / (2.0 * pi))
        v = 1.0 - theta * (1.0 / pi)
        self.column = int((hres - 1) * u)
        self.row    = int((vres - 1) * v)
