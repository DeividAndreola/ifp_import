import bpy
import os

from bpy.props import StringProperty, CollectionProperty, BoolProperty, BoolVectorProperty, EnumProperty, IntProperty

BLOPT_REGISTER = {'REGISTER', 'UNDO', 'INTERNAL'}

class OperatorInitGTATools(bpy.types.Operator):
    bl_idname = "gta_utils.init_gta_tools"
    bl_label = "Initialize GTA Tools"
    bl_description = "Revert \"GTA Tools\" Properties to Initial Settings"
    bl_options = BLOPT_REGISTER

    prop: StringProperty(
        default="")  ## Acceptable Strings are "dff_props", "ifp_props", "map_props", "weight_props", "util_props"

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)

        props = []
        if "" != self.prop:
            props.append(self.prop)

        from . import gta_utils
        gta_utils.init_tool_props(self.prop)
        gta_tools.show_msg_fin()
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)


class GTA_IFP_AnimProps(bpy.types.PropertyGroup):
    @classmethod
    def register(GTA_IFP_AnimProps):
        GTA_IFP_AnimProps.name = StringProperty(
            name="Anim Name",
            description="",
            default="")


class GTA_IFP_Props(bpy.types.PropertyGroup):
    @classmethod
    def register(GTA_IFP_Props):
        ## For Animation List in UI
        GTA_IFP_Props.anims = CollectionProperty(
            type=GTA_IFP_AnimProps,
            name="IFP Anims",
            description="")

        ## for Import
        GTA_IFP_Props.filepath = StringProperty(
            name="IFP File Path",
            description="Full Path Name of target IFP",
            default="")

        GTA_IFP_Props.ifp_name = StringProperty(
            name="IFP Name",
            description="Internal IFP Name",
            default="")

        GTA_IFP_Props.show_import_options = BoolProperty(
            name="Show Import Options",
            description="Show Import Options",
            default=False)

        GTA_IFP_Props.reset_anim = BoolProperty(
            name="Reset Anim",
            description="Clear All Anim Data in Selected Armature, before importing.",
            default=True)

        GTA_IFP_Props.skip_pos = BoolProperty(
            name="Skip POS Keys",
            description="Skip Pos Keys in Selected Directions",
            default=True)

        GTA_IFP_Props.skip_root = BoolVectorProperty(
            name="Root",
            description="Skip Root Bone's Pos Keys in Selected Directions",
            default=(False, False, False),
            subtype='XYZ')

        GTA_IFP_Props.skip_children = BoolProperty(
            name="Child Bones",
            description="Skip Child Bone's Pos Keys",
            default=True)

        GTA_IFP_Props.use_current_root = BoolProperty(
            name="Use Current Root",
            description="Set Anim based on Current Location of RootBone in Selected Axises",
            default=False)

        GTA_IFP_Props.use_current_root_pos = BoolVectorProperty(
            name="POS",
            description="Set Anim based on Current Location of RootBone in Selected Axises",
            # default = ( False, False, False ),
            default=(True, True, True),
            subtype='XYZ')

        GTA_IFP_Props.use_current_root_rot = EnumProperty(
            name="ROT",
            items=(
                ("NONE", "None", ""),
                ("ALL", "All", ""),
                ("XY", "XY", ""),
                ("YZ", "YZ", ""),
                ("ZX", "ZX", "")),
            description="Set Anim based on Current Rotation of RootBone in Selected Plane",
            default="NONE")

        GTA_IFP_Props.root_to_arm = BoolProperty(
            name="Root to Armature",
            description="Set Root Keys to Armature.",
            default=False)

        GTA_IFP_Props.root_to_arm_pos = BoolVectorProperty(
            name="POS",
            description="Set Root POS Keys to Armature.",
            # default = ( False, False, False ),
            default=(True, True, True),
            subtype='XYZ')

        GTA_IFP_Props.root_to_arm_rot = EnumProperty(
            name="ROT",
            items=(
                ("NONE", "None", ""),
                ("ALL", "All", ""),
                ("XY", "XY", ""),
                ("YZ", "YZ", ""),
                ("ZX", "ZX", "")),
            description="Set Root POT Keys to Armature in Selected Plane.",
            default="NONE")

        GTA_IFP_Props.show_frame_ops_imp = BoolProperty(
            name="Show Frame Options",
            description="Show Frame Options",
            default=False)

        GTA_IFP_Props.auto_snap = BoolProperty(
            name="Snap Time Keys",
            description="Snap Time Keys to the Nealest Flame",
            default=False)

        GTA_IFP_Props.frame_rate_preset = EnumProperty(
            name="Frame Rate",
            items=(
                ("30FPS", "30fps", ""),
                ("60FPS", "60fps", ""),
                ("CUSTOM", "Custom", ""),
                ("RENDER", "Render", "")),
            description="Frame Rate used for mapping IFP Frames to Blender Animation. ( \"Render\" : Use Render Frame Rate of Blender Settings )",
            default="30FPS")

        GTA_IFP_Props.frame_rate = IntProperty(
            name="fps",
            description="Custom Frame Rate.",
            min=10, max=120, default=30)

        GTA_IFP_Props.adjust_render_rate = BoolProperty(
            name="Adjust Render F.R.",
            description="Set Render Frame Rate of Blender, as the value set here.",
            default=True)

        GTA_IFP_Props.adjust_scene_range = BoolProperty(
            name="Adjust Scene Range",
            description="Set Scene Frame Range, as Imported Anim.",
            default=True)

        GTA_IFP_Props.load_at_end_anim = BoolProperty(
            name="Load at End Time",
            description="Load Anim at Time-Based End Key of Current Animation Data.( use in a case that the End of the Current Data is not snapped to any frames )",
            default=False)

        GTA_IFP_Props.reset_selbone_ops = BoolProperty(
            name="Reset Selected Bones",
            description="Reset Selected Bones",
            default=False)

        GTA_IFP_Props.active_anim_id = IntProperty(
            name="active_anim_id",
            description="Index of the active IFP Anim Name",
            default=-1,
            min=-1)

        ## for Export
        GTA_IFP_Props.ui_export = BoolProperty(
            name="Export IFP:",
            description="Show UI for Export IFP",
            default=True)

        GTA_IFP_Props.exp_filepath = StringProperty(
            name="IFP File Path",
            description="Full Path Name of target IFP",
            default="")

        GTA_IFP_Props.exp_mode = EnumProperty(
            name="Mode",
            items=(
                ("APPEND", "Append", "Export All Animations in Base IFP file, and \"Append\" Current Animation"),
                ("REPLACE", "Replace",
                 "Export All Animations in Base IFP file, and \"Replace\" same-named Animation with Current Animation "),
                ("SINGLE", "Single", "Export Current Animation as \"Single Animation IFP\"")),
            description="IFP Export Mode",
            default="SINGLE")

        GTA_IFP_Props.show_export_options = BoolProperty(
            name="Show Export Options",
            description="Show Export Options",
            default=False)

        GTA_IFP_Props.base_filepath = StringProperty(
            name="Base IFP File",
            description="Base IFP File for Export ( this property is updated with Loading Animation )",
            default="")

        GTA_IFP_Props.exp_ifp_name = StringProperty(
            name="Internal IFP file Name",
            description="Internal IFP file Name ( this property is updated with Loading Animation )",
            default="")

        GTA_IFP_Props.exp_anim_name = StringProperty(
            name="Anim Name",
            description="Anim Name for Export ( this property is updated with Loading Animation )",
            default="")

        GTA_IFP_Props.exp_ifp_format = EnumProperty(
            name="Format",
            items=(
                ("ANP3", "ANP3", "for Action Scene"),
                ("ANPK", "ANPK", "for Cut Scene")),
            description="IFP Data Format for Export ( this property is updated with Loading Animation )",
            default="ANP3")

        GTA_IFP_Props.rev_bone = BoolProperty(
            name="Original Bone Name:",
            description="Use Original Bone Name of the Loaded Character Model ( for internal description of IFP, not affect in Game )",
            default=True)

        GTA_IFP_Props.show_frame_ops_exp = BoolProperty(
            name="Show Frame Options",
            description="Show Frame Options ( options are Effective, even if Hide this )",
            default=False)

        GTA_IFP_Props.insert_final_key = BoolProperty(
            name="Insert Final Key",
            description="Insert Key at Final Frame of Keyed Bones",
            default=True)

        ## for Utilities
        GTA_IFP_Props.use_pelvis = BoolProperty(
            name="Use Pelvis",
            description="Rotate Pelvis Bone (if Character Direction in not Correct, try with this Option)",
            default=False)

        GTA_IFP_Props.clear_pose_selbone = BoolProperty(
            name="Clear Pose",
            description="Clear Pose of Selected Bones",
            default=True)

        GTA_IFP_Props.set_inirot_selbone = BoolProperty(
            name="Set Init-Rot-Key",
            description="Set Rotation Key at Initial Frame",
            default=False)

    def anims_clear(self):
        self.active_anim_id = -1
        for ia in range(len(self.anims)): self.anims.remove(0)


