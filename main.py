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
    
    def reflect(self, normal):
        return self - normal * (2 * self.dot(normal))
    
class Ray:

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def at(self, t):
        return self.origin + self.direction * t      

class HitRecord:
    def __init__(self,color, normal):
        self.color = color
        self.normal = normal
        self.p = Vec3(0,0,0)  
        self.t = math.inf

class Sphere:
    def __init__(self,center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

def ray_color(ray, sphere_list):
    unit_direction = ray.direction.as_unit_vector()
    bounces = 5
    hit_record = HitRecord(Vec3(0,0,0), Vec3(0,0,0))
    sun_direction = Vec3(-1,-1,-1).as_unit_vector()
    color = Vec3(0,0,0)
    multiplier = 1.0
    for i in range(bounces):
        hit = False
        # Kollar vilken sfär som träffas
        for s in sphere_list:
            if sphere(ray, s.center, s.radius,s.color, hit_record):
                hit = True
        if hit:
            rd =ray.direction.reflect(hit_record.normal)
            rayPos = hit_record.p + rd * 0.0001  
            ray = Ray(rayPos, rd)    
            color += hit_record.color * max(hit_record.normal.dot(sun_direction * -1.0),0) * multiplier
            multiplier *= 0.5
        else:
            a = 0.5 * (unit_direction.y + 1.0)
            bg = Vec3(1,1,1) * (1.0 - a)   + Vec3(0.5, 0.7, 1) * a
            return bg * multiplier + color
    return Vec3(0,0,0)  # Om ingen sfär träffas returneras svart

def sphere(ray, center, radius, color, hit_record):

    oc = center - ray.origin    
    a = ray.direction.length_squared()
    b = oc.dot(ray.direction) * -2.0
    c = oc.length_squared() - radius * radius 
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return False
    
    d_sqrt = math.sqrt(discriminant)
    t1 = (-b - d_sqrt) / (2.0 * a)
    t2 = (-b + d_sqrt)/(2.0*a)

    if t1 > hit_record.t :
        return False

    hit_point = ray.at(t1)
    hit_record.normal = (hit_point - center) / radius
    hit_record.color = color
    hit_record.p = hit_point
    hit_record.t = t1
    return True

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


viewport_upper_left = camera_pos - Vec3(0,0,focal_length) - viewport_uv/2.0
pixel00_loc =  viewport_upper_left + pixel_delt_uv/2.0

sphere_list = [Sphere(Vec3(0, 0, -1), 0.5, Vec3(1, 0, 1)),
                Sphere(Vec3(0,-100.5,-1),100, Vec3(0,1,0))
               ]

print("P3")
print(width, height)
print(255)

for y in range(height):
    for x in range(width):
        pixel_center = pixel00_loc + Vec3(pixel_delt_uv.x * x, pixel_delt_uv.y * y, 0)
        ray_direction = pixel_center - camera_pos
        ray = Ray(camera_pos,ray_direction)
        color = ray_color(ray, sphere_list)
        r = math.floor(color.x * 255)
        g = math.floor(color.y * 255)
        b = math.floor(color.z * 255)
        print(r,g,b)     
