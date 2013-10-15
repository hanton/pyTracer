import math
from Utility import Color

class Material:
    def shade(self, shading_point):
        pass


class Matte(Material):
    def __init__(self, kd, cd):
        self.diffuse_brdf = Lambertian(kd, cd)
        
    def shade(self, shading_point):
        #wo = -shading_point.ray.direction
        L = Color(0, 0, 0)
        for light in shading_point.scene.lights:
            wi = light.get_direction()
            print shading_point.normal
            ndotwi = shading_point.normal.dot(wi)
            ndotwi = - ndotwi
            #print ndotwi
            if ndotwi > 0.0:
                L += self.diffuse_brdf.f() * light.L().scalar(ndotwi)

        return L


class BRDF:
    def f(self):
        pass


class Lambertian(BRDF):
    def __init__(self, kd, cd):
        self.kd = kd
        self.cd = cd

    def f(self):
        return self.cd.scalar(self.kd / math.pi)
