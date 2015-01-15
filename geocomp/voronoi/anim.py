# -*- coding: utf-8 -*-

from geocomp.voronoi.voronoi import VoronoiDiagram
from geocomp.voronoi.geometry import intersection, INFINITY

from geocomp.common.control import plot_horiz_line, sleep, plot_line,  plot_circle, plot_delete, plot_parabola, clear_canvas, plot_disc
from geocomp import config

class PaperMixin(object):

	def plot_circle(self, x, y, r, **kwargs):
		print 'plot_circle', x,y,r
		plot_circle(x,y,r, **kwargs)
		#plot_disc(x,y,'blue',r)
		
	def plot_parabola(self, focus, directrix, endpoints=None, color='purple'):
		plot_parabola(focus, directrix, endpoints, color)
		
	def plot_points(self, pts, **kwargs):
		color = kwargs.pop('color', 'red')
		for p in pts:
			plot_disc (p[0],p[1],color,config.RADIUS)
		
	def plot_line(self, a,b,**kwargs):
		plot_line(a.x,a.y,b.x,b.y,**kwargs)

	def plot_horizontal_line(self, y, **kwargs):
		color = kwargs.pop('color', 'red')
		linewidth = kwargs.pop('linewidth', 1)
		plot_horiz_line(y,color,linewidth)
		

class AnimatedVoronoi(VoronoiDiagram, PaperMixin):

	def animate(self,e,draw_bottoms=True, draw_circles=False, draw_circle_events=True):
		beachline = self.T
		event_queue = self.Q
		hedges = self.edges
		pts = self.input


		clear_canvas()
		self._draw_step(e,beachline, event_queue, hedges)
		sleep()

	def _draw_beachline(self, e, beachline):
		isInfinity = lambda x: x is not None and x[0] == INFINITY and x[1] == INFINITY
		#print beachline.T.dumps()
		for arc in beachline:
			end,start=None,None
			pred,suc = beachline.predecessor(arc), beachline.sucessor(arc)
			#print pred, arc, suc
			if pred is not None:
				start = intersection(pred.site,arc.site,e.y)
				# if start[0] == INFINITY and start[1] == INFINITY:
				# 	start = None
			if suc is not None:
				end = intersection(arc.site,suc.site,e.y)
				# if end[0] == INFINITY and end[1] == INFINITY:
				# 	end = None
			if isInfinity(start) and isInfinity(end) or isInfinity(start) and end is None:
				continue
			elif isInfinity(start):
				start = None
			elif isInfinity(end):
				end = None
			# print 'arc is',arc, 'intersections are',start,end, 'pred/suc', beachline.predecessor(arc),beachline.sucessor(arc)
			self.plot_parabola(arc.site,e.y,endpoints=[start,end],color='purple')

	def _draw_hedges(self, e, hedges):
		for h in hedges:
			self.plot_line(h.vertex_from(e.y), h.vertex_to(e.y), color='blue')

	def _draw_circle_events(self, e, event_queue, draw_bottoms=True, draw_circles=False, draw_past_circles=False):
		if not e.is_site:
			bottom, center, radius = e.bottom, e.center, e.radius

			self.plot_circle(center.x, center.y, radius, outline='yellow')
			self.plot_points([bottom], color='green')

		
	def _draw_step(self, e, beachline, event_queue, hedges, **kwargs):
		print 'step for', e
		# Draw directrix
		self.plot_horizontal_line(e.y, color='red')

		self.plot_points(self.input)
		self._draw_beachline(e,beachline)
		self._draw_hedges(e, hedges)
		self._draw_circle_events(e, event_queue)

			
		if e.is_site:
			self.plot_points([e.site], color='white')


def VoronoiProxy(l):
	pts = []
	for p in l:
		pts.append((p.x, p.y))
	bbox = [-500,500,-500,500]
	v = AnimatedVoronoi(pts,bounding_box=bbox, step_by_step=True)
	return None

	# ------------------ #

