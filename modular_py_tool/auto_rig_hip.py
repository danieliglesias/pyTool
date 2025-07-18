import maya.cmds as cmds
import modular_py_tool.Utilities as utili
import modular_py_tool.UiAutoRig as auto_rig_ui

import importlib
importlib.reload(utili)
importlib.reload(auto_rig_ui)



def controller_hip_guide(char_name = None,parent_name = None, rebuild = False):

    # Create guide sphere
    sphere_name = cmds.sphere(name='{}_C_COG_BIND_guide'.format(char_name), r=1)[0]

    # Apply shader
    shader, shading_group = utili.create_shader_guide()
    shape = cmds.listRelatives(sphere_name, shapes=True, fullPath=True)[0]
    cmds.sets(shape, edit=True, forceElement=shading_group)
    final_position = None
    # Set position
    if rebuild:
        # Use custom position
        final_position = auto_rig_ui._nested_dict_instance['COG']['{}_C_COG_BIND_guide'.format(char_name)]['position']
        cmds.xform(sphere_name, ws=True, t=final_position)

    else:

        final_position = [0, (cmds.getAttr('heightDistance.distance') / 2.0), 0]
        cmds.move(final_position[0],final_position[1],final_position[2], sphere_name)
        ##### update dictionary #####
        auto_rig_ui._nested_dict_instance.update_limb(char_name = char_name, limb_name='COG', parent=parent_name, list=['COG'], suffix='guide')


    # Create annotation
    #final_position = position if position else (0, distance_value, 0)
    annotate = cmds.annotate(sphere_name, tx='COG', p=final_position)
    annotate_transform = cmds.listRelatives(annotate, parent=True)[0]
    cmds.parent(annotate_transform, sphere_name)

    # Set annotation color
    cmds.setAttr(annotate + '.overrideEnabled', 1)
    cmds.setAttr(annotate + '.overrideColor', 6)




def controller_hip_jnt(char_name = None,parent_name = None, rebuild = False):

    if rebuild:
        position = auto_rig_ui._nested_dict_instance.data['COG']['{}_C_COG_BIND_jnt'.format(char_name)]['position']
        cmds.select(clear=True)
        cmds.joint(p=position, name='{}_C_COG_BIND_jnt'.format(char_name))
    else:
        position = cmds.xform('{}_C_COG_BIND_guide'.format(char_name), t=True, ws=True, q=True)
        cmds.select(clear=True)
        cmds.joint(p=position, name='{}_C_COG_BIND_jnt'.format(char_name))
        cmds.delete('{}_C_COG_BIND_guide'.format(char_name))
        auto_rig_ui._nested_dict_instance.update_limb(char_name = char_name, limb_name='COG', parent=parent_name, list=['COG'], suffix='jnt')

    ##### update dictionary #####



