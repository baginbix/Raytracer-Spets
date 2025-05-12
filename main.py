import math

class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        return Vec3(self.x * other, self.y * other, self.z * other)
    
    def __truediv__(self, other):
        return Vec3(self.x / other, self.y / other, self.z / other)
    
    def length_squared(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def length(self):
        return math.sqrt(self.length_squared())
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def as_unit_vector(self):
        len = self.length()
        return  self / len
    
class Ray:

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def at(self, t):
        return self.origin + self.direction * t      


def ray_color(ray):
    unit_direction = ray.direction.as_unit_vector()
    a = 0.5 * (unit_direction.y + 1.0)
    return Vec3(1,1,1) * (1.0 - a)   + Vec3(0.5, 0.7, 1) * a

aspect_ratio = 16.0/9.0

width = 400
height = int(width//aspect_ratio)

#Kamera
focal_length = 1.0
viewport_height = 2.0
viewport_width = viewport_height * (width/height)
camera_pos = Vec3(0.0, 0.0, 0.0)

viewport_uv = Vec3(viewport_width, -viewport_height, 0)

pixel_delt_uv = Vec3(viewport_uv.x / width, viewport_uv.y / height,0) 

sphere_pos = Vec3(0, 0, -1)
sphere_radius = 2

viewport_upper_left = camera_pos - Vec3(0,0,focal_length) - viewport_uv/2.0
pixel00_loc =  viewport_upper_left + pixel_delt_uv/2.0

print("P3")
print(width, height)
print(255)

for y in range(height):
    for x in range(width):
        pixel_center = pixel00_loc + Vec3(pixel_delt_uv.x * x, pixel_delt_uv.y * y, 0)
        ray_direction = pixel_center - camera_pos
        ray = Ray(camera_pos,ray_direction)
        color = ray_color(ray)
        r = math.floor(color.x * 255)
        g = math.floor(color.y * 255)
        b = math.floor(color.z * 255)
        print(r,g,b)     
