import math

from Utility import Point

class Shape:
    def get_material(self):
        pass

    def hit(self, ray):
        pass
    
    def shadow_hit(self, ray):
        pass


class Sphere(Shape):
    def __init__(self, center, radius, material, block_light):
        self.center      = center
        self.radius      = radius
        self.material    = material
        self.block_light = block_light

    def hit(self, ray):
        # (p-c)*(p-c)-r^2=0
        # o+td=c
        # (d*d)*t^2+[2(o-c)*d]*t+(o-c)*(o-c)-r^2=0

        temp = ray.origin - self.center
        a = ray.direction * ray.direction
        b = 2.0 * temp * ray.direction
        c = temp * temp - self.radius * self.radius
        discriminant = b * b - 4.0 * a * c

        if discriminant < 0.0:
            return False
        else:
            e = math.sqrt(discriminant)
            t = (-b - e) / (2.0 * a)

            if t > 0.001:
                self.t = t
                hit_point = ray.origin + (self.t * ray.direction)
                self.hit_point_normal = (hit_point - self.center) / self.radius

#                v2o = Vector(0.0, 0.0, 0.0) - self.center
#                p2o = hit_point + v2o
#                self.local_hit_point = p2o + (self.radius * (-1.0 * self.hit_point_normal))
#                self.local_hit_point = hit_point + (self.radius * (-1.0 * self.hit_point_normal))
#                print v2o, p2o, self.radius, self.hit_point_normal, self.local_hit_point
                self.local_hit_point = Point(0.0, 0.0, 0.0) + self.hit_point_normal
                return True

            e = math.sqrt(discriminant)
            t = (-b + e) / (2.0 * a)

            if t > 0.001:
                self.t = t
                hit_point = ray.origin + (self.t * ray.direction)
                self.hit_point_normal = (hit_point - self.center) / self.radius

                v2o = Vector(0.0, 0.0, 0.0) - self.center
                p2o = hit_point + v2o
                self.local_hit_point = p2o + (self.radius * (-1.0 * self.hit_point_normal))
#                self.local_hit_point = hit_point + (self.radius * (-1.0 * self.hit_point_normal))
                self.local_hit_point = Point(0.0, 0.0, 0.0) + self.hit_point_normal
                return True

    def shadow_hit(self, ray):
        if not self.block_light:
            return False

        temp = ray.origin - self.center
        a = ray.direction * ray.direction
        b = 2.0 * temp * ray.direction
        c = temp * temp - self.radius * self.radius
        discriminant = b * b - 4.0 * a * c

        if discriminant < 0.0:
            return False
        else:
            e = math.sqrt(discriminant)
            t = (-b - e) / (2.0 * a)

            if t > 0.001:
                self.shadow_t = t
                return True

            e = math.sqrt(discriminant)
            t = (-b + e) / (2.0 * a)

            if t > 0.001:
                self.shadow_t = t            
                return True
        

class Plane:
    def __init__(self, center, normal, material, block_light):
        self.center      = center
        self.normal      = normal
        self.material    = material
        self.block_light = block_light

    def hit(self, ray):
        # (p - a) * n =0
        # (o + td -a) * n = 0
        # t = (a - o) * n / (d * n)
        t = (self.center -ray.origin) * self.normal / (ray.direction * self.normal)
        
        if t > 0.001:
            self.t = t
            hit_point = ray.origin + (self.t * ray.direction)
            self.hit_point_normal = self.normal
            self.local_hit_point = hit_point
            return True
        
        return False

    def shadow_hit(self, ray):
        if not self.block_light:
            return False

        t = (self.center - ray.origin) * self.normal / (ray.direction * (self.normal))
        
        if t > 0.001:
            self.shadow_t = t
            return True
        
        return False


class Rectangle(Shape):
    def __init__(self, p0, a, b, material, sampler, block_light):
        self.p0          = p0
        self.a           = a
        self.b           = b
        self.material    = material
        self.sampler     = sampler
        self.block_light = block_light

        normal = a.cross(b)
        self.normal = normal.normalize()

        area = a.length() * b.length()
        self.inv_area = 1.0 / area

    def hit(self, ray):
        t = self.p0.substract(ray.origin).dot(self.normal) / ray.direction.dot(self.normal)
        
        if t <= 0.001:
            return False

        hit_point = ray.origin.move(ray.direction.scalar(t))
        d = hit_point.substract(self.p0)

        ddota = d.dot(self.a)
        if ddota < 0.0 or ddota > self.a.length() * self.a.length():
            return False

        ddotb = d.dot(self.b)
        if ddotb < 0.0 or ddotb > self.b.length() * self.b.length():
            return False
            
        self.t = t
        self.hit_point_normal = self.normal
        self.local_hit_point = hit_point
        return True

    def sample(self):
        sample = self.sampler.sample_unit_square()
        return (self.p0.move(self.a.scalar(sample.x) + self.b.scalar(sample.y)))

    def pdf(self):
        return self.inv_area

    def shadow_hit(self, ray):
        if not self.block_light:
            return False

        t = self.p0.substract(ray.origin).dot(self.normal) / ray.direction.dot(self.normal)
        
        if t <= 0.001:
            return False

        hit_point = ray.origin.move(ray.direction.scalar(t))
        d = hit_point.substract(self.p0)

        ddota = d.dot(self.a)
        if ddota < 0.0 or ddota > self.a.length() * self.a.length():
            return False

        ddotb = d.dot(self.b)
        if ddotb < 0.0 or ddotb > self.b.length() * self.b.length():
            return False
            
        self.shadow_t = t
        return True
