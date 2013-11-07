#from PIL import Image
import sys, time
from Utility import Color

class Camera:
    def __init__(self, eye, lookat, up, viewplane_distance):
        self.eye                = eye
        self.lookat             = lookat
        self.up                 = up
        self.viewplane_distance = viewplane_distance

    def compute_uvw(self):
        self.w = self.eye - self.lookat
        self.w = self.w.normalize()
        self.u = self.up.cross(self.w)
        self.u = self.u.normalize()
        self.v = self.w.cross(self.u)


class PinholeCamera(Camera):
    def ray_direction(self, x, y):
        direction = x * self.u + y * self.v - self.viewplane_distance * self.w
        direction = direction.normalize()

        return direction

    def render(self, scene):
        width  = scene.view_plane.get_width()
        height = scene.view_plane.get_height()
#        picture = Image.new('RGB', (width, height))
#        pixels = picture.load()
        pixels = []  # list

        ray_origin = self.eye
        
#        for row in xrange(height):
        for row in xrange(height, 0, -1):
            for column in xrange(width):
                L = Color(0.0, 0.0, 0.0)                
                for j in xrange(scene.view_plane.sampler.num_samples):
                    # sp range [0.0 ~ 1.0] [0.0 ~ 1.0]
                    sp = scene.view_plane.sampler.sample_unit_square()
                    px = scene.view_plane.pixel_size * (column - 0.5 * width + sp.x)
                    py = scene.view_plane.pixel_size * (row - 0.5 * height + sp.y) 
                    ray_direction = self.ray_direction(px, py)
                    ray_depth = 0
                    L = L + scene.tracer.trace_ray(ray_origin, ray_direction, ray_depth)
                L = L / scene.view_plane.sampler.num_samples

                # clamp to >1.0 red, <0.0 green
                if L.r > 1.0 or L.g > 1.0 or L.b > 1.0:
                    L = Color(1.0, 0.0, 0.0)
                if L.r < 0.0 or L.g < 0.0 or L.b < 0.0:
                    L = Color(0.0, 1.0, 0.0)
                # Gamma Correction to 2.2
                L = L.powc(1.0 / 2.2)
                # color 0.0~1.0 to Image module's 0~255 color range
                L = L * 255.0
                # view plane coordinates to screen coordinates
#                pixels[column, height - 1 - row] = (int(L.r), int(L.g), int(L.b))
                pixels.append((int(L.r), int(L.g), int(L.b)))
#            sys.stdout.write("\r\x1b[K"+"Render {0:.2f}%".format(float(row + 1) / height * 100.0))
            sys.stdout.write("\r\x1b[K"+"Remain {0:.2f}%".format(float(row - 1) / height * 100.0))
            sys.stdout.flush()
        
#        filename = "render.tiff"        
#        picture.save(filename)
#        picture.show()

        # ppm file
        write_ppm("./Render/render" + str(time.time()) + ".ppm", width, height, pixels)


class ThinLens(Camera):
    def __init__(self):
        pass

    def ray_direction(self, x, y):
        pass

    def render(self, scene):
        pass


def write_ppm(filename, width, height, pixels):
    with open(filename, 'wb') as f:
        f.write('P6 %d %d 255\n' % (width, height))
#        pixels.reverse()
        for pixel in pixels:
            f.write(chr(pixel[0]) + chr(pixel[1]) + chr(pixel[2]))
        f.close()
