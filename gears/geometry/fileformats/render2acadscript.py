# This DOES NOT work properly for arcs! (perhaps also for other entities?)
# (the output looks ok, but ACAD gripes about radii of zero, etc???)
# GFS 20071231



from matrix import Matrix
from vector import Vector
from point import Point
from affinematrix import AffineMatrix
from line import Line
from polyline import Polyline
from circle import Circle
from arc import Arc
from block import Block

from math import sin, cos, pi

__doc__="""
A series of functions that make it easy to convert geometric entities into an AutoCAD script...
"""

def point2Script(p):
    '''
    returns the script text to draw a point
    '''
    s = "POINT %f,%f,%f\n" % (p.x,p.y,p.z)
    return s

def pointStr(p):
    return "%f,%f,%f" % (p.x,p.y,p.z)

def point2DStr(p):
    return "%f,%f" % (p.x,p.y)

def line2Script(l):
    '''
    returns the script text to draw a line
    '''
    s = "LINE %s %s\n\n" % (pointStr(l.startPoint),pointStr(l.endPoint))
    return s

def arc2Script(a):
    cp = a.center
    spx = a.center.x + a.radius * cos(a.startAngle)
    spy = a.center.y + a.radius * sin(a.startAngle)
    sp = Point(spx,spy,cp.z)
    epx = a.center.x + a.radius * cos(a.endAngle)
    epy = a.center.y + a.radius * sin(a.endAngle)
    ep = Point(epx,epy,cp.z)
    if (a.direction == 'CW'):
        (sp, ep) = (ep, sp)
    s = "ARC CE %s %s %s\n" % (point2DStr(cp),point2DStr(sp),point2DStr(ep))
    return s

def circle2Script(c):
    return "CIRCLE %s %f\n" % (pointStr(c.center),c.radius)

def polyline2Script(pl):
    s = 'LINE '
    for p in pl.points:
        s+='%s ' % pointStr(p)
    s+='\n'
    return s




def element2Script(g):
    '''
    converts a single geometry element to an AutoCAD script
    '''
    if isinstance(g,Point):
        return point2Script(g)
    elif isinstance(g,Line):
        return line2Script(g)
    elif isinstance(g,Arc):
        return arc2Script(g)
    elif  isinstance(g,Circle):
        return circle2Script(g)
    elif isinstance(g,Polyline):
        return polyline2Script(g)
    elif isinstance(g,Block):
        return block2Script(g)
    else:
        raise ValueError('Attempting to convert invalid type to ACAD Script.')

def elements2Script(seq):
    '''
    converts a sequence of geometry elements to an AutoCAD script
    '''
    if isinstance(seq,list):
        s=''
        for g in seq:
            s += element2Script(g)
        return s
    else:
        return element2Script(seq)

def block2Script(b):
    return elements2Script(b.seq)

def toFile(seq,fname):
    '''
    converts a sequence of geometry elements to an AutoCAD script and stores the results in a file
    '''
    s = elements2Script(seq)
    f = open(fname,'w')
    f.write(s)
    f.close()
