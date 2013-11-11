#from PIL import Image
import pdb # for debug
import sys, time
from math import log10
from Utility import Color

class Camera:
    def __init__(self, eye, lookat, up, viewplane_distance):
        self.eye = eye
        self.lookat = lookat
        self.up = up
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
        width = scene.view_plane.get_width()
        height = scene.view_plane.get_height()
#        picture = Image.new('RGB', (width, height))
#        pixels = picture.load()
        pixels = [] # list

        ray_origin = self.eye
        
#        for row in xrange(height):
        for row in xrange(height - 1, -1, -1):
            for column in xrange(width):
                L = Color(0.0, 0.0, 0.0)
                for j in xrange(scene.view_plane.sampler.num_samples):
                    # sp range [0.0 ~ 1.0] [0.0 ~ 1.0]
                    sp = scene.view_plane.sampler.sample_unit_square()
                    px = scene.view_plane.pixel_size * (column - 0.5 * width + sp.x)
                    py = scene.view_plane.pixel_size * (row - 0.5 * height + sp.y)
                    ray_direction = self.ray_direction(px, py)
                    ray_depth = 0
#                    if row == height - 2 and column == 0:
#                        pdb.set_trace()
                    L = L + scene.tracer.trace_ray(ray_origin, ray_direction, ray_depth)
                L = L / scene.view_plane.sampler.num_samples

#                # clamp to >1.0 red, <0.0 green
#                if L.r > 1.0 or L.g > 1.0 or L.b > 1.0:
##                   L = Color(1.0, 0.0, 0.0)
#                    L = Color(1.0, 1.0, 1.0)
#                if L.r < 0.0 or L.g < 0.0 or L.b < 0.0:
#                    L = Color(0.0, 1.0, 0.0)
#                # Gamma Correction to 2.2
#                L = L.powc(1.0 / 2.2)
#                # color 0.0~1.0 to Image module's 0~255 color range
#                L = L * 255.0
#                # view plane coordinates to screen coordinates
##                pixels[column, height - 1 - row] = (int(L.r), int(L.g), int(L.b))
#                pixels.append((int(L.r), int(L.g), int(L.b)))
                pixels.append(L)
            sys.stdout.write("\r"+"Remain {0:.2f}%".format(float(row) / height * 100.0))
            sys.stdout.flush()
        
#        filename = "render.tiff"
#        picture.save(filename)
#        picture.show()

#        tone_mapping_scalar = linear_tone_mapping(pixels)
#        print tone_mapping_scalar
        pixels = nonlinear_tone_mapping(pixels)
        for i in xrange(len(pixels)):
#            # tone mapping        
#            pixels[i] = pixels[i] * tone_mapping_scalar
#            print pixels[i], tone_mapping_scalar
            # Gamma Correction 2.2
            pixels[i] = pixels[i].powc(1.0 / 2.2)
            # clamp to >1.0 red, <0.0 green
            if pixels[i].r > 1.0 or pixels[i].g > 1.0 or pixels[i].b > 1.0:
                pixels[i] = Color(1.0, 1.0, 1.0)
            if pixels[i].r < 0.0 or pixels[i].g < 0.0 or pixels[i].b < 0.0:
                pixels[i] = Color(0.0, 1.0, 0.0)
            # color 0.0~1.0 to Image module's 0~255 color range
            pixels[i] = pixels[i] * 255.0

        # ppm file
        write_ppm("./Render/render" + str(time.time()) + ".ppm", width, height, pixels)


class ThinLens(Camera):
    def __init__(self):
        pass

    def ray_direction(self, x, y):
        pass

    def render(self, scene):
        pass

# Contrast-based Linear Scale
# Ward, Greg, A Contrast-Based Scalefactor for Luminance Display, Graphics Gems IV, p. 415-421.
def linear_tone_mapping(pixels):
    sum_of_logs = 0.0
    for pixel in pixels:
        # RGB Luminance is (0.2126,0.7152,0.0722)
        y = pixel.r * 0.2126 + pixel.g * 0.7152 + pixel.b * 0.0722
        sum_of_logs += log10(y if y > 1e-4 else 1e-4)
    adapt_luminance = 10.0 ** (sum_of_logs / len(pixels))
    display_luminance_max = 100.0
    a = 1.219 + (display_luminance_max / 2.0) ** 0.4
    b = 1.219 + adapt_luminance ** 0.4
    return ((a / b) ** 2.5) / display_luminance_max

# Spatially Varying Nonlinear Scale
# Erik Reinhard, Mike Stark, Peter Shirley and Jim Ferwerda, 'Photographic Tone Reproduction for Digital Images', ACM Transactions on Graphics, 21(3), pp 267--276, July 2002 (Proceedings of SIGGRAPH 2002).
def nonlinear_tone_mapping(pixels):
    max_y = 0.0
    for pixel in pixels:
        # RGB Luminance is (0.2126,0.7152,0.0722)
        y = pixel.r * 0.2126 + pixel.g * 0.7152 + pixel.b * 0.0722
        max_y = max(max_y, y)
    invY2 = 1.0 / (max_y * max_y)
    tone_mapped = []
    for pixel in pixels:
        y = pixel.r * 0.2126 + pixel.g * 0.7152 + pixel.b * 0.0722 
        scalar = (1.0 + y * invY2) / (1.0 + y)
        pixel = pixel * scalar
        tone_mapped.append(pixel)
    return tone_mapped

def write_ppm(filename, width, height, pixels):
    with open(filename, 'wb') as f:
        f.write('P6 %d %d 255\n' % (width, height))
# pixels.reverse()
        for pixel in pixels:
            f.write(chr(int(pixel.r)) + chr(int(pixel.g)) + chr(int(pixel.b)))
        f.close()
