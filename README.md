# Turtle3D
Turtle 3D is designed to be a 3D extension of the python turtle module. It is very limited as far as 3D renderers go, but can be useful for simple 3D modeling.

Effort was made to make this feel as much like the original turtle module as possible, and many functions simply point to the original turtle module. However, due
to the nature of the approach used and the difficulty of expanding some features to the third dimension, some of the original functions do not exist, and some occasional
visual defects do occur. Plans are to continue expanding this module to include more of the functionality the was present in the original turtle module, and hopefully remove
the visual defects, although some of these pose particularly difficult challenges. Suggestions or solutions are welcome.

# Installation

```
pip install turtle3D
```

# Examples
The following example shows a demonstration of creating a 3D cube, and then animating its rotation by calling the rotation functions repeatedly.

```
import time
from turtle3D import Turtle3D

def connect(t: Turtle3D, point1, point2):
    """Helper function to draw a connecting line between 2 points"""

    start = t.pos()
    d = t.isdown()
    t.penup()
    t.goto(point1)
    t.pendown()
    t.goto(point2)
    t.penup()
    t.goto(start)
    if d:
        t.pendown()

def draw_axes(t: Turtle3D):
    """Helper function to draw the x,y, and z axes in different colors to help visualize where they are"""

    t.pencolor("blue")
    t.goto(500, 0, 0)
    t.write("X")
    t.goto(-500, 0, 0)
    t.write("-X")
    t.home()
    t.pencolor("red")
    t.goto(0, 500, 0)
    t.write("Y")
    t.goto(0, -500, 0)
    t.write("-Y")
    t.home()
    t.pencolor("green")
    t.goto(0, 0, 500)
    t.write("Z")
    t.goto(0, 0, -500)
    t.write("-Z")
    t.home()
    t.pencolor("black")

def run(t: Turtle3D):
    """Main function to handle our drawing and animation"""

    # here we define the eight points that make up the corners of our cube
    points = [
        [50, -50, -50],  # bottom-right-front
        [50, 50, -50],  # top-right-front
        [-50, 50, -50],  # top-left-front
        [-50, -50, -50],  # bottom-left-front
        [50, -50, 50],  # bottom-right-back
        [50, 50, 50],  # top-right-back
        [-50, 50, 50],  # top-left-back
        [-50, -50, 50],  # bottom-left-back
    ]

    # connecting each of the points to the other points it needs to
    for i in range(4):
        connect(t, points[i], points[(i + 1) % 4])
        connect(t, points[i + 4], points[((i + 1) % 4) + 4])
        connect(t, points[i], points[i + 4])


    # animating 2 degree rotations of each axis 10,000 times
    angle = 2
    for i in range(10000):

        t.rotateX(angle, False) # False because we don't want to redraw the lines until the final rotation
        t.rotateY(angle, False)
        t.rotateZ(angle)

        time.sleep(1 / 60) # so we are redrawing 60 times per second. not exactly equal to 60fps due draw times, but pretty close.


if __name__ == "__main__":
    t = Turtle3D()
    s = t.getscreen()

    draw_axes(t) # comment out this line for smoother animation

    run(t)
    s.exitonclick()

```
# API Reference

Since many of these functions point to or expand on the original turtle functions, view
https://docs.python.org/3/library/turtle.html for more information.

#### Turtle3D.position()
#### Turtle3D.pos()
returns the current x,y,z coordinates of the turtle


#### Turtle3D.setpos(x: float | List[], y: float = None, z: float = None) -> None
#### Turtle3D.setposition(x: float | List[], y: float = None, z: float = None) -> None
#### Turtle3D.goto(x: float | List[], y: float = None, z: float = None) -> None
moves turtle to (x,y,z)


#### Turtle3D.fd(distance: float) -> None
#### Turtle3D.forward(distance: float) -> None
moves the turtle distance pixels in the direction it is currently heading


#### Turtle3D.back(distance: float) -> None
#### Turtle3D.backward(distance: float) | Turtle3D.bk() -> None
moves the turtle distance pixels in the opposite direction of its current heading


#### Turtle3D.rt(angle: float) -> None
#### Turtle3D.right(angle: float) -> None
turns the turtle clockwise by angle degrees in the XY plane


#### Turtle3D.lt(angle: float) -> None
#### Turtle3D.left(angle: float) -> None
turns the turtle counterclockwise by angle degrees in the XY plane


#### Turtle3D.seth(XY_angle: float, Z_angle: float = None) -> None
#### Turtle3D.setheading(XY_angle: float, Z_angle: float = None) -> None
set the turtle's current heading to be XY_angle in the XY plane, and Z_angle in the XZ plane


#### Turtle3D.clone()
returns a copy of the turtle with the same heading, position, pensize, fillcolor, and pencolor.


#### Turtle3D.heading()
returns the turtle's current heading, XY_angle in the XY plane, and Z_angle in the XZ plane


#### Turtle3D.stamp()
creates an imprint of the turtle at the current location. This will appear the same shape no matter how the axes are rotated.

returns an id for the stamp created


