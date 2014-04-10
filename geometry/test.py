from geometry import *
from math import pi, sin, cos, tan, atan2, radians, degrees

p1 = Point()
p2 = Point(1,2)
p3 = Point(0.9,1.9)
p4 = Point()
l1 = Line(p1,p2)
pl1= Polyline([p1,p2,p3],closed=True)
#print "pl1 = %s" % str(pl1)
a1 = Arc()
c1 = Circle()
am1 = AffineMatrix().identity()
am2 = AffineMatrix().Z_rotation(pi/180.0*45.0)
am3 = AffineMatrix().X_rotation(pi/180.0*30.0)
v1 = Vector(1,2,0)
am4 = AffineMatrix().translation(v1)

#print "am1 * a1 = %s" % str(am1*a1)
#print "am1 * pl1 = %s" % str(am1 * pl1)
#print "am1 * c1 = %s" % str(am1 * c1)


pList = []
theta = 0.0
thetaInc = pi/180.0 * 2.0
r=1.0
for i in range(360):
    x = r * cos(theta)
    y = r * sin(theta)
    p = Point(x,y,0)
    pList.append(p)
    theta += thetaInc
    r += 0.1

pl = Polyline(pList)

#s=element2Script(pl)

b1 = Block([Line(Point(-0.5,-1.0),Point(0.5,-1.0)),
        Arc(Point(0.5,-0.5),0.5,pi/180*270,pi/180*0,'CCW'),
        Line(Point(1.0,-0.5),Point(1.0,0.5)),
        Arc(Point(0.5,0.5),0.5,pi/180*0,pi/180*90,'CCW'),
        Line(Point(0.5,1.0),Point(-0.5,1.0)),
        Arc(Point(-0.5,0.5),0.5,pi/180*90,pi/180*180,'CCW'),
        Line(Point(-1.0,0.5),Point(-1.0,-0.5)),
        Arc(Point(-0.5,-0.5),0.5,pi/180*180,pi/180*270,'CCW')])

#b1 = Block([Arc(Point(0.5,-0.5),0.5,pi/180.0*270.0,0.0,'CCW')])

#b1 = Block([Line(Point(),Point(1.0,0.0))])

b1 = AffineMatrix().translation(Vector(1.0,0,0)) * b1

n=30
b = Block()
theta = 0.0
thetaInc = (360.0/n) * (pi/180.0)
for i in range(n):
    am1 = AffineMatrix().Z_rotation(theta)
    #print am1
    b2 = am1 * b1
    #print theta/pi * 180.0
    #print b2
    #print element2Script(b2)
    theta+=thetaInc
    for g in b2.seq:
        b.seq.append(g)

#toFile(b,'testscript.scr')
from fileformats import Render2DXF

l1 = Line(Point(0,-10),Point(10,0))
b2 = mirrorAboutLine(b2,l1)

r=Render2DXF()
r.render2File([b,b2],'test.dxf')

print b1
