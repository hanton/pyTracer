from PIL import Image

class Camera:
    pass


class PinholeCamera(Camera):
    def __init__(self, eye, lookat, up, viewplane_distance):
        self.eye                = eye
        self.lookat             = lookat
        self.up                 = up
        self.viewplane_distance = viewplane_distance

    def compute_uvw(self):
        self.w = self.eye.substract(self.lookat)
        self.w.normalize()
        self.u = self.up.cross(self.w)
        self.u.normalize()
        self.v = self.w.cross(self.u)

    def ray_direction(self, x, y):
        return direction

    def render(self, scene):
        width  = scene.view_plane.get_width()
        height = scene.view_plane.get_height()
        picture = Image.new('RGB', (width, height))
        pixels = picture.load()
        ray_origin = self.eye
        
        for row in range(0, width):
            for column in range(0, height):
                px = scene.view_plane.pixel_size * (column - 0.5 * height)
                py = scene.view_plane.pixel_size * (row - 0.5 * width) 
                ray_direction = self.u.scalar(px) + self.v.scalar(py) - self.w.scalar(self.viewplane_distance)
                ray_direction.normalize()
                L = scene.tracer.trace_ray(ray_origin, ray_direction)
                pixels[row, column] = (int(L.r), int(L.g), int(L.b))

        picture.show()
