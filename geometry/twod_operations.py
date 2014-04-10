from math import sin, cos, pi, degrees, radians, atan2
from geometry.point import Point
from geometry.line import Line
from geometry.arc import Arc
from geometry.circle import Circle
from geometry.polyline import Polyline
from geometry.block import Block
from geometry.vector import Vector
from geometry.affinematrix import AffineMatrix

def rotateAboutPoint(geom, p, radianAngle):
    '''
    rotates geometic entity about a point
    '''
    a1 = AffineMatrix().Z_rotation(radianAngle)
    a2 = AffineMatrix().translation(Vector(p.x,p.y,p.z))
    a3 = AffineMatrix().translation(Vector(-p.x,-p.y,-p.z))
    geom2 = a2*a1*a3*geom # translate to origin, rotate, translate back (in new frame)
    return geom2

def mirrorAboutLine(geom, l):
    '''
    mirror geometric entity about a line
    '''
    # this is the same as a 180 degree rotation about the line in 3D!
    v_shift = Vector(l.startPoint.x,l.startPoint.y,l.startPoint.z)
    #print "v_shift = %s" % str(v_shift)
    #print "-1.0 * v_shift = %s" % str(-1.0 * v_shift)
    v_axis = Vector(l.endPoint.x - l.startPoint.x,
            l.endPoint.y - l.startPoint.y,
            l.endPoint.z - l.startPoint.z)
    #print "v_axis = %s" % str(v_axis)
    tmshift = AffineMatrix().translation(-1.0 * v_shift)
    tpshift = AffineMatrix().translation(v_shift)
    y = l.endPoint.y - l.startPoint.y
    x = l.endPoint.x - l.startPoint.x
    theta = atan2(y,x)
    trot1 = AffineMatrix().Z_rotation(-theta)
    trot2 = AffineMatrix().Z_rotation(theta)
    tflip = AffineMatrix([[1.0, 0.0, 0.0, 0.0], [0.0, -1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
    #trot = AffineMatrix().rotationAboutVector(pi, v_axis)
    #geom_out = tpshift * trot * tmshift * geom # translate to origin, perform rotation, and translate back
    geom_out = tpshift * trot2 * tflip * trot1 * tmshift * geom
    return geom_out

def polarArray(geom,numberOfCopies,totalAngle=2*pi,center=Point(0,0)):
    '''
    array geometric entity in a polar pattern
    '''
    b = Block()
    theta_step = totalAngle / numberOfCopies
    theta = 0.0
    for i in range(numberOfCopies):
        g = rotateAboutPoint(geom,center,theta)
        b.append(g)
        theta += theta_step
    return b

def rectArray(geom,xNum,xStep,yNum=1,yStep=None):
    '''
    array geometric entity in a rectangular pattern
    '''
    b = Block()
    y = 0.0
    for j in range(yNum):
        x = 0.0
        for i in range(xNum):
            t = AffineMatrix().translation(Vector(x,y,0.0))
            b.append(t * geom)
            x += xStep
        y += yStep
    return b

if __name__=="__main__":
    p0 = Point()
    p1 = Point(1,1)
    p2 = Point(2,1)
    #print rotateAboutPoint(p1,p0,radians(45))
    #print rotateAboutPoint(p1,p2,radians(180))
    l1 = Line(p1,p2)
    l2 = rotateAboutPoint(l1, p1, radians(30))
    l3 = mirrorAboutLine(l2,l1)
    l4 = mirrorAboutLine(l1,l2)
    l5 = Line(Point(5,5),Point(6,5))
    b = polarArray(l5,50,center = Point(5,5))
    from fileformats.render2dxf import Render2DXF
    r = Render2DXF()
    q = [l1,l2,l3,l4]
    q += b.seq
    print q
    #r.render2File(q,'testpattern.dxf')
    r.render(q)
    print r.d.entities



