from Utility import Ray, Color

class Tracer:
    def __init__(self, scene):
        self.scene = scene

    def trace_ray(self, ray_origin, ray_direction):
        pass


class RayCast(Tracer):
    def trace_ray(self, ray_origin, ray_direction, ray_depth):
        shading_point = self.scene.hit_objects(ray_origin, ray_direction)
         
        if(shading_point.hit_an_object):
            ray = Ray(ray_origin, ray_direction)
            shading_point.ray = ray
            return shading_point.material.shade(shading_point)
        else:
            return self.scene.background_color


class AreaLighting(Tracer):
    def trace_ray(self, ray_origin, ray_direction, ray_depth):
        shading_point = self.scene.hit_objects(ray_origin, ray_direction)
         
        if(shading_point.hit_an_object):
            ray = Ray(ray_origin, ray_direction)
            shading_point.ray = ray
            return shading_point.material.area_light_shade(shading_point)
        else:
            return self.scene.background_color


class Whitted(Tracer):
    def trace_ray(self, ray_origin, ray_direction, ray_depth):
        if ray_depth > self.scene.view_plane.max_ray_depth:
            return Color(0.0, 0.0, 0.0)
        else:
            shading_point = self.scene.hit_objects(ray_origin, ray_direction)
            if(shading_point.hit_an_object):
                ray = Ray(ray_origin, ray_direction)
                shading_point.ray   = ray
                shading_point.ray_depth = ray_depth
                return shading_point.material.shade(shading_point)
            else:
                return self.scene.background_color

