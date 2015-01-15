# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""Implementacao das operacoes graficas em Tk.

Esse modulo nao deve ser usado diretamente. Para isso,
veja geocomp.common.control"""

from math import fabs

master = None
canvas = None

def init_display (master):
	globals()['canvas'] = master.canvas
	globals()['master'] = master

def get_canvas ():
	return canvas

def update ():
	canvas.update ()

def sleep ():
	if master.step_by_step.get ():
		master.tk.wait_variable (master.step)
	else:
		master.tk.after (master.delay.get (), master.tk.quit)
		master.tk.mainloop ()

def plot_circle (x, y, r, **kwargs):
	x = canvas.r2cx(x)
	y = canvas.r2cy(y)
	r = canvas.r2cx(x+r) - canvas.r2cx(x)
	print '\tplot circle',x,y
	return canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

def plot_disc (x, y, color, r):
	plot_id = canvas.create_oval (canvas.r2cx(x)-r, canvas.r2cy(y)-r, 
					canvas.r2cx(x)+r, canvas.r2cy(y)+r, fill=color)
	return plot_id

def plot_line (x0, y0, x1, y1, color, linewidth):
	lineto_id = canvas.create_line (canvas.r2cx(x0), canvas.r2cy(y0), 
					   canvas.r2cx(x1), canvas.r2cy(y1), 
					   fill=color, width=linewidth)
	return lineto_id

def plot_vert_line (x, color, linewidth, y=0):
	lineto_id = canvas.create_line (canvas.r2cx(x), 0, 
					   canvas.r2cx(x), int (canvas['height']), 
					   fill=color, width=linewidth)
	return lineto_id

def plot_horiz_line (y, color, linewidth):
	lineto_id = canvas.create_line (0, canvas.r2cy(y), 
					   int (canvas['width']), canvas.r2cy(y), 
					   fill=color, width=linewidth)
	return lineto_id

def plot_delete (id):
	canvas.delete (id)


from geocomp.voronoi.geometry import vertex, coefficients, Point
def _parabola(x, focus, directrix):
	A,B,C = coefficients(focus,directrix)
	if A == 0:
		return None
	return A*(x**2) + B*x + C

def linspace(start,end, total):
	dx = float((end - start)) / total
	x = start
	while x <= end:
		yield x
		x += dx

def fcmp(p,q,epsilon=0.00001):
	_eq = lambda a, b, t: abs(a - b) < t
	return _eq(p,q,epsilon)

CANVAS_START = -2000
CANVAS_WIDTH = 2000
CANVAS_HEIGHT = 2000
def plot_parabola(focus, directrix, endpoints=None, color='purple'):
	global CANVAS_START
	global CANVAS_WIDTH
	global CANVAS_HEIGHT
	#print 'plot_parabola', focus, directrix, endpoints

	# Plot the parabola
	if focus[1] == directrix:
		if endpoints[0]:
			end = endpoints[0][1]
		elif endpoints[1]:
			end = endpoints[1][1]
		else:
			end = CANVAS_HEIGHT
		print '\tplot focus', focus,end, 'C_HEIGHT', CANVAS_HEIGHT

		line = plot_line(focus[0],directrix,focus[0],end,color=color,linewidth=2)
		return line
		#plt.plot([a,a],[directrix,end],'b-',color=color,linewidth=2)
	else:
		start = endpoints[0][0] if endpoints[0] is not None else CANVAS_START
		end = endpoints[1][0] if endpoints[1] is not None else CANVAS_WIDTH
		print '\tplot focus', focus, start,end
		if fcmp(start,end):
			print 'wwtfffffffffffffff'
			return None
		lines = []
		f = lambda x: _parabola(x,focus,directrix)
		prev = start
		for x in linspace(start,end,240):
			p = (prev,f(prev))
			q = (x,f(x))
			prev = x
			line = plot_line(p[0],p[1],q[0],q[1],color=color,linewidth=2)
			lines.append(line)

		return lines
		#plt.plot(pts, parabola(pts,f,directrix), '-',color=color,linewidth=2)


def config_canvas (minx, maxx, miny, maxy):
	global CANVAS_START
	global CANVAS_WIDTH
	global CANVAS_HEIGHT
	for item in canvas.find_all ():
		canvas.delete (item)


	Dx = maxx - minx
	Dy = maxy - miny

	if canvas.winfo_width () <= 1 and canvas.winfo_height () <= 1:
		width = int (canvas['width'])
		height = int (canvas['height'])
	else:
		width = canvas.winfo_width ()
		height = canvas.winfo_height ()

	ratio = float (width)/ float (height)
	ratio_dxdy = float (Dx)/ float (Dy)

	if ratio != ratio_dxdy:
		if ratio_dxdy < ratio:
			new_dx = Dy * ratio
			minx = minx - fabs (Dx-new_dx)/2
			Dx = new_dx
		else:
			new_dy = Dx / ratio
			miny = miny - fabs (Dy-new_dy)/2
			Dy = new_dy

	CANVAS_START = ((-0.1/0.8)*Dx) + minx # Valor que garante que rc(CANVAS_WIDTH) = -0.1*width
	#CANVAS_WIDTH = (0.9*maxx-0.1*minx)/0.8 # Valor que garante que rc(CANVAS_WIDTH) = width
	CANVAS_WIDTH = (maxx-0.2*minx)/0.8 # Valor que garante que rx(CANVAS_WIDTH) = 1.1*width
	CANVAS_HEIGHT = ((0.9/0.8)*Dy)+miny	
	def rx (x, x0 = minx, dx = Dx, width=width):
		return int ((x - x0) * width*0.8 / dx + 0.1*width)
		#return int ((x - x0) * int (cv['width'])*0.8 / dx + 0.1*int (cv['width']))

	def ry (y, y0 = miny, dy = Dy, height=height):
		return height - int ((y - y0) * height*0.8 / dy + 0.1*height)
		#return int (cv['height']) - int ((y - y0) * int (cv['height'])*0.8 / dy + 0.1*int (cv['height']))

	#print canvas['width'], canvas['height'], canvas['confine']
	#print canvas.winfo_width (), canvas.winfo_height ()
	
	canvas.r2cx = rx
	canvas.r2cy = ry

def hide_algorithm ():
	return master.show_var.get () != 0

