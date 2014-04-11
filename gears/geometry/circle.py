from vector import Vector
from point import Point
from affinematrix import AffineMatrix
from math import pi

EPS = 1.0e-6

class Circle(object):
    '''
    circle
    '''
    radius=None

    def __init__(self,center=Point(),radius=1.0, normal=Vector(0.0,0.0,1.0)):
        self.center = center
        self.radius = float(radius)
        self.normal = normal

    def dup(self):
        return Circle(self.center.dup(),self.radius,self.normal.dup())

    def __type__(self):
        return 'Circle'
      
    def __str__(self):
        return "Circle(center=" + str(self.center) + ", radius=" + str(self.radius) + ", normal=" + str(self.normal) + ")"

    def __repr__(self):
        return str(self)
    
    def circumference(self):
        from math import pi
        return 2*pi*self.radius

    def area(self):
        from math import pi
        return pi*self.radius*self.radius

    def diameter(self):
        return 2*self.radius
        
    def __eq__(self, b):
        return ( (self.center == b.center) and ( abs(self.radius - b.radius) < EPS ) and (self.normal == b.normal))

    def __rmul__(self,a):
        if isinstance(a,AffineMatrix):
            cp = a * self.center
            nv = a * self.normal
            return Circle(center=cp,radius=self.radius,normal=nv)
        else:
            raise ValueError('Non-AffineMatrix in Circle __rmul__.')
