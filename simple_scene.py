from Geometry import *
import pygame

running = 1
camera = Camera()
line_color = (0, 0, 255)
screen = pygame.display.set_mode((800, 600))

#simple orthographic projection (drop z coord)
ortho = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]])

#perspective projection
far = -1
near = 1
right = 1
top = 1
perspective = Matrix([  [near/right, 0, 0, 0], \
                        [0, near/top, 0, 0], \
                        [0, 0, (-(far+near))/(-1), (-2*far*near)/(far-near)], \
                        [0, 0, -1, 0]])

p1 = Polygon([[0,0,0], [100,0,0], [100, 75, 0], [0,75,0]])
p2 = Polygon([[0, 85, 0], [0, 150, 0], [50, 150, 0], [50, 85, 0]])
p3 = Polygon([[35, 15, 0], [35, 45, 0], [75, 45, 0], [75, 15, 0]])
mesh_p = Mesh([p1, p2, p3])
p = Object(mesh_p)
p.Translate(Matrix().Translate(0, 0, 0))

e1 = Polygon([[0, 0, 0], [100, 0, 0], [100, 40, 0], [0, 40, 0]])
e2 = Polygon([[0, 60, 0], [75, 60, 0], [75, 90, 0], [0, 90, 0]])
e3 = Polygon([[0, 110, 0], [100, 110, 0], [100, 150, 0], [0, 150, 0]])
mesh_e = Mesh([e1, e2, e3])
e = Object(mesh_e)
e.Translate(Matrix().Translate(150, 0, 0))

t1 = Polygon([[0, 0, 0], [100, 0, 0], [100, 40, 0], [0, 40, 0]])
t2 = Polygon([[30, 50, 0], [70, 50, 0], [70, 150, 0], [30, 150, 0]])
mesh_t = Mesh([t1, t2])
t = Object(mesh_t)
t.Translate(Matrix().Translate(300, 0, 0))

c1 = Polygon([[0, 0, 0], [0, 50, 0], [50, 50, 0], [50, 0, 0]], (255, 0, 0)) # red
c2 = Polygon([[0, 0, 50], [0, 50, 50], [50, 50, 50], [50, 0, 50]], (0, 255, 0)) # green
c3 = Polygon([[0, 0, 0], [0, 0, 50], [0, 50, 50], [0, 50, 0]], (0, 0, 255)) # blue
c4 = Polygon([[50, 0, 0], [50, 0, 50], [50, 50, 50], [50, 50, 0]], (255, 255, 0)) # yellow
c5 = Polygon([[0, 0, 0], [50, 0, 0], [50, 0, 50], [0, 0, 50]], (255, 0, 255)) # pink
c6 = Polygon([[0, 50, 0], [50, 50, 0], [50, 50, 50], [0, 50, 50]], (0, 255, 255)) # cyan
mesh_cube = Mesh([c1, c2, c3, c4, c5, c6])
cube_parent = Object(mesh_cube)
cube_parent.Translate(Matrix().Translate(450, 0, 0))

cube_child = Object(mesh_cube)
cube_child.SetParent(cube_parent)
cube_child.Translate(Matrix().Translate(100, 100, 0))

objects = [p, e, t, cube_parent, cube_child]

camera.Translate(Matrix().Translate(50, 100, 0))

count = 0
x = 1

def animate():
    global count, x
    if count == 25:
        x *= -1
        count = 0
    count += 1

    #P
    p.Translate(Matrix().Translate(0,x*2,0))

    #E
    e.Rotate(Matrix().RotateY(.1))

    #T
    if x == 1:
        t.Scale(Matrix().Scale(1.1, 1.1, 1.1))
    else:
        t.Scale(Matrix().Scale(.9, .9, .9))

    #parent cube
    cube_parent.Rotate(Matrix().RotateX(0.1))
    cube_parent.Rotate(Matrix().RotateY(0.1))
    
    #child cube
    cube_parent.Rotate(Matrix().RotateX(0.1))
    cube_child.Rotate(Matrix().RotateY(0.1))
    cube_child.Rotate(Matrix().RotateZ(0.1))

def draw():
    for obj in objects:
        #apply projection, camera, world transforms        

        if(obj.GetParent() != None):
            con_matrix = perspective * camera.GetViewMatrix() * obj.GetParent().GetConMatrix() * obj.GetConMatrix()
        else:
            con_matrix =  perspective * camera.GetViewMatrix() * obj.GetConMatrix()
        for polygon in obj.GetMesh().GetPolygons():

            verticies = polygon.GetVerticies()
            for i in range(len(verticies)):
                v = verticies[i]
                point_a = con_matrix * Vertex(v[0], v[1], v[2])                
                if(i+1 < len(verticies)):
                    v = verticies[i+1]
                else:
                    v = verticies[0]
                point_b = con_matrix * Vertex(v[0], v[1], v[2])                
                pygame.draw.line(screen, polygon.GetColor(), (point_a[0], point_a[1]), (point_b[0], point_b[1]))

while running:
    pygame.time.Clock().tick(180)

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0

    screen.fill((0, 0, 0))
    animate()
    draw()
    pygame.display.flip()
