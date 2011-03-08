from Geometry import *
from terrain import *
import pygame
from pygame.locals import *
   
def animate():
    pass
    
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

#                pygame.draw.polygon(screen, color, points)
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

def create_boid():
    a = Vertex(0.0, 1.0, 0.0)
    b = Vertex(0.3, 0.0, 0.0)
    c = Vertex(-0.3, 0.0, 0.0)
    d = Vertex(0.0, 0.3, 0.3)

    left = Polygon([a, d, c], (255, 0, 0)) # red
    right = Polygon([a, b, d], (0, 255, 0)) # green
    back = Polygon([d, b, c], (0, 0, 255)) # blue
    #bottom = Polygon([a, b, c], (255, 255, 0)) # yellow
                                        
    return Mesh([left, right, back]) 

def check_distance(obj1, obj2):
    print obj1.GetConMatrix()
    print obj2.GetConMatrix()
    
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

#camera.Translate(Matrix().Translate(-5, -10, -40))
camera.Translate(Matrix().Translate(-2, 0, -10))
#camera.Rotate(Matrix().RotateX(.5))

t = Terrain(16)
t.applyHeightmap('heightmap.bmp')
terrain_polys = t.to_polys()
terrain_mesh = Mesh(terrain_polys)
terrain = Object(terrain_mesh)

boid_mesh = create_boid()
boid1 = Object(boid_mesh)
boid2 = Object(boid_mesh)

objects = [boid1, boid2]

check_distance(boid1, boid2)

while running:
    pygame.time.Clock().tick(180)

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
                                
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0

    screen.fill((0, 0, 0))
    animate()
    draw()
    pygame.display.flip()

pygame.quit()
