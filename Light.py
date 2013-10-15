
class Light:
    pass

class DirectionalLight(Light):
    def __init__(self, ls, color, direction):
        self.ls        = ls
        self.color     = color
        self.direction = direction

    def get_direction(self):
        return self.direction

    def L(self):
        return self.color.scalar(self.ls)
