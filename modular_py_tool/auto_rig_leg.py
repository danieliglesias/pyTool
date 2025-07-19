import maya.cmds as cmds
from maya.app.renderSetup.lightEditor.model.typeManager import rebuild

import modular_py_tool.Utilities as utili
import modular_py_tool.UiAutoRig as ui_autorig

import importlib
importlib.reload(utili)
importlib.reload(ui_autorig)

def controller_leg_guide(char_name = None,rebuild = False,limb_name = None,leg_type = None, limb_connection = None, kinematic_mode = None, limb_end = None):
    print(limb_name)
    """if rebuild:
        kinematic = kinematic_mode
        limb_end_leg = limb_end
    else:
        if kinematic_mode[0] == True:
            kinematic = 'ikfk'
        else:
            kinematic = 'fk'
        if limb_end[0] == True:
            limb_end_leg = True
        else:
            limb_end_leg = False"""

    ### [0] name, [1] Y offset, [2] Z offset
    joint_list = [['{}_{}_upperleg{}_guide'.format(char_name,limb_name[0].upper(),limb_name[-2:]),0,0],
                  ['{}_{}_lowerleg{}_guide'.format(char_name,limb_name[0].upper(),limb_name[-2:]),2,0],
                  ['{}_{}_ankle{}_guide'.format(char_name,limb_name[0].upper(),limb_name[-2:]),10,0],
                  ['{}_{}_ball{}_guide'.format(char_name,limb_name[0].upper(),limb_name[-2:]),100,10],
                  ['{}_{}_toe{}_guide'.format(char_name,limb_name[0].upper(),limb_name[-2:]),100,6]]


    final_position = None

    for index, item in enumerate(joint_list):
        print(item[0])
        sphere_name = cmds.sphere(name='{}'.format(item[0]), r=1)[0]
        shader, shading_group = utili.create_shader_guide()
        shape = cmds.listRelatives(sphere_name, shapes=True, fullPath=True)[0]
        cmds.sets(shape, edit=True, forceElement=shading_group)

        if rebuild == True:
            final_position = ui_autorig._nested_dict_instance.data[limb_name][item[0]]['position']
            cmds.move( final_position[0],final_position[1],final_position[2] ,sphere_name)
        elif limb_name[0].upper() == 'L':
            final_position = [(cmds.getAttr('heightDistance.distance') / 25.0),
                              (cmds.getAttr('heightDistance.distance') / 2.0)/ item[1] if item[1] != 0 else (cmds.getAttr('heightDistance.distance') / 2.0),
                              (cmds.getAttr('heightDistance.distance') / 2.0)/ item[2] if item[2] != 0 else 0]
            cmds.move(final_position[0],
                      final_position[1],
                      final_position[2],
                      sphere_name)
        elif limb_name[0].upper() == 'R':
            final_position = [(cmds.getAttr('heightDistance.distance') / 25.0)*-1,
                              ((cmds.getAttr('heightDistance.distance') / 2.0) / item[1] if item[1] != 0 else (
                                          cmds.getAttr('heightDistance.distance') / 2.0)),
                              ((cmds.getAttr('heightDistance.distance') / 2.0) / item[2] if item[2] != 0 else 0)]
            cmds.move(final_position[0],
                      final_position[1],
                      final_position[2],
                      sphere_name)


        # Create annotation
        # final_position = position if position else (0, distance_value, 0)
        annotate = cmds.annotate(item[0], tx='{}'.format("_".join(item[0].split("_")[1:])),
                                 p=(final_position[0],
                                    final_position[1] if rebuild == True else final_position[1] + final_position[1]/30,
                                    final_position[2]))
        annotate_transform = cmds.listRelatives(annotate, parent=True)[0]
        cmds.parent(annotate_transform, item[0])

        # Set annotation color
        cmds.setAttr(annotate + '.overrideEnabled', 1)
        cmds.setAttr(annotate + '.overrideColor', 6)


        ### UPDATE LIMB
        # kinematic_mode = kinematic, limb_type = None, limb_end = limb_end_leg
    ui_autorig._nested_dict_instance.update_limb(char_name = char_name,limb_name=limb_name,
                                                 parent=limb_connection,
                                                 list=['{}_upperleg{}'.format(limb_name[0],limb_name[-2:]),
                                                       '{}_lowerleg{}'.format(limb_name[0],limb_name[-2:]),
                                                       '{}_ankle{}'.format(limb_name[0],limb_name[-2:]),
                                                       '{}_ball{}'.format(limb_name[0],limb_name[-2:]),
                                                       '{}_toe{}'.format(limb_name[0],limb_name[-2:])], suffix='guide',
                                                 kinematic_mode = kinematic_mode, limb_end = limb_end,limb_type = leg_type)

