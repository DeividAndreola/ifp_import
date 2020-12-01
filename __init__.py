import bpy
from . import ifp_module

bl_info = {
    "name": "IFP Import",
    "author": "ponz",
    "blender": (2, 80, 0),
    "description": "Tools for GTA SA 3DModels/Animations",
    "category": "3D View",
}

_classes = [
    ifp_module.GTA_IFP_AnimProps,
    ifp_module.GTA_IFP_Props,
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
    ifp_module.GTA_IFPIO_UI
]

register, unregister = bpy.utils.register_classes_factory(_classes)
