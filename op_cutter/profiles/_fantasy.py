# ##### BEGIN GPL LICENSE BLOCK #####
#
#  JewelCraft jewelry design toolkit for Blender.
#  Copyright (C) 2015-2021  Mikhail Rachinskiy
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####


from typing import Tuple, List
from math import pi, tau, sin, cos

from bmesh.types import BMesh, BMVert


def _get_oval(detalization: int) -> List[Tuple[float, float, float]]:
    angle = -tau / detalization
    return [
        (
            sin(i * angle),
            cos(i * angle),
            0.0,
        )
        for i in range(detalization)
    ]


def _get_marquise(detalization: int, mul_1: float, mul_2: float) -> List[Tuple[float, float, float]]:
    res = detalization // 4 + 1
    angle = (pi / 2) / (res - 1)
    m1 = 1.0
    m2 = 1.0
    vs = []
    app = vs.append

    for i in range(res):
        x = sin(i * angle)
        y = cos(i * angle) * m1

        app((-x, y, 0.0))

        m1 *= (mul_1 * m2 - 1) / res + 1
        m2 *= mul_2 / res + 1

    for x, y, z in reversed(vs[:-1]):
        app((x, -y, z))

    for x, y, z in reversed(vs[1:-1]):
        app((-x, y, z))

    return vs


def _get_pear(detalization: int, mul_1: float, mul_2: float) -> List[Tuple[float, float, float]]:
    res = detalization + 1
    angle = pi / (res - 1)
    vs = []
    app = vs.append

    for i in range(res):
        x = sin(i * angle) * ((res - i) / res * mul_1) ** mul_2
        y = cos(i * angle)
        app((-x, y, 0.0))

    for x, y, z in reversed(vs[1:-1]):
        app((-x, y, z))

    return vs


def _get_heart(detalization: int, mul_1: float, mul_2: float, mul_3: float) -> List[Tuple[float, float, float]]:
    curve_resolution = detalization + 1
    angle = pi / (curve_resolution - 1)
    vs = []
    app = vs.append

    z = -mul_3
    m1 = -mul_1
    basis1 = curve_resolution / 5
    basis2 = curve_resolution / 12

    for i in range(curve_resolution):
        x = sin(i * angle)
        y = cos(i * angle) + m1 + 0.2
        app([-x, y, z])

        if m1 < 0.0:
            m1 -= m1 / basis1

        if z < 0.0:
            z -= z / basis2

    m2 = -mul_2
    basis = curve_resolution / 4

    for co in reversed(vs):
        if m2 < 0.0:
            co[1] += m2
            m2 -= m2 / basis

    for x, y, z in reversed(vs[1:-1]):
        app((-x, y, z))

    return vs


class Section:
    __slots__ = (
        "coords",
    )

    def __init__(self, operator) -> None:
        detalization = operator.detalization
        mul_1 = operator.mul_1
        mul_2 = operator.mul_2
        mul_3 = operator.mul_3

        if operator.cut == "MARQUISE":
            self.coords = _get_marquise(detalization, mul_1, mul_2)
        elif operator.cut == "PEAR":
            self.coords = _get_pear(detalization, mul_1, mul_2)
        elif operator.cut == "HEART":
            self.coords = _get_heart(detalization, mul_1, mul_2, mul_3)
        else:
            self.coords = _get_oval(detalization)

    def add(self, bm: BMesh, size, co_fmt=lambda a, b: b) -> Tuple[List[BMVert], List[BMVert]]:
        vs1 = []
        vs2 = []
        app1 = vs1.append
        app2 = vs2.append

        for x, y, z in self.coords:
            app1(bm.verts.new((x * size.x, y * size.y, size.z1)))
            app2(bm.verts.new((x * size.x, y * size.y, co_fmt(z, size.z2))))

        return vs1, vs2

    def add_preserve_z2(self, bm: BMesh, size) -> Tuple[List[BMVert], List[BMVert]]:
        return self.add(bm, size, co_fmt=lambda a, b: a - b)
