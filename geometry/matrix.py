# To do:
    # look at the methods to implement section below!

class Matrix:
    '''
    A light weight (floating point) matrix class that does the basics so that it is not necessary
    to import Numeric Python for small projects
    '''
    
    def __init__(self,seq=None):
        '''
        create a matrix from a sequence such as [[1,2],[3,4]]
        '''
        if seq == None:
            self.seq = []
            self.numRows = 0
            self.numCols = 0
        else:
            seq = list(seq) # try to convert a a list
            self.numRows = len(seq)
            self.numCols = len(seq[0])
            self.seq = seq
            for j in range(self.numRows):
                for i in range(self.numCols):
                    self.seq[j][i] = float(self.seq[j][i])

    def size(self):
        '''
        return the dimensions of the matrix (# rows, #columns)
        '''
        return (self.numRows,self.numCols)

    def __str__(self):
        outStr = ''
        for j in range(self.numRows):
            outStr += '[ '
            for i in range(self.numCols):
                outStr += '%10.6g\t' % self.seq[j][i]
            outStr += ' ]\n'
        return outStr

    def __repr__(self):
        return "Matrix(%s)" % repr(self.seq)

    def dup(self):
        '''
        return a duplicate copy
        '''
        # m=Matrix(self.seq)  #,--- does not work, only a shallow copy of the sequence
        # we want a deep copy, but don't want to import copy.deepcopy!
        localSeq = []
        for j in range(self.numRows):
            rowList=[]
            for i in range(self.numCols):
                rowList.append(self.seq[j][i])
            localSeq.append(rowList)
        m = Matrix(localSeq)
        return m

    def __add__(self,b):
        '''
        add matrices, returning a new matrix
        (matrices must be the same size to add them)
        '''
        m = self.dup() # create a copy
        if isinstance(b,Matrix):
            # matrices must be of the same dimensions for addition
            if ( m.size() != b.size() ):
                raise ValueError('Matrices of different sizes cannot be added.')
            for j in range(m.numRows):
                for i in range(m.numCols):
                    m.seq[j][i] = m.seq[j][i] + b.seq[j][i]
        else:
            b = float(b)
            for j in range(m.numRows):
                for i in range(m.numCols):
                    m.seq[j][i] = m.seq[j][i] + b
        return m

    def __radd__(self,b):
        return self.__add__(b)

    def __sub__(self,b):
        return self.__add__(-1.0*b)

    def __mul__(self,b):
##        print '"Matrix.__mul__" has been called'
        if isinstance(b,Matrix):
            # matrices being multiplied must have agreeable sizes to be multiplied
            sizeResult = (self.numRows,b.numCols)
            if self.numCols != b.numRows:
                raise ValueError('Matrices are not sized appropriately for multipication.\nThe number of columns of the left matrix must be the same as the number of rows of the right matrix.')
            resultList = []
            for j in range(sizeResult[0]):
                rowList=[]
                for i in range(sizeResult[1]):
                        curVal = 0
                        for k in range(self.numCols):
                            curVal += self.seq[j][k] * b.seq[k][i]
                        rowList.append(curVal)
                resultList.append(rowList)
            m = Matrix(resultList)
            return m
        elif isinstance(b,(int,float)):
            b = float(b)
            m = self.dup()
            for j in range(self.numRows):
                for i in range(self.numCols):
                    m.seq[j][i] = self.seq[j][i] * b
            return m
        else:
            raise ValueError

    def __rmul__(self,b):
        '''
        this handles multiplication of two matrices or the multiplication of a matrix and a constant
        '''
##        print "'Matrix.__rmul__' called."
        if isinstance(b,Matrix):
            m = Matrix(b.seq)
            return m.__mul__(self)
        elif isinstance(b,(int,float)):
            return self.__mul__(b)
        else:
            raise ValueError

    def __neg__(self):
        '''
        negate matrix (multiplication by negative one)
        '''
        m=self.dup()
        for j in range(self.numRows):
            for i in range(self.numCols):
                m.seq[j][i] *= -1.0
        return m

    def transpose(self):
        localSeq = []
        for i in range(self.numCols):
            rowList = []
            for j in range(self.numRows):
                rowList.append(self.seq[j][i])
            localSeq.append(rowList)
        m = Matrix(localSeq)
        return m
                
    # other methods to implement???
        # __iadd__
        # __isub__
        # __imul__
        # __getitem__
        # determinate
        # inverse
        
            
        
        
# test!
if __name__ == "__main__":
    a = Matrix ([[1,2,3,0],[4,5,6,0],[7,8,9,0],[0,0,0,1]])
    A = Matrix ([[1,0,2],[-1,3,1]])
    B = Matrix ([[3,1],[2,1],[1,0]])
    C = Matrix()
    D = Matrix([[1]])
    print 'a = \n' + str(a)
    print 'repr(a) = \n' + repr(a)
    print 'a + 1 = \n' + str(a+1)
    print 'a = \n' + str(a)
    print 'repr(a) = \n' + repr(a)
    print '1 + a = \n' + str(1+a)
    print 'a = \n' + str(a)
    print 'a * 3.0 = \n' + str(a * 3.0)
    print '2.5 * a = \n' + str(2.5 * a)
    print 'A = \n' + str(A)
    print 'B = \n' + str(B)
    print 'A * B = \n' + str(A * B)
    print '-a =\n' + str(-a)
    print 'A.transpose() = \n' + str(A.transpose())
    m = Matrix([[1.0], [2.0], [3.0], [1.0]])
    b = Matrix([[0.86602540378443871, -0.49999999999999994, 0.0, 0.0], [0.49999999999999994, 0.86602540378443871, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
    print (b * m)
