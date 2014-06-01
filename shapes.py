import turtle
from math import sin, cos
from random import random as f

def rotate(points, angle, direction, point=(0,0,0)):
	"""Points is collection of 3-tuples, angle is an amount to rotate in
	radians, direction is a 3-tuple representing a direction vector, and
	point is a 3-tuple representing a point the vector d passes through."""
	#this function is based on a heavily refactored version of the math found
	#at http://inside.mines.edu/~gmurray/ArbitraryAxisRotation/ .
	#I refactored it to make heavy precomputation easier.
	#This is to make the 3d animations as fast as possible (turtle isn't
	#the best when it comes to speed.)
	a, b, c = point
	u, v, w = direction
	c0, s = cos(angle), sin(angle)
	c1 = 1 - c0
	u2, v2, w2 = u*u, v*v, w*w
	au, bv, cw = a*u, b*v, c*w

	x1, x2 = c1*(a*(v2 + w2) - u*(bv + cw)) + s*(b*w - c*v), u*c1
	y1, y2 = c1*(b*(w2 + u2) - v*(cw + au)) + s*(c*u - a*w), v*c1
	z1, z2 = c1*(c*(u2 + v2) - w*(au + bv)) + s*(a*v - b*u), w*c1

	for i, p in enumerate(points):
		x, y, z = p
		dotp = u*x + v*y + w*z
		x_ = x1 + x2*dotp + x*c0 + s*(v*z - w*y)
		y_ = y1 + y2*dotp + y*c0 + s*(w*x - u*z)
		z_ = z1 + z2*dotp + z*c0 + s*(u*y - v*x)
		points[i] = (x_, y_, z_)

	return

def apply_perspective(points, camera_pos, viewer_pos):
	#computes the projection of 3d points onto 2d space (the y/z plane)
	#based on math found at
	#http://en.wikipedia.org/wiki/3D_projection#Perspective_projection
	a, b, c = viewer_pos
	d, e, f = camera_pos
	#cx, cy, cz = map(cos, orientation)
	#sx, sy, sz = map(sin, orientation)
	for p in points:
		x, y, z = p
		x, y, z = x - d, y - e, z - f
		#szy, czx, cyz, czy = sz*y, cz*x, cy*z, cz*y
		#t1, t2 = cyz + sy*(szy - czx), czy - sz*x
		#x_ = cy*(szy+czx) - sy*z
		#y_ = sx*t1 + cx*t2
		#z_ = cx*t1 - sx*t2
		t4 = a/x
		yield (b - t4*y, c - t4*z)

def make_cube(p, s):
	"""p is the upper right (your right) front corner, s is side length"""
	points = []
	add = points.append
	x, y ,z = p
	xs, ys, zs = x - s, y - s, z - s
	add(p)
	add((x, y, zs))
	add((x, ys, zs))
	add((x, ys, z))
	add((xs, ys, z))
	add((xs, ys, zs))
	add((xs, y, zs))
	add((xs, y, z))
	return points

def draw_cube(cube, colors, camera, viewer):
	"""Uses the camera position to decide which order to paint the faces.
	Each face is treated as being as far away from the camera as the average
	of the distances of each of it's vertices."""
	a,b,c = camera
	faces = zip([[0,1,2,3],[0,7,4,3],[0,1,6,7],[2,5,4,3],[1,2,5,6],[5,6,7,4]], colors)
	#print cube
	d = [((a-x)**2 + (b-y)**2 + (c-z)**2)**0.5 for (x,y,z) in cube]
	ps = list(apply_perspective(cube, camera, viewer))
	faces.sort(key=lambda ((r,s,t,u),v): (d[r]+d[s]+d[t]+d[u])/4, reverse=True)
	for face, color in faces:
		r,s,t,u = face
		turtle.fillcolor(color)
		turtle.up()
		turtle.goto(ps[r])
		turtle.down()
		turtle.fill(True)
		turtle.goto(ps[s])
		turtle.goto(ps[t])
		turtle.goto(ps[u])
		turtle.goto(ps[r])
		turtle.fill(False)
	return

def demo():
	turtle.title("3d cube demo") 
	cube = make_cube((200,200,200), 200)
	colors = [(f(),f(),f()) for _ in range(6)]
	turtle.tracer(0)
	x = 3**0.5 / 3
	axis = x, x, x
	camera = 500, 200, 200
	viewer = 550, 200, 200
	#orientation = 0, 0, 0
	angle = 0.001
	while True:
		draw_cube(cube,colors,camera,viewer)
		turtle.update()
		turtle.clear()
		rotate(cube, angle, axis)

if __name__ == "__main__":
	demo()

