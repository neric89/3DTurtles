from __future__ import annotations
import turtle
from turtle import Screen
from typing import Tuple
import numpy as np
import math

# def _go(self, distance):
#     """move turtle forward by specified distance"""
#     ende = self._position + self._orient * distance
#     self._goto(ende)

# def _rotate(self, angle):
#     """Turn turtle counterclockwise by specified angle if angle > 0."""
#     angle *= self._degreesPerAU
#     self._orient = self._orient.rotate(angle)

# def heading(self):
#     """ Return the turtle's current heading.

#     No arguments.

#     Example (for a Turtle instance named turtle):
#     >>> turtle.left(67)
#     >>> turtle.heading()
#     67.0
#     """
#     x, y = self._orient
#     result = round(math.atan2(y, x)*180.0/math.pi, 10) % 360.0
#     result /= self._degreesPerAU
#     return (self._angleOffset + self._angleOrient*result) % self._fullcircle

# def setheading(self, to_angle):
#     """Set the orientation of the turtle to to_angle.

#     Aliases:  setheading | seth

#     Argument:
#     to_angle -- a number (integer or float)

#     Set the orientation of the turtle to to_angle.
#     Here are some common directions in degrees:

#      standard - mode:          logo-mode:
#     -------------------|--------------------
#        0 - east                0 - north
#       90 - north              90 - east
#      180 - west              180 - south
#      270 - south             270 - west

#     Example (for a Turtle instance named turtle):
#     >>> turtle.setheading(90)
#     >>> turtle.heading()
#     90
#     """
#     angle = (to_angle - self.heading())*self._angleOrient
#     full = self._fullcircle
#     angle = (angle+full/2.)%full - full/2.
#     self._rotate(angle)


class INum:
    def __init__(self, num):
        if isinstance(num, INum) or isinstance(num, JNum) or isinstance(num, KNum):
            self.__num = num.coef()
        elif isinstance(num, int) or isinstance(num, float):
            self.__num = num
        else:
            try:
                self.__num = float(num)
            except ValueError:
                raise TypeError("num must be of a numeric type")

    def __mul__(self, other):
        if isinstance(other, INum):
            return -1 * self.coef() * other.coef()
        if isinstance(other, JNum):
            return KNum(self.coef() * other.coef())
        if isinstance(other, KNum):
            return JNum(-1 * self.coef() * other.coef())
        if isinstance(other, Quaternion):
            return Quaternion(0, self.coef(), 0, 0) * other
        if isinstance(other, int) or isinstance(other, float):
            return INum(self.coef() * other)
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, INum):
            return INum(self.coef() + other.coef())
        if isinstance(other, KNum):
            return Quaternion(0, self, 0, other)
        if isinstance(other, JNum):
            return Quaternion(0, self, other, 0)
        if isinstance(other, float) or isinstance(other, int):
            return Quaternion(other, self, 0, 0)
        if isinstance(other, Quaternion):
            return Quaternion(other[0], other[1].coef() + self.coef(), other[2], other[3])
        return NotImplemented

    def __neg__(self):
        return INum(-self.coef())

    def __sub__(self, other):
        return self + (-other)

    def coef(self):
        return self.__num

    def __repr__(self) -> str:
        return f"{self.coef()}i"

    def __rmul__(self, other):
        return self * other

    def __eq__(self, other):
        if isinstance(other, INum):
            return self.__num == other.__num
        return False

    def __truediv__(self, other):
        if type(other) not in (INum, JNum, KNum, Quaternion, float, int):
            return NotImplemented
        if isinstance(other, float) or isinstance(other, int):
            return INum(self.__num / other)
        return self * (1 / other)

    def __rtruediv__(self, other):
        if type(other) not in (INum, JNum, KNum, Quaternion, float, int):
            return NotImplemented
        if isinstance(other, float) or isinstance(other, int):
            return -INum(other / self.__num)
        return other * (1 / self)

    def __round__(self, ndigits):
        return INum(round(self.__num, ndigits))

    def __abs__(self):
        return abs(self.coef())

    def __format__(self, spec: str) -> str:
        return f"{self.__num.__format__(spec)}i"


