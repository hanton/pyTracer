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
                hit_point = ray.origin.move(ray.direction.scalar(self.t))
                self.hit_point_normal = hit_point.substract(self.center).scalar(1.0 / self.radius) 
                self.local_hit_point = hit_point
                return True

            e = math.sqrt(discriminant)
            t = (-b + e) / (2.0 * a)

            if t > 0.001:
                self.t = t
                hit_point = ray.origin.move(ray.direction.scalar(self.t))
                self.hit_point_normal = hit_point.substract(self.center).scalar(1.0 / self.radius)
                self.local_hit_point = hit_point
                return True

    def shadow_hit(self, ray):
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
                return True

            e = math.sqrt(discriminant)
            t = (-b + e) / (2.0 * a)

            if t > 0.001:
                return True
        

class Plane:
    def __init__(self, center, normal, material):
        self.center   = center
        self.normal   = normal
        self.material = material

    def get_material(self):
        return self.material

    def hit(self, ray):
        # (p - a) * n =0
        # (o + td -a) * n = 0
        # t = (a - o) * n / (d * n)
        t = self.center.substract(ray.origin).dot(self.normal) / ray.direction.dot(self.normal)
        
        if t > 0.001:
            self.t = t
            hit_point = ray.origin.move(ray.direction.scalar(self.t))
            self.hit_point_normal = self.normal
            self.local_hit_point = hit_point
            return True
        
        return False

    def shadow_hit(self, ray):
        t = self.center.substract(ray.origin).dot(self.normal) / ray.direction.dot(self.normal)
        
        if t > 0.001:
            return True
        
        return False
