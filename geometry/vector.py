EPS = 1.0e-6

class Vector:
    def __init__(self,x=0.0,y=0.0,z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.__type__ = 'Vector'

    def dup(self):
        '''
        create a duplicate copy of the vector
        '''
        return Vector(self.x,self.y,self.z)

    def length(self):
        '''
        compute the length of the vector
        '''
        from math import sqrt
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def __abs__(self):
        '''
        return a normalized copy of the vector
        '''
        # it is consistent with the built-in "abs" function to return a copy, and not modify the original object
        v = self.dup()
        d = v.length()
        v.x /= d
        v.y /= d
        v.z /= d
        return v

    def __add__(self,b):
        '''
        add a vector, or scalar (b) to self
        returning a copy
        '''    
        v = self.dup()
        if (isinstance(b,int) or isinstance(b,float)):
            b = float(b)
            v.x += b
            v.y += b
            v.z += b
        else:
            v.x += b.x
            v.y += b.y
            v.z += b.z
        return v
    
    def __radd__(self,b):
        return self.__add__(b)

    def __sub__(self,b):
        '''
        subtract a vector, or scalar (b) from self
        returns a copy
        '''
        v = self.dup()
        if (isinstance(b,int) or isinstance(b,float)):
            b = float(b)
            v.x -= b
            v.y -= b
            v.z -= b
        else:
            v.x -= b.x
            v.y -= b.y
            v.z -= b.z
        return v
        
    def __mul__(self,b):
        '''
        multiply a vector by a scalar, b
        returns a copy
        '''
        v = self.dup()
        b = float(b)
        v.x *= b
        v.y *= b
        v.z *= b
        return v

    def __rmul__(self,b):
        return self.__mul__(b)

    def __div__(self,b):
        '''
        divide a vector by a scalar, b
        returns a copy
        '''
        v = self.dup()
        b = float(b)
        v.x /= b
        v.y /= b
        v.z /= b
        return v
    
    def dot(self,b):
        '''
        compute the dot product between a vector(self) and another (b)
        '''
        return self.x * b.x + self.y * b.y + self.z * b.z

    def angleBetween(self,b):
        '''
        compute the angle between two vectors
        result in radians
        '''
        # theta = ACOS ( (a dot b) / abs(a) * abs(b) )
        t1 = self.abs()
        t2 = b.abs()
        t3 = t1 * t2
        t4 = self.dot(b)
        t5 = t4 / t3
        theta = math.acos(t5)
        return theta

    def cross(self,b):
        '''
        compute the cross product of a vector (self) and another (b)
        '''
        v = self.dup()
        v.x = self.y * b.z - self.z * b.y
        v.y = self.z * b.x - self.x * b.z
        v.z = self.x * b.y - self.y * b.x
        return v

    def __str__(self):
        return "Vector(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

    def __repr__(self):
        return str(self)

    def __eq__(self,b):
        # vectors are the same if the distance between their endpoints is less than EPS
        return ((self - b).length() < EPS)

if __name__ == "__main__":
    # this is for test purposes!
##    from geometry import *
    v1 = Vector(1,2,3)
    print "v1 = " + str(v1)
    v2 = Vector(1,0,0)
    print "v2 = " + str(v2)
    v3 = Vector(0,1,0)
    print "v3 = " + str(v3)
    print "v1 dot v2 = " + str(v1.dot(v2))
    print "v2 cross v3= " + str(v2.cross(v3))
    print "v1 * 3 = " + str(v1 * 3)
    print "2 * v1 = " + str(2.0 * v1) 
    print "v1 / 3 = " + str(v1/3)
    print "abs(v1) = " + str(abs(v1))
    print "v1 + 1 = " + str(v1+1)
    print "1 + v1 = " + str(1+v1)
    print "v1 - 1= " + str(v1 -1)
    print 'v1.length() = ' + str(v1.length())
##    p1=Point(1,2,3)
##    print "p1 = " + str(p1)
##    print "p1 = " + str(p1)
##    print "v1 - p1 = " + str(v1-p1)
    print 'v1 == v1 = ' + str(v1==v1)
    print 'v1 == v2 = ' + str(v1==v2)
