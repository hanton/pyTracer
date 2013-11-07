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
        if isinstance(other, Color):
#        if type(other) == Color:
            return Color(self.r * other.r, self.g * other.g, self.b * other.b)
        else:
            return Color(self.r * other, self.g * other, self.b * other)

    def __rmul__(self, other): 
        if isinstance(other, Color):
#        if type(other) == Color:
            return Color(self.r * other.r, self.g * other.g, self.b * other.b)
        else:
            return Color(self.r * other, self.g * other, self.b * other)

    def __div__(self, other):
        return Color(self.r / other, self.g / other, self.b / other)

    def powc(self, power):
        return Color(self.r ** power, self.g ** power, self.b ** power)


class Point:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def __str__(self): 
        return "(%s,%s,%s)" % (self.x, self.y, self.z)

    def __repr__(self): 
        return "Point" + str(self)
         
    def __add__(self, vector):
        # move the point in the vector direction
        return Point(self.x + vector.x, self.y + vector.y, self.z + vector.z)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)

#    def scalar(self, scalar):
#        return Point(self.x * scalar, self.y * scalar, self.z * scalar)


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

    def __mul__(self, other):
#        if isinstance(other, Vector):
        if type(other) == Vector:
            # dot multiple
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:    
            # scale
            return Vector(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other): 
#        if isinstance(other, Vector):
        if type(other) == Vector:
            # dot multiple
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:    
            # scale
            return Vector(self.x * other, self.y * other, self.z * other)

    def __div__(self, other):
        return Vector(self.x / other, self.y / other, self.z / other)

    def cross(self, other): 
        return Vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self): 
#        return self / self.length()
        return self / math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)


class Ray:
    def __init__(self, origin, direction):
        self.origin    = origin
        self.direction = direction