### IFP Tools ###
# Operators

class OperatorSelectIFP(bpy.types.Operator):
    bl_idname = "import_ifp.sel_ifp"
    bl_label = "Select IFP"
    bl_description = "Update Animation List in UI Panel"
    bl_options = BLOPT_REGISTER

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filename_ext = ".ifp"
    filter_glob: StringProperty(default="*.ifp", options={'HIDDEN'})

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_description)
        gta_tools.ifp_props.filepath = self.filepath

        from . import import_ifp
        import_ifp.import_ifp(gta_tools.ifp_props.filepath,
                              mode="UPDATE_LIST")
        gta_tools.show_msg_fin(err_only=True)
        return {'FINISHED'}

    def invoke(self, context, event):
        gta_tools = bpy.context.scene.gta_tools
        self.filepath = gta_tools.ifp_props.filepath
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OperatorImportAnim(bpy.types.Operator):
    bl_idname = "import_ifp.imp_anim"
    bl_label = "Load Selected Animation"
    bl_description = "Load Selected Animation"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)

        from . import import_ifp
        import_ifp.import_ifp(gta_tools.ifp_props.filepath,
                              mode="LOAD_ANIM")
        gta_tools.show_msg_fin(err_only=True)
        return {'FINISHED'}


class OperatorSelectBaseIFP(bpy.types.Operator):
    bl_idname = "import_ifp.sel_base_ifp"
    bl_label = "Select Base IFP"
    bl_description = "Base IFP File for Export ( this property is updated with Loading Animation )"
    bl_options = BLOPT_REGISTER

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filename_ext = ".ifp"
    filter_glob: StringProperty(default="*.ifp", options={'HIDDEN'})

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_description)
        gta_tools.ifp_props.base_filepath = self.filepath

        # from . import import_ifp
        # import_ifp.import_ifp( gta_tools.ifp_props.base_filepath,
        #							mode = "BASE_IFP_INFO" )
        gta_tools.show_msg_fin(err_only=True)
        return {'FINISHED'}

    def invoke(self, context, event):
        gta_tools = bpy.context.scene.gta_tools
        self.filepath = gta_tools.ifp_props.base_filepath
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OperatorResetAnim(bpy.types.Operator):
    bl_idname = "import_ifp.reset_anim"
    bl_label = "Reset Anim"
    bl_description = "Reset Animation Data"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import import_ifp
        import_ifp.reset_anim()
        import_ifp.reset_pose()
        gta_tools.show_msg_fin(err_only=True)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)


