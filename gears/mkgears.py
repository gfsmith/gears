from gear import gear

gList = range(3,200+1) + range(220,500+10,10) + range(550,1050,50)

for i in gList:
	try:
		print "Generating %i tooth gear..." % i
		g = gear(numTeeth = i)
		fname = './gearDXFs/gear%i.dxf' % i 
		g.render2DXF(fname)
	except KeyboardInterrupt:
		print "Stopped."
		break