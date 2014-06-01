import turtle
from math import sin, cos
from random import random as f

def rotate(points, angle, direction, point=(0,0,0)):
	#http://inside.mines.edu/~gmurray/ArbitraryAxisRotation/ .
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

def apply_perspective(points, camera_pos, viewer_pos):
	#http://en.wikipedia.org/wiki/3D_projection#Perspective_projection
	a, b, c = viewer_pos
	d, e, f = camera_pos
	for p in points:
		x, y, z = p
		x, y, z = x - d, y - e, z - f
		t4 = a/x
		yield (b - t4*y, c - t4*z)

def make_cube(p, s):
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
	a,b,c = camera
	faces = zip([[0,1,2,3],[0,7,4,3],[0,1,6,7],[2,5,4,3],[1,2,5,6],[5,6,7,4]], colors)
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

def draw_axis(camera, viewer):
	turtle.width(10)
	X, Y, Z, O = apply_perspective([(300,0,0),(0,300,0),(0,0,300),(0,0,0)],camera,viewer)
	turtle.color(1,0,0)
	turtle.up()
	turtle.goto(O)
	turtle.down()
	turtle.goto(X)
	turtle.goto(O)
	turtle.color(0,1,0)
	turtle.goto(Y)
	turtle.goto(O)
	turtle.color(0,0,1)
	turtle.goto(Z)
	turtle.goto(O)
	turtle.color(0,0,0)
	turtle.width(1)

def demo():
	turtle.title("3d cube demo") 
	cube = make_cube((100,100,100), 200)
	colors = [(f(),f(),f()) for _ in range(6)]
	turtle.tracer(0)
	x = 3**0.5 / 3
	axis = x, x, x
	camera = 500, 0, 0
	viewer = 550, 0, 0
	angle = 0.001
	while True:
		draw_axis(camera,viewer)
		draw_cube(cube,colors,camera,viewer)
		turtle.update()
		turtle.clear()
		rotate(cube, angle, axis)

if __name__ == "__main__":
	demo()