def controller_leg_jnt(char_name = None,rebuild = False,limb_name = None,leg_type = None, limb_connection = None, kinematic_mode = None, limb_end = None):
    """if rebuild:
        kinematic = kinematic_mode
        limb_end_leg = limb_end
    else:
        if kinematic_mode[0] == True:
            kinematic = 'ikfk'
        else:
            kinematic = 'fk'
        if limb_end[0] == True:
            limb_end_leg = True
        else:
            limb_end_leg = False"""

    joint_list = ['{}_{}_upperleg{}_guide'.format(char_name, limb_name[0].upper(), limb_name[-2:]),
                  '{}_{}_lowerleg{}_guide'.format(char_name, limb_name[0].upper(), limb_name[-2:]),
                  '{}_{}_ankle{}_guide'.format(char_name, limb_name[0].upper(), limb_name[-2:]),
                  '{}_{}_ball{}_guide'.format(char_name, limb_name[0].upper(), limb_name[-2:]),
                  '{}_{}_toe{}_guide'.format(char_name, limb_name[0].upper(), limb_name[-2:])]


    if rebuild == False:
        for i, item in enumerate(joint_list):
            world_pos = cmds.xform(item, t=True, ws=True, q=True)
            cmds.select(clear=True)
            if i == 0:
                jnt = cmds.joint(p=world_pos, name='{}_jnt'.format(item[0:-6]))
            else:
                jnt = cmds.joint(p=world_pos, name='{}_jnt'.format(item[0:-6]))
                cmds.parent(jnt, '{}_jnt'.format(joint_list[i - 1][0:-6]))

            cmds.delete(item)

        ui_autorig._nested_dict_instance.update_limb(char_name=char_name, limb_name=limb_name,
                                                     parent=limb_connection,
                                                     list=['{}_upperleg{}'.format(limb_name[0], limb_name[-2:]),
                                                           '{}_lowerleg{}'.format(limb_name[0], limb_name[-2:]),
                                                           '{}_ankle{}'.format(limb_name[0], limb_name[-2:]),
                                                           '{}_ball{}'.format(limb_name[0], limb_name[-2:]),
                                                           '{}_toe{}'.format(limb_name[0], limb_name[-2:])],
                                                     suffix='jnt',
                                                     kinematic_mode=kinematic_mode, limb_end=limb_end,
                                                     limb_type=leg_type)
    else:

        ui_autorig._nested_dict_instance.create_joints_from_limb(limb_name=limb_name)


def controller_leg_jnt_mirror(char_name = None, limb_name = None):

    cmds.select(original_joint)
    mirrored_joint = cmds.mirrorJoint(
        mirrorYZ=True,  # or mirrorBehavior=True depending on setup
        searchReplace=["_L_", "_R_"],  # rename in one go
        mirrorBehavior=True
    )


def controller_leg_guide_mirror(char_name = None, limb_name = None):

    ### before mirror we make shure that there is a update version of the guides in the dictionary
    mirrored_name = None
    #controller_leg_guide(side = limb_name[1].upper(), char_name = char_name)

    component = ui_autorig._nested_dict_instance.data.get(limb_name)


    for joint_key, info in component.items():
        cmds.select(clear=True)
        if joint_key == 'general':
            continue

        bone_name = info.get('bone_name')
        if "_L_" in bone_name:
            mirrored_name = bone_name.replace("_L_", "_R_")
        elif "_R_" in bone_name:
            mirrored_name = bone_name.replace("_R_", "_L_")

        position = info.get('position')
        final_position = [position[0]*-1,position[1],position[2]]
        utili.create_guide_sphere(mirrored_name, final_position = final_position)

        parent = ui_autorig._nested_dict_instance.data[limb_name]['general']['parent']
        kinematic_mode = ui_autorig._nested_dict_instance.data[limb_name]['general']['kinematic_mode']
        limb_type = ui_autorig._nested_dict_instance.data[limb_name]['general']['limb_type']
        limb_end = ui_autorig._nested_dict_instance.data[limb_name]['general']['limb_end']

        oposite_side = utili.switch_side_prefix(limb_name[0])

        ui_autorig._nested_dict_instance.update_limb(char_name=char_name, limb_name=utili.switch_side_prefix(limb_name),
                                                     parent=parent,
                                                     list=['{}_upperleg{}'.format(oposite_side, limb_name[-2:]),
                                                           '{}_lowerleg{}'.format(oposite_side, limb_name[-2:]),
                                                           '{}_ankle{}'.format(oposite_side, limb_name[-2:]),
                                                           '{}_ball{}'.format(oposite_side, limb_name[-2:]),
                                                           '{}_toe{}'.format(oposite_side, limb_name[-2:])],
                                                     suffix='guide',
                                                     kinematic_mode=kinematic_mode, limb_end=limb_end,
                                                     limb_type=limb_type)

