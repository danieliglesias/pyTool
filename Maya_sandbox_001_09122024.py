import maya.cmds as cmds
import pyTool.autoTentaclesUi as autoTen
import pyTool.utilities as utili
import pyTool.facialRigUI as faceUi
import pyTool.facialRig as face
import importlib
import os
import json
import math
import sys

importlib.reload(face)
importlib.reload(faceUi)
importlib.reload(utili)
importlib.reload(autoTen)


cmds.orientConstraint('Max_r_eyeball_jnt', 'Max_r_global_eyelit_upp_ctrl_off_constrain')
cmds.aimConstraint('Max_l_eyeball_jnt', 'Max_l_global_eyelit_low_ctrl_off_constrain', aimVector=[0, 0, -1], upVector=[0, 1, 0], worldUpType='objectrotation',worldUpVector=[0, 1, 0], worldUpObject='Max_r_eyeball_jnt')

#utili.createSimpleFkController(ctrlsize = 20)
#autoTen.tentacle_ui()
faceUi.face_ui()
face.build_face_guide()
face.build_face_structure(name = 'Max')
face.save_mainstructure_guide(name = 'Max',guide_type = 'selected')

cmds.select(clear=True)

autoTen.tentacle_ui()

utili.createRibbonSystem(name = 'test')

utili.build_struct_outliner(name='octopus')


utili.createSimpleFkController(align = 'z')


## get the point in between 2 objects
utili.get_midpoint(position1='head01_guide', position2='neck01_guide')
	
### controller color
utili.colorObject(color=6) #left
utili.colorObject(color=4) #right
utili.colorObject(color=17) #center
utili.colorObject(color=18) #face general controller
utili.colorObject(color=16) #face second controller
utili.colorObject(color=13) #chest ik controller


### control visibility
utili.visibilitySwitch(targetCtrl = 'Max_c_pelvis01_jnt_fk_ctrl',targetVariable = 'FreeSpineControls')
utili.visibilitySwitch(targetCtrl = 'Max_c_pelvis01_jnt_fk_ctrl',targetVariable = 'ikblend',direct= 'ik',reverse='fk')

selection = cmds.ls(sl=True)

print(selection)

for item in selection:
    cmds.setAttr('{}.visibility'.format(item), lock=0)

utili.visibilitySwitch(targetCtrl = 'Max_l_arm_main_ctrl',targetVariable = 'FreeArmControls')
utili.visibilitySwitch(targetCtrl = 'Max_r_arm_main_ctrl',targetVariable = 'FreeArmControls')


utili.visibilitySwitch(targetCtrl = 'Max_l_arm_main_ctrl',targetVariable = 'ikblend',direct= 'ik',reverse='fk')
utili.visibilitySwitch(targetCtrl = 'Max_r_arm_main_ctrl',targetVariable = 'ikblend',direct= 'ik',reverse='fk')

utili.visibilitySwitch(targetCtrl = 'Max_l_arm_main_ctrl',targetVariable = 'FreeElbo')
utili.visibilitySwitch(targetCtrl = 'Max_r_arm_main_ctrl',targetVariable = 'FreeElbo')

###LEG

utili.visibilitySwitch(targetCtrl = 'Max_l_leg_main_ctrl',targetVariable = 'FreeLegControls')
utili.visibilitySwitch(targetCtrl = 'Max_r_leg_main_ctrl',targetVariable = 'FreeLegControls')


utili.visibilitySwitch(targetCtrl = 'Max_l_leg_main_ctrl',targetVariable = 'ikblend',direct= 'ik',reverse='fk')
utili.visibilitySwitch(targetCtrl = 'Max_r_leg_main_ctrl',targetVariable = 'ikblend',direct= 'ik',reverse='fk')

utili.visibilitySwitch(targetCtrl = 'Max_l_leg_main_ctrl',targetVariable = 'LockKnee')
utili.visibilitySwitch(targetCtrl = 'Max_r_leg_main_ctrl',targetVariable = 'LockKnee')


### aim join back (for cheek for example)
cmds.delete(cmds.aimConstraint('Max_facelow_jnt', 'Max_r_cheek2_jnt' , aimVector = [0 ,0,-1], upVector = [0,1,0],worldUpType = 'objectrotation',worldUpVector = [0,1,0],worldUpObject = 'Max_facelow_jnt'))

### adding mesh to a mesh retaining the smooth skinning

cmds.polyUniteSkinned( 'Body', 'L_Shoes', ch=0 )

