from Utility import Vector

class Light:
    pass

class AmbientLight(Light):
    def __init__(self, ls, color):
        self.ls    = ls
        self.color = color

    def get_direction(self):
        return Vector(0.0, 0.0, 0.0)

    def L(self):
        return self.color.scalar(self.ls)

class DirectionalLight(Light):
    def __init__(self, ls, color, direction, cast_shadow):
        self.ls          = ls
        self.color       = color
        self.direction   = direction
        self.cast_shadow = cast_shadow

    def get_direction(self):
        return self.direction

    def L(self):
        return self.color.scalar(self.ls)

    def in_shadow(self, ray, shading_point): 
        for shape in shading_point.scene.shapes:
            if shape.shadow_hit(ray):
                return True

        return False
