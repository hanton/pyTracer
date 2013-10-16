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
        #wo = -shading_point.ray.direction
        L = self.ambient_brdf.rho() * shading_point.scene.ambient_light.L()
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
                    L = L + self.diffuse_brdf.f() * light.L()
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
        L = self.ambient_brdf.rho() * shading_point.scene.ambient_light.L()
        for light in shading_point.scene.lights:
            wi = light.get_direction().scalar(-1.0)
            wi = wi.normalize()
            ndotwi = shading_point.normal.dot(wi)
            if ndotwi > 0.0:
                L = L + (self.diffuse_brdf.f() + self.specular_brdf.f(shading_point, wo, wi)) * light.L()
                L = L.scalar(ndotwi)

        return L


class BRDF:
    def f(self):
        pass


class Lambertian(BRDF):
    def __init__(self, kd, cd):
        self.kd = kd
        self.cd = cd

    def rho(self):
        return self.cd.scalar(self.kd)
    
    def f(self):
        return self.cd.scalar(self.kd / math.pi)


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
            return self.cd.scalar(self.ks * pow(rdotwo, self.exp))
        else:
            return Color(0.0, 0.0, 0.0)
