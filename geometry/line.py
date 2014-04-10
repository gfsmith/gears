from point import Point
from affinematrix import AffineMatrix

class Line:
    '''
    Line class
    '''
    def __init__(self, startPoint=Point(), endPoint=Point()):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.__type__ = 'Line'
      
    def __str__(self):
        return "Line(startPoint=" + str(self.startPoint) + ", endPoint=" + str(self.endPoint) + ")"

    def __repr__(self):
        return str(self)

    def __eq__(self,b):
        if ((self.startPoint == b.startPoint) and (self.endPoint == b.endPoint)):
            return True
        else:
            return False

    def midpoint(self):
        return Point( (self.startPoint.x + self.endPoint.x)/2.0, (self.startPoint.y + self.endPoint.y)/2.0, (self.startPoint.z + self.endPoint.z)/2.0)

    def length(self):
        return self.startPoint.dist(self.endPoint)

    def reverse(self):
        (self.startPoint, self.endPoint) = (self.endPoint, self.startPoint)

    def dup(self):
        return Line(startPoint=self.startPoint.dup(),endPoint=self.endPoint.dup())

    def __rmul__(self,a):
        if isinstance(a,AffineMatrix):
            # Line_new = AffineMatrix * Line_old
            p1 = a * self.startPoint
            p2 = a * self.endPoint
            return Line(p1,p2)
        else:
            raise ValueError('Non-AffineMatrix in Line __rmul__.')
            

