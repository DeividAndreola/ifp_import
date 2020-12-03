import bpy

from .gta_utils import BLOPT_REGISTER, BoolProperty
from . import ifp_module

bl_info = {
    "name": "IFP Import",
    "author": "ponz",
    "blender": (2, 80, 0),
    "description": "Tools for GTA SA 3DModels/Animations",
    "category": "3D View",
}


# Operators

class MsgPopupOperator(bpy.types.Operator):
    bl_idname = "scene.msg_popup"
    bl_label = "GTA Tools Message"
    bl_description = "Message Popup"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        return {'CANCELLED'}

    def invoke(self, context, event):
        wm = context.window_manager
        msg = bpy.context.scene.gta_tools.msg
        lines = msg.split('\n')
        max_len = 0
        for line in lines: max_len = max((max_len, len(line)))
        return wm.invoke_popup(self, width=20 + 8 * max_len)

    # return wm.invoke_props_dialog( self, width = 20+8*max_len )

    def draw(self, context):
        layout = self.layout
        msg = bpy.context.scene.gta_tools.msg
        lines = msg.split('\n')

        col = layout.column()
        if 0 < bpy.context.scene.gta_tools.err_count:
            col.label(text="Error", icon="ERROR")
        if 0 < bpy.context.scene.gta_tools.warn_count:
            col.label(text="Warning", icon="ERROR")
        for line in lines:
            col.label(text=line)


class OperatorToggleNameVisibility(bpy.types.Operator):
    bl_idname = "gta_utils.tgl_name"
    bl_label = "Toggle Visibility of Object Names"
    bl_description = "Toggle Visibility of Object Names"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import gta_utils
        gta_utils.toggle_name()
        gta_tools.show_msg_fin(err_only=True)
        return {'FINISHED'}


class OperatorToggleNodeVisibility(bpy.types.Operator):
    bl_idname = "gta_utils.tgl_node"
    bl_label = "Toggle Visibility of Nodes/Bones"
    bl_description = "Toggle Visibility of Nodes/Bones"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import gta_utils
        gta_utils.toggle_node()
        gta_tools.show_msg_fin(err_only=True)
        return {'FINISHED'}


class OperatorToggleXRay(bpy.types.Operator):
    bl_idname = "gta_utils.tgl_xray"
    bl_label = "Toggle X-Ray Option of Nodes"
    bl_description = "Toggle X-Ray Option of Nodes"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import gta_utils
        gta_utils.toggle_xray()
        gta_tools.show_msg_fin(err_only=True)
        return {'FINISHED'}


class OperatorHideObjSets(bpy.types.Operator):
    bl_idname = "gta_utils.hide_objsets"
    bl_label = "Set Props for Grouped and Linked Objects"
    bl_description = "Show/Hide Grouped and Linked Objects"
    bl_options = BLOPT_REGISTER
    val = BoolProperty()

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import gta_utils
        gta_utils.set_sel_show(0, self.val)  # mode: 0 = hide/show, 1 = select/deselect
        gta_tools.show_msg_fin(err_only=True)
        return {'FINISHED'}


class OperatorSelectObjSets(bpy.types.Operator):
    bl_idname = "gta_utils.sel_objsets"
    bl_label = "Set Props for Grouped and Linked Objects"
    bl_description = "Select/Deselect Grouped and Linked Objects"
    bl_options = BLOPT_REGISTER
    val = BoolProperty()

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import gta_utils
        gta_utils.set_sel_show(1, self.val)  # mode: 0 = hide/show, 1 = select/deselect
        gta_tools.show_msg_fin(err_only=True)
        return {'FINISHED'}


class OperatorSetPropsSelObj(bpy.types.Operator):
    bl_idname = "gta_utils.set_props"
    bl_label = "Set Properties in Selected Objects"
    bl_description = "Set Properties in Selected Objects"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import gta_utils
        gta_utils.set_props()
        gta_tools.show_msg_fin()
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)


class OperatorAlignBones(bpy.types.Operator):
    bl_idname = "gta_utils.align_bones"
    bl_label = "Align / Mirror Bones"
    bl_description = "Align / Mirror Bones"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import gta_utils
        gta_utils.align_bones()
        gta_tools.show_msg_fin()
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)


class OperatorResizeBones(bpy.types.Operator):
    bl_idname = "gta_utils.resize_bones"
    bl_label = "Resize Bones"
    bl_description = "Resize Bones ( Bone Size \"not\" affects to Bone Behavior and Export Result, just affects to Bone Appearance )"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import gta_utils
        gta_utils.resize_bones()
        gta_tools.show_msg_fin()
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)


