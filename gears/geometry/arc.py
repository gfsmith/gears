from point import Point
from affinematrix import AffineMatrix
from math import pi, sin, cos, atan2, acos

from polyline import Polyline

# To do:
# create arcs in other ways (3 points?)
# blow arc into line segments?
# fix "area" function to work with direction

EPS = 1.0e-6

class Arc(object):
    '''
    an arc in a plane parallel to the X-Y plane
    (start and end angle are not defined in other planes)
    startAngle and endAngle are defined CCW from the X-axis, in radians
    direction controls the wrap direction of the arc
    '''
    def __init__(self, center=Point(x=0.0,y=0.0,z=0.0), radius=1.0, startAngle=0.0, endAngle=90.0*pi/180.0, direction='CCW'):
        self.center = center
        self.radius = float(radius)
        self.startAngle = float(startAngle)
        self.endAngle = float(endAngle)
        self.direction = str(direction)
        self.__type__ = type('Arc')
        
    def getEndpoints(self):
        return (Point(self.center.x + self.radius*cos(self.startAngle), self.center.y + self.radius*sin(self.startAngle), self.center.z), Point(self.center.x + self.radius*cos(self.endAngle), self.center.y + self.radius*sin(self.endAngle), self.center.z))

    def reverse(self):
        (self.startAngle,self.endAngle) = (self.endAngle,self.startAngle)
        if self.direction == 'CW':
            self.direction = 'CCW'
        elif self.direction == 'CCW':
            self.direction = 'CW'
        else:
            raise ValueError('Arc direction is not "CW" or "CCW", undefined behavior!- cannot REVERSE')

    def __eq__(self,b):
        print "EPS_ = %f" % float(EPS)
        if  ( ( self.center == b.center ) and 
                ( abs(self.radius - b.radius ) < EPS ) and
                ( abs(self.startAngle - b.startAngle) < EPS ) and
                ( abs(self.endAngle - b.endAngle) < EPS ) and
                ( self.direction == b.direction ) ):
            return True
        else:
            return False
            

    def length(self):
        '''
        chord length
        '''
        # start angle and end angle are stored in radians, so chord length is simply radius * angle
        return ( self.radius * abs(self.startAngle - self.endAngle) )

#    def area(self):
#        '''
#        pie slice area
#        '''
#        return (pi * self.radius * self.radius * ( abs(self.endAngle-self.startAngle)/(2.0*pi) ) )
        
    def __str__(self):
        return 'Arc(center=' + str(self.center) + ', radius=' + str(self.radius) + ', startAngle=' + str(self.startAngle) + ', endAngle=' + str(self.endAngle) + ', direction="' + str(self.direction) + '")'

    def __repr__(self):
        return str(self)

    def dup(self):
        # center=Point(x=0.0,y=0.0,z=0.0), radius=1.0, startAngle=0.0, endAngle=90.0*pi/180.0, direction='CW'):
        return Arc(center=self.center.dup(),radius=self.radius,startAngle=self.startAngle,endAngle=self.endAngle,direction=self.direction)

    def __rmul__(self,a):
        if isinstance(a,AffineMatrix):
            cp = a * self.center
            spx1 = self.radius * cos(self.startAngle) + self.center.x
            spy1 = self.radius * sin(self.startAngle) + self.center.y
            sp = Point(spx1,spy1)
            sp2 = a * sp
            sa2 = atan2(sp2.y-cp.y,sp2.x-cp.x)
            r2 = sp2.dist(cp)
            epx1 = self.radius * cos(self.endAngle) + self.center.x
            epy1 = self.radius * sin(self.endAngle) + self.center.y
            ep = Point(epx1,epy1)
            ep2 = a * ep
            ea2 = atan2(ep2.y - cp.y, ep2.x - cp.x)
            return Arc(center=cp,radius=r2,startAngle=sa2,endAngle=ea2,direction=self.direction)
        else:
            raise ValueError('Non-AffineMatrix in Arc __rmul__.')

    def toPolyline(self,maxError=1.0e-5):
        '''
        converts an arc to a Polyline with enough segments so as not to exceed a maxError
        '''
        theta_step = 2.0 * acos( 1.0 - (maxError/self.radius) ) # the angular step needed to exactly meet maxError condition
        theta = self.endAngle - self.startAngle
        numSteps = int(abs(theta) / theta_step) + 1
        theta_step = theta/numSteps
        pList = []
        for i in range(numSteps+1):
            x = self.center.x + self.radius * cos(self.startAngle + theta_step * i)
            y = self.center.y + self.radius * sin(self.startAngle + theta_step * i)
            p = Point(x,y,0.0)
            pList.append(p)
        pl = Polyline(pList)
        return pl

#if __name__ == "__main__":
    #a=Arc()
    #print "a = %s" % str(a)
    #b=Arc()
    #print "b = %s" % str(b)
    #print "EPS = %f" % EPS
    #print "a.center = %s, b.center = %s" % (str(a.center), str(b.center))
    #print "a.center == b.center : %s" % str(a.center == b.center)
    #print "abs(a.radius - b.radius) : %s" % str(abs(a.radius - b.radius)) 
    #print "abs(a.radius - b.radius) < EPS : %s" % str(abs(a.radius-b.radius)<EPS)
    #print "abs(a.startAngle - b.startAngle) < EPS : %s" % str(abs(a.startAngle-b.startAngle)<EPS)
    #print "abs(a.endAngle - b.endAngle) < EPS : %s" % str(abs(a.endAngle-b.endAngle)<EPS)
    #print "a.direction = %s" % str(a.direction)
    #print "b.direction = %s" % str(b.direction)
    #print "a.direction == b.direction : %s" % str(a.direction==b.direction)
    #print "a==b : %s" % str(a==b)
