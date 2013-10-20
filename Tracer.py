from Utility import Ray

class Tracer:
    def __init__(self, scene):
        self.scene = scene

    def trace_ray(self, ray_origin, ray_direction):
        pass


class RayCast(Tracer):
    def trace_ray(self, ray_origin, ray_direction):
        shading_point = self.scene.hit_objects(ray_origin, ray_direction)
         
        if(shading_point.hit_an_object):
            ray = Ray(ray_origin, ray_direction)
            shading_point.ray = ray
            return shading_point.material.shade(shading_point)
        else:
            return self.scene.background_color


class AreaLighting(Tracer):
    def trace_ray(self, ray_origin, ray_direction):
        shading_point = self.scene.hit_objects(ray_origin, ray_direction)
         
        if(shading_point.hit_an_object):
            ray = Ray(ray_origin, ray_direction)
            shading_point.ray = ray
            return shading_point.material.area_light_shade(shading_point)
        else:
            return self.scene.background_color
