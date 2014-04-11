# To do:
# slicing? getItem, setItem?
# reverse?
# length?

from point import Point
from line import Line
from affinematrix import AffineMatrix

class Polyline(object):
    '''
    A polyline is a list of points that are connected, in the order in which they are stored
    '''

    def __init__(self, pointList=None, closed=None):
        if pointList == None:
            self.points = []
        else:
            self.points = pointList

        if closed == None:
            self.closed = False
        else:
            self.closed = closed

        if self.closed:
            try:
                if self.points[0] != self.points[-1]:
                    self.points.append(self.points[0].dup())
            except:
                pass

    def get_bounds(self):
        if self.points:
            minx,miny,minz = self.points[0]
            maxx,maxy,maxz = self.points[0]
            for x,y,z in self:
                if x > maxx:
                    maxx = x
                elif x < minx:
                    minx = x
                if y > maxy:
                    maxy = y
                elif y < miny:
                    miny = y
                if z > maxz:
                    maxz = z
                elif z < minz:
                    minz = z
            return Point(minx,miny,minz), Point(maxx,maxy,maxz)
            
    def appendPoint(self, p):
        if self.closed:
            if len(self.points) > 0:
                self.points = self.points[:-1]
                self.points.append(p)
                self.points.append(self.points[0].dup())
            else:
                self.points.append(p)
                self.points.append(p.dup())
            
        else:
            self.points.append(p)
        
    def prependPoint(self, p):
        self.points.insert(0,p)
        if(self.closed):
            if self.points[0] != self.points[-1]:
                self.points.append(self.points[0].dup())
            
    def startPoint(self):
        return self.points[0]

    def endPoint(self):
        return self.points[-1]
    
    def endPoints(self):
        if self.closed:
            return None
        else:
            return (self.startPoint(), self.endPoint())

    def getPoint(self, i):
        return self.points[i]

    def getLine(self, i):
        return Line(self.points[i], self.points[i+1])

    def __iter__(self):
        return iter(self.points)

    #TODO
    # Reimplement "Closed" polygons in a more uniform format

    def setClosed(self, closed, keepDuplicateEndpoint=False):
        '''
        TODO: Think about/implement duplicate endpoint switch
        '''
        self.closed = bool(closed)
        if self.closed:
            if len(self.points) > 1:
                if self.points[0] != self.points[-1]:
                    self.points.append(self.points[0].dup())
            else:
                pass
        else:
            pass
            
    def isClosed(self):
        return self.closed

    def isOpen(self):
        return not self.closed

    def length(self):
        d = 0
        for i in range(len(self.points) - 1):
            d += Line(self.points[i],self.points[i+1]).length()
        return d

    def area(self):
        '''
        all points are assumed to lie in the x-y plane!
        '''
        if (self.isOpen()):
            raise ValueError("Polyline is open, area is not valid")
        a = 0
        for i in range(len(self.points) - 1):
            pi1 = self.points[i]
            pi2 = self.points[i+1]
            dx = pi2.x - pi1.x
            dy = pi2.y - pi1.y
            ai = dx * pi1.y + 0.5 * dy * dx
            a += ai
        return a
    
    def __len__(self):
        if self.closed:
            if len(self.points) == 0:
                return 0
            else:
                return len(self.points) - 1
        else:
            return len(self.points)
    
    def __str__(self):
        return 'Polyline(pointList=' + repr(self.points) + ',closed=' + str(self.closed) + ')'

    def __repr__(self):
        return str(self)

    def __rmul__(self,a):
        if isinstance(a,AffineMatrix):
            pl = []
            for p in self.points:
                pl.append(a*p)
            return Polyline(pointList=pl, closed=self.closed)
        else:
            raise ValueError('Non-AffineMatrix in Polyline __rmul__.')

    def dup(self):
        pl=[]
        for p in self.points:
            pl.append(p.dup())
        return Polyline(pointList=pl, closed=self.closed)

    def reverse(self):
        self.points.reverse()

