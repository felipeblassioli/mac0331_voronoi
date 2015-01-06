def parse_file(selected_file):
	with open('dados/%s' % selected_file) as f:
		lines = f.read().split('\n')
		pts = []
		for l in lines:
			try:
				c = [ float(c)*1 for c in l.split(' ') ]
				x,y = c[0], c[1]
				p = (x,y)
				#p = (x,-y+600)
				pts.append(p)
			except:
				print 'Warning: Failed to parse line=[%s]' % l
		return pts

from geocomp.voronoi.anim2 import animate
from geocomp.voronoi.voronoi import VoronoiDiagram

from os import listdir
if __name__ == "__main__":
	bbox = [-5,35,-5,35]
	VoronoiDiagram.animate = animate
	for f in listdir('dados'):
		pts = parse_file(f)
		v = VoronoiDiagram(pts,bounding_box=bbox, step_by_step=False, filename=f[:-4])