class JNum:
    def __init__(self, num):
        if isinstance(num, INum) or isinstance(num, JNum) or isinstance(num, KNum):
            self.__num = num.coef()
        elif isinstance(num, int) or isinstance(num, float):
            self.__num = num
        else:
            try:
                self.__num = float(num)
            except ValueError:
                raise TypeError("num must be of a numeric type")

    def __mul__(self, other):
        if isinstance(other, JNum):
            return -1 * self.coef() * other.coef()
        if isinstance(other, INum):
            return KNum(-1 * self.coef() * other.coef())
        if isinstance(other, KNum):
            return INum(self.coef() * other.coef())
        if isinstance(other, Quaternion):
            return Quaternion(0, 0, self.coef(), 0) * other
        if isinstance(other, int) or isinstance(other, float):
            return JNum(self.coef() * other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __add__(self, other):
        if isinstance(other, JNum):
            return JNum(self.coef() + other.coef())
        if isinstance(other, INum):
            return Quaternion(0, other, self, 0)
        if isinstance(other, KNum):
            return Quaternion(0, 0, self, other)
        if isinstance(other, float) or isinstance(other, int):
            return Quaternion(other, 0, self, 0)
        if isinstance(other, Quaternion):
            return Quaternion(other[0], other[1], other[2].coef() + self.coef(), other[3])
        return NotImplemented

    def __neg__(self):
        return JNum(-self.coef())

    def __sub__(self, other):
        return self + (-other)

    def coef(self):
        return self.__num

    def __repr__(self) -> str:
        return f"{self.coef()}j"

    def __eq__(self, other):
        if isinstance(other, JNum):
            return self.__num == other.__num
        return False

    def __round__(self, ndigits):
        return JNum(round(self.__num, ndigits))

    def __truediv__(self, other):
        if type(other) not in (INum, JNum, KNum, Quaternion, float, int):
            return NotImplemented
        if isinstance(other, float) or isinstance(other, int):
            return JNum(self.__num / other)
        return self * (1 / other)

    def __rtruediv__(self, other):
        if type(other) not in (INum, JNum, KNum, Quaternion, float, int):
            return NotImplemented
        if isinstance(other, float) or isinstance(other, int):
            return -JNum(other / self.__num)
        return other * (1 / self)

    def __abs__(self):
        return abs(self.coef())

    def __format__(self, spec: str) -> str:
        return f"{self.__num.__format__(spec)}j"


class KNum:
    def __init__(self, num):
        if isinstance(num, INum) or isinstance(num, JNum) or isinstance(num, KNum):
            self.__num = num.coef()
        elif isinstance(num, int) or isinstance(num, float):
            self.__num = num
        else:
            try:
                self.__num = float(num)
            except ValueError:
                raise TypeError("num must be of a numeric type")

    def __mul__(self, other):
        if isinstance(other, KNum):
            return -1 * self.coef() * other.coef()
        if isinstance(other, JNum):
            return INum(-1 * self.coef() * other.coef())
        if isinstance(other, INum):
            return JNum(self.coef() * other.coef())
        if isinstance(other, Quaternion):
            return Quaternion(0, 0, 0, self.coef()) * other
        if isinstance(other, int) or isinstance(other, float):
            return KNum(self.coef() * other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __add__(self, other):
        if isinstance(other, KNum):
            return KNum(self.coef() + other.coef())
        elif isinstance(other, INum):
            return Quaternion(0, other, 0, self)
        elif isinstance(other, JNum):
            return Quaternion(0, 0, other, self)
        elif isinstance(other, float) or isinstance(other, int):
            return Quaternion(other, 0, 0, self)
        if isinstance(other, Quaternion):
            return Quaternion(other[0], other[1], other[2], other[3].coef() + self.coef())
        return NotImplemented

    def __round__(self, ndigits):
        return KNum(round(self.__num, ndigits))

    def __neg__(self):
        return KNum(-self.coef())

    def __sub__(self, other):
        return self + (-other)

    def coef(self):
        return self.__num

    def __repr__(self) -> str:
        return f"{self.coef()}k"

    def __eq__(self, other):
        if isinstance(other, KNum):
            return self.__num == other.__num
        return False

    def __truediv__(self, other):
        if type(other) not in (INum, JNum, KNum, Quaternion, float, int):
            return NotImplemented
        if isinstance(other, float) or isinstance(other, int):
            return KNum(self.__num / other)
        return self * (1 / other)

    def __rtruediv__(self, other):
        if type(other) not in (INum, JNum, KNum, Quaternion, float, int):
            return NotImplemented
        if isinstance(other, float) or isinstance(other, int):
            return -KNum(other / self.__num)
        return other * (1 / self)

    def __abs__(self):
        return abs(self.coef())

    def __format__(self, spec: str) -> str:
        return f"{self.__num.__format__(spec)}k"


class Quaternion(tuple):
    def __new__(cls, x, i, j, k):
        return tuple.__new__(cls, (x, INum(i), JNum(j), KNum(k)))

    def __add__(self, other):
        if isinstance(other, KNum):
            other = Quaternion(0, 0, 0, other)
        elif isinstance(other, JNum):
            other = Quaternion(0, 0, other, 0)
        elif isinstance(other, INum):
            other = Quaternion(0, other, 0, 0)

        if isinstance(other, Quaternion):
            return Quaternion(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])
        elif isinstance(other, float) or isinstance(other, int):
            return Quaternion(self[0] + other, self[1], self[2], self[3])
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, KNum):
            other = Quaternion(0, 0, 0, other)
        elif isinstance(other, JNum):
            other = Quaternion(0, 0, other, 0)
        elif isinstance(other, INum):
            other = Quaternion(0, other, 0, 0)

        if isinstance(other, Quaternion):
            x = (
                self[0] * other[0]
                - self[1].coef() * other[1].coef()
                - self[2].coef() * other[2].coef()
                - self[3].coef() * other[3].coef()
            )
            i = (
                self[1].coef() * other[0]
                + self[0] * other[1].coef()
                + self[2].coef() * other[3].coef()
                - self[3].coef() * other[2].coef()
            )
            j = (
                self[0] * other[2].coef()
                - self[1].coef() * other[3].coef()
                + self[2].coef() * other[0]
                + self[3].coef() * other[1].coef()
            )
            k = (
                self[0] * other[3].coef()
                + self[1].coef() * other[2].coef()
                - self[2].coef() * other[1].coef()
                + self[3].coef() * other[0]
            )
            return Quaternion(x, i, j, k)
        elif isinstance(other, float) or isinstance(other, int):
            return Quaternion(self[0] * other, self[1] * other, self[2] * other, self[3] * other)
        return NotImplemented

    def conjugate(self):
        return Quaternion(self[0], -self[1], -self[2], -self[3])

    def norm(self):
        return math.sqrt(self[0] ** 2 + self[1].coef() ** 2 + self[2].coef() ** 2 + self[3].coef() ** 2)

    def inverse(self):
        return self.conjugate() / (self.norm() ** 2)

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return (1 / other) * self

        if isinstance(other, KNum):
            other = Quaternion(0, 0, 0, other)
        elif isinstance(other, JNum):
            other = Quaternion(0, 0, other, 0)
        elif isinstance(other, INum):
            other = Quaternion(0, other, 0, 0)

        if isinstance(other, Quaternion):
            return self * other.inverse()
        return NotImplemented

    def __rtruediv__(self, other):
        if type(other) not in (INum, JNum, KNum, Quaternion, float, int):
            return NotImplemented
        return other * self.inverse()

    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Quaternion(self[0] * other, self[1] * other, self[2] * other, self[3] * other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, KNum):
            other = Quaternion(0, 0, 0, other)
        elif isinstance(other, JNum):
            other = Quaternion(0, 0, other, 0)
        elif isinstance(other, INum):
            other = Quaternion(0, other, 0, 0)

        if isinstance(other, Quaternion):
            return Quaternion(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])
        elif isinstance(other, float) or isinstance(other, int):
            return Quaternion(self[0] - other, self[1], self[2], self[3])
        return NotImplemented

    def __neg__(self):
        return Quaternion(-self[0], -self[1], -self[2], -self[3])

    def __getnewargs__(self):
        return (self[0], self[1].coef(), self[2].coef(), self[3].coef())

    def __repr__(self):
        return f"({self[0]:.2f}, {self[1]:.2f}, {self[2]:.2f}, {self[3]:.2f})"

    def __eq__(self, other):
        if isinstance(other, Quaternion):
            if self[0] == other[0] and self[1] == other[1] and self[2] == other[2] and self[3] == other[3]:
                return True
        return False

    def __abs__(self):
        return self.norm()

    def __round__(self, ndigits=None):
        return Quaternion(
            round(self[0], ndigits),
            round(self[1].coef(), ndigits),
            round(self[2].coef(), ndigits),
            round(self[3].coef(), ndigits),
        )

    def rotate(self, angle):
        s = math.sin(angle)
        return Quaternion(math.cos(angle) * self[0], s * self[1], s * self[2], s * self[3])


