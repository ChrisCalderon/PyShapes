from operator import add, mul

class Vector(object):
	def __init__(self, x, y, z):
		self.data = [x, y, z]

	@property
	def x(self):
	    return self[0]
	@x.setter
	def x(self, value):
	    self[0] = value

	@property
	def y(self):
		return self[1]

	@y.setter
	def y(self, value):
		self[1] = value

	@property
	def z(self):
	    return self[2]

	@z.setter
	def z(self, value):
	    self[2] = value

	def __getitem__(self, *args):
		return self.data.__getitem__(*args)

	def __setitem__(self, *args):
		return self.data.__setitem__(*args)

	def __iter__(self):
		return iter(self.data)

	def __str__(self):
		return "<{}, {}, {}>".format(self.x, self.y, self.z)

	def __repr__(self):
		return "Vector(x={}, y={}, z={})".format(self.x, self.y, self.z)

	def __add__(self, other):
		if isinstance(other, Vector):
			return Vector(*map(add, self, other))
		return Vector(self.x+other, self.y+other, self.z+other)

	def __mul__(self, other):
		return sum(map(mul, self, other))

	def __sub__(self, other):
		return self + -other

	def __neg__(self):
		return -1*self
		
	def __radd__(self, other):
		return self + other

	def __rmul__(self, other):
		return Vector(self.x*other, self.y*other, self.z*other)

	def __rsub__(self, other):
		return other + -self

	def __iadd__(self, other):
		if isinstance(other, Vector):
			self.x += other.x
			self.y += other.y
			self.z += other.z
			return self
		self.x += other
		self.y += other
		self.z += other
		return self

	def __imul__(self, other):
		if isinstance(other, (int, float, complex)):
			self.x *= other
			self.y *= other
			self.z *= other
			return self

	def __isub__(self, other):
		if isinstance(other, Vector):
			self.x -= other.x
			self.y -= other.y
			self.z -= other.z
			return self
		self.x -= other
		self.y -= other
		self.z -= other
		return self

	def __abs__(self):
		return (self*self)**0.5
