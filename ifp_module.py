import time

import bpy
import os


from . gta_utils import BLOPT_REGISTER

from bpy.props import StringProperty, CollectionProperty, BoolProperty, BoolVectorProperty, EnumProperty, IntProperty, \
    PointerProperty, FloatProperty, FloatVectorProperty

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


class GTA_IPL_Props(bpy.types.PropertyGroup):
    @classmethod
    def register(GTA_IPL_Props):
        GTA_IPL_Props.path = StringProperty(
            name="IPL filepath",
            description="",
            default="")

        GTA_IPL_Props.name = StringProperty(
            name="IPL Name",
            description="",
            default="")

        GTA_IPL_Props.ipl_name = StringProperty(
            name="IPL Name, Num Insts, Num Bin Insts",
            description="",
            default="")

class GTA_DFF_Props(bpy.types.PropertyGroup):
    @classmethod
    def register(GTA_DFF_Props):
        # GTA_DFF_Props.tex_path = StringProperty(
        #	name = "Texture Path",
        #	description = "",
        #	default = "" )

        ## for Import Menu
        GTA_DFF_Props.imp_filepath = StringProperty(
            name="DFF File Path",
            description="Full Path Name of Import DFF",
            default="")

        GTA_DFF_Props.show_import_menu = BoolProperty(
            name="DFF Import",
            description="Open/Close DFF Import Menu",
            default=True)

        GTA_DFF_Props.imp_type = EnumProperty(
            name="Type",
            items=(
                ("OTHER", "Other", ""),
                ("VEHICLE", "Vehicle", ""),
                ("CHAR", "Character", "")),
            description="Model Type for Import",
            default="CHAR")

        GTA_DFF_Props.show_import_options = BoolProperty(
            name="Show Import Options",
            description="Show Import Options",
            default=False)

        GTA_DFF_Props.read_vcol = BoolProperty(
            name="Read VCOL",
            description="Read Vertex Colors",
            default=True)

        GTA_DFF_Props.root_origin = BoolProperty(
            name="Root Origin",
            description="Draw Character using Root Bone Orientation",
            default=True)

        GTA_DFF_Props.ren_bone = BoolProperty(
            name="Rename Bone",
            description="Rename bone for Mirroring Modifire in Blender",
            default=True)

        GTA_DFF_Props.use_msplit = BoolProperty(
            name="Use Material Split",
            description="Assign Sub-Material ID to each Faces.",
            default=True)

        GTA_DFF_Props.use_remdbls = BoolProperty(
            name="Weld By Normal",
            description="Weld vertices doubled( very close ) in both coordinate space and normal space.",
            default=True)

        GTA_DFF_Props.remdbls_th_co = FloatProperty(
            name="co",
            description="Matching length for COORDINATE space used in \"Weld By Normal\" function.",
            min=.0001, max=2.0, default=0.0001, step=0.01,
            precision=4)

        GTA_DFF_Props.remdbls_th_no = FloatProperty(
            name="no",
            description="Matching length for NORMAL space used in \"Weld By Normal\" function.",
            min=.0001, max=2.0, default=0.0001, step=0.01,
            precision=4)

        GTA_DFF_Props.show_tex_options = BoolProperty(
            name="Show Texture Options",
            description="Show Texture Options",
            default=False)

        GTA_DFF_Props.extract_txd = BoolProperty(
            name="Extract TXD",
            description="Extract Images from TXD",
            default=True)

        GTA_DFF_Props.img_fmt = EnumProperty(
            name="Format",
            items=(
                ("BMP", "BMP", "BMP( Windows Bitmap )"),
                ("PNG", "PNG", "PNG( Portable Network Graphics )")),
            description="Image Format",
            default="BMP")

        GTA_DFF_Props.alp_mode = EnumProperty(
            name="Alpha",
            items=(
                (
                "COL_ALP", "COL+ALP", "24Bit-RGB for Deffuse Collor Terxture, and 24Bit-AAA for Alpha Channel Texture"),
                ("RGBA", "RGBA", "32Bit-RGBA Texture")),
            description="Alpha Image Type for Textures",
            default="COL_ALP")

        GTA_DFF_Props.generic_tex = BoolProperty(
            name="Use Generic Texs",
            description="Extract Generic Textures from \"GTA SA\" Folder for Vehicle Models.",
            default=False)

        GTA_DFF_Props.gta_path = StringProperty(
            name="GTASA folder",
            description="Set \"GTA San Andreas\" folder.",
            default="")

        ## for Export Menu
        GTA_DFF_Props.exp_filepath = StringProperty(
            name="Exoprt DFF File Path",
            description="Full Path Name of Export DFF",
            default="")

        GTA_DFF_Props.exp_type = EnumProperty(
            name="Type",
            items=(
                ("OTHER", "Other", ""),
                ("VEHICLE", "Vehicle", ""),
                ("CHAR", "Character", "")),
            description="Model Type for Export",
            default="CHAR")

        GTA_DFF_Props.show_export_options = BoolProperty(
            name="Show Export Options",
            description="Show Export Options",
            default=False)

        GTA_DFF_Props.write_vcol = BoolProperty(
            name="Write VCOL",
            description="Write Vertex Color Data",
            default=True)

        GTA_DFF_Props.vg_limit = IntProperty(
            name="VG Limit",
            description="Maximum Number of Assigned Vertex Groups for each Bones",
            max=4, min=1, default=4)

        GTA_DFF_Props.show_ths = BoolProperty(
            name="Show Thresholds",
            description="Show Matching Thresholds using Vertex Splitting",
            default=False)

        GTA_DFF_Props.uv_th = FloatProperty(
            name="UV",
            description="Matching Threshold for UV coods",
            min=0.0, default=0.0001,
            precision=4)

        GTA_DFF_Props.vc_th = FloatProperty(
            name="VCOL",
            description="Matching Threshold for Vertex Colors",
            min=0.0, default=0.0001,
            precision=4)

        GTA_DFF_Props.rev_bone = BoolProperty(
            name="Revert Bone Name",
            description="Revert bone name to original DFF bone",
            default=True)

        GTA_DFF_Props.use_alphatex = BoolProperty(
            name="Use Alpha Texture",
            description="Use Alpha Textures named [texture name]+\"a\".",
            default=True)

        class GTA_MAP_Props(bpy.types.PropertyGroup):
            @classmethod
            def register(GTA_MAP_Props):
                ## for IPL Import
                GTA_MAP_Props.gta_path = StringProperty(
                    name="GTA SA Folder",
                    description="Full Path Name of \"GTA San Andreas\"",
                    default="")

                GTA_MAP_Props.gtadat_path = StringProperty(
                    name="GTA.DAT File Path",
                    description="Full Path Name of GTA.DAT",
                    default="")

                GTA_MAP_Props.ipls = CollectionProperty(
                    type=GTA_IPL_Props,
                    name="IPL Entries",
                    description="IPL Entries")

                GTA_MAP_Props.active_ipl_id = IntProperty(
                    name="active_ipl_id",
                    description="Index of the active IPL Entriy",
                    default=-1,
                    min=-1)

                GTA_MAP_Props.show_import_options = BoolProperty(
                    name="Show Import Options",
                    description="Show Import Options",
                    default=False)

                GTA_MAP_Props.skip_lod = BoolProperty(
                    name="Skip LOD objs",
                    description="Skip LOD Models ( LOD:Long Distance )",
                    default=True)

                GTA_MAP_Props.skip_nonlod = BoolProperty(
                    name="Skip Non-LOD objs",
                    description="Skip Non-LOD Models ( LOD:Long Distance )",
                    default=False)

                GTA_MAP_Props.skip_nodes = BoolProperty(
                    name="Skip Nodes",
                    description="Skip Non-Meshed Models ( e.g. Omni Light )",
                    default=True)

                GTA_MAP_Props.skip_binipl = BoolProperty(
                    name="Skip BIN-IPLs",
                    description="Skip Models entried in Binary-IPLs",
                    default=False)

                # GTA_MAP_Props.sel_objs = BoolProperty(
                #	name = "Select with Loading",
                #	description = "Select Objects( not Node ) with Loading",
                #	default = True )

                ## for Extract TXDs
                GTA_MAP_Props.extract_txd = BoolProperty(
                    name="Extract TXD",
                    description=".",
                    default=False)

                GTA_MAP_Props.tex_path = StringProperty(
                    name="Path",
                    description=".",
                    default="")

                GTA_MAP_Props.img_fmt = EnumProperty(
                    name="Format",
                    items=(
                        ("BMP", "BMP", "BMP( Windows Bitmap )"),
                        ("PNG", "PNG", "PNG( Portable Network Graphics )")),
                    description="Image Format for Extracting Textures",
                    default="PNG")

                GTA_MAP_Props.alp_mode = EnumProperty(
                    name="Alpha",
                    items=(
                        ("COL_ALP", "COL+ALP",
                         "24Bit-RGB for Deffuse Collor Terxture, and 24Bit-AAA for Alpha Channel Texture"),
                        ("RGBA", "RGBA", "Extract to 32Bit-RGBA Texture File")),
                    description="Alpha Image Type for Textures",
                    default="RGBA")

            def ipls_clear(self):  ##  move to map_tools.py ????
                self.active_ipl_id = -1
                for ia in range(len(self.ipls)): self.ipls.remove(0)


