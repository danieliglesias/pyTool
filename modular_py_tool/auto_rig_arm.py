import maya.cmds as cmds
from maya.app.renderSetup.lightEditor.model.typeManager import rebuild

import modular_py_tool.Utilities as utili
import modular_py_tool.UiAutoRig as ui_autorig

import importlib
importlib.reload(utili)
importlib.reload(ui_autorig)

def controller_arm_guide(char_name = None,rebuild = False,limb_name = None,leg_type = None, limb_connection = None, kinematic_mode = None, limb_end = None):
    if rebuild:
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
            limb_end_leg = False

    ### [0] name, [1] Y offset, [2] Z offset
    joint_list_arm = [['{}_{}_clav{}_guide'.format(char_name, limb_name[1].upper(), limb_name[-2:]), 60, 0],
                  ['{}_{}_upperarm{}_guide'.format(char_name, limb_name[1].upper(), limb_name[-2:]), 10, 0],
                  ['{}_{}_lowerarm{}_guide'.format(char_name, limb_name[1].upper(), limb_name[-2:]), 4, 0],
                  ['{}_{}_wrist{}_guide'.format(char_name, limb_name[1].upper(), limb_name[-2:]), 2.7, 0],
                  ['{}_{}_hand{}_guide'.format(char_name, limb_name[1].upper(), limb_name[-2:]), 2.5, 0]]

    joint_list_finger = [['{}_{}_thumb{}_guide'.format(char_name, limb_name[1].upper(), limb_name[-2:]), 0, 0],
                      ['{}_{}_index{}_guide'.format(char_name, limb_name[1].upper(), limb_name[-2:]), 2, 0],
                      ['{}_{}_middle{}_guide'.format(char_name, limb_name[1].upper(), limb_name[-2:]), 10, 0],
                      ['{}_{}_ring{}_guide'.format(char_name, limb_name[1].upper(), limb_name[-2:]), 100, 10],
                      ['{}_{}_pinky{}_guide'.format(char_name, limb_name[1].upper(), limb_name[-2:]), 100, 6]]

    final_position = None

    for index, item in enumerate(joint_list_arm):
        sphere_name = cmds.sphere(name='{}'.format(item[0]), r=1)[0]
        shader, shading_group = utili.create_shader_guide()
        shape = cmds.listRelatives(sphere_name, shapes=True, fullPath=True)[0]
        cmds.sets(shape, edit=True, forceElement=shading_group)

        final_position = [(cmds.getAttr('heightDistance.distance') / 25.0),
                          cmds.getAttr('heightDistance.distance') / 1.27,
                          cmds.getAttr('heightDistance.distance')/item[1] if item[1] != 0 else 0]

        cmds.move(final_position[0],
                  final_position[1],
                  final_position[2],
                  sphere_name)

        # Create annotation
        annotate = cmds.annotate(item[0], tx='{}'.format("_".join(item[0].split("_")[1:])),
                                 p=(final_position[0],
                                    final_position[1] if rebuild == True else final_position[1] + final_position[1] / 30,
                                    final_position[2]))
        annotate_transform = cmds.listRelatives(annotate, parent=True)[0]
        cmds.parent(annotate_transform, item[0])

        # Set annotation color
        cmds.setAttr(annotate + '.overrideEnabled', 1)
        cmds.setAttr(annotate + '.overrideColor', 6)

    ui_autorig._nested_dict_instance.update_limb(char_name=char_name, limb_name=limb_name,
                                                 parent=limb_connection,
                                                 list=['{}_clav{}'.format(limb_name[1], limb_name[-2:]),
                                                       '{}_upperarm{}'.format(limb_name[1], limb_name[-2:]),
                                                       '{}_lowerarm{}'.format(limb_name[1], limb_name[-2:]),
                                                       '{}_wrist{}'.format(limb_name[1], limb_name[-2:]),
                                                       '{}_hand{}'.format(limb_name[1], limb_name[-2:])], suffix='guide',
                                                 kinematic_mode=kinematic, limb_end=limb_end_leg, limb_type=leg_type)


def controller_hand_build():
    return 0