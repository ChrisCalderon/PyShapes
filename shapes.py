import turtle
import time
import sys
from vector import Vector
from math import pi, cos, sin

I, J, K = Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)

class Shape(object):
	def __init__(self, start_point, *args):
		self.make_vertices(start_point, *args)

	def make_vertices(self, start_point, *args):
		self.vertices = []
		print "Not Implemented: __make_vertices"

	def __getitem__(self, *args):
		return self.vertices.__getitem__(*args)

	def rotate(self, theta, d, point=(0,0,0)):
		"""Rotates every vertex by theta radians about the line through point
		in the direction of vector d (which must be a unit vector.)"""
		cos_ = cos(theta)
		cos_1 = 1 - cos_
		sin_ = sin(theta)
		u, v, w = d
		a, b, c = point
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
		#The plane that points are projected onto is y/z plane.
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

	def draw(self):
		print "Not Implemented: draw"

class Tetrahedron(Shape):
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

	@staticmethod
	def draw(vs):
		turtle.up()
		turtle.goto(vs[0])
		turtle.down()
		turtle.goto(vs[3])
		turtle.goto(vs[2])
		turtle.goto(vs[0])
		turtle.goto(vs[1])
		turtle.goto(vs[2])
		turtle.goto(vs[3])
		turtle.goto(vs[1])
		return

class Cube(Shape):
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

	@staticmethod
	def draw(vs):
		turtle.up()
		turtle.goto(vs[0])
		turtle.down()
		turtle.goto(vs[1])
		turtle.goto(vs[2])
		turtle.goto(vs[3])
		turtle.goto(vs[0])
		turtle.goto(vs[7])
		turtle.goto(vs[6])
		turtle.goto(vs[5])
		turtle.goto(vs[4])
		turtle.goto(vs[7])
		turtle.goto(vs[6])
		turtle.goto(vs[1])
		turtle.goto(vs[2])
		turtle.goto(vs[5])
		turtle.goto(vs[4])
		turtle.goto(vs[3])	
		return

def demo(shapes):
	def draw_shapes():
		[shape.draw(shape.apply_perspective(camera_pos, orientation, viewer_pos)) for shape in shapes]
		turtle.update()
		turtle.clear()

	def print_(string):
		sys.stdout.write(string + "\r")
		sys.stdout.flush()

	turtle.tracer(False)
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
		print ""
		for _ in range(500):
			start = time.clock()
			viewer_pos += I
			draw_shapes()
			fps = 1/(time.clock() - start)
			msg = "Camera position: %s. Viewer position: %s. FPS: %3.2f."
			print_(msg % (str(camera_pos), str(viewer_pos), fps))
		print ""
	except KeyboardInterrupt:
		pass
	finally:
		sys.stdout.write("\n")
		turtle.bye()

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

	demo(shapes)


	