import pygame
from random import random
from pygame.locals import *
from Geometry import *
from terrain import *

def animate():
    for pred in pred_list:
        move_random(pred)
    
    for prey in prey_list:
        move_random(prey)

    for pred in pred_list:
        for prey in prey_list:
            if(check_distance(pred, prey) <= 2):
                #simulate prey being destroyed and new prey taking its place
                print 'predator caught prey!'
                prey.SetPos((0,1,0))

def draw():
    for obj in objects:
        #local -> world -> camera -> projection
        if(obj.GetParent() != None):
            con_matrix = perspective * camera.GetViewMatrix() * obj.GetParent().GetConMatrix() * obj.GetConMatrix()
        else:
            con_matrix =  perspective * camera.GetViewMatrix() * obj.GetConMatrix()

        for polygon in obj.GetMesh().GetPolygons():
            verticies = polygon.GetVerticies()
            points = []
            
            render_poly = False
            
            for vertex in verticies:
                withinAABB = True
                #apply concatenated proj/cam/world transforms
                vertex = con_matrix * vertex
                
                #culling - near plane
                if(vertex[2] > 1):
                    withinAABB = False
                    
                #normalize w coord of vertex
                vertex = divide_by_w(vertex)
                
                #culling - right/left and top/bottom planes
                if(vertex[0] > right or vertex[0] < -(right) or \
                    vertex[1] > top or vertex [1] < -(top)):
                    withinAABB = False
                
                #only polgyons completely outside the AABB are culled
                if(withinAABB == True):
                    render_poly = True
                    
                #convert point to screen coords
                point = convert_to_screen(vertex)
                points.append(point)
        
            if(render_poly and len(points) > 1):
                if (obj.GetColor() != None):
                    color = obj.GetColor()
                else: color = polygon.GetColor()               

                #pygame.draw.polygon(screen, color, points)
                pygame.draw.lines(screen, color, True, points)
                

def divide_by_w(vertex):
    w = vertex[3]
    #offset to avoid divide by zero
    if w == 0: w = .01
    return Vertex(vertex[0]/w, vertex[1]/w, vertex[2]/w)

def convert_to_screen(vertex):
    x = vertex[0] * (screen_width/2) + (screen_width/2)
    y = -1.0 * vertex[1] * (screen_height/2) + (screen_height/2)
    return (x, y)

def check_distance(obj1, obj2):
    m1 = obj1.GetConMatrix()    
    m2 = obj2.GetConMatrix()
    distance = ((m1[0][3] - m2[0][3])**2 +(m1[1][3] - m2[1][3])**2 + (m1[2][3] - m2[2][3])**2)**.5
    return distance
    
def set_random_pos(obj):
    x = (random()*(size-4))+2
    z = (random()*(size-4))+2
    obj.SetPos((x, 1, z))
    
def move_random(obj):
    m = obj.GetConMatrix()
    if (m[0][3] < 2):
        x = 1
    elif (m[0][3] > size-2):
        x = -1
    else: x = random()*2 - 1

    if (m[2][3] < 2):
        z = 1        
    elif (m[2][3] > size-2):
        z = -1
    else: z = random()*2 - 1
    
    obj.Translate(Matrix().Translate(x, 0, z))

running = 1
camera = Camera()
line_color = (0, 0, 255)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

#simple orthographic projection (drop z coord)
ortho = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]])

#perspective projection
right = 1
top = 1
near = 1
far = 10
perspective = Matrix([  [near/right, 0, 0, 0], \
                        [0, near/top, 0, 0], \
                        [0, 0, (-(far+near))/(-1), (-2*far*near)/(far-near)], \
                        [0, 0, -1, 0] \
                    ])

camera.Translate(Matrix().Translate(-8, -10, -20))
camera.Rotate(Matrix().RotateX(.5))
size = 16
t = Terrain(size)
t.applyHeightmap('heightmap16.bmp')
terrain_polys = t.to_polys()
terrain_mesh = Mesh(terrain_polys)
terrain = Object(terrain_mesh)

