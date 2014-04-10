from matrix import Matrix
from vector import Vector
from point import Point
from affinematrix import AffineMatrix
from line import Line
from polyline import Polyline
from circle import Circle
from arc import Arc

class Block:
    '''
    a container for geometric entities
    '''
    def __init__(self,seq=None):
        if seq == None:
            self.seq = []
        else:
            self.seq = list(seq)

    def append(self,geom):
        '''
        append geometry to block
        '''
        self.seq.append(geom)

    def dup(self):
        '''
        a deep copy
        '''
        seq2 = []
        for g in self.seq:
            seq2.append(g.dup())
        return Block(seq2)

    def __str__(self):
        return "Block(%s)" % repr(self.seq)

    def __repr__(self):
        return str(self)

    def __rmul__(self,am):
        seq2 = []
        if isinstance(am,AffineMatrix):
            for g in self.seq:
                seq2.append(am*g)
            return Block(seq2)
        else:
            raise ValueError('Non-AffineMatrix in Block __rmul__.')


