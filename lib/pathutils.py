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


import os

import bpy

from .. import var


def get_asset_lib_path() -> str:
    wm_props = bpy.context.window_manager.jewelcraft
    return bpy.path.abspath(wm_props.asset_libs.active_item().path)


def get_weighting_lib_path() -> str:
    prefs = bpy.context.preferences.addons[var.ADDON_ID].preferences
    return bpy.path.abspath(prefs.weighting_lib_path)


def get_weighting_list_filepath(name) -> str:
    return os.path.join(get_weighting_lib_path(), name + ".json")
