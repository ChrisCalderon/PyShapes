import turtle
import time
import sys
from vector import Vector
from math import pi, cos, sin

I, J, K = Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)

class Shape(object):
	def __init__(self, start_point, *args):
		self._make_vertices(start_point, *args)

	def _make_vertices(self, start_point, *args):
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

class Cube(Shape):
	def __init__(self, start_point, side_length):
		"""start_point is the fron upper right (your right) corner of the cube."""
		Shape.__init__(self, start_point, side_length)

	def _make_vertices(self, start_point, side_length):
		vertices = []
		append = vertices.append
		start_point = Vector(*(start_point))
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

def main(cubes, theta, axis=None):
	turtle.tracer(False)
	while True:
		start = time.clock()
		[cube.draw() for cube in cubes]
		[cube.rotate(theta, axis) for cube in cubes]
		message = "Frame rate: %3.2f frames/sec." % (1/(time.clock() - start))
		turtle.up()
		turtle.goto(0,0)
		turtle.write(message, font=("Arial", 18, "normal"))
		turtle.down()
		turtle.update()
		turtle.clear()

def main_(cube, rotations, theta, axis=None):
	turtle.tracer(False)
	d = abs(axis)
	if d != 1:
		axis *= 1./d
	for _ in xrange(rotations):
		start = time.clock()
		cube.draw()
		cube.rotate(theta, axis)
		message = "Frame rate: %3.2f frames/sec.\r" % (1/(time.clock() - start))
		print message,
		sys.stdout.flush()
		#turtle.up()
		#turtle.goto(0,0)
		#turtle.write(message, font=("Arial", 18, "normal"))
		#turtle.down()
		turtle.update()
		turtle.clear()

if __name__=="__main__":
	#cubes = sum([[Cube([450-200*i,450-200*j,-100], 100) for i in range(5)] for j in range(5)], [])
	#main(cubes, pi/20, I+J)
	main_(Cube([100,100,100], 200), 1000, pi/200, I+J+K)
	