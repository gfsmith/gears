from geometry import *
import math

epsilon = 1.0E-6

class Gear:
    # a few conventions need to be described:
    # theta is the angle that the contact point of the "string" makes with the base circle in generating the involute
    # rho is the angle from the abcissa (x-axis) to the point of interest (polar angle)
    def __init__(self, numTeeth, diametricalPitch=18, pressureAngleDegrees=20):
        '''
        creates an involute spur gear based on ANSI B6.1-1968(R1974)
        (ANSI Coarse pitch Spur gears)

        This is valid for gears with pressure angles of 20 and 25
        degrees with a minimum of 18 and 12 teeth respectively
        '''
        self.N = int(numTeeth)
        self.P = int(diametricalPitch)
        self.p = math.pi / self.P   #circular pitch
        self.phi = math.radians(float(pressureAngleDegrees)) #pressure angle
        self.D_pitch = float(self.N) / float(self.P)  #pitch circle diameter
        self.R_pitch = 0.5 * self.D_pitch # pitch circle radius

        self.D_base = self.D_pitch * math.cos(self.phi) # base circle diameter
        self.R_base = 0.5 * self.D_base # base circle radius

        self.a = 1.0 / self.P     # addendum
        self.b = 1.25 / self.P    # dedendum (preferred)

        self.D_outside = self.D_pitch + ( 2 * self.a ) # OD
        self.R_outside = 0.5 * self.D_outside # outside radius

        self.D_root = self.D_pitch - ( 2 * self.b ) # root Diameter
        self.R_root = 0.5 * self.D_root # root radius

        self.radians_per_tooth = 2.0 * math.pi / self.N

        self._gearGeometry()

    def _involute(theta, R_base):
        '''
        returns a dictionary containing interesting parameters of an involute
        '''
        x = R_base * math.cos(theta) + R_base * theta * math.sin(theta)
        y = R_base * math.sin(theta) - R_base * theta * math.cos(theta)
        R = math.sqrt(x**2 + y**2)
        rho = math.atan2(y,x)
        d={}
        d['x']=x
        d['y']=y
        d['R']=R
        d['rho']=rho
        d['theta']=theta
        return d

    def _gearGeometry(self):
        '''
        solve for and create the actual gear geometry
        '''
        # clearance trochoid is only necessary if root diamater is smaller than base circle diameter?
        if (self.D_root > self.D_base):
            # no clearance trochoid is necessary

            # figure out involute bounds
            def involute_R(theta): # intermediate function
                d = self._involute(theta, R_base = self.R_base)
                return d['R']
            theta1 = self._bisectionMethodSolver(involute_R,float(0),math.radians(90.0),self.R_pitch)   # theta at pitch circle
            theta2 = self._bisectionMethodSolver(involute_R,float(0),math.radians(90.0),self.R_outside) # theta at outer circle
            theta3 = self._bisectionMethodSolver(involute_R,float(0),math.radians(90.0),self.R_root) # theta at root circle
            rho1 = self._involute(theta1, R_base = self.R_base)['rho'] # rho at pitch circle
            rho2 = self._involute(theta2, R_base = self.R_base)['rho'] # rho at outer circle
            rho3 = self._involute(theta3, R_base = self.R_base)['rho'] # rho at root circle
            involute_angular_width = rho2-rho1
            # print "theta1 = %g, theta2 = %g, rho1 = %g, rho2 = %g" % (theta1, theta2, rho1, rho2)

            # create involute
            pointList = []
            xList = []
            yList = []
            involute_angular_offset = 0.25 * self.radians_per_tooth - rho1
            theta = theta3 # start at root circle
            numPoints = int(50)
            theta_increment = (theta2-theta)/float(numPoints - 1)
            for i in range(numPoints):
                d = self._involute(theta, self.R_base)
                pointList.append(Point(d['x'],d['y']))
                theta += theta_increment
            invPL = Polyline(pointList)
            t1 = AffineMatrix().Z_rotation(involute_angular_offset)
            invPL = t1 * invPL
            print "involute for theta from %f to %f (radians):" % (theta3+involute_angular_offset,theta2+involute_angular_offset)
            print "  x = %f * cos(theta) + %f * theta * sin(theta)" % (self.R_base,self.R_base)
            print "  y = %f * sin(theta) - %f * theta * cos(theta)" % (self.R_base,self.R_base)

            outerArc = Arc(radius = self.R_outside, startAngle = rho2 + involute_angular_offset, endAngle = math.pi/self.N, direction = 'CCW')
            # outer arc at radius self.R_outside from rho2+involute_angular_offset
            # print "outer arc at radius %f, from %f to %f (radians)" % (self.R_outside,rho2+involute_angular_offset,math.pi/self.N)
            print "outerArc = %s" % str(outerArc)
            innerArc = Arc(radius = self.R_root,startAngle  = 0.0, endAngle = rho3 + involute_angular_offset, direction = 'CCW')
            #print "inner arc at radius %f, from %f to %f (radians)" % (self.R_root, 0.0,rho3 + involute_angular_offset)
            print "innerArc = %s" % str(innerArc)
            print
            innerArcPL = innerArc.toPolyline()
            outerArcPL = outerArc.toPolyline()
            halfTooth = Polyline(innerArcPL.points + invPL.points + outerArcPL.points)
        else:
            # figure out involute bounds
            def involute_R(theta): # intermediate function
                d = self._involute(theta, R_base = self.R_base)
                return d['R']
            theta1 = self._bisectionMethodSolver(involute_R,float(0),math.radians(90.0),self.R_pitch)   # theta at pitch circle
            theta2 = self._bisectionMethodSolver(involute_R,float(0),math.radians(90.0),self.R_outside) # theta at outer circle
            rho1 = self._involute(theta1, R_base = self.R_base)['rho'] # rho at pitch circle
            rho2 = self._involute(theta2, R_base = self.R_base)['rho'] # rho at outer circle
            involute_angular_width = rho2-rho1
            # print "theta1 = %g, theta2 = %g, rho1 = %g, rho2 = %g" % (theta1, theta2, rho1, rho2)

            # create involute
            pointList = []
            xList = []
            yList = []
            involute_angular_offset = 0.25 * self.radians_per_tooth - rho1
            theta = 0.0 # start at base circle
            numPoints = int(50)
            theta_increment = (theta2-theta)/float(numPoints - 1)
            for i in range(numPoints):
                d = self._involute(theta, self.R_base)
                pointList.append(Point(d['x'],d['y']))
                theta += theta_increment
            invPL = Polyline(pointList)
            t1 = AffineMatrix().Z_rotation(involute_angular_offset)
            invPL = t1 * invPL
            print "involute for theta from %f to %f (radians):" % (involute_angular_offset,theta2+involute_angular_offset)
            print "  x = %f * cos(theta) + %f * theta * sin(theta)" % (self.R_base,self.R_base)
            print "  y = %f * sin(theta) - %f * theta * cos(theta)" % (self.R_base,self.R_base)

            outerArc = Arc(radius = self.R_outside, startAngle = rho2 + involute_angular_offset, endAngle = math.pi/self.N, direction = 'CCW')
            print "outerArc = %s" % str(outerArc)

            # define clearance trochoid
            # figure out trochoid bounds
            def clearance_trochoid_R(theta): # intermediate function
                d = self._clearance_trochoid(-1.0 * theta, R_pitch = self.R_pitch, r = self.R_root)
                return d['R']
            theta1 = 0.0 # theta at root
            theta2 = self._bisectionMethodSolver(clearance_trochoid_R,float(0),math.radians(90.0),self.R_base) # theta at base circle
            rho1 = self._clearance_trochoid(theta1, R_pitch = self.R_pitch, r = self.R_root)['rho']
            rho2 = self._clearance_trochoid(theta2, R_pitch = self.R_pitch, r = self.R_root)['rho']
            clearance_trochoid_angular_width = abs(rho2-rho1)
            # print "theta1 = %g, theta2 = %g, rho1 = %g, rho2 = %g" % (theta1, theta2, rho1, rho2)

            # create clearance trochoid
            pointList = []
            xList = []
            yList = []
            clearance_trochoid_angular_offset = involute_angular_offset - clearance_trochoid_angular_width
            #print "clearance_trochoid_angular_offset = %f" % math.degrees(clearance_trochoid_angular_offset)
            theta = theta1
            numPoints = int(50)
            theta_increment = (theta2-theta1)/float(numPoints - 1)
            for i in range(numPoints):
                d = self._clearance_trochoid(-1.0 * theta, self.R_pitch, r = self.R_root)
                pointList.append(Point(d['x'],d['y']))
                theta += theta_increment
            ctrochPL = Polyline(pointList)
            t1 = AffineMatrix().Z_rotation(clearance_trochoid_angular_offset)
            ctrochPL = t1 * ctrochPL
            print "clearance trochoid from %f to %f" % (theta1+clearance_trochoid_angular_offset,theta2+clearance_trochoid_angular_offset)
            print "x = %f * cos(-theta) + %f * -theta * sin(-theta)" % (self.R_root,self.R_pitch)
            print "y = %f * sin(-theta) - %f * -theta * math.cos(-theta)" % (self.R_root,self.R_pitch)
            innerArc = Arc(radius = self.R_root, startAngle = 0.0, endAngle = clearance_trochoid_angular_offset + rho1, direction='CCW')
            print
            print "innerArc = %s" % str(innerArc)
            innerArcPL = innerArc.toPolyline()
            outerArcPL = outerArc.toPolyline()
            print "outerArc = %s" % str(outerArc)
            print
            halfTooth = Polyline(innerArcPL.points + ctrochPL.points + invPL.points + outerArcPL.points)

            #self.toothGeometry = Block([innerArcPL,ctrochPL,invPL,outerArcPL])
            #halfTooth = Polyline(innerArcPL.points + ctrochPL.points + invPL.points + outerArcPL.points)
            mirrorLine = Line(startPoint=Point(0,0),endPoint = Point(self.R_outside * math.cos(math.pi/self.N),self.R_outside * math.sin(math.pi/self.N),0.0) )
            halfTooth2 = mirrorAboutLine(halfTooth,mirrorLine)
            #print "halfTooth.points = %s" % str(halfTooth.points)
            #print "halfTooth2.points = %s" % str(halfTooth2.points)
            #halfTooth2 = halfTooth.dup()
            halfTooth2.reverse()
            pl = halfTooth.points + halfTooth2.points
            fullTooth = Polyline(pl)
            self.toothGeometry = fullTooth
            gearBlock = polarArray(self.toothGeometry,self.N)
            l = []
            for pl in gearBlock.seq:
                l += pl.points
            self.geom = Polyline(l)

    def render2DXF(self,fname):
        '''
        render a gear to DXF
        '''
        r = Render2DXF()
        r.render2File([self.geom],fname)

    def render2SVG(self,fname):
        '''
        render a gear to SVG
        '''
        r = Render2SVG()
        r.render2File([self.geom], fname)

    def _clearance_trochoid(self,theta, R_pitch,r):
        '''
        returns a dictionary containing interesting parameters of a clearance involute
        where r is R_root
        '''
        x = r * math.cos(theta) + R_pitch * theta * math.sin(theta)
        y = r * math.sin(theta) - R_pitch * theta * math.cos(theta)
        R = math.sqrt(x**2 + y**2)
        rho = math.atan2(y,x)
        d={}
        d['x']=x
        d['y']=y
        d['R']=R
        d['rho']=rho
        d['theta']=theta
        #print "theta = %g, rho = %g, R = %g" % (math.degrees(theta),math.degrees(rho),R)
        #time.sleep(0.25)
        return d

    def _bisectionMethodSolver(self,f_of_x,xl,xu,y_desired):
        yl = f_of_x(xl) - y_desired
        yu = f_of_x(xu) - y_desired
        while True:
            xr = 0.5 * (xl+xu)
            yr = f_of_x(xr) - y_desired
            if ( abs(yr) < epsilon ): return xr
            #print "%f,\t%f,\t%f\t:\t%f,\t%f,\t%f" % (xl,xu,xr, yl, yu, yr)
            if ( ( yl * yr ) < 0 ):
             # root lies in lower interval
                xu = xr
                yu = yr
            else:
                # root lies in upper interval
                xl = xr
                yl = yr

    def _involute(self,theta, R_base):
        '''
        returns a dictionary containing interesting parameters of an involute
        '''
        x = R_base * math.cos(theta) + R_base * theta * math.sin(theta)
        y = R_base * math.sin(theta) - R_base * theta * math.cos(theta)
        R = math.sqrt(x**2 + y**2)
        rho = math.atan2(y,x)
        d={}
        d['x']=x
        d['y']=y
        d['R']=R
        d['rho']=rho
        d['theta']=theta
        return d

    def __str__(self):
        s = ''
        s+= "Number of Teeth   = %i\n" % self.N
        s+= "Diametrical Pitch = %i\n" % self.P
        s+= "Circular Pitch    = %f\n" % self.p
        s+= "Pitch Diameter    = %f\n" % self.D_pitch
        s+= "Pressure Angle    = %f\n" % self.phi
        s+= "Base Circle Dia   = %f\n" % self.D_base
        s+= "Addendum          = %f\n" % self.a
        s+= "Dedendum          = %f\n" % self.b
        s+= "Outside Dia       = %f\n" % self.D_outside
        s+= "Root Dia          = %f\n" % self.D_root
        return s


if __name__ == "__main__":
    g = Gear(numTeeth = 7)
    print g
    #g.render2DXF('gearG.dxf')
    raw_input('Press a key')