class Turtle3D:
    def __init__(self):
        self.__t = turtle.Turtle()

        default_angle = math.radians(0)
        self.__z_angle = default_angle
        self.__x_angle = default_angle
        self.__y_angle = default_angle

        self.__projection_matrix = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        self.__queue = []

        self.__coordinates = (0, 0, 0)
        self.__orientation = (1.0, 0, 0)

        self.begin_fill = self.__t.begin_fill
        self.end_fill = self.__t.end_fill
        self.filling = self.__t.filling

        self.ht = self.__t.ht
        self.hideturtle = self.ht
        self.st = self.__t.st
        self.showturtle = self.st
        self.isvisible = self.__t.isvisible

        self.shape = self.__t.shape

        self.pu = self.penup
        self.up = self.penup
        self.pd = self.pendown
        self.down = self.pendown

        self.width = self.pensize
        self.isdown = self.__t.isdown

        self.onclick = self.__t.onclick
        self.onrelease = self.__t.onrelease
        self.ondrag = self.__t.ondrag

        self.position = self.pos
        self.setpos = self.goto
        self.setposition = self.goto

        self.fd = self.forward
        self.back = self.backward
        self.bk = self.backward
        self.rt = self.right
        self.lt = self.left

        self.seth = self.setheading

        self.speed = self.__t.speed

        self.getscreen = self.__t.getscreen
        self.update = turtle.update

    def clone(self) -> Turtle3D:
        t = Turtle3D()
        t.__t = self.__t.clone()
        t.__z_angle = self.__z_angle
        t.__x_angle = self.__x_angle
        t.__y_angle = self.__y_angle
        t.__projection_matrix = self.__projection_matrix
        t.__queue = self.__queue
        t.__coordinates = self.__coordinates
        t.__orientation = self.__orientation

        return t

    def heading(self) -> Tuple[float, float]:
        x, y, z = self.__orientation
        rho = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        phi = math.asin(z / rho)  # z_angle, radians
        theta = math.atan2(y, x)
        return (math.degrees(theta), math.degrees(phi))

    def setheading(self, XY_angle, Z_angle=None) -> None:
        if isinstance(XY_angle, tuple) or isinstance(XY_angle, list):
            XY_angle, Z_angle = XY_angle
        angleXY, angleZ = self.heading()
        to_XY = ((XY_angle - angleXY) + 180) % 360 - 180
        to_Z = ((Z_angle - angleZ) + 180) % 360 - 180

        self.__rotate_Z(to_XY)
        self.__rotate_X(to_Z)

    def stamp(self) -> int:
        stamp_id = self.__t.stamp()
        self.__queue.append({"action": f"stamp_{stamp_id}", "function": self.stamp, "args": []})
        return stamp_id

    # def circle(self, radius, extent=None, steps=None, axis=None):
    #     pass

    def clearstamps(self, n: int = None) -> None:
        assert (n is None) or (type(n) == int), "n must be of type int or NoneType."
        tbd = []
        if n is None:
            for idx, item in enumerate(self.__queue):
                if item["action"][:5] == "stamp":
                    tbd.append(idx)
        elif n >= 0:
            count = 0
            for idx, item in enumerate(self.__queue):
                if count == n:
                    break
                if item["action"][:5] == "stamp":
                    count += 1
                    tbd.append(idx)
        else:
            lim = abs(n)
            count = 0
            for i in range(len(self.__queue) - 1, -1, -1):
                item = self.__queue[i]
                if count == lim:
                    break
                if item["action"][:5] == "stamp":
                    count += 1
                    tbd.append(i)

            tbd.reverse()

        tbd.reverse()
        for i in tbd:
            del self.__queue[i]

        self.__t.clearstamps(n)

    def clearstamp(self, stamp_id: int) -> None:
        assert type(stamp_id) == int, "stamp_id must be an integer!"
        stamp_index = None
        for idx, item in enumerate(self.__queue):
            if item["action"] == f"stamp_{stamp_id}":
                stamp_index = idx
                break
        if stamp_index is not None:
            self.__t.clearstamp(stamp_id)
            del self.__queue[stamp_index]

    def yup(self, angle: float) -> None:
        self.__rotate_X(angle)

    def ydown(self, angle: float) -> None:
        self.__rotate_X(-angle)

    def xup(self, angle: float) -> None:
        self.__rotate_Y(angle)

    def xdown(self, angle: float) -> None:
        self.__rotate_Y(-angle)

    def left(self, angle: float) -> None:
        self.__rotate_Z(angle)

    def right(self, angle: float) -> None:
        self.__rotate_Z(-angle)

    def __rotate_Z(self, angle) -> None:
        angle = math.radians(angle)
        q_start = Quaternion(1, 0, 0, 1)
        self.__orientation = self.__quaternion_rotation(self.__orientation, q_start, angle)

    def __rotate_Y(self, angle) -> None:
        angle = math.radians(angle)
        q_start = Quaternion(1, 0, 1, 0)
        self.__orientation = self.__quaternion_rotation(self.__orientation, q_start, angle)

    def __rotate_X(self, angle) -> None:
        angle = math.radians(angle)
        q_start = Quaternion(1, 1, 0, 0)
        self.__orientation = self.__quaternion_rotation(self.__orientation, q_start, angle)

    def forward(self, distance: float) -> None:
        self.__go(distance)

    def backward(self, distance: float) -> None:
        self.__go(-distance)

    def __go(self, distance) -> None:
        q_coord = Quaternion(0, *self.__coordinates)
        q_orient = Quaternion(0, *self.__orientation)
        q_to = q_orient * distance
        q_end = q_to + q_coord
        endpoint = tuple(i.coef() for i in q_end[1:])
        self.goto(endpoint)

    def pencolor(self, *args) -> turtle._AnyColor | None:
        self.__queue.append({"action": "pencolor", "function": self.pencolor, "args": args})
        return self.__t.pencolor(*args)

    def color(self, *args) -> Tuple | None:
        self.__queue.append({"action": "color", "function": self.color, "args": args})
        return self.__t.color(*args)

    def fillcolor(self, *args) -> turtle._AnyColor | None:
        self.__queue.append({"action": "fillcolor", "function": self.fillcolor, "args": args})
        return self.__t.fillcolor(*args)

    def pensize(self, *args) -> int | None:
        self.__queue.append({"action": "pensize", "function": self.pensize, "args": args})
        return self.__t.pensize(*args)

    def pendown(self) -> None:
        self.__t.pendown()
        self.__queue.append({"action": "pendown", "function": self.pendown, "args": []})

    def penup(self) -> None:
        self.__t.penup()
        self.__queue.append({"action": "penup", "function": self.penup, "args": []})

    def reset(self) -> None:
        self.__t.reset()
        self.__queue = []
        self.__coordinates = (0, 0, 0)

    def clear(self) -> None:
        self.__t.clear()
        self.__queue = []

    def xcor(self) -> float:
        return self.__coordinates[0]

    def ycor(self) -> float:
        return self.__coordinates[1]

    def zcor(self) -> float:
        return self.__coordinates[2]

    def setx(self, x: float) -> None:
        assert type(x) in (float, int), "X value must be numeric!"
        self.goto(x, self.__coordinates[1], self.__coordinates[2])

    def sety(self, y: float) -> None:
        assert type(y) in (float, int), "Y value must be numeric!"
        self.goto(self.__coordinates[0], y, self.__coordinates[2])

    def setz(self, z: float) -> None:
        assert type(z) in (float, int), "Z value must be numeric!"
        self.goto(self.__coordinates[0], self.__coordinates[1], z)

    def undo(self) -> None:
        ## the turtle undo() function does the following:
        #
        # if action == "rot":
        #     angle, degPAU = data
        #     self._rotate(-angle*degPAU/self._degreesPerAU)
        #     dummy = self.undobuffer.pop()
        # elif action == "stamp":
        #     stitem = data[0]
        #     self.clearstamp(stitem)
        # elif action == "go":
        #     self._undogoto(data)
        # elif action in ["wri", "dot"]:
        #     item = data[0]
        #     self.screen._delete(item)
        #     self.items.remove(item)
        # elif action == "dofill":
        #     item = data[0]
        #     self.screen._drawpoly(item, ((0, 0),(0, 0),(0, 0)),
        #                           fill="", outline="")
        # elif action == "beginfill":
        #     item = data[0]
        #     self._fillitem = self._fillpath = None
        #     if item in self.items:
        #         self.screen._delete(item)
        #         self.items.remove(item)
        # elif action == "pen":
        #     TPen.pen(self, data[0])
        #     self.undobuffer.pop()
        if len(self.__queue) > 0 and self.__t.undobufferentries() > 0:
            self.__queue.pop()

        self.__t.undo()

    def dot(self, *args) -> None:
        self.__queue.append({"function": self.dot, "action": "dot", "args": args})
        self.__t.dot(*args)

    def write(self, *args) -> None:
        self.__queue.append({"function": self.write, "action": "write", "args": args})
        self.__t.write(*args)

    def home(self) -> None:
        self.goto(0, 0, 0)

    def pos(self) -> Tuple[float, float, float]:
        return self.__coordinates

    def rotateZ(self, angle, redraw=True) -> None:  # XY
        assert type(angle) in (float, int), "Angle must be a numeric value!"

        self.__z_angle += math.radians(angle)
        if redraw:
            self.__redraw()

    def rotateX(self, angle, redraw=True) -> None:  # YZ
        assert type(angle) in (float, int), "Angle must be a numeric value!"

        self.__x_angle += math.radians(angle)
        if redraw:
            self.__redraw()

    def rotateY(self, angle, redraw=True) -> None:  # XZ
        assert type(angle) in (float, int), "Angle must be a numeric value!"

        self.__y_angle += math.radians(angle)
        if redraw:
            self.__redraw()

    def goto(self, x, y=None, z=None) -> None:
        if type(x) in [list, tuple, np.ndarray]:
            assert len(x) == 3, f"Incorrect number of points, expected 3 (x, y, and z), got: {x}"
            try:
                x, y, z = float(x[0]), float(x[1]), float(x[2])
            except:
                assert 1 == 2, "X, Y, and Z values must be numerical!"

        assert (
            type(x) in (int, float) and type(y) in (int, float) and type(z) in (int, float)
        ), "X, Y, and Z values must be numerical!"

        self.__coordinates = (x, y, z)
        self.__queue.append({"function": self.goto, "action": "goto", "args": [x, y, z]})

        point = np.array([x, y, z])

        rotated = self.__quaternion_z_rotation(point)
        rotated = self.__quaternion_y_rotation(rotated)
        rotated = self.__quaternion_x_rotation(rotated)

        point_2D = self.__projection_matrix.dot(rotated)

        self.__t.goto(point_2D)

    def __quaternion_z_rotation(self, point) -> Tuple[float, float, float]:
        q_start = Quaternion(1, 0, 0, 1)
        return self.__quaternion_rotation(point, q_start, self.__z_angle)

    def __quaternion_y_rotation(self, point) -> Tuple[float, float, float]:
        q_start = Quaternion(1, 0, 1, 0)
        return self.__quaternion_rotation(point, q_start, self.__y_angle)

    def __quaternion_x_rotation(self, point) -> Tuple[float, float, float]:
        q_start = Quaternion(1, 1, 0, 0)
        return self.__quaternion_rotation(point, q_start, self.__x_angle)

    def __quaternion_rotation(self, point, q_start, angle) -> Tuple[float, float, float]:
        angle = angle / 2
        q_end = q_start.rotate(-angle)
        q_start = q_start.rotate(angle)

        quaternion_point = Quaternion(0, point[0], point[1], point[2])

        qpoint = q_start * quaternion_point
        qpoint = qpoint * q_end

        coords = (qpoint[1].coef(), qpoint[2].coef(), qpoint[3].coef())
        return coords

    def __redraw(self) -> None:
        s = turtle.speed()
        turtle.speed(0)
        turtle.tracer(False)
        q = [*self.__queue]
        self.__queue = []

        self.clear()
        self.__coordinates = (0, 0, 0)
        # self.__t.dot(1, "white")
        for i in q:
            i["function"](*i["args"])

        turtle.update()
        turtle.tracer(True)
        turtle.speed(s)


