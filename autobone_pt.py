import bpy

# ------------------------------------------------------
# UI Class
# ------------------------------------------------------
class CLS_PT_Panel(bpy.types.Panel):
    bl_idname = "CLS_PT_Panel   "
    bl_label = "Auto Bone Controller"
    bl_category = "Rigging"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        o = context.object
        if o:
            if o.mode == "EDIT":
                if o.type == "ARMATURE":
                    return True

        return False

    # ------------------------------
    # Draw UI
    # ------------------------------
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        o = context.object
        row = layout.row(align=False)
        row.operator("bone.add_controller", icon='GROUP_BONE')
        row = layout.row(align=False)
        row.prop(scene, "auto_bone_subdivisions", text="Bone Segments")

        row = layout.row()
        box = row.box()
        box.label(text="Controller A")
        box.prop(scene, "auto_bone_txt_a", text="Subfix")
        box.prop(scene, "auto_bone_size_a", text="Size")
        box.prop(scene, "auto_bone_list_a", text="Shape")
        box.prop(scene, "auto_bone_scale_a", text="Scale")

        row = layout.row()
        box = row.box()
        box.label(text="Controller B")
        box.prop(scene, "auto_bone_txt_b", text="Subfix")
        box.prop(scene, "auto_bone_size_b", text="Size")
        box.prop(scene, "auto_bone_list_b", text="Shape")
        box.prop(scene, "auto_bone_scale_b", text="Scale")

        row = layout.row(align=False)
        row.prop(scene, "auto_bone_color", text="Use color for controllers")

        amt = context.object.data
        if o.mode == "EDIT":
            active_bone = amt.edit_bones.active
        elif o.mode == "POSE":
            active_bone = context.active_bone
        else:
            active_bone = None

        if active_bone:
            row = layout.row(align=False)
            row.label(text="Active Bone: " + active_bone.name)

            if active_bone.name.endswith("_In") or active_bone.name.endswith(
                    "_Out"):
                row = layout.row(align=False)
                row.label(text=
                    "Selected bone looks a bone controller", icon="ERROR")