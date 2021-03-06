"""
Bryan Petzinger
VR hw 5
"""

from Geometry import *
import pygame

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
                        [0, 0, -1, 0]])

#letter P
p1 = Polygon([	Vertex(0, 1, 0), \
                Vertex(1, 1, 0), \
                Vertex(1, 0, 0), \
                Vertex(0.25, 0, 0), \
                Vertex(0.25, -1, 0), \
                Vertex(0, -1, 0), \
                Vertex(0, 0, 0)])

p2 = Polygon([  Vertex(0.25, 0.75, 0), \
                Vertex(0.75, 0.75, 0), \
                Vertex(0.75, 0.25, 0), \
                Vertex(0.25, 0.25, 0)])

mesh_p = Mesh([p1, p2])
p = Object(mesh_p)
p.Translate(Matrix().Translate(-1.5, 0, 0))

#letter E
e1 = Polygon([	Vertex(0, 1, 0), \
                Vertex(1, 1, 0), \
                Vertex(1, 0.75, 0), \
                Vertex(0.25, 0.75, 0), \
                Vertex(0.25, 0.1, 0), \
                Vertex(0.75, 0.1, 0), \
                Vertex(0.75, -0.1, 0), \
                Vertex(0.25, -0.1, 0), \
                Vertex(0.25, -0.75, 0), \
                Vertex(1, -0.75, 0), \
                Vertex(1, -1, 0), \
                Vertex(0, -1, 0),])

mesh_e = Mesh([e1])
e = Object(mesh_e)

#letter T
t1 = Polygon([	Vertex(-1, 1, 0), \
                Vertex(1, 1, 0), \
                Vertex(1, 0.75, 0), \
                Vertex(0.25, 0.75, 0), \
                Vertex(0.25, -1, 0), \
                Vertex(-0.25, -1, 0), \
                Vertex(-0.25, 0.75, 0), \
                Vertex(-1, 0.75, 0)])

mesh_t = Mesh([t1])
t = Object(mesh_t)
t.Translate(Matrix().Translate(1.5, 0, 0))

#cube
cube_front = Polygon([	Vertex(1, 1, 1), \
		                Vertex(-1, 1, 1), \
		                Vertex(-1, -1, 1), \
		                Vertex(1, -1, 1)], \
                        (255, 0, 0)) # red

cube_back = Polygon([	Vertex(1, 1, -1), \
		                Vertex(-1, 1, -1), \
		                Vertex(-1, -1, -1), \
		                Vertex(1, -1, -1)], \
                        (0, 255, 0)) # green

cube_left = Polygon([	Vertex(-1, 1, 1), \
		                Vertex(-1, 1, -1), \
		                Vertex(-1, -1, -1), \
		                Vertex(-1, -1, 1)], \
                        (0, 0, 255)) # blue

cube_right = Polygon([	Vertex(1, 1, 1), \
		                Vertex(1, 1, -1), \
		                Vertex(1, -1, -1), \
		                Vertex(1, -1, 1)], \
                        (255, 255, 0)) # yellow

cube_top = Polygon([    Vertex(1, 1, -1), \
                        Vertex(-1, 1, -1), \
		                Vertex(-1, 1, 1), \
		                Vertex(1, 1, 1)], \
                        (255, 0, 255)) # pink

cube_bottom = Polygon([ Vertex(1, -1, -1), \
                        Vertex(-1, -1, -1), \
		                Vertex(-1, -1, 1), \
		                Vertex(1, -1, 1)], \
                        (0, 255, 255)) # cyan

mesh_cube = Mesh([cube_front, cube_back, cube_left, cube_right, cube_top, cube_bottom])
cube_parent = Object(mesh_cube)
cube_parent.Translate(Matrix().Translate(5, 0, 0))

cube_child = Object(mesh_cube)
cube_child.SetParent(cube_parent)
cube_child.Translate(Matrix().Translate(-3, 3, 0))

objects = [p, e, t, cube_parent, cube_child]

camera.Translate(Matrix().Translate(.5, 0, -10))

count = 0
x = 1

def animate():
    global count, x
    if count == 25:
        x *= -1
        count = 0
    count += 1

    #P
    p.Translate(Matrix().Translate(0,x*.1,0))

    #E
    e.Rotate(Matrix().RotateY(.1))

    #T
    scale_factor = 1.1
    if x == 1:
        t.Scale(Matrix().Scale(scale_factor, scale_factor))
    else:
        t.Scale(Matrix().Scale(1/scale_factor, 1/scale_factor))

    #parent cube
    cube_parent.Rotate(Matrix().RotateX(0.1))
    cube_parent.Rotate(Matrix().RotateY(0.1))
    
    #child cube
    cube_parent.Rotate(Matrix().RotateX(0.1))
    cube_child.Rotate(Matrix().RotateY(0.1))
    cube_child.Rotate(Matrix().RotateZ(0.1))

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

            for vertex in verticies:
                #apply concatenated proj/cam/world transforms
                vertex = con_matrix * vertex
                #normalize w coord of vertex and convert to point (x, y)
                point = divide_by_w(vertex)
                #convert point to screen coords
                point = convert_to_screen(point)
                points.append(point)

            pygame.draw.lines(screen, polygon.GetColor(), True, points)

def divide_by_w(vertex):
    w = vertex[3]
    return (vertex[0]/w, vertex[1]/w)

def convert_to_screen(point):
    x = point[0] * (screen_width/2) + (screen_width/2)
    y = -1.0 * point[1] * (screen_height/2) + (screen_height/2)
    return (x, y)
    

while running:
    pygame.time.Clock().tick(180)

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0

    screen.fill((0, 0, 0))
    animate()
    draw()
    pygame.display.flip()

pygame.quit()
