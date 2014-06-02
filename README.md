PyShapes
==========

Simple 3d graphics in python.

To see a demo, run `python shapes.py` in a terminal (or console if you are in Windows). If you have the `pygame` module installed, then you can run `python shapes_pygame.py` file, ~~which is about twice as fast on my MacBook Pro.~~ *EDIT*: I haven't rewritten the pygame code in a long time, there are bound to be bugs in it's old demo, and the demo is not nearly as pretty as the shapes.py one.

####TODO:
- [ ] **Switch to using a plain Tkinter canvas instead of turtle!**
- [ ] Replace the face ordering function with something that uses the distance to the berycenter or centroid of a face. [This page](http://en.wikipedia.org/wiki/Centroid#Of_triangle_and_tetrahedron) should help.
- [ ] Generalize the '''draw_cube''' function in a function that takes a list, a camera position, and a viewer position as arguments. The list argument should contain a list of points as it's first element, a list of of lists of points that represent the faces as the second element, and a list of colors, one for each face, as the last element.
- [ ] Rewrite '''make_cube''' so that it returns a list like the one expected '''draw_cube'''
- [ ] Implement a function like make_cube, but for tetrahedrons instead.
- [ ] Perspective projection onto an arbitrary plane, [more info here](http://www.ecse.rpi.edu/~wrf/Research/Short_Notes/homogeneous.html) and [here](http://tutorial.math.lamar.edu/Classes/CalcII/EqnsOfPlanes.aspx).
  - [ ] Fix perspective projection to work with a camera orientation vector.

If you can think of any other features that would be cool just let me know!