class GTA_MAP_Props(bpy.types.PropertyGroup):

    def ipls_clear(self):  ##  move to map_tools.py ????
        self.active_ipl_id = -1
        for ia in range(len(self.ipls)): self.ipls.remove(0)


### Weight Tools ###
# Data Class

class GTA_WEIGHT_Props(bpy.types.PropertyGroup):
    @classmethod
    def register(GTA_WEIGHT_Props):
        GTA_WEIGHT_Props.marker_option = BoolProperty(
            name="Show Marker Option",
            description="Show Marker Option",
            default=False)

        GTA_WEIGHT_Props.weight_color = BoolProperty(
            name="Weight Color",
            description="Display Weight Color",
            default=True)

        GTA_WEIGHT_Props.mark_unweighted = BoolProperty(
            name="Mark UnWeighted",
            description="Mark UnWeighted Vertices",
            default=True)

        # GTA_WEIGHT_Props.show_zero = BoolProperty(
        #	name = "Show Zero",
        #	description = "Mark Zero Weight",
        #	default = False )

        GTA_WEIGHT_Props.mark_bone = BoolProperty(
            name="Mark Bone",
            description="Mark Active Bone",
            default=True)

        GTA_WEIGHT_Props.sel_verts_only = BoolProperty(
            name="SelVerts Only",
            description="Display Color only Selected Vertices",
            default=False)

        GTA_WEIGHT_Props.weight_size = FloatProperty(
            name="Size",
            description="Size of Weight Marker",
            min=0.0, max=10.0, default=3.0)

        GTA_WEIGHT_Props.weight_alpha = FloatProperty(
            name="Alpha",
            description="Alpha of Weight Marker",
            min=0.0, max=1.0, default=1.0)

        ## for Weight Options
        GTA_WEIGHT_Props.show_weight_option = BoolProperty(
            name="Show Weight Option",
            description="Show Weight Option",
            default=False)

        GTA_WEIGHT_Props.norm_mode = EnumProperty(
            name="Mode",
            items=(
                ("ALL", "All VGs", "Adjust All VG\'s Weight when Normalize"),
                ("EX_ACT", "Keep Active VG", "Keep Active VG\'s Weight when Normalize ( Adjust other VG\'s Weights )")),
            description="Normalize Mode",
            default="EX_ACT")

        GTA_WEIGHT_Props.auto_norm = BoolProperty(
            name="Auto Normalize",
            description="Nomalize Weights Automatically when Assigned",
            default=True)

        GTA_WEIGHT_Props.auto_clear_zero = BoolProperty(
            name="Auto Clear Zero",
            description="Crear Zero Weights Automatically when Assigned",
            default=True)

        GTA_WEIGHT_Props.weight_calc_margin = FloatProperty(
            name="Calc Margin",
            description="Margin for Weight Calculation ( for Zero Weight Judgement, Range Judgement, etc.. )",
            min=0.0, max=0.01, step=0.1, default=0.001)

        ## for Weight Assign Uniformly
        GTA_WEIGHT_Props.weight_value = FloatProperty(
            name="Value",
            description="Weight Value",
            min=0.0, max=1.0, default=1.0)

        ## for Weight Gradient
        GTA_WEIGHT_Props.cur_loc_1st = FloatVectorProperty(
            name="cur_loc_1st",
            description="Location of Gradient Start Point")

        GTA_WEIGHT_Props.cur_loc_2nd = FloatVectorProperty(
            name="cur_loc_2nd",
            description="Location of Gradient End Point")

        GTA_WEIGHT_Props.show_grad_option = BoolProperty(
            name="Show Grad Option",
            description="Show Gradient Option",
            default=False)

        GTA_WEIGHT_Props.grad_range = FloatVectorProperty(
            name="Range",
            description="Weight Range for Gradiation, between Start And End Point",
            size=2,
            default=(0.0, 1.0),
            max=1.0,
            min=0.0)

        GTA_WEIGHT_Props.grad_contour = EnumProperty(
            name="Contour",
            items=(
                ("SPHARE", "Sphare", "Weights are Varying with Radial Direction in 3D Space"),
                ("CYLINDER", "Cylinder",
                 "Weights are Varying with Radial Direction in View Plane, Uniform in Depth Direction"),
                ("PLANE", "Plane",
                 "Weights are Varying with only Specified Direction, Uniform in Flat Plane Perpendicular to Specified Line")),
            description="Contour Type for Weight Gradiation",
            default="PLANE")

        GTA_WEIGHT_Props.grad_view = EnumProperty(
            name="View",
            items=(
                ("TOP", "Top", ""),
                ("RIGHT", "Right", ""),
                ("FRONT", "Front", ""),
                ("USER", "User", "")),
            description="if Used Quad View, Cylinder Axis and Circle Plane are defined as View Direciton secified here",
            default="USER")

        GTA_WEIGHT_Props.wg_line_size = FloatProperty(
            name="Size",
            description="Size of Marker/Line",
            min=0.0, max=30.0, default=10.0)

        GTA_WEIGHT_Props.wg_line_alpha = FloatProperty(
            name="Alpha",
            description="Alpha  of Marker/Line",
            min=0.0, max=1.0, default=0.5)

        ## for Mirror Tool
        GTA_WEIGHT_Props.show_mirror_option = BoolProperty(
            name="Show Mirror Option",
            description="Show Mirror Option",
            default=False)

        GTA_WEIGHT_Props.mirror_verts = EnumProperty(
            name="Verts",
            items=(
                ("DEST", "Sel DEST", "Selected Vertices( as \"Mirroring Destination\" )"),
                ("SRC", "Sel SRC", "Selected Vertices( as \"Mirroring Source\" )"),
                ("SELECTED", "Selected", "Selected Vertices( both \"Source / Destination\" )"),
                ("ALL", "All", "All Vertices")),
            description="Vertices Selection",
            default="ALL")

        GTA_WEIGHT_Props.mirror_axis = EnumProperty(
            name="Axis",
            items=(
                ("Z", "Z", ""),
                ("Y", "Y", ""),
                ("X", "X", "")),
            description="Mirroring Axis in Mesh Object Space",
            default="X")

        # GTA_WEIGHT_Props.copy_mode = EnumProperty(
        #	name = "Mode",
        #	items = (
        #		( "GET", "Get", "Copy Weights from Mirrored Location to Selected Vertices" ),
        #		( "PUT", "Put", "Copy Weights from Selected Vertices to Mirrored Location" ) ),
        #	description = "Mirror Copy Mode",
        #	default = "GET" )

        GTA_WEIGHT_Props.copy_direction = EnumProperty(
            name="Direction",
            items=(
                ("TO_MINUS", "+ to -", "Copy Weights from Plus-Area to Minus-Area"),
                ("TO_PLUS", "- to +", "Copy Weights from Minus-Area to Plus-Area")),
            description="Mirroring Direction in Mesh Object Space",
            default="TO_PLUS")

        GTA_WEIGHT_Props.pos_calc_margin = FloatProperty(
            name="Matching Margin",
            description="Margin for Position-Mathcing Calculations",
            min=0.0, max=0.01, step=0.1, default=0.001)

        ## for Select Tool
        GTA_WEIGHT_Props.sel_type = EnumProperty(
            name="Type",
            items=(
                ("WEIGHT_RANGE", "Weight: Range",
                 "Select Vertices assigned in Specified Weight Range in Total ( with Calc Margin for Include )"),
                ("WEIGHT_OVER", "Weight: Over",
                 "Select Vertices assigned Over Weight Limit in Total ( with Calc Margin for Exclude )"),
                ("WEIGHT_UNDER", "Weight: Under",
                 "Select Vertices assigned Under Weight Limit in Total ( with Calc Margin for Exclude )"),
                ("VG_OVER", "VGs: Over", "Select Vertices assigned too many Vertex-Groups"),
                ("VG_NUM", "VGs: Number", "Select Vertices assigned Specified Number of Vertex-Groups")),
            description="Selection Mode",
            default="VG_NUM")

        GTA_WEIGHT_Props.target_num_vg = IntProperty(
            name="Number",
            description="Target Number of Assigned Vertex-Groups",
            min=0, max=10, default=0)

        GTA_WEIGHT_Props.over_assign_limit = IntProperty(
            name="Limit",
            description="Limit for Number of Assigned Vertex-Groups",
            min=0, max=10, default=4)

        GTA_WEIGHT_Props.weight_limit = FloatProperty(
            name="Limit",
            description="Limit for Total Weight ( with Calc Margin for Exclude )",
            min=0.0, max=10.0, step=0.1, default=1.0)

        GTA_WEIGHT_Props.target_weight_range = FloatVectorProperty(
            name="Range",
            description="Target Weight Range ( with Calc Margin for Include )",
            size=2, min=0.0, max=10.0, default=(0.0, 1.0))

    def clear_cb_properties(self):
        print("Crear CB Props")
        from . import weight_tools
        weight_tools.wc_state.enabled = False
        weight_tools.wg_state.enabled = [False, False, False]

