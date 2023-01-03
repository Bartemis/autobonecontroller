# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Auto Bone Controller",
    "author": "Antonio Vazquez (antonioya)",
    "version": (2, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Properties",
    "description": "Add controllers for bendy bones automatically",
    "category": "3D View"
}
import bpy
from mathutils import Vector

# ------------------------------------------------------
# Load combox objects
# ------------------------------------------------------
# noinspection PyUnusedLocal
def combobox_object_callback(scene, context):
    items = []
    i = 0
    i += 1
    items.append(("*NONE", "No custom shape", "No custom shape", "OBJECT", i))
    for obj in context.scene.objects:
        if obj.type in ('MESH', 'EMPTY'):
            i += 1
            items.append((obj.name, obj.name, "Select this object", "OBJECT",
                          i))
    return items


# --------------------------------------------------------------------
# Parent armature (keep positions)
# --------------------------------------------------------------------
def parent_armature(armature, parentobj, childobj):
    for mybone in armature.edit_bones:
        mybone.select = False

    parent = armature.edit_bones[parentobj]
    child = armature.edit_bones[childobj]
    armature.edit_bones.active = parent

    parent.select = True
    child.select = True
    bpy.ops.armature.parent_set(type='OFFSET')

from . autobone_op import CLS_OT_Operator
from . autobone_pt import CLS_PT_Panel

# ------------------------------------------------------
# Registration
# ------------------------------------------------------
def register():
    bpy.utils.register_class(CLS_OT_Operator)
    bpy.utils.register_class(CLS_PT_Panel)
    # Define properties
    bpy.types.Scene.auto_bone_subdivisions = bpy.props.IntProperty(
        name='Div',
        min=1,
        max=25,
        default=10,
        description='Number total of subdivisions')

    bpy.types.Scene.auto_bone_txt_a = bpy.props.StringProperty(
        name="Subfix",
        maxlen=48,
        description="Subfix added to first controler bone",
        default="_In")
    bpy.types.Scene.auto_bone_txt_b = bpy.props.StringProperty(
        name="Subfix",
        maxlen=48,
        description="Subfix added to second controler bone",
        default="_Out")

    bpy.types.Scene.auto_bone_size_a = bpy.props.FloatProperty(
        name='Size',
        min=0,
        max=100,
        default=0.2,
        precision=3,
        description="Controller size factor")
    bpy.types.Scene.auto_bone_size_b = bpy.props.FloatProperty(
        name='Size',
        min=0,
        max=100,
        default=0.2 ,
        precision=3,
        description="Controller size factor")

    bpy.types.Scene.auto_bone_list_a = bpy.props.EnumProperty(
        items=combobox_object_callback,
        name="Object",
        description="List of available objects")

    bpy.types.Scene.auto_bone_list_b = bpy.props.EnumProperty(
        items=combobox_object_callback,
        name="Object",
        description="List of available objects")
    bpy.types.Scene.auto_bone_scale_a = bpy.props.FloatProperty(
        name='Scale',
        min=0.1,
        max=25,
        default=1.0,
        precision=3,
        description="Custom shape scale")
    bpy.types.Scene.auto_bone_scale_b = bpy.props.FloatProperty(
        name='Scale',
        min=0.1,
        max=25,
        default=1.0,
        precision=3,
        description="Custom shape scale")
    bpy.types.Scene.auto_bone_color = bpy.props.BoolProperty(
        name="Color",
        description="Use color groups for controllers",
        default=True)


def unregister():
    bpy.utils.unregister_class(CLS_OT_Operator)
    bpy.utils.unregister_class(CLS_PT_Panel)

    del bpy.types.Scene.auto_bone_subdivisions
    del bpy.types.Scene.auto_bone_txt_a
    del bpy.types.Scene.auto_bone_size_a
    del bpy.types.Scene.auto_bone_list_a
    del bpy.types.Scene.auto_bone_scale_a

    del bpy.types.Scene.auto_bone_txt_b
    del bpy.types.Scene.auto_bone_size_b
    del bpy.types.Scene.auto_bone_list_b
    del bpy.types.Scene.auto_bone_scale_b

    del bpy.types.Scene.auto_bone_color


if __name__ == "__main__":
    register()
