# ##### BEGIN GPL LICENSE BLOCK #####
#
#  JewelCraft jewelry design toolkit for Blender.
#  Copyright (C) 2015-2020  Mikhail Rachinskiy
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


bl_info = {
    "name": "JewelCraft",
    "author": "Mikhail Rachinskiy",
    "version": (2, 8, 1),
    "blender": (2, 90, 0),
    "location": "3D View > Sidebar",
    "description": "Jewelry design toolkit.",
    "doc_url": "https://github.com/mrachinskiy/jewelcraft#readme",
    "tracker_url": "https://github.com/mrachinskiy/jewelcraft/issues",
    "category": "Object",
}


if "bpy" in locals():


    def reload_recursive(path, mods):
        import importlib

        for entry in os.scandir(path):

            if entry.is_file() and entry.name.endswith(".py") and not entry.name.startswith("__"):
                filename, _ = os.path.splitext(entry.name)

                if filename in mods:
                    importlib.reload(mods[filename])

            elif entry.is_dir() and not entry.name.startswith((".", "__")):

                if entry.name in mods:
                    importlib.reload(mods[entry.name])
                    reload_recursive(entry.path, mods[entry.name].__dict__)
                    continue

                reload_recursive(entry.path, mods)


    reload_recursive(var.ADDON_DIR, locals())
else:
    import os

    import bpy
    from bpy.props import PointerProperty

    from . import (
        var,
        ui,
        preferences,
        localization,
        mod_update,
        op_cutter,
        op_gem_map,
        op_microprong,
        op_design_report,
        op_prongs,
        op_distribute,
        ops_asset,
        ops_gem,
        ops_measurement,
        ops_object,
        ops_utils,
        ops_weighting,
    )
    from .lib import on_load


classes = (
    preferences.MeasurementCollection,
    preferences.MaterialCollection,
    preferences.AssetLibsCollection,
    preferences.SizeCollection,
    preferences.MeasurementsList,
    preferences.MaterialsList,
    preferences.AssetLibsList,
    preferences.SizeList,
    preferences.JewelCraftPreferences,
    preferences.WmProperties,
    preferences.SceneProperties,
    ui.VIEW3D_UL_jewelcraft_weighting_set,
    ui.VIEW3D_UL_jewelcraft_measurements,
    ui.VIEW3D_UL_jewelcraft_asset_libs,
    ui.VIEW3D_UL_jewelcraft_asset_libs_select,
    ui.VIEW3D_UL_jewelcraft_sizes,
    ui.VIEW3D_MT_jewelcraft,
    ui.VIEW3D_MT_jewelcraft_select_gem_by,
    ui.VIEW3D_MT_jewelcraft_asset_folder,
    ui.VIEW3D_MT_jewelcraft_weighting_set,
    ui.VIEW3D_MT_jewelcraft_weighting_mats,
    ui.VIEW3D_PT_jewelcraft_asset_libs,
    ui.VIEW3D_PT_jewelcraft_update,
    ui.VIEW3D_PT_jewelcraft_warning,
    ui.VIEW3D_PT_jewelcraft_gems,
    ui.VIEW3D_PT_jewelcraft_spacing_overlay,
    ui.VIEW3D_PT_jewelcraft_assets,
    ui.VIEW3D_PT_jewelcraft_jeweling,
    ui.VIEW3D_PT_jewelcraft_object,
    ui.VIEW3D_PT_jewelcraft_object_editmesh,
    ui.VIEW3D_PT_jewelcraft_curve,
    ui.VIEW3D_PT_jewelcraft_curve_editmesh,
    ui.VIEW3D_PT_jewelcraft_weighting,
    ui.VIEW3D_PT_jewelcraft_design_report,
    ui.VIEW3D_PT_jewelcraft_measurement,
    op_cutter.OBJECT_OT_cutter_add,
    op_gem_map.VIEW3D_OT_gem_map,
    op_microprong.OBJECT_OT_microprong_cutter_add,
    op_design_report.WM_OT_design_report,
    op_prongs.OBJECT_OT_prongs_add,
    op_distribute.OBJECT_OT_curve_distribute,
    op_distribute.OBJECT_OT_curve_redistribute,
    ops_asset.WM_OT_asset_folder_create,
    ops_asset.WM_OT_asset_folder_rename,
    ops_asset.WM_OT_asset_ui_refresh,
    ops_asset.WM_OT_asset_add,
    ops_asset.WM_OT_asset_remove,
    ops_asset.WM_OT_asset_rename,
    ops_asset.WM_OT_asset_replace,
    ops_asset.WM_OT_asset_preview_replace,
    ops_asset.WM_OT_asset_import,
    ops_asset.WM_OT_asset_favorite_add,
    ops_asset.WM_OT_asset_favorite_del,
    ops_asset.WM_OT_asset_menu,
    ops_gem.OBJECT_OT_gem_add,
    ops_gem.OBJECT_OT_gem_edit,
    ops_gem.OBJECT_OT_gem_recover,
    ops_gem.OBJECT_OT_gem_select_by_trait,
    ops_gem.OBJECT_OT_gem_select_overlapping,
    ops_measurement.WM_OT_ul_measurements_add,
    ops_measurement.WM_OT_ul_measurements_material_select,
    ops_object.CURVE_OT_size_curve_add,
    ops_object.CURVE_OT_length_display,
    ops_object.OBJECT_OT_stretch_along_curve,
    ops_object.OBJECT_OT_move_over_under,
    ops_object.OBJECT_OT_mirror,
    ops_object.OBJECT_OT_radial_instance,
    ops_object.OBJECT_OT_make_instance_face,
    ops_object.OBJECT_OT_lattice_project,
    ops_object.OBJECT_OT_lattice_profile,
    ops_object.OBJECT_OT_resize,
    ops_utils.SCENE_OT_ul_del,
    ops_utils.SCENE_OT_ul_clear,
    ops_utils.SCENE_OT_ul_move,
    ops_utils.WM_OT_ul_add,
    ops_utils.WM_OT_ul_del,
    ops_utils.WM_OT_ul_clear,
    ops_utils.WM_OT_ul_move,
    ops_utils.SCENE_OT_scene_units_set,
    ops_utils.WM_OT_goto_prefs,
    ops_utils.OBJECT_OT_overlay_override_add,
    ops_utils.OBJECT_OT_overlay_override_del,
    ops_weighting.WM_OT_ul_materials_add,
    ops_weighting.OBJECT_OT_weight_display,
    ops_weighting.WM_OT_weighting_set_add,
    ops_weighting.WM_OT_weighting_set_replace,
    ops_weighting.WM_OT_weighting_set_del,
    ops_weighting.WM_OT_weighting_set_rename,
    ops_weighting.WM_OT_weighting_set_refresh,
    ops_weighting.WM_OT_weighting_set_autoload_mark,
    ops_weighting.WM_OT_weighting_set_load,
    ops_weighting.WM_OT_weighting_set_load_append,
    mod_update.WM_OT_update_check,
    mod_update.WM_OT_update_download,
    mod_update.WM_OT_update_whats_new,
)


