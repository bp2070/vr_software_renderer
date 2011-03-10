import Image
from Geometry import *

class Terrain:
    """
    the terrain is composed of a grid of squares with all verticies at 0 height (initially).

    height can be adjusted via a heightmap passed in a bitmap, where pixels and verticies are mapped 1-to-1
    and the height of each vertex is set based on the red (0-255) value for the corresponding pixel and a scale parameter.

    data/heightmap are stored as single list, so some work is required to index by row/col.

    """
    
    def __init__(self, size):
        self.size = size
        self.data = (size*size)*[None]
    
    #for testing    
    def initdata(self):
        for i in range(self.size):
            for j in range(self.size):
                self.data[i*self.size + j] = i*self.size + j
        
    def applyHeightmap(self, filename):
        heightmap = Image.open(filename)
        heightmap_data = heightmap.getdata()
        heightmap_size = len(heightmap_data) ** .5
        
        for i in range(self.size):
            for j in range(self.size):
                self.data[(i*self.size)+j] = heightmap_data[(i*int(heightmap_size))+j]
                
                
    def get(self, x,  y):
        return self.data[x * self.size + y]
        
    def getdata(self):
        return self.data

    def to_polys(self, scale = .01):
        polygons = []
        for i in range(self.size-1):
            for j in range(self.size-1):
                polygons.append(Polygon([   Vertex(i, self.get(i, j)[0]*scale, j), \
                                            Vertex(i+1, self.get(i+1, j)[0]*scale, j), \
                                            Vertex(i+1, self.get(i+1, j+1)[0]*scale, j+1), \
                                            Vertex(i, self.get(i, j+1)[0]*scale, j+1) \
                                        ]))            
        return polygons
