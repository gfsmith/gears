# Authors: Greg Smith & Ryan Sturmer

"""A package for dealing with geometry."""

__version__ = '0.0.a'

#__all__ = [
#    'matrix',
#    'vector',
#    'point',
#    'affinematrix',
#    'line',
#    'polyline',
#    'circle',
#    'arc'
#    ]

EPS = 1.0e-6

from matrix import Matrix
from vector import Vector
from point import Point
from affinematrix import AffineMatrix
from line import Line
from polyline import Polyline
from circle import Circle
from arc import Arc
from block import Block
from fileformats.render2dxf import Render2DXF
from twod_operations import *
#from toacadscript import element2Script, elements2Script, toFile

if __name__ == "__main__":
    p1=Point(1,2,3)
    p2=Point(4,5,6)
    l1=Line(p1,p2)
    print "p1 = " + str(p1)
    print "p2 = " + str(p2)
    print "l1 = " + str(l1)
    print "l1.length() = %f" % l1.length()
    pl1=Polyline([Point(0,0),Point(1,1),Point(1,0),Point(0,0)],closed=True)
    print "pl1 = " + str(pl1)
    print "pl1.length() = %f" % pl1.length()
    print "pl1.area() = %f" % pl1.area()
    v1 = Vector(1,2,3)
    print "v1 = " + str(v1)
    v2 = Vector(1,0,0)
    print "v2 = " + str(v2)
    v3 = Vector(0,1,0)
    print "v3 = " + str(v3)
    print "v1 dot v2 = " + str(v1.dot(v2))
    print "v2 cross v3= " + str(v2.cross(v3))
    print "v1 * 3 = " + str(v1 * 3)
    print "2 * v1 = " + str(2.0 * v1) #this doesn;t work becuse of the ordering of the arguments to __mul__, that sucks!
    print "v1 / 3 = " + str(v1/3)
    print "abs(v1) = " + str(abs(v1))
    print "v1 + 1 = " + str(v1+1)
    print "1 + v1 = " + str(1+v1)
    print "v1 - 1= " + str(v1 -1)
    print "v1 - p1 = " + str(v1-p1)

    am1 = AffineMatrix()
    am1 = am1.identity()
    print "am1 * p1 = %s" % str(am1 * p1)
    

