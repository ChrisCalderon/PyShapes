import pygame
import time
import sys
from vector import Vector
from math import pi, cos, sin

I, J, K = Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)

class Shape(object):
	"""Shapes are any collection of points in space. They can only be rotated and 
	projected with perspective onto the y/z plane right now, but hopefully projection
	onto arbitrary planes and more kinds of projections will be added. These aren't drawn,
	just used as a base class for other more interesting things, and used to do all the
	math involed with all this 3d stuff."""
	def __init__(self, start_point, *args):
		self.make_vertices(start_point, *args)

	def make_vertices(self, start_point, *args):
		#Every Shape subclass needs to add a list of vertices
		#to self after being called.
		self.vertices = []
		print "Not Implemented: make_vertices"

	def __getitem__(self, *args):
		return self.vertices.__getitem__(*args)

	def rotate(self, theta, d, p=(0,0,0)):
		"""Rotates every point in the Surface by theta radians, counter-clockwise about 
		the line through the point p in the direction of vector d (which must be a unit vector.)"""
		cos_ = cos(theta)
		cos_1 = 1 - cos_
		sin_ = sin(theta)
		u, v, w = d
		a, b, c = p
		u2, v2, w2 = u*u, v*v, w*w
		bv, au, cw = b*v, a*u, c*w
		t1 = a*(v2+w2) - u*(bv+cw)
		t2 = b*(u2*w2) - v*(au+cw)
		t3 = c*(u2*v2) - w*(au+bv)
		t4 = b*w - c*v
		t5 = c*u - a*w
		t6 = a*v - b*u

		for p in self.vertices:
			x, y, z = p
			t7 = d*p #d is the direction vector, p is the vertex
			t8 = u*t7
			t9 = v*t7
			t10 = w*t7
			newx = (t1 + t8)*cos_1 + x*cos_ + (t4 + v*z - w*y)*sin_
			newy = (t2 + t9)*cos_1 + y*cos_ + (t5 + w*x - u*z)*sin_
			newz = (t3 + t10)*cos_1 + z*cos_ + (t6 + u*y - v*x)*sin_
			p.x = newx
			p.y = newy
			p.z = newz
		return

	def apply_perspective(self, camera_pos, orientation, viewer_pos):
		"""Applies a perspective projection of the points in the Surface onto the y/z plane,
		using the supplied camer position, orientation vector, and viewer position."""
		a, b, c = viewer_pos
		cx, cy, cz = map(cos, orientation)
		sx, sy, sz = map(sin, orientation)
		transformed_vertices = []
		append = transformed_vertices.append
		for v in self.vertices:
			x, y, z = v - camera_pos
			t1 = sz*y + cz*x
			t2 = cz*y - sz*x
			x_ = cy*t1 - sy*z
			t3 = cy*z + sy*t1
			y_ = sx*t3 + cx*t2
			z_ = cx*t3 - sx*t2
			t4 = a/x_
			newx = t4*y_ - b
			newy = t4*z_ - c
			append((-newx, -newy)) #perspective images are flipped, so flip it the right way
		return transformed_vertices

class WireFrame(Shape):
	"""WireFrame objects are very fast to draw and animate, but aren't very pretty."""
	def make_vertices(self, *args):
		#In a WireFrame subclass, you need to provide a draw order as well as
		#a list of vertices when you override the make_vertices function.
		self.vertices = []
		self.draw_order = []

	def draw(self, screen, vs):
		width, height = screen.get_size()
		#Get a list of the vertices in the drawing order, and map them to pixel coordinates.
		points = [(x + width/2, height/2 - y) for (x, y) in [vs[i] for i in self.draw_order]]
		pygame.draw.aalines(screen, (0,0,0), False, points, 2)

class Tetrahedron(WireFrame):
	def make_vertices(self, start_point, side_length):
		"""start_point is the top point."""
		vertices = []
		append = vertices.append
		start_point = Vector(*start_point)
		height = 6**0.5/3*side_length
		base_alt = cos(pi/6)*side_length
		long_half = 2*base_alt/3
		append(start_point)
		append(vertices[-1] - height*K - long_half*I)
		append(vertices[-1] + base_alt*I + .5*side_length*J)
		append(vertices[-1] - side_length*J)
		self.vertices = vertices
		self.draw_order = [0, 3, 2, 0, 1, 2, 3, 1]

