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


utili.createSimpleFkController()


	
### controller color
utili.colorObject(color=6) #left
utili.colorObject(color=4) #right
utili.colorObject(color=17) #center

### control visibility
utili.visibilitySwitch(targetCtrl = 'Max_c_pelvis01_jnt_fk_ctrl',targetVariable = 'FreeSpineControls')
utili.visibilitySwitch(targetCtrl = 'Max_c_pelvis01_jnt_fk_ctrl',targetVariable = 'ikblend',direct= 'ik',reverse='fk')

