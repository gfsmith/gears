from geometry import Point, Line, Arc, Circle, Polyline

def EAGLEArc(arc):
    from math import cos, sin
    
    a = (arc.center.x + arc.radius*cos(arc.startangle), arc.center.y + arc.radius*sin(arc.startangle))
    b = (arc.center.x - arc.radius*cos(arc.startangle), arc.center.y - arc.radius*sin(arc.startangle))
    c = (arc.center.x + 2*arc.radius*cos(arc.endangle), arc.center.y + 2*arc.radius*sin(arc.endangle))

    direction = 'CCW'

    return "ARC " + direction + " (%0.6lf %0.6lf)" % a + " (%0.6lf %0.6lf)" % b + " (%0.6lf %0.6lf)" % c + ";"
    

def EAGLELine(line):
    return  "WIRE  (%0.6lf %0.6lf)" % (line.a.x, line.a.y) + " (%0.6lf %0.6lf);" % (line.b.x, line.b.y)

def EAGLEPolyline(pl):
    if len(pl) > 0:
        command = "WIRE "
        for p in pl.points:
            command += " (%0.6lf %0.6lf) " % (p.x,p.y)
        command += ";"
        return command
    else:
        return ''
    
def EAGLECircle(circle, drill=False):
    if drill:
        return "HOLE %0.6lf (%0.6lf %0.6lf);" % (circle.radius*2.0, circle.center.x, circle.center.y)
    else:
        return "CIRCLE (%0.6lf %0.6lf)" % (circle.center.x,circle.center.y) + " (%0.6lf %0.6lf);" % (circle.center.x+circle.radius,circle.center.y)
     

def EAGLEGeometry(geometry):
    if isinstance(geometry, Arc): return EAGLEArc(geometry)
    elif isinstance(geometry, Line): return EAGLELine(geometry)
    elif isinstance(geometry, Circle): return EAGLECircle(geometry)
    elif isinstance(geometry, Polyline): return EAGLEPolyline(geometry)
    else: return ''

