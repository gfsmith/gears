from .. import Point, Line, Arc, Circle, Polyline
import svgwrite
#from math import pi, sin, cos, degrees
import math

def _point(p):
    '''
    convert a geometry Point into a tuple
    '''
    return (p.x,p.y)

def _points(pList):
    '''
    convert a geometry list of points into a list of tuples
    '''
    s = []
    for p in pList:
        s.append(_point(p))
    return s

class Render2SVG:
    def __init__(self):
        self.dwg=svgwrite.Drawing() #create svg drawing instance

    def _addEntity(self,entity,addTo=None):
        '''
        add an entity to a drawing
        '''
        if not isinstance(addTo,svgwrite.Drawing):
            addTo = self.dwg

        if isinstance(entity,Point):
            addTo.add(addTo.circle(center=_point(entity)))
        elif isinstance(entity,Line):
            addTo.add(addTo.line(start=_point(entity.startPoint),end=_point(entity.endPoint)))
        elif isinstance(entity,Polyline):
            pl = _points(entity.points)
            if entity.closed == True:
                pl = pl[:-1]
                addTo.add(addTo.polygon(pl))
            else:
                addTo.add(addTo.polyline(pl))
        elif isinstance(entity,Arc):# not yet sure how to handle arcs in SVG, but shouldn't be bad?
            cp = _point(entity.center)
            r = entity.radius
            #sa = degrees(g.startAngle)
            #ea = degrees(g.endAngle)
            addTo.add(addTo.circle(center=cp,radius=r))#,startAngle=sa,endAngle=ea))
        elif isinstance(entity,Circle):
            cp = _point(entity.center)
            r = entity.radius
            addTo.add(addTo.circle(center=cp,radius=r))
        else:
            print "Nothing was matched for: %s" % str(g)
        #print repr(self.d.entities) + '\n\n'

    def render(self,entityList):
        for entity in entityList:
            self._addEntity(entity)

    def render2File(self,entityList,fname):
        self.render(entityList)
        self.dwg.saveas(fname)

    def __str__(self):
        return str(self.dwg)

if __name__=="__main__":
    l1 = Line(Point(1,1),Point(2,1))
    l2 = Line(Point(2,2),Point(3,2))
    r = Render2SVG()
    print l1
    print l2
    r.render2File([l1,l2],'junk.svg')

