import turtle
from collections import namedtuple
from operator import mul
from math import sin, cos, pi, atan
turtle.tracer(False)
Point3D = namedtuple("Point3D", ["x", "y", "z", "tag"])
vertices = [Point3D(*junk) for junk in [map(lambda x: (1-2*bool(i&(1<<x)))*100, range(3))+[i] for i in range(8)]]
pairs = sum([[(vertex, other_vertex) for other_vertex in vertices[i+1:]] for i, vertex in enumerate(vertices)], [])
edges = map(lambda edge: [[u.x+200, u.y, u.z] for u in edge], filter(lambda vertex_pair: sum(map(int, bin(vertex_pair[0].tag^vertex_pair[1].tag)[2:]))==1, pairs))
def makePoint(data):
	return lambda cmd: data[0] if cmd=="x" else (data[1] if cmd=="y" else (data[2] if cmd=="z" else "undefined"))
def multiply(A, B):
	return map(lambda row: map(lambda column: sum(map(mul, row, column)), zip(*B)), A)
def rotate(point, xangle=0, yangle=0, zangle=0):
	x_matrix = [[1, 0, 0], [0, cos(xangle), -sin(xangle)],[0, sin(xangle), cos(xangle)]]
	y_matrix = [[cos(yangle), 0, sin(yangle)],[0, 1, 0],[-sin(yangle), 0, cos(yangle)]]
	z_matrix = [[cos(zangle), -sin(zangle), 0],[sin(zangle), cos(zangle), 0],[0, 0, 1]]
	return zip(*reduce(multiply, [x_matrix, y_matrix, z_matrix, zip(*point)]))
def draw_cube(edges):
	if edges==[]:
		turtle.update()
		return
	edge = edges.pop()
	turtle.up()
	turtle.goto(edge[0][:2])
	turtle.down()
	turtle.goto(edge[1][:2])
	return draw_cube(edges)
def animated_cube(cube, xstep, ystep, zstep):
	while True:
		draw_cube(cube[:])
		cube = [[rotate([point], xstep, ystep, zstep)[0] for point in edge] for edge in cube]
		turtle.clear()
animated_cube(edges, pi/2000, pi/2000, pi/2000)
turtle.mainloop()