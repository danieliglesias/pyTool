import maya.cmds as cmds
import modular_py_tool.Utilities as utili
import modular_py_tool.UiAutoRig as auto_rig_ui

import importlib
importlib.reload(utili)
importlib.reload(auto_rig_ui)



def controller_hip_guide(rebuild = False):

    # Create guide sphere
    sphere_name = cmds.sphere(name='C_COG_BIND_guide', r=1)[0]

    # Apply shader
    shader, shading_group = utili.create_shader_guide()
    shape = cmds.listRelatives(sphere_name, shapes=True, fullPath=True)[0]
    cmds.sets(shape, edit=True, forceElement=shading_group)
    final_position = None
    # Set position
    if rebuild:
        # Use custom position
        final_position = auto_rig_ui._nested_dict_instance['COG']['C_COG_BIND_guide']['position']
        cmds.xform(sphere_name, ws=True, t=final_position)

    else:
        # Use default distance from heightDistance
        try:
            final_position = [0, (cmds.getAttr('heightDistance.distance') / 2.0), 0]
        except:
            distance_value = 10  # fallback if node doesn't exist
            print('Warning: heightDistance node not found, using default value 10')

        cmds.move(final_position[0],final_position[1],final_position[2], sphere_name)


    # Create annotation
    #final_position = position if position else (0, distance_value, 0)
    annotate = cmds.annotate(sphere_name, tx='COG', p=final_position)
    annotate_transform = cmds.listRelatives(annotate, parent=True)[0]
    cmds.parent(annotate_transform, sphere_name)

    # Set annotation color
    cmds.setAttr(annotate + '.overrideEnabled', 1)
    cmds.setAttr(annotate + '.overrideColor', 6)

    ##### update dictionary #####
    parent_name = cmds.textField('cog_parent_name', query=True, text=True)
    auto_rig_ui._nested_dict_instance.update_limb(limb_name='COG',parent = parent_name, list=['COG'], suffix='guide')


def controller_hip_jnt(rebuild = False):

    if rebuild:
        position = auto_rig_ui._nested_dict_instance.data['COG']['C_COG_BIND_jnt']['position']
        cmds.select(clear=True)
        cmds.joint(p=position, name='C_COG_BIND_jnt')
    else:
        position = cmds.xform('C_COG_BIND_guide', t=True, ws=True, q=True)
        cmds.select(clear=True)
        cmds.joint(p=position, name='C_COG_BIND_jnt')
        cmds.delete('C_COG_BIND_guide')

    ##### update dictionary #####
    parent_name = cmds.textField('cog_parent_name', query=True, text=True)
    auto_rig_ui._nested_dict_instance.update_limb(limb_name='COG', parent =parent_name, list=['COG'], suffix='jnt')



