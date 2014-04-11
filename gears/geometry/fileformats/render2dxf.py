from .. import Point, Line, Arc, Circle, Polyline
import sdxf
#from math import pi, sin, cos, degrees
import math

def _point(p):
    '''
    convert a geometry Point into an sdxf point
    '''
    return (p.x,p.y,p.z)

def _points(pList):
    '''
    convert a geometry list of points into an sdxf list of points
    '''
    s = []
    for p in pList:
        s.append(_point(p))
    return s

class Render2DXF:
    def __init__(self):
        self.d=sdxf.Drawing() #create sdxf drawing instance
        self.blockNumber = 1 #so that blocks can be uniquely named

    def _appendEntity(self,entity,appendTo=None):
        '''
        append an entity to a block or drawing
        '''
        g = entity # because I'm too lazy to change this everywhere
        if not ( isinstance(appendTo,sdxf.Drawing) or isinstance(appendTo,sdxf.Block) ):
            appendTo = self.d

        if isinstance(g,Point):
            appendTo.append(sdxf.Point(_point(g)))
        elif isinstance(g,Line):
            appendTo.append(sdxf.Line(points=[_point(g.startPoint),_point(g.endPoint)]))
        #elif g.__type__ == 'Line':
        #    appendTo.append(sdxf.Line(points=[_point(g.startPoint),_point(g.endPoint)]))
        elif isinstance(g,Polyline):
            pl = _points(g.points)
            if g.closed == True:
                pl = pl[:-1]
                appendTo.append(sdxf.PolyLine(points=pl,closed=1))
            else:
                appendTo.append(sdxf.PolyLine(points=pl,closed=0))
        elif isinstance(g,Arc):
            cp = _point(g.center)
            r = g.radius
            sa = degrees(g.startAngle)
            ea = degrees(g.endAngle)
            appendTo.append(sdxf.Arc(center=cp,radius=r,startAngle=sa,endAngle=ea))
        elif isinstance(g,Circle):
            cp = _point(g.center)
            r = g.radius
            appendTo.append(sdxf.Circle(center=cp,radius=r))
        elif isinstance(g,Block):
            bString = "Block%i" %self.blockNumber
            #print bString
            b = sdxf.Block(bString)
            self.blockNumber += 1
            for ent in g.seq:
                self._appendEntity(ent,appendTo=b)
            self.d.blocks.append(b)
            self.d.append(sdxf.Insert(bString,point=(0,0,0)))
        #print "Appended:\n%s" % str(g)
        else:
            print "Nothing was matched for: %s" % str(g)
        #print repr(self.d.entities) + '\n\n'

    def render(self,entityList):
        for g in entityList:
            self._appendEntity(g)
            #self.d.blocks.append(b)                     #table blocks
        self.d.styles.append(sdxf.Style())          #table styles
        self.d.views.append(sdxf.View('Normal'))    #table view

    def render2File(self,entityList,fname):
        self.render(entityList)
        self.d.saveas(fname)

    def __str__(self):
        return str(self.d)

if __name__=="__main__":
    l1 = Line(Point(1,1),Point(2,1))
    l2 = Line(Point(2,2),Point(3,2))
    b = Block([l1,l2])
    r = Render2DXF()
    r.render2File([b],'junk.dxf')

