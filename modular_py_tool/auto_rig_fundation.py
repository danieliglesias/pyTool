import maya.cmds as cmds
import os
import json

import modular_py_tool.UiAutoRig as auto_rig_ui
import modular_py_tool.Utilities as utili
import modular_py_tool.FileClass as FileClass

import importlib
importlib.reload(auto_rig_ui)
importlib.reload(utili)
importlib.reload(FileClass)


def CreateBasicRigStructure(char_name='Character'):


    # Top group
    root_grp = cmds.group(em=True, name=f'{character_name}_Root_GRP')

    # Sub groups
    geo_grp         = cmds.group(em=True, name='GEO_GRP', parent=root_grp)
    move_geometry_to_group(geo_grp)
    rig_grp         = cmds.group(em=True, name='RIG_GRP', parent=root_grp)
    jnt_grp         = cmds.group(em=True, name='JNT_GRP', parent=rig_grp)
    ik_grp          = cmds.group(em=True, name='IK_GRP', parent=rig_grp)
    fk_grp          = cmds.group(em=True, name='FK_GRP', parent=rig_grp)
    constraint_grp  = cmds.group(em=True, name='CONSTRAINT_GRP', parent=rig_grp)

    ctrl_grp        = cmds.group(em=True, name='CTRL_GRP', parent=root_grp)
    #main_ctrl       = cmds.circle(name='Main_CTRL', normal=[1, 0, 0], radius=5)[0]
    main_ctrl       = utili.createController(name='{}_root'.format(character_name), character_name=None, shape='circle', target=None, contraint_target=None,
                         facing='y',type='simple', size='root')

    cmds.parent('{}_root_off'.format(character_name), ctrl_grp)

    body_ctrls_grp  = cmds.group(em=True, name='Body_CTRLs_GRP', parent=ctrl_grp)
    limb_ctrls_grp  = cmds.group(em=True, name='Limb_CTRLs_GRP', parent=ctrl_grp)

    util_grp        = cmds.group(em=True, name='UTIL_GRP', parent=root_grp)
    no_touch_grp    = cmds.group(em=True, name='NO_TOUCH_GRP', parent=root_grp)


def type_rig_option_menu_change(type_rig = None,char_name = None):

    #auto_rig_ui._nested_dict_instance.update_limb(limb_name='general', list=['spine', 'chest'], suffix='jnt')

    #game
    if type_rig == 'Game':
        CreateBasicRigStructure(char_name)
        #guide = cmds.sphere(radius=1, name='{}_root_guide'.format(char_name))\
        cmds.select(clear=True)
        jnt = cmds.joint(p=[0,0,0], name='{}_root_jnt'.format(char_name))
    



    auto_rig_ui._nested_dict_instance.update_limb(limb_name='fundation',parent = type_rig, list=['root'], suffix='jnt')


def ToolBasicSetup(rig_type = None):

    if rig_type == 'Game':
    #create a guide in 0,0,0 of the esene


        return 0



def move_geometry_to_group(group_name):
    # Find all mesh shape nodes
    geometry = cmds.ls(type='mesh', long=True)
    if not geometry:
        print('No geometry found.')
        return

    # Get the parent transform nodes of each mesh shape
    geometry_transforms = list(set(cmds.listRelatives(geometry, parent=True, fullPath=True)))

    # Create the group if it doesn't exist
    if not cmds.objExists(group_name):
        group_name = cmds.group(empty=True, name=group_name)

    # Parent each geometry transform under the group
    for geo in geometry_transforms:
        try:
            cmds.parent(geo, group_name)
        except RuntimeError:
            print('Could not parent {} (may cause cycle or already parented)'.format(geo))

    print('Moved {} geometries to group \'{}\'.'.format(len(geometry_transforms), group_name))
