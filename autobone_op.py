import bpy
from mathutils import Vector

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

# ------------------------------------------------------
# Action class
# ------------------------------------------------------
class CLS_OT_Operator(bpy.types.Operator):
    bl_idname = "bone.add_controller"
    bl_label = "Add"
    bl_description = "Create bone controllers"

    @classmethod
    def poll(cls, context):
        if context.active_bone is None:
            return False

        return True

    # ------------------------------
    # Create bone groups (POSE mode)
    # ------------------------------
    # noinspection PyMethodMayBeStatic
    def create_bone_groups(self, ob):
        bpy.ops.object.mode_set(mode='POSE')
        if 'Grp_In' in bpy.data.objects[ob.name].pose.bone_groups:
            grp_in = bpy.data.objects[ob.name].pose.bone_groups['Grp_In']
        else:
            grp_in = bpy.data.objects[ob.name].pose.bone_groups.new(name="Grp_In")
            grp_in.color_set = 'THEME03'  # Green

        if 'Grp_Out' in bpy.data.objects[ob.name].pose.bone_groups:
            grp_out = bpy.data.objects[ob.name].pose.bone_groups['Grp_Out']
        else:
            grp_out = bpy.data.objects[ob.name].pose.bone_groups.new(
                name="Grp_Out")
            grp_out.color_set = 'THEME01'  # Red

        bpy.ops.object.mode_set(mode='EDIT')

        return grp_in, grp_out

    # ------------------------------
    # Set bone groups
    # ------------------------------
    # noinspection PyMethodMayBeStatic
    def set_bone_group(self, ob, bone_name, grp):
        bpy.data.objects[ob.name].pose.bones[bone_name].bone_group = grp

    # ------------------------------
    # Create bone controllers
    # ------------------------------
    # noinspection PyMethodMayBeStatic
    def create_controllers(self, amt, main_bone, txt_a, txt_b, size_a, size_b,
                           bx, bz, roll):
        main_name = main_bone.name
        tail = main_bone.tail
        head = main_bone.head

        v1 = Vector((
            head[0] - tail[0],
            head[1] - tail[1],
            head[2] - tail[2],
        ))
        v1.normalize()

        # create controller A
        bone_a = amt.edit_bones.new(main_name + txt_a)
        bone_a.tail = head
        bone_a.head = (head[0] + (v1[0] * size_a), head[1] + (v1[1] * size_a),
                       head[2] + (v1[2] * size_a))
        bone_a.bbone_x = bx * 1.15
        bone_a.bbone_z = bz * 1.15
        bone_a.roll = roll

        # create controller B
        bone_b = amt.edit_bones.new(main_name + txt_b)
        bone_b.head = tail
        bone_b.tail = (tail[0] + (v1[0] * -size_b),
                       tail[1] + (v1[1] * -size_b),
                       tail[2] + (v1[2] * -size_b))
        bone_b.bbone_x = bx * 1.20
        bone_b.bbone_z = bz * 1.20
        bone_b.roll = roll

    # ------------------------------
    # Set custom shapes and segments
    # ------------------------------
    # noinspection PyMethodMayBeStatic
    def set_custom_shapes(self, context, ob, main_bone, main_name, txt_a,
                          txt_b):
        scene = context.scene
        # increase segments and set properties
        if type(main_bone).__name__ != "EditBone":
            bpy.ops.object.mode_set(mode='EDIT')

        bpy.data.objects[ob.name].data.edit_bones[
            main_bone.name].bbone_segments = scene.auto_bone_subdivisions

        # need set as object mode
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.object.mode_set(mode='OBJECT')
        b = ob.data.bones[main_name]
        b.bbone_custom_handle_start = ob.data.bones[main_name + txt_a]
        b.bbone_custom_handle_end = ob.data.bones[main_name + txt_b]
        
        b.bbone_handle_type_start = 'ABSOLUTE' 
        b.bbone_handle_type_end = 'ABSOLUTE' 

    # ------------------------------
    # Set lock and deform
    # ------------------------------
    # noinspection PyMethodMayBeStatic
    def set_lock_and_deform(self, context, main_name, ob, txt_a, txt_b):
        scene = context.scene
        bpy.ops.object.mode_set(mode='POSE')
        ma = bpy.data.objects[ob.name].pose.bones[main_name]
        # lock rot and scale
        ma.lock_rotation[0] = True
        ma.lock_rotation[1] = True
        ma.lock_rotation[2] = True
        if ma.rotation_mode == 'QUATERNION':
            ma.lock_rotation_w = True

        ma.lock_location[0] = True
        ma.lock_location[1] = True
        ma.lock_location[2] = True

        ba = bpy.data.objects[ob.name].pose.bones[main_name + txt_a]
        bb = bpy.data.objects[ob.name].pose.bones[main_name + txt_b]
        # disable deform
        ob.data.bones[main_name + txt_a].use_deform = False
        ob.data.bones[main_name + txt_b].use_deform = False
        
        if scene.auto_bone_list_a != "*NONE":
            ba.custom_shape = bpy.data.objects[scene.auto_bone_list_a]
            ba.custom_shape_scale_xyz = (scene.auto_bone_scale_a, scene.auto_bone_scale_a, scene.auto_bone_scale_a)

        if scene.auto_bone_list_b != "*NONE":
            bb.custom_shape = bpy.data.objects[scene.auto_bone_list_b]
            bb.custom_shape_scale_xyz = (scene.auto_bone_scale_b, scene.auto_bone_scale_b, scene.auto_bone_scale_b)

    # ------------------------------
    # Set constraintlock and deform
    # ------------------------------
    # noinspection PyMethodMayBeStatic
    def set_constraint(self, context, main_name, ob, txt_b):
        # flush modes to force recalc
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode='POSE')
        bpy.data.objects[ob.name].data.bones.active = bpy.data.objects[
            ob.name].pose.bones[main_name].bone
        # constraint
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.data.objects[ob.name].pose.bones[main_name].constraints[
            0].target = ob  # "Stretch To"
        context.object.pose.bones[main_name].constraints[
            0].subtarget = main_name + txt_b

    # ------------------------------
    # Set bone controllers
    # ------------------------------
    # noinspection PyMethodMayBeStatic
    def set_bone(self, context, ob, amt, main_bone, size_a, txt_a, size_b,
                 txt_b):
        scene = context.scene
        oldmode = ob.mode

        if oldmode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')

        main_name = main_bone.name
        # save main bone parent
        if bpy.data.armatures[amt.
                              name].edit_bones[main_name].parent is not None:
            main_parent = bpy.data.armatures[amt.name].edit_bones[
                main_name].parent.name
        else:
            main_parent = ""
        # get roll
        roll = bpy.data.armatures[amt.name].edit_bones[main_name].roll

        # get scale
        bx = bpy.data.armatures[amt.name].edit_bones[main_name].bbone_x
        bz = bpy.data.armatures[amt.name].edit_bones[main_name].bbone_z
        # create groups
        if scene.auto_bone_color is True:
            grp_in, grp_out = self.create_bone_groups(ob)

        # create controllers
        self.create_controllers(amt, main_bone, txt_a, txt_b, size_a, size_b,
                                bx, bz, roll)

        # increase segments and set properties
        self.set_custom_shapes(context, ob, main_bone, main_name, txt_a, txt_b)

        # set lock and deform
        self.set_lock_and_deform(context, main_name, ob, txt_a, txt_b)

        # set constraint
        self.set_constraint(context, main_name, ob, txt_b)

        # back to edit mode (need a flush)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')

        # parent bone with controller A
        parent_armature(amt, main_name + txt_a, main_name)

        # if original bone was parented, parent controllers
        if main_parent != "":
            parent_armature(amt, main_parent, main_name + txt_a)
            parent_armature(amt, main_parent, main_name + txt_b)

        # set bone groups
        if scene.auto_bone_color is True:
            # noinspection PyUnboundLocalVariable
            self.set_bone_group(ob, main_name + txt_a, grp_in)
            # noinspection PyUnboundLocalVariable
            self.set_bone_group(ob, main_name + txt_b, grp_out)

        # back to original mode
        bpy.ops.object.mode_set(mode=oldmode)

        return {'FINISHED'}

    # ------------------------------
    # Execute
    # ------------------------------
    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        scene = context.scene
        size_a = scene.auto_bone_size_a
        txt_a = scene.auto_bone_txt_a
        size_b = scene.auto_bone_size_b
        txt_b = scene.auto_bone_txt_b

        ob = context.object        

        # retry armature
        amt = ob.data
        # save the list of selected bones because the selection is missing when parent
        selbones = []
        if context.mode == "EDIT_ARMATURE":
            for bone in context.selected_bones:
                selbones.extend([bone])

        if context.mode == 'POSE':
            for bone in context.selected_pose_bones:
                selbones.extend([bone])

        # Loop
        for main_bone in selbones:
            self.set_bone(context, ob, amt, main_bone, size_a, txt_a, size_b,
                          txt_b)
        ob.data.display_type = 'BBONE'
        return {'FINISHED'}
