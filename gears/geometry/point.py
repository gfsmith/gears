# to do:
# function "inPlane" to test if a list of points is in the same plane (can return the definition of the plane?)

EPS = 1.0e-6

class Point(object):
    '''
    Simple point class
    '''
    def __init__(self,x=0.0,y=0.0,z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.__type__ = 'Point'

    def __str__(self):
        return "Point(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

    def __repr__(self):
        return str(self)

    def __eq__(self, b):
        return (self.dist(b) < EPS)

    def __mul__(self,b):
        '''
        multiplication of a point and a scalar
        '''
##        print '"Point.__mul__" was called.'
        p = self.dup()
        if ( isinstance(b,int) or isinstance(b,float) ):
            # its a scalar
            b = float(b)
            p.x *= b
            p.y *= b
            p.z *= b
            return p
        else:
            raise ValueError
   
    def dist(self, b=None):
        import math
##        print 'b = ' + str(b)
        if b==None:
            b=Point(0,0,0)
        return math.sqrt((b.x - self.x)**2 + (b.y - self.y)**2 + (b.z - self.z)**2)
          
    def dup(self):
        return Point(self.x, self.y, self.z)
