GitHub: https://github.com/hanton/pyRayTracer

pyRayTracer
===========

pyRayTracer is a Ray Tracer in Python. I write it for learning speaking Python and Ray Tracing.

(functions) =
Camera : Pinhole Camera
Sampler: Multijittered Sampler, Regular Sampler
Texture: Image Texture
BRDF: Diffuse, Specular
Light: Ambient Light, Direction Light, Ambient Occlusion, Area Light
Shadow
Geometry: Sphere, Plane


How to Run
===========
   python pyRayTracer                            - to render a default 640*320 with 4 pixel samples picture
or python pyRayTracer width height pixel_samples - to render a width*height with num_samples pixel samples picture


===========
Reference: 
    Ray Tracing from the Ground Up by Kevin Suffern
    Physically Based Rendering, Second Edition: From Theory To Implementation by Matt Pharr, Greg Humphreys
    Mitsuba Renderer : http://www.mitsuba-renderer.org
    LuxRender : http://www.luxrender.net