tri_a = Vertex(0.0, 0.0, -0.3)
tri_b = Vertex(0.3, 0.0, 0.0)
tri_c = Vertex(-0.3, 0.0, 0.0)
tri_d = Vertex(0.0, 0.3, -0.3)

tri_left = Polygon([tri_a, tri_d, tri_c], (255, 255, 0))
tri_right = Polygon([tri_a, tri_b, tri_d], (255, 255, 0))
tri_back = Polygon([tri_d, tri_b, tri_c], (255, 255, 0))
#tri_bottom = Polygon([a, b, c], (255, 255, 0))
                                        
tri_mesh = Mesh([tri_left, tri_right, tri_back])
prey_1 = Object(tri_mesh)
prey_2 = Object(tri_mesh)
prey_3 = Object(tri_mesh)
prey_4 = Object(tri_mesh)
prey_5 = Object(tri_mesh)

prey_list = [prey_1, prey_2, prey_3, prey_4, prey_5]
for prey in prey_list:
    set_random_pos(prey)

cube_a = Vertex(-0.5, 0.5, 0.5)
cube_b = Vertex(0.5, 0.5, .5)
cube_c = Vertex(0.5, -0.5, 0.5)
cube_d = Vertex(-0.5, -0.5, 0.5)
cube_e = Vertex(-0.5, 0.5, -0.5)
cube_f = Vertex(0.5, 0.5, -0.5)
cube_g = Vertex(0.5, -0.5, -0.5)
cube_h = Vertex(-0.5, -0.5, -0.5)

cube_front = Polygon([cube_a, cube_b, cube_c, cube_d], (255, 0, 0))
cube_back = Polygon([cube_e, cube_f, cube_g, cube_h], (255, 0, 0))
cube_top = Polygon([cube_e, cube_f, cube_b, cube_a], (255, 0, 0))
cube_bottom = Polygon([cube_h, cube_g, cube_c, cube_d], (255, 0, 0))
cube_left = Polygon([cube_e, cube_a, cube_d, cube_h], (255, 0, 0))
cube_right = Polygon([cube_b, cube_f, cube_g, cube_c], (255, 0, 0))

cube_mesh = Mesh([cube_front, cube_back, cube_top, cube_bottom, cube_left, cube_right])
pred_1 = Object(cube_mesh)
pred_2 = Object(cube_mesh)
pred_3 = Object(cube_mesh)

pred_list = [pred_1, pred_2, pred_3]
for pred in pred_list:
    set_random_pos(pred)

objects = [terrain]
objects.extend(pred_list)
objects.extend(prey_list)

while running:
    pygame.time.Clock().tick(1)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0
            break
            
        elif event.type == KEYDOWN:
            if event.key == K_w:
                #move forward
                camera.Translate(Matrix().Translate(0,0,1))
                
            if event.key == K_a:
                #move left
                camera.Translate(Matrix().Translate(1,0,0))
                
            if event.key == K_s:
                #move back
                camera.Translate(Matrix().Translate(0,0,-1))
                
            if event.key == K_d:
                #move right
                camera.Translate(Matrix().Translate(-1,0,0))
                
            if event.key == K_r:
                #move up
                camera.Translate(Matrix().Translate(0,-1,0))
                
            if event.key == K_f:
                #move down
                camera.Translate(Matrix().Translate(0,1,0))
                
            if event.key == K_UP:
                #rotate up
                camera.Rotate(Matrix().RotateX(.1))
                
            if event.key == K_DOWN:
                #rotate down
                camera.Rotate(Matrix().RotateX(-.1))
                
            if event.key == K_LEFT:
                #rotate left
                camera.Rotate(Matrix().RotateY(-.1))
                
            if event.key == K_RIGHT:
                #rotate right
                camera.Rotate(Matrix().RotateY(.1))
                                
    screen.fill((0, 0, 0))
    
    animate()
    draw()
    
    pygame.display.flip()

pygame.quit()