### GTA Tools Utility
# Data Class
class GTA_UTIL_Props(bpy.types.PropertyGroup):
    @classmethod
    def register(GTA_UTIL_Props):
        ## for Vehicle Menu
        GTA_UTIL_Props.show_vehicle_ops = BoolProperty(
            name="Show Vehicle Menu",
            description="Show Vehicle Object Operations",
            default=False)

        GTA_UTIL_Props.target_all = BoolProperty(
            name="ALL",
            description="All Objects in Linked",
            default=False)

        GTA_UTIL_Props.target_coll = BoolProperty(
            name="COLL",
            description="Collisions/Shadows",
            default=True)

        GTA_UTIL_Props.target_vlo = BoolProperty(
            name="VLO",
            description="\"VLO\" Objs",
            default=True)

        GTA_UTIL_Props.target_ok = BoolProperty(
            name="OK",
            description="\"OK\" Objs",
            default=False)

        GTA_UTIL_Props.target_dam = BoolProperty(
            name="DAM",
            description="\"DAM\" Objs",
            default=True)

        ## for Material/Texture Menu
        GTA_UTIL_Props.show_mat_tex_ops = BoolProperty(
            name="Show MAT/TEX Menu",
            description="Show Matarial/Texture Operations",
            default=False)

        GTA_UTIL_Props.normal_map = EnumProperty(
            name="Normal Map",
            items=(
                ("SET", "Set", "Set \"Use Normal Map\""),
                ("UNSET", "UnSet", "UnSet \"Use Normal Map\""),
                ("CURRENT", "Not Change", "Use Current Setting")),
            description="Normal Map",
            default="CURRENT")

        GTA_UTIL_Props.normal_factor = FloatProperty(
            name="Normal Factor",
            description="Amount texture affects normal values.",
            default=1.0)

        GTA_UTIL_Props.use_alpha = EnumProperty(
            name="Use Alpha",
            items=(
                ("SET", "Set", "Set \"Use Alpha\""),
                ("UNSET", "UnSet", "UnSet \"Use Alpha\""),
                ("CURRENT", "Not Change", "Use Current Setting")),
            description="Use Alpha",
            default="CURRENT")

        GTA_UTIL_Props.use_transparent_shadows = EnumProperty(
            name="Tra-Shadows",
            items=(
                ("SET", "Set", "Set \"Receive Transparent Shadows\""),
                ("UNSET", "UnSet", "UnSet \"Receive Transparent Shadows\""),
                ("CURRENT", "Not Change", "Use Current Setting")),
            description="Receive Transparent Shadows",
            default="CURRENT")

        GTA_UTIL_Props.show_mat_tex_test = BoolProperty(
            name="Show Test Operations",
            description="Show Test Operations",
            default=False)

        GTA_UTIL_Props.transparency_method = EnumProperty(
            name="Tra-Method",
            items=(
                ("MASK", "Mask", "Mask the background."),
                ("Z_TRANSPARENCY", "Z Transparency", "Use alpha buffer for transparent faces."),
                ("RAYTRACE", "Raytrace", "Use raytracing for transparent refraction rendering."),
                ("CURRENT", "Not Change", "Use Current Setting")),
            description="Method to use for rendering transparency",
            default="CURRENT")

        GTA_UTIL_Props.rename_alpha_objs = EnumProperty(
            name="Object",
            items=(
                ("RENAME", "Rename", "Rename"),
                ("CURRENT", "Not Change", "Use Current Setting")),
            description="Rename Selected Objects For Sorting by Using Alpha texs or Not.",
            default="CURRENT")

        GTA_UTIL_Props.rename_alpha_mats = EnumProperty(
            name="Material",
            items=(
                ("RENAME", "Rename", "Rename"),
                ("CURRENT", "Not Change", "Use Current Setting")),
            description="Rename Materials For Sorting by Using Alpha texs or Not.",
            default="CURRENT")

        # GTA_UTIL_Props.mat_alpha_blend = EnumProperty(
        #	name = "AlpMatBlend",
        #	items = (
        #		( "MULTIPLY", "Multiply",   "Multiply" ),
        #		( "MIX" ,     "Mix",        "Mix" ),
        #		( "CURRENT",  "Not Change", "Use Current Setting" ) ),
        #	description = "Set",
        #	default = "CURRENT" )

        ## for Utilities
        GTA_UTIL_Props.show_char_menu = BoolProperty(
            name="Show Character Menu",
            description="Show Character Menu ( Enabled @Armature Object / @Object Mode )",
            default=False)

        GTA_UTIL_Props.center_bone = BoolProperty(
            name="Center",
            description="Align Loc/Rot of \"NON-L/R Named\" Bones to Center Plane( for Root Bone, Align Loc only)",
            default=True)

        GTA_UTIL_Props.side_bone = BoolProperty(
            name="Side",
            description="Mirror Loc/Rot of \"L/R Named\" bones",
            default=True)

        # GTA_UTIL_Props.align_target = EnumProperty(
        #	name = "Bones",
        #	items = (
        #		( "DEST", "Sel DEST" , "Select Bones as \"Mirror Destination\" (or Center bones)" ),
        #		( "SRC" , "Sel SRC"  , "Select Bones as \"Mirror Source\"  (or Center bones)" ),
        #		( "ALL" , "All"      , "All Bones" ) ),
        #	description = "Bones Selection",
        #	default = "ALL" )

        GTA_UTIL_Props.align_axis = EnumProperty(
            name="Axis",
            items=(
                ("Z", "Z", ""),
                ("Y", "Y", ""),
                ("X", "X", "")),
            description="Aligning / Mirroring Axis in Armature Space",
            default="X")

        GTA_UTIL_Props.copy_direction = EnumProperty(
            name="Direction",
            items=(
                ("R", "R to L", "Align \"R\" bone to Mirrored \"L\" bone"),
                ("L", "L to R", "Align \"L\" bone to Mirrored \"R\" bone")),
            description="Align Direction for \"L/R\" String",
            default="L")

        GTA_UTIL_Props.bone_size = FloatProperty(
            name="Size",
            description="Bone Size",
            min=0.0, default=0.05, step=1,
            precision=4)

        GTA_UTIL_Props.forward_axis = EnumProperty(
            name="Forward",
            items=(
                ("Z-", "Z-", ""),
                ("Z+", "Z+", ""),
                ("Y-", "Y-", ""),
                ("Y+", "Y+", ""),
                ("X-", "X-", ""),
                ("X+", "X+", "")),
            description="Definition of Current \"Forward\" Direction of Character in Armature Space",
            default="Y+")

        GTA_UTIL_Props.top_axis = EnumProperty(
            name="Up",
            items=(
                ("Z-", "Z-", ""),
                ("Z+", "Z+", ""),
                ("Y-", "Y-", ""),
                ("Y+", "Y+", ""),
                ("X-", "X-", ""),
                ("X+", "X+", "")),
            description="Definition of Current \"Up\" Direction of Character in Armature Space",
            default="Z+")

        GTA_UTIL_Props.align_pelvis_pos = BoolProperty(
            name="Align Pelvis",
            description="Align Pelvis Position \"with Mesh\" to Center Plane of Side Direction",
            default=True)

        # GTA_UTIL_Props.align_pelvis_rot = BoolProperty(
        #	name = "Rot",
        #	description = "Align Pelvis Rotation \"with Mesh\" to Center Plane of Side Direction",
        #	default = False )

        ## for Test Codes
        GTA_UTIL_Props.show_test_codes = BoolProperty(
            name="Test/Debug Codes",
            description="Show Test/Debug Codes",
            default=False)

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

