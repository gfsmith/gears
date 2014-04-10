from matrix import *
from vector import *
import math

class Quaternion(Matrix):
    '''
    a light weight coordinate transformation matrix (quaternion) module
    '''
    def invert(self):
        '''
        invert a quaternion taking advantage of some tricks specific to
        quaternions to make it quick and easy
        '''
        # see page 39 of 'Robotics' by John J. Craig
        q = self.dup()
        # first transpose the rotation matrix part of the quaternion
        r = self.getRotationMatrix()
        r = r.transpose()
        t = Matrix([[self.seq[0][3]],[self.seq[1][3]],[self.seq[2][3]]])
        t = -r * t
        m = r.seq
        m[0].append(t.seq[0][0])
        m[1].append(t.seq[1][0])
        m[2].append(t.seq[2][0])
        m.append([0,0,0,1])
        q = Quaternion(m)
        return q

    def dup(self):
        '''
        Quaternions have to have "dup" redefined to return a Quaternion
        '''
        q = Quaternion(self.seq)
        return q

    def getRotationMatrix(self):
        '''
        return the rotation matrix portion of the quaternion
        '''
        rseq=[]
        for rowNum in range(self.numRows-1):
            rseq.append(self.seq[rowNum][:-1])
        r = Matrix(rseq)
        return r

    def getTranslationVector(self):
        '''
        return the translation vector portion of the quaternion
        '''
        vseq=[]
        for rowNum in range(self.numRows-1):
            vseq.append(self.seq[rowNum][-1])
        v = Vector(vseq[0],vseq[1],vseq[2])
        return v

    def getCFDescAsVects(self):
        '''
        get coordinate frame description as a dictionary of vectors

        the first vector 'X' describes the orientation of the x axis,
        the vector 'Y'describes the y axis, etc.
        the vector 'T' describes the translation
        '''
        v = {}
        v['X'] = Vector(self.seq[0][0],self.seq[1][0],self.seq[2][0])
        v['Y'] = Vector(self.seq[0][1],self.seq[1][1],self.seq[2][1])
        v['Z'] = Vector(self.seq[0][2],self.seq[1][2],self.seq[2][2])
        v['T'] = Vector(self.seq[0][3],self.seq[1][3],self.seq[2][3])
        return v

    def __mul__(self,b):
        '''
        Quaternions can be multiplied by other quaternions, or by scalars,
        multipication by geometricEntity types must be handled by that type
        '''
##        print "'Quaternion.__mul__' called"
        q = self.dup()
        if isinstance(b,Quaternion):
            m = Matrix(q.seq) * Matrix(b.seq)
            q = Quaternion(m.seq)
            return q
        elif isinstance(b,(int,float)):
            m = b * Matrix(q.seq)
            q = Quaternion(m.seq)
            return q
        elif isinstance(b,Vector): # its a vector
            v=b # for clarity
            m = Matrix([[float(v.x)],[float(v.y)],[float(v.z)],[1.0]])
            q = Quaternion((q * m).seq)
            l=q.seq
            v=Vector(l[0][0],l[1][0],l[2][0])
            return v
        else:
            # deal with the many possibilities of Quaternions multiplied with other types (points, arcs, etc)
            return b.__rmul__(q)

    def X_rotation(theta):
        '''
        returns a Quaternion that represents a rotation about the X axis
        theta represents the rotation angle in radians
        '''
        q = Quaternion([[1,0,0,0],[0,math.cos(theta),-math.sin(theta),0],[0,math.sin(theta),math.cos(theta),0],[0,0,0,1]])
        return q

    def Y_rotation(theta):
        '''
        returns a Quaternion that represents a rotation about the Y axis
        theta represents the rotation angle in radians
        '''
        q = Quaternion([[math.cos(theta),0,math.sin(theta),0],[0,1,0,0],[-math.sin(theta),0,math.cos(theta),0],[0,0,0,1]])
        return q

    def Z_rotation(theta):
        '''
        returns a Quaternion that represents a rotation about the Z axis
        theta represents the rotation angle in radians
        '''
        q = Quaternion([[math.cos(theta),-math.sin(theta),0,0],[math.sin(theta),math.cos(theta),0,0],[0,0,1,0],[0,0,0,1]])
        return q

    def translation(translateVector):
        '''
        returns a Quaternion that represents a translation according to the vector passed in
        '''
        v = translateVector
        q = Quaternion([[1,0,0,v.x],[0,1,0,v.y],[0,0,1,v.z],[0,0,0,1]])
        return q

    def identity():
        '''
        returns a Quaternion that represents no operation

        this is probably useless, but it sure was easy to program...
        '''
        q = Quaternion([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
        return q
    
    X_rotation = staticmethod(X_rotation)
    Y_rotation = staticmethod(Y_rotation)
    Z_rotation = staticmethod(Z_rotation)
    translation = staticmethod(translation)
    identity = staticmethod(identity)
    
        

    # VERY important!
        # consider what happens when a point is multiplied by a quaternion!

# test!    
if __name__ == '__main__':
    q=Quaternion([[1,0,0,1.0],[0,1,0,2.5],[0,0,1,0],[0,0,0,1]])
    print q
    print "Identity Quaternion = \n" + str(Quaternion.identity())
    print "30 degree rotation about X = \n" + str(Quaternion.X_rotation(math.pi/180.0*30.0))
    print "30 degree rotation about Y = \n" + str(Quaternion.Y_rotation(math.pi/180.0*30.0))
    print "30 degree rotation about Z = \n" + str(Quaternion.Z_rotation(math.pi/180.0*30.0))
    print "[1,2,3] translation = \n" + str(Quaternion.translation(Vector(1,2,3)))
    A = Quaternion.identity()
    print 'A = \n' + str(A)
    B = Quaternion.Z_rotation(math.pi/180.0*30.0)
    print 'B = \n' + str(B)
    C = Quaternion.translation(Vector(1,2,3))
    print 'C = \n' + str(C)
    print "A * B * C =\n" + str(A * B)
##    p = Point(1,2,3)
##    print "C * p = \n" + str(C*p)
    print "C.invert() =\n" + str(C.invert())
##    m = Matrix([[1.0], [2.0], [3.0], [1.0]])
##    b = Quaternion([[0.86602540378443871, -0.49999999999999994, 0.0, 0.0], [0.49999999999999994, 0.86602540378443871, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
##    print (b * m)
    v = Vector(1,2,3)
    q = B * q
    print 'q = \n' + str(q)
    print 'v = ' + str(v)
    print 'q * v = ' + str(q*v)
