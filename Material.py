import math
from Utility import Color, Ray, Vector

class Material:
    def shade(self, shading_point):
        pass


class Matte(Material):
    def __init__(self, ka, kd, cd, sampler = None):
        self.ambient_brdf = Lambertian(ka, cd)
        self.diffuse_brdf = Lambertian(kd, cd, sampler)
        
    def shade(self, shading_point):
        L = self.ambient_brdf.rho(shading_point) * shading_point.scene.ambient_light.L(shading_point)
        for light in shading_point.scene.lights:
            wi = light.get_direction(shading_point) * -1.0
            wi = wi.normalize()
            ndotwi = shading_point.normal * wi
            if ndotwi > 0.0:
                in_shadow = False

                if light.cast_shadow:
                    shadow_ray = Ray(shading_point.hit_point, wi)
                    in_shadow = light.in_shadow(shadow_ray, shading_point)
                if not in_shadow:
                    L = L + self.diffuse_brdf.f(shading_point) * light.L() * ndotwi

        return L

    def area_light_shade(self, shading_point):
        L = self.ambient_brdf.rho(shading_point) * shading_point.scene.ambient_light.L(shading_point)
        for light in shading_point.scene.lights:
            wi = -1.0 * light.get_direction(shading_point)
            wi = wi.normalize()
            ndotwi = shading_point.normal * wi
            if ndotwi > 0.0:
                in_shadow = False

                if light.cast_shadow:
                    shadow_ray = Ray(shading_point.hit_point, wi)
                    in_shadow = light.in_shadow(shadow_ray, shading_point)
                if not in_shadow:
                    L = L + self.diffuse_brdf.f(shading_point) * light.L()
                    L = L * ndotwi * light.G(shading_point) / light.pdf(shading_point)

        return L

    def path_shade(self, shading_point):
        pdf, wi, f  = self.diffuse_brdf.sample_f(shading_point)
        ndotwi = shading_point.normal * wi
        reflected_ray_origin = shading_point.hit_point
        reflected_ray_dicrection = wi
        return (f * shading_point.scene.tracer.trace_ray(reflected_ray_origin, reflected_ray_dicrection, shading_point.ray_depth + 1) * ndotwi / pdf)


class Phong(Material):
    def __init__(self, ka, kd, ks, cd, exp):
        self.ambient_brdf = Lambertian(ka, cd)
        self.diffuse_brdf = Lambertian(kd, cd)
        self.specular_brdf = GlossySpecular(ks, exp, cd)
        
    def shade(self, shading_point):
        wo = shading_point.ray.direction * -1.0
        wo = wo.normalize()
        L = self.ambient_brdf.rho(shading_point) * shading_point.scene.ambient_light.L(shading_point)
        for light in shading_point.scene.lights:
            wi = light.get_direction(shading_point) * -1.0
            wi = wi.normalize()
            ndotwi = shading_point.normal * wi
            if ndotwi > 0.0:
                in_shadow = False

                if light.cast_shadow:
                    shadow_ray = Ray(shading_point.hit_point, wi)
                    in_shadow = light.in_shadow(shadow_ray, shading_point)
                if not in_shadow:
                    L = L + (self.diffuse_brdf.f(shading_point) + self.specular_brdf.f(shading_point, wo, wi)) * light.L()  * ndotwi

        return L

    def area_light_shade(self, shading_point):
        wo = shading_point.ray.direction * -1.0
        wo = wo.normalize()
        L = self.ambient_brdf.rho(shading_point) * shading_point.scene.ambient_light.L(shading_point)
        for light in shading_point.scene.lights:
            wi = light.get_direction(shading_point) * -1.0
            wi = wi.normalize()
            ndotwi = shading_point.normal * wi
            if ndotwi > 0.0:
                in_shadow = False

                if light.cast_shadow:
                    shadow_ray = Ray(shading_point.hit_point, wi)
                    in_shadow = light.in_shadow(shadow_ray, shading_point)
                if not in_shadow:
                    L = L + (self.diffuse_brdf.f(shading_point) + self.specular_brdf.f(shading_point, wo, wi)) * light.L() 
                    L = L * ndotwi * light.G(shading_point) / light.pdf(shading_point)

        return L


