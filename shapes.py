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
		print "Not Implemented: __make_vertices"

	def rotate(self, theta, u):
		cos_ = cos(theta)
		cos_1 = 1 - cos_
		ux, uy, uz = u.x, u.y, u.z
		ux2cos = ux*ux*cos_1
		uy2cos = uy*uy*cos_1
		uz2cos = uz*uz*cos_1
		uxycos = ux*uy*cos_1
		uyzcos = uy*uz*cos_1
		uxzcos = ux*uz*cos_1
		sin_ = sin(theta)
		uxsin = ux*sin_
		uysin = uy*sin_
		uzsin = uz*sin_

		Rx = Vector(cos_ + ux2cos, uxycos - uzsin, uxzcos + uysin)
		Ry = Vector(uxycos + uzsin, cos_ + uy2cos, uyzcos - uxsin)
		Rz = Vector(uxzcos - uysin, uyzcos + uxsin, cos_ + uz2cos)

		for v in self.vertices:
			v.x, v.y, v.z = v*Rx, v*Ry, v*Rz
		return

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

	def __getitem__(self, *args):
		return self.vertices.__getitem__(*args)[:2]

	def draw(self):
		turtle.up()
		turtle.goto(self[0])
		turtle.down()
		turtle.goto(self[3])
		turtle.goto(self[2])
		turtle.goto(self[0])
		turtle.goto(self[1])
		turtle.goto(self[2])
		turtle.goto(self[3])
		turtle.goto(self[1])
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
		
	def __getitem__(self, *args):
		return self.vertices.__getitem__(*args)[:2]

	def draw(self):
		turtle.up()
		turtle.goto(self[0])
		turtle.down()
		turtle.goto(self[1])
		turtle.goto(self[2])
		turtle.goto(self[3])
		turtle.goto(self[0])
		turtle.goto(self[7])
		turtle.goto(self[6])
		turtle.goto(self[5])
		turtle.goto(self[4])
		turtle.goto(self[7])
		turtle.goto(self[6])
		turtle.goto(self[1])
		turtle.goto(self[2])
		turtle.goto(self[5])
		turtle.goto(self[4])
		turtle.goto(self[3])	
		return

def main(shapes, rotations, theta, axes):
	turtle.tracer(False)
	axes = [1/abs(axis)*axis for axis in axes]
	stuff = zip(shapes, axes)
	for _ in xrange(rotations):
		start = time.clock()
		[shape.draw() for shape in shapes]
		[shape.rotate(theta, axis) for shape, axis in stuff]
		turtle.update()
		turtle.clear()
		sys.stdout.write("Frame rate: %3.2f frames/sec.\r" % (1/(time.clock() - start)))
		sys.stdout.flush()

def main_(shape, rotations, theta, axis):
	turtle.tracer(False)
	d = abs(axis)
	if d != 1:
		axis *= 1./d
	draw = shape.draw
	rotate = shape.rotate
	for _ in xrange(rotations):
		start = time.clock()
		draw()
		rotate(theta, axis)
		#turtle.up()
		#turtle.goto(0,0)
		#turtle.write(message, font=("Arial", 18, "normal"))
		#turtle.down()
		turtle.update()
		turtle.clear()
		sys.stdout.write("Frame rate: %3.2f frames/sec.\r" % (1/(time.clock() - start)))
		sys.stdout.flush()

if __name__=="__main__":
	#import cProfile
	#cubes = sum([[Cube([450-200*i,450-200*j,-100], 100) for i in range(5)] for j in range(5)], [])
	#main(cubes, pi/20, I+J)
	#main_(Tetrahedron([0,0,100], 200), 1000, pi/200, I+J+K)
	#cProfile.run("main_(Cube([100,100,100], 200), 1000, pi/200, I+J+K)")
	import random
	shapes = []
	axes = []
	for i in range(16):
		x = random.randrange(-400,400)
		y = random.randrange(-400,400)
		z = random.randrange(-400,400)
		side_length = random.randrange(200)
		if i&1:
			shapes.append(Tetrahedron([x,y,z], side_length))
		else:
			shapes.append(Cube([x,y,z], side_length))
		i = random.randrange(-5,5)
		j = random.randrange(-5,5)
		k = random.randrange(-10,10)
		axes.append(i*I+j*J+k*K)
	main(shapes, 2000, pi/200, axes)


	