class OperatorFixDirection(bpy.types.Operator):
    bl_idname = "gta_utils.fix_direction"
    bl_label = "Fix Character Direction"
    bl_description = "Fix Default Direction of Character to \"GAME Orientation\" in Armature Space"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import gta_utils
        gta_utils.fix_direction()
        gta_tools.show_msg_fin()
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)


class OperatorBoxQuadHookCallbacksControl(bpy.types.Operator):
    bl_idname = "gta_utils.box_quad_hook"
    bl_label = "Eneble/Diseble to Keep \"box\" option to Enable in \"Quad View\""
    bl_description = "Eneble/Diseble to Keep \"box\" option to Enable in \"Quad View\""
    bl_options = BLOPT_REGISTER

    def modal(self, context, event):
        from . import gta_utils
        if 'VIEW_3D' == bpy.context.space_data.type:
            if None != bpy.context.space_data.region_quadview:  ## is Quad View
                view_3d = bpy.context.space_data.region_quadview
                if view_3d.lock_rotation:
                    if False == view_3d.show_sync_view:
                        view_3d.show_sync_view = True
                    # print( "Enabled Box Quad" )

        if not gta_utils.hook_state.box_quad_enabled:
            print("Disabled HOOK Box Quad")
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def cancel(self, context):
        from . import gta_utils
        if gta_utils.hook_state.box_quad_enabled:
            gta_utils.hook_state.box_quad_enabled = False
            print("Disabled HOOK Box Quad")
        return {'CANCELLED'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            from . import gta_utils
            if not gta_utils.hook_state.box_quad_enabled:
                gta_utils.hook_state.box_quad_enabled = True
                context.window_manager.modal_handler_add(self)
                gta_utils.hook_state.box_quad_enabled = True
                print("Enabled HOOK Box Quad")
                return {'RUNNING_MODAL'}
            else:
                gta_utils.hook_state.box_quad_enabled = False
                return {'CANCELLED'}
        else:
            self.report({'WARNING'}, "View3D not found, can't run operator")
            return {'CANCELLED'}


class OperatorRemoveUnusedData(bpy.types.Operator):
    bl_idname = "gta_utils.rm_unused"
    bl_label = "Remove UnUsed Data"
    bl_description = "Remove UnUsed Data"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import gta_utils
        gta_utils.remove_unused()
        bpy.context.scene.gta_tools.show_msg_fin()
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)


class OperatorRemoveImages(bpy.types.Operator):
    bl_idname = "gta_utils.rm_images"
    bl_label = "Remove All Images"
    bl_description = "Remove All Images"
    bl_options = BLOPT_REGISTER

    def execute(self, context):
        gta_tools = bpy.context.scene.gta_tools
        gta_tools.init_msg("--- %s ---" % self.bl_label)
        from . import gta_utils
        gta_utils.remove_images()
        bpy.context.scene.gta_tools.show_msg_fin()
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)

_classes = [
    ifp_module.GTA_UTIL_Props,
    ifp_module.GTA_IFP_AnimProps,
    ifp_module.GTA_IFP_Props,
    ifp_module.GTA_MAP_Props,
    ifp_module.GTA_WEIGHT_Props,
    ifp_module.GTA_DFF_Props,
    ifp_module.GTATOOLS_Props,
    ifp_module.GTA_IFPIO_UI,

    ifp_module.OperatorInitGTATools,
    ifp_module.OperatorSelectIFP,
    ifp_module.OperatorImportAnim,
    ifp_module.OperatorSelectBaseIFP,
    ifp_module.OperatorResetAnim,
    ifp_module.OperatorResetArmature,
    ifp_module.OperatorAnimDirection,
    ifp_module.OperatorSelectKeyedBones,
    ifp_module.OperatorSelectRootChildren,
    ifp_module.OperatorResetSelectedBones,
    ifp_module.OperatorApplyPose,
    MsgPopupOperator,
    OperatorBoxQuadHookCallbacksControl,
    OperatorRemoveUnusedData,
    OperatorSetPropsSelObj,
    OperatorToggleNameVisibility,
    OperatorToggleNodeVisibility,
    OperatorAlignBones,
    OperatorFixDirection,
    OperatorToggleXRay

]

register, unregister = bpy.utils.register_classes_factory(_classes)