if __name__ == "__main__":
    ## This just runs a demo which draws and rotates the x, y, and z axes, as well as a cube

    def connect(t: Turtle3D, point1, point2):
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

    def run(t: Turtle3D):
        # t.fillcolor("blue")

        points = [
            [50, -50, -50],  # b_right front
            [50, 50, -50],  # t_right front
            [-50, 50, -50],  # t_left front
            [-50, -50, -50],  # b_left front
            [50, -50, 50],  # b_right back
            [50, 50, 50],  # t_right back
            [-50, 50, 50],  # t_left back
            [-50, -50, 50],  # b_left back
        ]

        for i in range(4):
            connect(t, points[i], points[(i + 1) % 4])
            connect(t, points[i + 4], points[((i + 1) % 4) + 4])
            connect(t, points[i], points[i + 4])

        for i in range(10000):
            angle = 2

            t.rotateX(angle, False)
            t.rotateY(angle, False)
            t.rotateZ(angle)

    def draw_axes(t: Turtle3D):
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

    def draw_sphere(t: Turtle3D) -> None:
        t.pensize(5)
        radius = 360 / (2 * math.pi)
        t.up()
        t.home()
        t.rt(90)
        t.fd(radius)
        t.lt(90)
        t.down()
        t.color("green")
        for _ in range(360):
            t.fd(1)
            t.lt(1)
        t.up()
        t.goto(0, 0, radius)
        t.down()
        t.color("blue")
        for _ in range(360):
            t.fd(1)
            t.xup(1)
        t.up()
        t.goto(0, 0, -radius)
        t.down()
        t.lt(90)
        t.color("red")
        for _ in range(360):
            t.fd(1)
            t.yup(1)
        t.up()
        t.home()

    t = Turtle3D()
    s = Screen()
    t.speed(0)

    h = t.heading()

    t.home()
    t.seth(h)

    draw_axes(t)

    run(t)
    s.exitonclick()
