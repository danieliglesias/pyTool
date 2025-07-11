import maya.cmds as cmds
import os
import json

import pyTool.modular_py_tool.auto_rig_fundation as fundation
import pyTool.modular_py_tool.Utilities as utili
import pyTool.modular_py_tool.FileClass as FileClass

import importlib
importlib.reload(fundation)
importlib.reload(utili)
importlib.reload(FileClass)


def CreateBasicRigStructure(character_name='Character'):


    # Top group
    root_grp = cmds.group(em=True, name=f'{character_name}_Root_GRP')

    # Sub groups
    geo_grp         = cmds.group(em=True, name='GEO_GRP', parent=root_grp)
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


def type_rig_option_menu_change(type = None,char_name = None):

    #check for character name

    #lets create basic structure

    #game
    if type == 'Game':
        CreateBasicRigStructure(char_name)
        guide = cmds.sphere(radius=1, name='{}_root_guide'.format(char_name))



    print(type)


def ToolBasicSetup(rig_type = None):

    if rig_type == 'Game':
    #create a guide in 0,0,0 of the esene


        return 0