#### Turtle3D.clearstamps(n: int = None) -> None
Delete all or first/last n of turtle's stamps.

Optional argument   n -- an integer

If n is None, delete all of pen's stamps, else if n > 0 delete first n stamps else if n < 0 delete last n stamps.


#### Turtle3D.clearstamp(stampid: int) -> None
clears stamp with given stampid


#### Turtle3D.yup(angle: float) -> None
turns the turtle counterclockwise in the XZ plane by angle degrees


#### Turtle3D.ydown(angle: float) -> None
turns the turtle clockwise in the XZ plane by angle degrees


#### Turtle3D.xup(angle: float) -> None
turns the turtle counterclockwise in the YZ plane by angle degrees


#### Turtle3D.xdown(angle: float) -> None
turns the turtle clockwise in the YZ plane by angle degrees

#### Turtle3D.reset() -> None
Delete the turtle's drawings from the screen, re-center the turtle and set variables to the default values.


#### Turtle3D.clear() -> None
Delete the turtle's drawings from the screen. Do not move turtle. State and position of the turtle as well as drawings of other turtles are not affected.


#### Turtle3D.xcor() -> float
returns the current X-coordinate of the turtle in the 3D space


#### Turtle3D.ycor() -> float
returns the current Y-coordinate of the turtle in the 3D space


#### Turtle3D.zcor() -> float
returns the current Z-coordinate of the turtle in the 3D space


#### Turtle3D.setx(x: float) -> None
moves the turtle to the given x-position. y and z positions remain unchanged


#### Turtle3D.sety(y: float) -> None
moves the turtle to the given y-position. x and z positions remain unchanged


#### Turtle3D.setz(z: float) -> None
moves the turtle to the given z-position. x and y positions remain unchanged


#### Turtle3D.undo() -> None
undoes the last command and removes it from the redraw buffer


#### Turtle3D.dot() -> None
Points to turtle.dot()
Due to the 3d nature of the drawing, the dot at this location will appear as an orb in 3d space.


#### Turtle3D.write() -> None
puts the given text on the screen at the current location. text changes position when axes are rotated, but does not itself rotate (i.e. the letter 'E' will always display as an 'E', it will not become skewed or flattened if rotated)


#### Turtle3D.home() -> None
moves the turtle to (0, 0, 0)


#### Turtle3D.rotateZ(angle: float, redraw=True) -> None
rotate the XY plane angle degrees about the Z axis and redraws the canvas from the new canvas perspective.

if redraw is set to False, the redraw phase is skipped. new lines will be drawn from the new perspective,
but on the next redraw all lines will change to the new perspective. setting this to False is only recommended
when doing multiple rotations at once, so that the canvas only needs to be redrawn from the final rotation of
perspective.


#### Turtle3D.rotateX(angle: float, redraw=True) -> None
rotate the YZ plane angle degrees about the X axis and redraws the canvas from the new canvas perspective.

if redraw is set to False, the redraw phase is skipped. new lines will be drawn from the new perspective,
but on the next redraw all lines will change to the new perspective. setting this to False is only recommended
when doing multiple rotations at once, so that the canvas only needs to be redrawn from the final rotation of
perspective.


#### Turtle3D.rotateY(angle: float, redraw=True) -> None
rotate the XZ plane angle degrees about the Y axis and redraws the canvas from the new canvas perspective.

if redraw is set to False, the redraw phase is skipped. new lines will be drawn from the new perspective,
but on the next redraw all lines will change to the new perspective. setting this to False is only recommended
when doing multiple rotations at once, so that the canvas only needs to be redrawn from the final rotation of
perspective.


#### Turtle3D.begin_fill() -> None
points to turtle.begin_fill()


#### Turtle3D.end_fill() -> None
points to turtle.end_fill()


#### Turtle3D.filling() -> bool
points to turtle.filling()


#### Turtle3D.ht() -> None
#### Turtle3D.hideturtle() -> None
points to turtle.hideturtle()


#### Turtle3D.st() -> None
#### Turtle3D.showturtle() -> None
points to turtle.showturtle()


#### Turtle3D.isvisible() -> bool
points to turtle.isvisible()


#### Turtle3D.shape()
points to turtle.shape()


#### Turtle3D.pu() -> None
#### Turtle3D.penup() -> None
#### Turtle3D.up() -> None
points to turtle.penup()


#### Turtle3D.pd() -> None
#### Turtle3D.down() -> None
#### Turtle3D.pendown() -> None
points to turtle.pendown()


#### Turtle3D.width()
#### Turtle3D.pensize()
points to turtle.pensize()


#### Turtle3D.isdown()
points to turtle.isdown()


#### Turtle3D.onclick()
points to turtle.onclick()


#### Turtle3D.onrelease()
points to turtle.onrelease()


#### Turtle3D.ondrag()
points to turtle.ondrag()


#### Turtle3D.speed()
points to turtle.speed()


#### Turtle3D.getscreen()
points to turtle.getscreen()


#### Turtle3D.pencolor()
points to turtle.pencolor()


#### Turtle3D.color()
points to turtle.color()


#### Turtle3D.fillcolor()
points to turtle.fillcolor()
