#from PIL import Image
import pdb # for debug
import sys, time
from math import log10, sqrt
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

#        # Bloom Effect
#        pixels = blooming_effect(pixels, width, height)

        # Tone Mapping
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

    
# Apply Bloom Filter
# K. Chiu, M. Herf, P. Shirley, S. Swamy, C. Wang, and K. Zimmerman. Spatially nonuniform scaling functions for high contrast images. In Proceedings of Graphics Interface '93, pages 245--253, 1993.
def blooming_effect(pixels, width, height):
    bloom_radius = 0.05
    bloom_weight = 0.2
    bloom_exp = 6.0
    if bloom_radius > 0.0 and bloom_weight > 0.0:
        bloom_width = int(bloom_radius * max(width, height)) / 2
        # Initialize Bloom Filter List
        bloom_filter = []
        for i in xrange(bloom_width * bloom_width):
            dist = sqrt(float(i)) / float(bloom_width)
            bloom_filter_value = pow(max(0.0, 1.0 - dist), bloom_exp)
            bloom_filter.append(bloom_filter_value)
        # Apply Bloom Filter to Image Pixels
        bloom_image = []
        for i in xrange(len(pixels)):
            bloom_image.append(Color(0.0, 0.0, 0.0))
        bloom_x_start = 220 #0
        bloom_x_end   = 500 #width
        bloom_y_start = height - 700 #0
        bloom_y_end   = height - 580 #height
        for y in xrange(bloom_y_start, bloom_y_end):
            sys.stdout.write("\r"+"Blooming Effect Remain {0:.2f}%".format(float(y) / (bloom_y_end - bloom_y_start) * 100.0))
            sys.stdout.flush()
            for x in xrange(bloom_x_start, bloom_x_end):
                x0 = max(0, x - bloom_width)
                x1 = min(x + bloom_width, width - 1)
                y0 = max(0, y - bloom_width)
                y1 = min(y + bloom_width, height - 1)
                offset = y * width + x
                sum_weight = 0.0
                bx , by = x0, y0
                for by in xrange(y1):
                    for bx in xrange(x1):
                        dx = x - bx
                        dy = y - by
                        if dx == 0 and dy == 0:
                            continue
                        dist2 = dx * dx + dy * dy
                        if dist2 < bloom_width * bloom_width:
                            bloom_offset = by * width + bx
                            weight = bloom_filter[dist2]
                            sum_weight += weight
                            bloom_image[offset] += pixels[bloom_offset] * weight
                bloom_image[offset] = bloom_image[offset] / sum_weight
            
    for y in xrange(bloom_y_start, bloom_y_end):
        for x in xrange(bloom_x_start, bloom_x_end):
            offset = y * width + x
            pixels[offset] = bloom_image[offset] * bloom_weight + pixels[offset] * (1.0 - bloom_weight)
    return pixels

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
    max_y = 0.01
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
        for pixel in pixels:
            f.write(chr(int(pixel.r)) + chr(int(pixel.g)) + chr(int(pixel.b)))
        f.close()