class OperatorResetArmature(bpy.types.Operator):
    bl_idname = "import_ifp.reset_armature"
    bl_label = "Reset Armature's POS/ROT"
    bl_description = "Reset Armature's POS/ROT"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import import_ifp
        import_ifp.reset_armature()
        gta_tools.show_msg_fin(err_only=True)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)


class OperatorAnimDirection(bpy.types.Operator):
    bl_idname = "import_ifp.anim_direction"
    bl_label = "Set Anim Direction"
    bl_description = "Set Character Direction as Standard IFP Animation"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import import_ifp
        import_ifp.anim_direction()
        gta_tools.show_msg_fin(err_only=True)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)


class OperatorSelectKeyedBones(bpy.types.Operator):
    bl_idname = "import_ifp.sel_keyed_bones"
    bl_label = "Select Keyed Bones"
    bl_description = "Select Bones Assigned Animation Keys"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import import_ifp
        import_ifp.select_keyed_bones()
        gta_tools.show_msg_fin(err_only=True)
        return {'FINISHED'}


class OperatorSelectRootChildren(bpy.types.Operator):
    bl_idname = "import_ifp.sel_root_children"
    bl_label = "Select Child Bones"
    bl_description = "Select Child Bones Linked Directly to the Root Bone"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import import_ifp
        import_ifp.sel_root_children()
        return {'FINISHED'}


class OperatorResetSelectedBones(bpy.types.Operator):
    bl_idname = "import_ifp.reset_sel_bones"
    bl_label = "Reset Selected Bones"
    bl_description = "Reset Animation Keys Assigned to Select Bones"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import import_ifp
        import_ifp.reset_selected_bones()
        gta_tools.show_msg_fin(err_only=True)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)


class OperatorApplyPose(bpy.types.Operator):
    bl_idname = "import_ifp.apply_pose"
    bl_label = "Apply Current Pose"
    bl_description = "Apply Current Pose to Mesh and Bones"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import import_ifp
        import_ifp.apply_pose()
        gta_tools.show_msg_fin(err_only=True)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)


### IFP Tools ###
# UI Panel

