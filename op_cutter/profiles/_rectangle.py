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

import bmesh
from bmesh.types import BMesh, BMVert

from ...lib import mesh


def _add_rect(bm: BMesh, x: float, y: float, z: float) -> List[BMVert]:
    return [
        bm.verts.new(co)
        for co in (
            ( x,  y, z),
            (-x,  y, z),
            (-x, -y, z),
            ( x, -y, z),
        )
    ]


def _add_rect_bevel(
    bm: BMesh,
    x: float,
    y: float,
    z: float,
    bv_width: float,
    bv_type: str,
    bv_segments: int,
    bv_profile: float,
) -> List[BMVert]:
    bm_temp = bmesh.new()
    vs = _add_rect(bm_temp, x, y, z)
    bm_temp.faces.new(vs)

    bmesh.ops.bevel(
        bm_temp,
        geom=vs,
        affect="VERTICES",
        clamp_overlap=True,
        offset=bv_width,
        offset_type=bv_type,
        segments=bv_segments,
        profile=bv_profile,
    )

    f = next(iter(bm_temp.faces))
    verts = [bm.verts.new(v.co) for v in f.verts]
    bm_temp.free()
    return verts


class Section:
    __slots__ = (
        "bv_width",
        "bv_type",
        "bv_segments",
        "bv_profile",
        "add",
    )

    def __init__(self, operator) -> None:
        if operator.shape_rect:
            self.bv_type = "OFFSET"
            self.bv_width = operator.bevel_corners_width
        else:
            self.bv_type = "PERCENT"
            self.bv_width = operator.bevel_corners_percent
        self.bv_segments = operator.bevel_corners_segments
        self.bv_profile = operator.bevel_corners_profile

        if self.bv_width:
            self.add = self._add_bevel
        else:
            self.add = self._add

    @staticmethod
    def _add(bm: BMesh, size) -> Tuple[List[BMVert], List[BMVert]]:
        s1 = _add_rect(bm, size.x, size.y, size.z1)
        s2 = [bm.verts.new((*v.co.xy, size.z2)) for v in s1]
        return s1, s2

    def _add_bevel(self, bm: BMesh, size) -> Tuple[List[BMVert], List[BMVert]]:
        s1 = _add_rect_bevel(
            bm,
            size.x,
            size.y,
            size.z1,
            self.bv_width,
            self.bv_type,
            self.bv_segments,
            self.bv_profile,
        )
        s2 = [bm.verts.new((*v.co.xy, size.z2)) for v in s1]
        return s1, s2

    @staticmethod
    def add_seat_rect(bm, girdle_verts, Girdle, Hole) -> None:
        scale_y = Hole.y / (Girdle.y or Hole.y)
        vs = [bm.verts.new((v.co.x, v.co.y * scale_y, Hole.z1)) for v in girdle_verts]
        es = mesh.connect_verts(bm, vs)
        mesh.bridge_verts(bm, girdle_verts, vs)

        es1 = []
        es2 = []
        app1 = es1.append
        app2 = es2.append

        for e in es:
            v1, v2 = e.verts
            if v1.co.y > 0.0 and v2.co.y > 0.0:
                app1(e)
            elif v1.co.y < 0.0 and v2.co.y < 0.0:
                app2(e)

        bmesh.ops.collapse(bm, edges=es1)
        bmesh.ops.collapse(bm, edges=es2)