class Reflective(Phong):
    def __init__(self, ka, kd, ks, cd, exp, kr, cr):
        Phong.__init__(self, ka, kd, ks, cd, exp)
        self.reflective_brdf = PerfectSpecular(kr, cr)
        
    def shade(self, shading_point):
        #L = Color(0.0, 0.0, 0.0)
        L = Phong.shade(self, shading_point)

        wo = shading_point.ray.direction * -1.0
        fr = self.reflective_brdf.sample_f(shading_point, wo)
        wi = self.reflective_brdf.wi
        reflected_ray_origin = shading_point.hit_point
        reflected_ray_direction = wi
        ndotwi = shading_point.normal.dot(wi)
        L = L + shading_point.scene.tracer.trace_ray(reflected_ray_origin, reflected_ray_direction, shading_point.ray_depth + 1) * fr.scalar(ndotwi)

        return L

    def path_shade(self, shading_point):
        wo = -1.0 * shading_point.ray.direction
        pdf, wi, fr = self.reflective_brdf.sample_f(shading_point, wo)
        ndotwi = shading_point.normal * wi
        reflected_ray = Ray(shading_point.hit_point, wi)

        return (fr * shading_point.scene.tracer.trace_ray(reflected_ray, shading_point.depth + 1) * ndotwi / pdf)


class Emissive(Material):
    def __init__(self, ls, ce):
        self.ls = ls
        self.ce = ce

    def area_light_shade(self, shading_point):
        wo = shading_point.ray.direction * -1.0
        wo = wo.normalize()  
        if shading_point.normal * wo > 0.0:
            return self.ls * self.ce 
        else:
            return Color(0.0, 0.0, 0.0)

    def path_shade(self, shading_point):
        wo = shading_point.ray.direction * -1.0
        wo = wo.normalize()  
        if shading_point.normal * wo > 0.0:
            return self.ls * self.ce 
        else:
            return Color(0.0, 0.0, 0.0)
    
    def Le(self):
        return self.ls * self.ce


class BRDF:
    def f(self):
        pass


class Lambertian(BRDF):
    def __init__(self, kd, surface, sampler = None):
        self.kd      = kd
        self.surface = surface
        if sampler != None:
            self.sampler = sampler
            self.sampler.map_samples_to_hemisphere(1)

    def rho(self, shading_point):
        color = self.surface.get_color(shading_point)
        return  self.kd * color
    
    def f(self, shading_point):
        color = self.surface.get_color(shading_point)
        return (self.kd * color) / math.pi

    def sample_f(self, shading_point):
        w = shading_point.normal
        # jitter the up vector
        v = Vector(0.0024, 1.0, 0.0081).cross(w)
        v = v.normalize()
        u = v.cross(w)

        sample_point = self.sampler.sample_hemisphere()
        wi = sample_point.x * u + sample_point.y * v + sample_point.z * w
        wi = wi.normalize()
        pdf = shading_point.normal * wi / math.pi
        color = self.surface.get_color(shading_point)
        return pdf, wi, (self.kd * color / math.pi)


class GlossySpecular(BRDF):
    def __init__(self, ks, exp, surface):
        self.ks  = ks
        self.exp = exp
        self.surface  = surface

    def f(self, shading_point, wo, wi):
        ndotwi = shading_point.normal * wi
        r = wi * -1.0 + shading_point.normal * (2.0 * ndotwi)
        rdotwo = r * wo

        if rdotwo > 0.0:
            color = self.surface.get_color(shading_point)
            return (self.ks * color) * pow(rdotwo, self.exp)
        else:
            return Color(0.0, 0.0, 0.0)


class PerfectSpecular(BRDF):
    def __init__(self, kr, surface):
        self.kr      = kr
        self.surface = surface

    def sample_f(self, shading_point, wo):
        ndotwo = shading_point.normal * wo
        wi     = wo * -1.0 + shading_point.normal * (2.0 * ndotwo)
        pdf = shading_point.normal * wi
        color = self.surface.get_color(shading_point)
        return pdf, wi, (self.kr * color)
        

class Surface:
    def get_color(self, shading_point):
        pass


class ConstantColor(Surface):
    def __init__(self, color):
        self.color = color

    def get_color(self, shading_point = None):
        return self.color


class ImageTexture(Surface):
    def __init__(self, texels, mapping, image_width, image_height):
        self.texels  = texels
        self.mapping = mapping
        self.hres    = image_width
        self.vres    = image_height

    def get_color(self, shading_point):
        column, row = self.mapping.get_texel_coordinates(shading_point.local_hit_point, self.hres, self.vres)
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
        column = int((hres - 1) * u)
        row    = int((vres - 1) * v)

        return column, row
