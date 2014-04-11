from matrix import Matrix
from vector import Vector
from point import Point
from math import sin, cos, acos

EPS = 1.0e-6

class AffineMatrix(Matrix):
    '''
    a light weight 3D coordinate transformation matrix (affine matrix, aka quaternion) module
    '''

    def __init__(self,seq=None):
        if seq == None:
            seq = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        Matrix.__init__(self,seq)
        if ( ( self.numRows != 4 ) or  (self.numCols != 4) ):
            raise ValueError('Sequence incorrectly sized for AffineMatrix.')

    def invert(self):
        '''
        invert an affine matrix taking advantage of some tricks specific to
        them to make it quick and easy

        (see page 39 of 'Robotics' by John J. Craig)
        '''
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
        q = AffineMatrix(m)
        return q

    def dup(self):
        '''
        create a duplicate copy
        '''
        # affine matrices have to have "dup" redefined to return an affine matrix
        q = AffineMatrix(self.seq)
        return q

    def getRotationMatrix(self):
        '''
        return the rotation matrix portion of the affine matrix
        '''
        rseq=[]
        for rowNum in range(self.numRows-1):
            rseq.append(self.seq[rowNum][:-1])
        r = Matrix(rseq)
        return r

    def getTranslationVector(self):
        '''
        return the translation vector portion of the affine matrix
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

    def isUniform(self):
        '''
        tests if the transformation is uniform in all axes (preserves aspect ratio)
        '''
        d=getCFDescAsVects(self)
        if (  ( abs( d['X'].length() - d['Y'].length() ) < EPS ) and ( abs( d['X'].length() - d['Z'].length() ) < EPS ) ):
            return True
        else:
            return False

    def getScaleFactor(self):
        '''
        returns the scale factor
        '''
        d=getCFDescAsVects(self)
        if (  ( abs( d['X'].length() - d['Y'].length() ) < EPS ) and ( abs( d['X'].length() - d['Z'].length() ) < EPS ) ):
            return d['X'].length()
        else:
            raise ValueError('Non-uniform scaling!')

    def __mul__(self,b):
        '''
        multiplication of affine matrices
        '''
        # Affine matrices can be multiplied by other affine matrices, or by scalars,
        # multipication by other types must be handled by that type
        q = self.dup()
        if isinstance(b,AffineMatrix):
            m = Matrix(q.seq) * Matrix(b.seq)
            q = AffineMatrix(m.seq)
            return q
        elif isinstance(b,(int,float)):
            m = b * Matrix(q.seq)
            q = AffineMatrix(m.seq)
            return q
        elif isinstance(b,Vector): # its a Vector
            v=b # for clarity
            m = Matrix([[float(v.x)],[float(v.y)],[float(v.z)],[1.0]])
            q = Matrix((q * m).seq)
            l=q.seq
            v=Vector(l[0][0],l[1][0],l[2][0])
            return v
        elif isinstance(b,Point): # its a Point
            p=b # for clarity
            m = Matrix([[p.x],[p.y],[p.z],[1.0]])
            m2 = q * m
            p = Point(x=m2.seq[0][0],y=m2.seq[1][0],z=m2.seq[2][0])
            return p
        else:
            # deal with the many possibilities of affine matrices multiplied with other types (lines, arcs, etc)
            return b.__rmul__(q)

    def X_rotation(theta):
        '''
        returns an affine matrix that represents a rotation about the X axis
        theta represents the rotation angle in radians
        '''
        am = AffineMatrix([[1,0,0,0],[0,cos(theta),-1.0*sin(theta),0],[0,sin(theta),cos(theta),0],[0,0,0,1]])
        return am

    def Y_rotation(theta):
        '''
        returns an affine matrix that represents a rotation about the Y axis
        theta represents the rotation angle in radians
        '''
        am = AffineMatrix([[cos(theta),0,sin(theta),0],[0,1,0,0],[-1.0*sin(theta),0,cos(theta),0],[0,0,0,1]])
        return am

    def Z_rotation(theta):
        '''
        returns an affine matrix that represents a rotation about the Z axis
        theta represents the rotation angle in radians
        '''
        am = AffineMatrix([[cos(theta),-1.0*sin(theta),0,0],[sin(theta),cos(theta),0,0],[0,0,1,0],[0,0,0,1]])
        return am

    def translation(translateVector):
        '''
        returns an affine matrix that represents a translation according to the vector passed in
        '''
        v = translateVector
        am = AffineMatrix([[1,0,0,v.x],[0,1,0,v.y],[0,0,1,v.z],[0,0,0,1]])
        return am

    def scale(s):
        '''
        returns an affine matrix that represents a scaling by the amount "s"
        '''
        s = float(s)
        am = AffineMatrix([[s,0,0,0],[0,s,0,0],[0,0,s,0],[0,0,0,1]])
        return am

    def identity():
        '''
        returns a Quaternion that represents no operation
        '''
        # this is probably useless, but it sure was easy to program...
        #am = AffineMatrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
        return AffineMatrix()

    def rotationAboutVector(radianAngle,vect):
        '''
        returns a transformation describing a rotation about a vector according to the right hand rule
        '''
        k = vect # for clarity
        v = 1.0 - cos(radianAngle)
        c = cos(radianAngle)
        s = sin(radianAngle)
        am = AffineMatrix([
            [k.x*k.x*v+c,k.x*k.y*v-k.z*s,k.x*k.z*v+k.y*s,0],
            [k.x*k.y*v+k.z*s,k.y*k.y*v+c,k.y*k.z*v-k.x*s,0],
            [k.x*k.z*v-k.y*s,k.y*k.z*v+k.x*s,k.z*k.z*v+c,0],
            [0,0,0,1]
            ])
        return am

    def equivalentAngleAxis(self):
        '''
        returns a dictionary that describes the equivalent axis (vect) and angle of a rotation, obeying the right hand rule
        (ignores any translation component)
        '''
        # see p52, Intro to Robotics, John J. Craig
        theta = acos( 0.5 * (self.seq[0][0] + self.seq[1][1] + self.seq[2][2] - 1) )
        k = (1.0 / (2.0 * sin(theta) ) ) * Vector(self.seq[2][1] - self.seq[1][2],
            self.seq[0][2] - self.seq[2][0],
            self.seq[1][0] - self.seq[0][1])
        d = {}
        d['Angle'] = theta
        d['Vector'] = k
        return d

    X_rotation = staticmethod(X_rotation)
    Y_rotation = staticmethod(Y_rotation)
    Z_rotation = staticmethod(Z_rotation)
    translation = staticmethod(translation)
    scale = staticmethod(scale)
    identity = staticmethod(identity)
    rotationAboutVector = staticmethod(rotationAboutVector)
    
        

    # VERY important!
        # consider what happens when a point is multiplied by a quaternion!

# test!    
if __name__ == '__main__':
    am=AffineMatrix([[1,0,0,1.0],[0,1,0,2.5],[0,0,1,0],[0,0,0,1]])
    print am
    print "Identity Affine Matrix = \n" + str(AffineMatrix.identity())
    print "30 degree rotation about X = \n" + str(AffineMatrix.X_rotation(pi/180.0*30.0))
    print "30 degree rotation about Y = \n" + str(AffineMatrix.Y_rotation(pi/180.0*30.0))
    print "30 degree rotation about Z = \n" + str(AffineMatrix.Z_rotation(pi/180.0*30.0))
    print "[1,2,3] translation = \n" + str(AffineMatrix.translation(Vector(1,2,3)))
    A = AffineMatrix.identity()
    print 'A = \n' + str(A)
    B = AffineMatrix.Z_rotation(pi/180.0*30.0)
    print 'B = \n' + str(B)
    C = AffineMatrix.translation(Vector(1,2,3))
    print 'C = \n' + str(C)
    print "A * B * C =\n" + str(A * B)
##    p = Point(1,2,3)
##    print "C * p = \n" + str(C*p)
    print "C.invert() =\n" + str(C.invert())
##    m = Matrix([[1.0], [2.0], [3.0], [1.0]])
##    b = AffineMatrix([[0.86602540378443871, -0.49999999999999994, 0.0, 0.0], [0.49999999999999994, 0.86602540378443871, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
##    print (b * m)
    v = Vector(1,2,3)
    q = B * q
    print 'q = \n' + str(q)
    print 'v = ' + str(v)
    print 'q * v = ' + str(q*v)
