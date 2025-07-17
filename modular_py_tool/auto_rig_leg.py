import maya.cmds as cmds
import modular_py_tool.Utilities as utili
import modular_py_tool.UiAutoRig as ui_autorig

import importlib
importlib.reload(utili)
importlib.reload(ui_autorig)

def controller_leg_guide(char_name = None,rebuild = False,limb_name = None,leg_type = None, limb_connection = None, kinematic_mode = None, limb_end = None):

    if kinematic_mode[0] == True:
        kinematic = 'ikfk'
    else:
        kinematic = 'fk'
    if limb_end[0] == True:
        limb_end_leg = True
    else:
        limb_end_leg = False

    print('Here we enter the controller guide //// {}'.format(limb_name))
    print('leg type:  {}'.format(leg_type))
    print('limb conection:  {}'.format(limb_connection))
    print('ikfk value? {}'.format(kinematic_mode))
    print('Include leg? {}'.format(limb_end))



    ### [0] name, [1] Y offset, [2] Z offset
    joint_list = [['{}_upperleg{}_guide'.format(limb_name[1],limb_name[-2:]),0,0],
                  ['{}_lowerleg{}_guide'.format(limb_name[1],limb_name[-2:]),2,0],
                  ['{}_ankle{}_guide'.format(limb_name[1],limb_name[-2:]),10,0],
                  ['{}_ball{}_guide'.format(limb_name[1],limb_name[-2:]),100,10],
                  ['{}_toe{}_guide'.format(limb_name[1],limb_name[-2:]),100,6]]


    final_position = None

    for index, item in enumerate(joint_list):
        sphere_name = cmds.sphere(name='{}'.format(item[0]), r=1)[0]
        shader, shading_group = utili.create_shader_guide()
        shape = cmds.listRelatives(sphere_name, shapes=True, fullPath=True)[0]
        cmds.sets(shape, edit=True, forceElement=shading_group)

        if rebuild == True:
            final_position = ui_autorig._nested_dict_instance.data[limb_name]['general']['position']
            cmds.move( final_position ,sphere_name)
        else:
            final_position = [(cmds.getAttr('heightDistance.distance') / 25.0),
                              (cmds.getAttr('heightDistance.distance') / 2.0)/ item[1] if item[1] != 0 else (cmds.getAttr('heightDistance.distance') / 2.0),
                              (cmds.getAttr('heightDistance.distance') / 2.0)/ item[2] if item[2] != 0 else 0]
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
    ui_autorig._nested_dict_instance.update_limb(limb_name=limb_name,
                                                 parent=limb_connection,
                                                 list=['{}_upperleg{}'.format(limb_name[1],limb_name[-2:]),
                                                       '{}_lowerleg{}'.format(limb_name[1],limb_name[-2:]),
                                                       '{}_ankle{}'.format(limb_name[1],limb_name[-2:]),
                                                       '{}_ball{}'.format(limb_name[1],limb_name[-2:]),
                                                       '{}_toe{}'.format(limb_name[1],limb_name[-2:])], suffix='guide',
                                                 kinematic_mode = kinematic, limb_end = limb_end_leg,limb_type = leg_type)

def controller_leg_jnt(char_name = None,limb_name = None,leg_type = None, limb_connection = None, ikfk = None, leg = None):

    print('Here we enter the controller jnt //// {}'.format(limb_name))
    print('leg type:  {}'.format(leg_type))
    print('limb conection:  {}'.format(limb_connection))
    print('ikfk value? {}'.format(ikfk))
    print('Include leg? {}'.format(leg))