class GTA_IFPIO_UI(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "posemode"
    bl_label = "GTA IFP Tools"
    bl_idname = "IFP_PT_PANEL"

    def draw(self, context):
        layout = self.layout

        gta_tools = bpy.context.scene.gta_tools

        col = layout.column()
        col.label(text="IFP Import", icon='POSE_HLT')
        is_ifp_selected = ("" != gta_tools.ifp_props.ifp_name)
        if is_ifp_selected:
            str_imp_fname = os.path.split(gta_tools.ifp_props.filepath)[1]
        else:
            str_imp_fname = "Select IFP File"
        col.operator("import_ifp.sel_ifp", text=str_imp_fname, icon='FILEBROWSER')

        row_animlist = col.row()
        row_animlist.template_list("UI_UL_list", "anims", gta_tools.ifp_props, "anims", gta_tools.ifp_props,
                                   "active_anim_id")
        row_animlist.enabled = is_ifp_selected
        is_anim_selected = (-1 != gta_tools.ifp_props.active_anim_id)

        row_load = col.row()
        row_load.enabled = is_anim_selected
        if is_anim_selected:
            str_load = "Load : " + gta_tools.ifp_props.anims[gta_tools.ifp_props.active_anim_id].name
        else:
            str_load = "Load :"
        row_load.operator("import_ifp.imp_anim", text=str_load, icon='POSE_HLT')

        col = layout.column()
        col.prop(gta_tools.ifp_props, "show_import_options")
        if gta_tools.ifp_props.show_import_options:
            box = col.box()
            boxcol = box.column()
            boxcol.prop(gta_tools.ifp_props, "reset_anim")

            col = boxcol.column()
            col.prop(gta_tools.ifp_props, "skip_pos")
            if gta_tools.ifp_props.skip_pos:
                sub_boxcol = col.box().column(align=True)
                sub_boxcol.row().prop(gta_tools.ifp_props, "skip_root", emboss=False)
                sub_boxcol.prop(gta_tools.ifp_props, "skip_children")

            col = boxcol.column()
            col.prop(gta_tools.ifp_props, "use_current_root")
            if gta_tools.ifp_props.use_current_root:
                sub_boxcol = col.box().column(align=True)
                sub_boxcol.row().prop(gta_tools.ifp_props, "use_current_root_pos", emboss=False)
                sub_boxcol.prop(gta_tools.ifp_props, "use_current_root_rot")

            col = boxcol.column()
            col.prop(gta_tools.ifp_props, "root_to_arm")
            if gta_tools.ifp_props.root_to_arm:
                sub_boxcol = col.box().column(align=True)
                sub_boxcol.row().prop(gta_tools.ifp_props, "root_to_arm_pos", emboss=False)
                sub_boxcol.prop(gta_tools.ifp_props, "root_to_arm_rot")

            col = boxcol.column()
            col.prop(gta_tools.ifp_props, "show_frame_ops_imp")
            if gta_tools.ifp_props.show_frame_ops_imp:
                sub_boxcol = col.box().column(align=True)
                sub_boxcol.label(text="Frame Rate:")
                sub_boxcol.prop(gta_tools.ifp_props, "frame_rate_preset", text="")
                if "CUSTOM" == gta_tools.ifp_props.frame_rate_preset:
                    sub_boxcol.prop(gta_tools.ifp_props, "frame_rate")
                if "RENDER" != gta_tools.ifp_props.frame_rate_preset:
                    sub_boxcol.prop(gta_tools.ifp_props, "adjust_render_rate")
                sub_boxcol.prop(gta_tools.ifp_props, "adjust_scene_range")
                sub_boxcol.prop(gta_tools.ifp_props, "auto_snap")
                sub_boxcol.prop(gta_tools.ifp_props, "load_at_end_anim")


        col = layout.column(align=True)
        col.label(text="- - - - - - - - - -")
        col.label(text="Utilities", icon='POSE_HLT')
        col = layout.column(align=True)
        col.label(text="Animation:")
        col.operator("import_ifp.reset_anim", text="Reset Anim")

        col.label(text="Armature:")
        col.operator("import_ifp.reset_armature", text="Reset Armature")

        col.label(text="Bones:")
        col.operator("import_ifp.sel_keyed_bones", text="Select Keyed Bones")
        col = layout.column()
        boxcol = col.box().column(align=True)
        boxcol.operator("import_ifp.reset_sel_bones", text="Reset Seleced Bones")
        boxcol.prop(gta_tools.ifp_props, "clear_pose_selbone")
        boxcol.prop(gta_tools.ifp_props, "set_inirot_selbone")
        col.operator("import_ifp.sel_root_children", text="Select Child of Root")

        col.label(text="Pose:")
        boxcol = col.box().column(align=True)
        boxcol.operator("import_ifp.anim_direction", text="Anim Direction")
        boxcol.prop(gta_tools.ifp_props, "use_pelvis")
        col.operator("import_ifp.apply_pose", text="Apply Pose")

        col = layout.column(align=True)
        col.label(text="- - - - - - - - - -")
        col.label(text="Initialize Script:", icon='PREFERENCES')
        col.operator("gta_utils.init_gta_tools", text="Init IFP Tools").prop = "ifp_props"


class IFPImport(bpy.types.Operator):
    bl_idname = "view3d.cursor_center"
    bl_label = "Simple Operator"
    bl_description = "Simple Description"

    def execute(self, context: 'Context'):
        print("Exec")
        return {'FINISHED'}
