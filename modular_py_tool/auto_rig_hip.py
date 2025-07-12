import maya.cmds as cmds
import pyTool.modular_py_tool.Utilities as utili

import importlib
importlib.reload(utili)


def controller_hip_guide():

    sphere_name = cmds.sphere(name='C_COG_BIND_guide', r=1)[0]
    shader, shading_group = utili.create_shader_guide()
    # Step 5: Assign the material to the sphere
    #cmds.select(sphere_name)
    #cmds.hyperShade(assign='{}'.format(shader_name))
    shape = cmds.listRelatives(sphere_name, shapes=True, fullPath=True)[0]
    cmds.sets(shape, edit=True, forceElement=shading_group)


    distance_value = cmds.getAttr('heightDistance.distance') / 2
    cmds.move(0, distance_value, 0, sphere_name)
    """annotate = cmds.annotate(sphere_name, tx='COG', p=(0, distance_value, 0))
    cmds.parent(annotate, sphere_name)"""

    annotate = cmds.annotate(sphere_name, tx='COG', p=(0, distance_value, 0))
    annotate_transform = cmds.listRelatives(annotate, parent=True)[0]
    cmds.parent(annotate_transform, sphere_name)

    # cmds.rename(annotate, "hip_annotation")
    cmds.setAttr(annotate + '.overrideEnabled', 1)
    cmds.setAttr(annotate + '.overrideColor', 6)