def register():
    if not os.path.exists(var.ICONS_DIR):
        integrity_check = FileNotFoundError("!!! READ INSTALLATION GUIDE !!!")
        raise integrity_check

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.jewelcraft = PointerProperty(type=preferences.WmProperties)
    bpy.types.Scene.jewelcraft = PointerProperty(type=preferences.SceneProperties)

    # Menu
    # ---------------------------

    bpy.types.VIEW3D_MT_object.append(ui.draw_jewelcraft_menu)

    # Translations
    # ---------------------------

    for k, v in mod_update.localization.init().items():
        if k in localization.DICTIONARY.keys():
            localization.DICTIONARY[k].update(v)
        else:
            localization.DICTIONARY[k] = v

    bpy.app.translations.register(__name__, localization.DICTIONARY)

    # On load
    # ---------------------------

    prefs = bpy.context.preferences.addons[__package__].preferences
    preferences.upd_asset_popover_width(prefs, None)

    on_load.handler_add()

    # mod_update
    # ---------------------------

    mod_update.init(
        addon_version=bl_info["version"],
        releases_url="https://api.github.com/repos/mrachinskiy/jewelcraft/releases",
    )


def unregister():
    import bpy.utils.previews
    from .lib import dynamic_list
    from .lib.view3d_lib import spacing_overlay

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.WindowManager.jewelcraft
    del bpy.types.Scene.jewelcraft

    # Menu
    # ---------------------------

    bpy.types.VIEW3D_MT_object.remove(ui.draw_jewelcraft_menu)

    # Translations
    # ---------------------------

    bpy.app.translations.unregister(__name__)

    # Previews
    # ---------------------------

    for pcoll in var.preview_collections.values():
        bpy.utils.previews.remove(pcoll)

    var.preview_collections.clear()
    dynamic_list._cache.clear()
    preferences._folder_cache.clear()

    # Handlers
    # ---------------------------

    spacing_overlay.handler_del()
    on_load.handler_del()


if __name__ == "__main__":
    register()