class GTATOOLS_Props(bpy.types.PropertyGroup):
    @classmethod
    def register(GTATOOLS_Props):
        GTATOOLS_Props.dff_props = PointerProperty(
            type=GTA_DFF_Props,
            name="DFF Props",
            description="Properties for DFF format @GTA Tools")

        GTATOOLS_Props.map_props = PointerProperty(
            type=GTA_MAP_Props,
            name="MAP Props",
            description="Properties for MAP Import @GTA Tools")

        GTATOOLS_Props.ifp_props = PointerProperty(
            type=GTA_IFP_Props,
            name="IFP Props",
            description="Properties for IFP format @GTA Tools")

        GTATOOLS_Props.weight_props = PointerProperty(
            type=GTA_WEIGHT_Props,
            name="Weight Props",
            description="Properties for Weight Tools @GTA Tools")

        GTATOOLS_Props.util_props = PointerProperty(
            type=GTA_UTIL_Props,
            name="Utility Props",
            description="Properties for Utilities @GTA Tools")

        bpy.types.Scene.gta_tools = PointerProperty(
            type=GTATOOLS_Props,
            name="GTA Tools Props",
            description="GTA Tools Properties")

        ## For Message / Error
        GTATOOLS_Props.msg = StringProperty(
            name="Message",
            description="Message",
            default="")

        GTATOOLS_Props.err_count = IntProperty(
            name="Error Count",
            description="Error Count",
            default=0)

        GTATOOLS_Props.warn_count = IntProperty(
            name="Warn Count",
            description="Warn Count",
            default=0)

        GTATOOLS_Props.time_ini = FloatProperty(
            name="Initial Time Stump",
            description="Initial Time Stump",
            default=0.0)

    def init_msg(self, msg=None):
        self.time_ini = time.clock()
        if None != msg:
            self.msg = msg + "\n"
        else:
            self.msg = ""
        self.err_count = 0
        self.warn_count = 0

    def set_msg(self, msg, warn_flg=False, err_flg=False, indent=2):
        for i in range(indent): self.msg += " "
        self.msg += msg + "\n"
        if warn_flg: self.warn_count += 1
        if err_flg: self.err_count += 1

    def show_msg(self):
        bpy.ops.scene.msg_popup('INVOKE_DEFAULT', msg=self.msg)
        print("\n" + self.msg)
        self.init_msg()

    def show_msg_fin(self, err_only=False):
        fin_msg = ""
        if 0 < self.err_count:
            fin_msg += "Finished with %d Error( s ).\n" % self.err_count
        elif 0 < self.warn_count:
            fin_msg += "Finished with %d Warning( s ).\n" % self.warn_count
        else:
            fin_msg += "Finished Successfully.\n"
        fin_msg += "Elapsed Time : %.3lf sec" % ((time.clock() - self.time_ini))

        print("\n%s%s\n" % (self.msg, fin_msg))

        if (not err_only):
            lines = self.msg.split('\n')
            max_lines = 30
            if max_lines < len(lines):
                self.msg = ""
                for il in range(max_lines): self.msg += lines[il] + "\n"
                self.msg += "*** Too Many Infomations, See \"System Console\" to Get All. ***\n"
            # bpy.ops.scene.msg_popup( 'INVOKE_DEFAULT', msg = self.msg + fin_msg )
            self.msg += fin_msg
            bpy.ops.scene.msg_popup('INVOKE_DEFAULT')

        self.init_msg()

    @classmethod
    def unregister(GTATOOLS_Props):
        del bpy.types.Scene.gta_tools

