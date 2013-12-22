import turtle
import time
from vector import Vector
from math import pi, cos, sin

I, J, K = Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)

PATHS = (3, 1, 0, 2, 3, 7, 6, 4, 5, 7), (2, 6), (0, 4), (1, 5) 

class Cube(object):
	def __init__(self, start_point, side_length):
		self.vertices = []
		append = self.vertices.append
		start_point = Vector(*(start_point))
		for i in range(8):
			x, y, z = (i&4)>>2, (i&2)>>1, i&1
			point = Vector(x, y, z)
			point *= side_length 
			point -= start_point
			append(point)
		self.i = start_point - side_length*(I+J+K)
		self.i = 1.0/abs(self.i)*self.i

	def __getitem__(self, *args):
		return self.vertices.__getitem__(*args)[:2]

	def rotate(self, theta, u=None):
		if u==None:
			u = self.i
		if abs(u) != 1:
			u *= 1.0/abs(u)
		cos_ = cos(theta)
		cos_1 = 1 - cos_
		ux2cos = u.x**2*cos_1
		uy2cos = u.y**2*cos_1
		uz2cos = u.y**2*cos_1
		uxycos = u.x*u.y*cos_1
		uyzcos = u.y*u.z*cos_1
		uxzcos = u.x*u.z*cos_1
		sin_ = sin(theta)
		uxsin = u.x*sin_
		uysin = u.y*sin_
		uzsin = u.z*sin_

		Rx = Vector(cos_ + ux2cos, uxycos - uzsin, uxzcos + uysin)
		Ry = Vector(uxycos + uzsin, cos_ + uy2cos, uyzcos - uxsin)
		Rz = Vector(uxzcos - uysin, uyzcos + uxsin, cos_ + uz2cos)

		for v in self.vertices:
			v.x, v.y, v.z = v*Rx, v*Ry, v*Rz
		return

	def draw(self):
		turtle.up()
		turtle.goto(self[3])
		turtle.down()
		turtle.goto(self[1])
		turtle.goto(self[0])
		turtle.goto(self[2])
		turtle.goto(self[3])
		turtle.goto(self[7])
		turtle.goto(self[6])
		turtle.goto(self[4])
		turtle.goto(self[5])
		turtle.goto(self[7])
		turtle.up()
		turtle.goto(self[2])
		turtle.down()
		turtle.goto(self[6])
		turtle.up()
		turtle.goto(self[0])
		turtle.down()
		turtle.goto(self[4])
		turtle.up()
		turtle.goto(self[1])
		turtle.down()
		turtle.goto(self[5])
		return

def main(cubes, theta):
	turtle.tracer(False)
	while True:
		start = time.clock()
		[cube.draw() for cube in cubes]
		[cube.rotate(theta) for cube in cubes]
		message = "Frame rate: %3.2f frames/sec." % (1/(time.clock() - start))
		turtle.up()
		turtle.goto(0,0)
		turtle.write(message, font=("Arial", 18, "normal"))
		turtle.down()
		turtle.update()
		turtle.clear()

if __name__=="__main__":
	cubes = sum([[Cube([450-200*i,450-200*j,-100], 100) for i in range(5)] for j in range(5)], [])
	main(cubes, pi/200)