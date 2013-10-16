import math

class Color:
    def __init__(self, red, green, blue):
        self.r, self.g, self.b = red, green, blue
   
    def __str__(self):
        return "(%s,%s,%s)" % (self.r, self.g, self.b)

    def __repr__(self): 
        return "Color" + str(self)
    
    def __add__(self, other): 
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)
    
    def __sub__(self, other): 
        return Color(self.r - other.r, self.g - other.g, self.b - other.b)
    
    def __mul__(self, other): 
        return Color(self.r * other.r, self.g * other.g, self.b * other.b)

    def scalar(self, scalar): 
        return Color(scalar * self.r, scalar * self.g, scalar * self.b)

    def pow(self, power):
        return Color(self.r ** power, self.g ** power, self.b ** power)


class Point:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def __str__(self): 
        return "(%s,%s,%s)" % (self.x, self.y, self.z)

    def __repr__(self): 
        return "Point" + str(self)
         
    def move(self, vector): 
        return Point(self.x + vector.x, self.y + vector.y, self.z + vector.z)
    
    def substract(self, other): 
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)


class Vector(object):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def __str__(self): 
        return "(%s,%s,%s)" % (self.x, self.y, self.z)

    def __repr__(self): 
        return "Vector" + str(self)
    
    def __add__(self, other): 
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other): 
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def scalar(self, scalar): 
        return Vector(scalar * self.x, scalar * self.y, scalar * self.z)

    def dot(self, other): 
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other): 
        return Vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self): 
        length = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        return self.scalar(1.0 / self.length())


class Ray:
    def __init__(self, origin, direction):
        self.origin    = origin
        self.direction = direction
