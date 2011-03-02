"""
Bryan Petzinger
Vector & Matrix based on: http://www.math.okstate.edu/~ullrich/PyPlug/
"""

import math
from numbers import Real
from operator import add, sub, mul

class Vector(object):
  def __init__(self, data):
    self.data = data

  def Len(self):
   return math.sqrt(reduce(add, map(lambda x: math.pow(x, 2), self)))

  def Normalize(self):
    length = self.Len()
    return Vector(map(lambda x: x/length, self))

  def Dot(self, other):
    if not isinstance(other, Vector): raise Exception
    if len(self) != len(other): raise Exception
    return reduce(add, map(mul, self, other))

  def Cross(self, other):
    """only valid for 3-dimensional vectors"""
    if len(self) != 3 or len(other) != 3: raise Exception
    x = (self[1] * other[2]) - (self[2] * other[1])
    y = (self[2] * other[0]) - (self[0] * other[2])
    z = (self[0] * other[1]) - (self[1] * other[0])
    return Vector([x, y, z])

  def __add__(self, other):
    if len(self) != len(other): raise Exception
    return Vector(map(add, self, other))

  def __sub__(self, other):
    if len(self) != len(other): raise Exception
    return Vector(map(sub, self, other))

  def __mul__(self, other):
    """multiplication against a scalar or matrix"""
    if isinstance(other, Real):
      return Vector(map(lambda x: x * other, self))

    elif isinstance(other, Vector):
      return Vector(map(other.Dot, self))

    else:
      raise Exception

  def __str__(self):
    result = ', '.join(map(str, self))
    return '{' + result + '}'

  def __getitem__(self, index):
    return self.data[index]

  def __len__(self):
    return len(self.data)

class Matrix(Vector):

  """default to identity matrix"""
  def __init__(self, data = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]):
    self.data = map(Vector, data)

  def Transpose(self):
    return Matrix(zip(*self.data))

  def RotateX(self, theta):
    return Matrix([[1, 0, 0, 0], [0, math.cos(theta), -math.sin(theta), 0], [0, math.sin(theta), math.cos(theta), 0], [0, 0, 0, 1]])

  def RotateY(self, theta):
    return Matrix([[math.cos(theta), 0, math.sin(theta), 0], [0, 1, 0, 0], [-math.sin(theta), 0, math.cos(theta), 0], [0, 0, 0, 1]])

  def RotateZ(self, theta):
    return Matrix([[math.cos(theta), -math.sin(theta), 0, 0], [math.sin(theta), math.cos(theta), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

  def Scale(self, x = 1, y = 1, z = 1):
    return Matrix([[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]])

  def Translate(self, x = 0, y = 0, z = 0):
    return Matrix([[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]])
    
class Vertex(Vector):
  def __init__(self, x, y, z, w = 1):
    super(Vertex, self).__init__([x,y,z,w])

class Polygon:
  def __init__(self, verticies = [], color = (255, 255, 255)):
    self.verticies = verticies
    self.color = color

  def AddVertex(self, vertex):
    self.verticies.append(vertex)

  def GetVertex(self, index):
    return self.verticies[index]
    
  def GetVerticies(self):
    return self.verticies

  def SetColor(self, color):
    self.color = color

  def GetColor(self):
    return self.color

  def __str__(self):
    result = ', '.join(map(str, self))
    return '{' + result + '}'

  def __getitem__(self, index):
    return self.verticies[index]

  def __len__(self):
    return len(self.verticies)
    
class Mesh:
  def __init__(self, polygons = []):
    self.polygons = polygons

  def AddPolygon(self, polygon):
    self.polygons.append(polygon)

  def GetPolygon(self, index):
    return self.polygons[index]
    
  def GetPolygons(self):
    return self.polygons

  def __str__(self):
    result = ', '.join(map(str, self))
    return '{' + result + '}'

  def __getitem__(self, index):
    return self.polygons[index]

  def __len__(self):
    return len(self.polygons)
    
class Object:
  def __init__(self, mesh = None):
    self.mesh = mesh
    self.world_rotate = Matrix()
    self.world_scale = Matrix().Scale()
    self.world_translate = Matrix().Translate()
    self.parent = None

  def ReferenceMesh(self, mesh):
    self.mesh = mesh

  def SetParent(self, parent):
    self.parent = parent

  def GetParent(self):
    return self.parent

  def Rotate(self, rot_matrix):
    self.world_rotate *= rot_matrix

  def Translate(self, trans_matrix):
    self.world_translate *= trans_matrix

  def Scale(self, scale_matrix):
    self.world_scale *= scale_matrix
  
  def GetMesh(self):
    return self.mesh

  def GetTranslateMatrix(self):
    return self.world_translate

  def GetConMatrix(self):
    return Matrix(self.world_translate * self.world_rotate * self.world_scale)

class Camera:
  def __init__(self):
    self.view_rotate = Matrix()
    self.view_scale = Matrix().Scale()
    self.view_translate = Matrix().Translate()

  def GetViewMatrix(self):
    return Matrix(self.view_translate * self.view_rotate * self.view_scale)

  def Translate(self, trans_matrix):
    self.view_translate = self.view_translate * trans_matrix

