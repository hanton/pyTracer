import math

from Utility import Point, Vector

class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color  = color

    def get_color(self):
        return self.color.r, self.color.g, self.color.b

    def hit(self, ray):
        p0 = ray.origin
        pc = self.center
        d = ray.direction
        r = self.radius

        a = d.dot(d)
        v = p0.substract(pc)
        b = d.scalar(2).dot(v)
        c = v.dot(v) - r**2
        try:
            val1 = (-b+math.sqrt(b**2 - (4*a*c)))/(2*a)
            val2 = (-b-math.sqrt(b**2 - (4*a*c)))/(2*a)
        except ValueError:
            return False
            
        return True
