import maya.cmds as cmds
import pyTool.modular_py_tool.auto_Rig_UI as auto_rig_ui
import pyTool.utilities as utili
import importlib

import os
import json
import math
import sys

importlib.reload(auto_rig_ui)
importlib.reload(utili)

auto_rig_ui.modular_ui()


#calculate height character

distance_shape  = cmds.distanceDimension( sp=(0, 0, 0), ep=(0,2,0) )
transform_node = cmds.listRelatives(distance_shape , parent=True)[0]
locators = cmds.listConnections(distance_shape , type='locator')

cmds.rename(transform_node,'heightDistance')
for i,loc in enumerate(locators):
    if i == 0:
        cmds.rename(loc,'heightLocA')
    else:
        cmds.rename(loc,'heightLocB')
        
emptyGrp = utili.createEmptyGroup(name='height')
[cmds.parent(object1,emptyGrp) for object1 in ('heightDistance','heightLocA','heightLocB')]
