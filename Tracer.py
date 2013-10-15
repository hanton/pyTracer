
class Tracer:
    pass


class RayCast:
    def __init__(self, scene):
        self.scene = scene

    def trace_ray(self, ray_origin, ray_direction):
        shading_point = self.scene.hit_objects(ray_origin, ray_direction)
         
        if(shading_point.hit_an_object):
            #print "hit"
            #shading_point.ray = ray
            return shading_point.material.shade(shading_point)
        else:
            return self.scene.background_color