class Cube(WireFrame):
	def make_vertices(self, start_point, side_length):
		"""start_point is the upper right front corner."""
		vertices = []
		append = vertices.append
		start_point = Vector(*start_point)
		i, j, k = side_length*I, side_length*J, side_length*K
		append(start_point)
		append(vertices[-1] - k)
		append(vertices[-1] - j)
		append(vertices[-1] + k)
		append(vertices[-1] - i)
		append(vertices[-1] - k)
		append(vertices[-1] + j)
		append(vertices[-1] + k)
		self.vertices = vertices
		self.draw_order = [0, 1, 2, 3, 0, 7, 6, 5, 4, 7, 6, 1, 2, 5, 4, 3]

def demo(shapes):
	def draw_shapes():
		screen.fill((255,255,255))
		[shape.draw(screen, shape.apply_perspective(camera_pos, orientation, viewer_pos)) for shape in shapes]
		pygame.display.flip()

	def print_(string):
		sys.stdout.write(string + "\r")
		sys.stdout.flush()

	axis = I + J + K
	axis *= 1./abs(axis)
	camera_pos = Vector(250, 0, 0)
	viewer_pos = Vector(1500, 0, 0)
	orientation = Vector(0, 0, 0)

	try:
		print "Demoing changing camera orientation."
		for i, axis in enumerate((I, J, K)):
			step = pi/100*axis
			axis_name = "x" if axis == I else ("y" if axis == J else "z")
			for _ in range(200):
				start = time.clock()
				draw_shapes()
				orientation += step
				degrees = (orientation[i]%(2*pi))*180/pi #convert radians -> degrees
				fps = 1/(time.clock() - start)
				msg = "Demoing %s axis orientation changes: %3.2f degrees counter-clockwise. FPS: %3.2f."
				print_(msg % (axis_name, degrees, fps))
			print ""
		print "Demoing change in camera distance from center of projection."
		print "Viewer distance from camera is constant."
		for _ in range(1000):
			start = time.clock()
			camera_pos += I
			viewer_pos += I
			draw_shapes()
			fps = 1/(time.clock() - start)
			msg = "Camera position: %s. Viewer position: %s. FPS: %3.2f."
			print_(msg % (str(camera_pos), str(viewer_pos), fps))
		for _ in range(1000):
			start = time.clock()
			camera_pos -= I
			viewer_pos -= I
			draw_shapes()
			fps = 1/(time.clock() - start)
			msg = "Camera position: %s. Viewer position: %s. FPS: %3.2f."
			print_(msg % (str(camera_pos), str(viewer_pos), fps))
		print ""
		print "Demoing change in viewer distance from camera point."
		print "Camera position stays constant."
		for _ in range(500):
			start = time.clock()
			viewer_pos -= I
			draw_shapes()
			fps = 1/(time.clock() - start)
			msg = "Camera position: %s. Viewer position: %s. FPS: %3.2f."
			print_(msg % (str(camera_pos), str(viewer_pos), fps))
		for _ in range(500):
			start = time.clock()
			viewer_pos += I
			draw_shapes()
			fps = 1/(time.clock() - start)
			msg = "Camera position: %s. Viewer position: %s. FPS: %3.2f."
			print_(msg % (str(camera_pos), str(viewer_pos), fps))
	except KeyboardInterrupt:
		pass
	finally:
		sys.stdout.write("\n")
		pygame.quit()

if __name__=="__main__":
	import random
	shapes = []
	for i in range(25):
		x = random.randrange(-401,-1)
		y = random.randrange(-200,200)
		z = random.randrange(-200,200)
		side_length = 50
		if i&1:
			shapes.append(Tetrahedron([x,y,z], side_length))	
		else:
			shapes.append(Cube([x,y,z], side_length))

	pygame.init()
	size = 800, 800
	screen = pygame.display.set_mode(size)
	demo(shapes)
	