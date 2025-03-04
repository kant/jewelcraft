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

from bpy.types import Operator
from bpy.props import StringProperty

from .. import var
from ..lib import data, dynamic_list, pathutils


class WM_OT_weighting_list_save(Operator):
    bl_label = "Save To File"
    bl_description = "Save material list to file"
    bl_idname = "wm.jewelcraft_weighting_list_save"
    bl_options = {"INTERNAL"}

    list_name: StringProperty(name="File Name", options={"SKIP_SAVE"})

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.separator()
        layout.alert = not self.list_name
        layout.prop(self, "list_name")
        layout.separator()

    def execute(self, context):
        if not self.list_name:
            self.report({"ERROR"}, "Name must be specified")
            return {"CANCELLED"}

        lib_path = pathutils.get_weighting_lib_path()
        filepath = pathutils.get_weighting_list_filepath(self.list_name)

        if not os.path.exists(lib_path):
            os.makedirs(lib_path)

        data.weighting_list_serialize(filepath)
        dynamic_list.weighting_lib_refresh()

        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class WM_OT_weighting_list_save_as(Operator):
    bl_label = "Save As"
    bl_description = "Save material list as existing file"
    bl_idname = "wm.jewelcraft_weighting_list_save_as"
    bl_options = {"INTERNAL"}

    list_name: StringProperty(options={"SKIP_SAVE", "HIDDEN"})

    def execute(self, context):
        filepath = pathutils.get_weighting_list_filepath(self.list_name)
        if os.path.exists(filepath):
            data.weighting_list_serialize(filepath)
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)


class WM_OT_weighting_list_del(Operator):
    bl_label = "Remove"
    bl_description = "Remove file"
    bl_idname = "wm.jewelcraft_weighting_list_del"
    bl_options = {"INTERNAL"}

    list_name: StringProperty(options={"SKIP_SAVE", "HIDDEN"})

    def execute(self, context):
        filepath = pathutils.get_weighting_list_filepath(self.list_name)
        if os.path.exists(filepath):
            os.remove(filepath)
        dynamic_list.weighting_lib_refresh()
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)


class WM_OT_weighting_list_import(Operator):
    bl_label = "Import"
    bl_description = "Import materials from file"
    bl_idname = "wm.jewelcraft_weighting_list_import"
    bl_options = {"INTERNAL"}

    load_id: StringProperty(options={"SKIP_SAVE", "HIDDEN"})

    def execute(self, context):
        data.weighting_list_deserialize(self.load_id)
        context.area.tag_redraw()
        return {"FINISHED"}


class WM_OT_weighting_list_set_default(Operator):
    bl_label = "Set Default"
    bl_description = "Import materials from default list when new scene is created"
    bl_idname = "wm.jewelcraft_weighting_list_set_default"
    bl_options = {"INTERNAL"}

    load_id: StringProperty(options={"SKIP_SAVE", "HIDDEN"})

    def execute(self, context):
        prefs = context.preferences.addons[var.ADDON_ID].preferences
        prefs.weighting_default_list = self.load_id
        context.preferences.is_dirty = True
        dynamic_list.weighting_lib_refresh()
        return {"FINISHED"}


class WM_OT_weighting_ui_refresh(Operator):
    bl_label = "Refresh"
    bl_description = "Refresh asset UI"
    bl_idname = "wm.jewelcraft_weighting_ui_refresh"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        dynamic_list.weighting_lib_refresh()
        return {"FINISHED"}
