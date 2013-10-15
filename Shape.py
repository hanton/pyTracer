import math

class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material  = material

    def get_material(self):
        return self.material

    def hit(self, ray):
        # (p-c)*(p-c)-r^2=0
        # o+td=c
        # (d*d)*t^2+[2(o-c)*d]*t+(o-c)*(o-c)-r^2=0

        temp = ray.origin.substract(self.center)
        a = ray.direction.dot(ray.direction)
        b = 2.0 * temp.dot(ray.direction)
        c = temp.dot(temp) - self.radius * self.radius
        discriminant = b * b - 4.0 * a * c

        if discriminant < 0.0:
            return False
        else:
            e = math.sqrt(discriminant)
            t = (-b - e) / (2.0 * a)

            if t > 0.001:
                self.t = t
                return True

            e = math.sqrt(discriminant)
            t = (-b + e) / (2.0 * a)

            if t > 0.001:
                self.t = t
                return True
