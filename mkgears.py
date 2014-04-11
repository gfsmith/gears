from gears import Gear
import os

OUTPUT_DIR = 'output'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

gList = range(3,200+1) + range(220,500+10,10) + range(550,1050,50)

for i in gList:
	try:
		print "Generating %i tooth gear..." % i
		g = Gear(numTeeth = i)
		fname = './output/gear%i.dxf' % i
		g.render2DXF(fname)
	except KeyboardInterrupt:
		print "Stopped."
		break
