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


utili.createSimpleFkController(align = 'z',size = 5,shape = 'circle')


## get the point in between 2 objects
utili.get_midpoint(position1='head01_guide', position2='neck01_guide')
	
### controller color
utili.colorObject(color=6) #left
utili.colorObject(color=4) #right
utili.colorObject(color=17) #center
utili.colorObject(color=18) #face general controller
utili.colorObject(color=16) #face second controller
utili.colorObject(color=11) #chest ik controller


utili.colorObject(color=7) #sub left


utili.colorObject(color=8) #sub right

### control visibility
utili.visibilitySwitch(targetCtrl = 'Max_r_tentacle4_27_end_ctrl',targetVariable = 'ribbon_detail_ctrl')

utili.visibilitySwitch(targetCtrl = 'Max_c_pelvis01_jnt_fk_ctrl',targetVariable = 'ribbon_detail_ctrl')



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

###____________________ MOVING NURB PLANE FOR MOUTH AND ADJUSTING BASE OFFSET NUMBER FOR EACH JNT _______________

import maya.cmds as cmds
name = 'Max'
selected = cmds.ls(sl=True)
#lets create the locator to get position offset 
loc = cmds.spaceLocator(absolute=True, name='guide_loc')[0]
loc_closestPointOnSurface = cmds.createNode('closestPointOnSurface',n='{}_closestPointOnSurface_del'.format(loc))

cmds.connectAttr('{}.translate'.format(loc), '{}.inPosition'.format(loc_closestPointOnSurface))
cmds.connectAttr('{}.worldSpace[0]'.format('{}_mouth_surface'.format(name)),'{}.inputSurface'.format(loc_closestPointOnSurface))


### we disconect all befo changing the shape of the nurbsurface
for item in selected:
    print(item)
    cmds.disconnectAttr('Max_mouth_surfaceShape.worldSpace[0]','{}_pointOnSurfaceInfo.inputSurface'.format(item))
    

for item in selected:
    print(item)
    
    #from here lets add the offset for the joints base on the surface using this locator as a dummy guide
    cmds.delete(cmds.pointConstraint(item,loc))
    u_value = cmds.getAttr('{}.parameterU'.format(loc_closestPointOnSurface))
    v_value = cmds.getAttr('{}.parameterV'.format(loc_closestPointOnSurface))

    positions = cmds.getAttr('{}.result.position'.format(loc_closestPointOnSurface))[0]

    [cmds.setAttr('{}_plusMinusAverageEnd.input3D[1].input3D{}'.format(item,axis),positions[i]) for i,axis in enumerate('xyz')]

    cmds.setAttr('{}_plusMinusAverageStart.input2D[0].input2Dx'.format(item), u_value)
    cmds.setAttr('{}_plusMinusAverageStart.input2D[0].input2Dy'.format(item), v_value)

    cmds.connectAttr('{}.worldSpace[0]'.format('{}_mouth_surface'.format(name)),'{}_pointOnSurfaceInfo.inputSurface'.format(item))

###____________________ END
###____________________ FUNCTION TO RENAME OBJECT OR HIRARCHY SELECTED __________________

import maya.cmds as cmds
selected = cmds.ls(sl=True)
char_name = 'Max'
portion = 'sechair05'
object_type = 'jnt'
#this mini function will check for the entire hirarcky to change the name if only one object was selected.
if len(selected) == 1:
    cmds.select( selected, hi=True )
    selected = cmds.ls(sl=True)   
for i,item in enumerate(selected):
    print('{}_{}_{}{:02d}'.format(char_name,item,portion,i))
    cmds.rename(item,'{}_{}_{:02d}_{}'.format(char_name,portion,i,object_type))
###____________________ END


###____________________ HAIR_TOOL for joint creating naming and orientation(cluster is required) __________________
import maya.cmds as cmds
selected = cmds.ls(sl=True)
char_name = 'Max'
portion = 'single_hair01'
object_type = 'jnt'
#this mini function will check for the entire hirarcky to change the name if only one object was selected.
for i,item in enumerate(selected):
    cmds.select(clear=True)
    jnt =cmds.joint(name = '{}_{}_{:02d}_{}'.format(char_name,portion,i,object_type), component = False, rad = 0.5)
    cmds.delete(cmds.parentConstraint(item ,jnt,maintainOffset = False))
    if i != 0:
        cmds.parent(jnt,'{}_{}_{:02d}_{}'.format(char_name,portion,i-1,object_type))
        
cmds.joint( '{}_{}_{:02d}_{}'.format(char_name,portion,0,object_type), e=True, zso=True, oj='xyz',ch = True, secondaryAxisOrient = 'xup')
cmds.joint( '{}_{}_{:02d}_{}'.format(char_name,portion,len(selected)-1,object_type), e=True, oj='none', zeroScaleOrient = True)
###____________________ END
###____________________ FIXING LOCAL TRANSLATION AFTER CHANGING MANUALY LOCAL ROTATION (CGANT ) 
selected = cmds.ls(sl=True)                   
cmds.joint(selected, edit=True,zeroScaleOrient=True )   
###____________________ END
###__ADDING SCALE FEATURE r TO THE BIPED RIG
import maya.cmds as cmds
selected = cmds.ls(sl=True)
char_name = 'Max'
listTorso = ['c_spine01_jnt','c_spine02_jnt','c_spine03_jnt','c_spine04_jnt','c_spine05_jnt','c_chest01_jnt'] 
listLeg = ['knee01_jnt','knee02_jnt','foot01_jnt']
listArm = ['elbo01_jnt','elbo02_jnt','wrist01_jnt']
char_name = 'Max'




#torso
for item in listTorso:
    cmds.disconnectAttr('curveInfo1.arcLength','{}_{}_ik_translateX.input'.format(char_name,item))
    multiplydivide = cmds.createNode('multiplyDivide', n='{}_{}_multiplyDivide_scale'.format(char_name, item))
    cmds.setAttr('{}.operation'.format(multiplydivide),2)
    cmds.connectAttr('curveInfo1.arcLength','{}.input1.input1X'.format(multiplydivide))
    cmds.connectAttr('Max_trs_ctrl.scale.scaleX','{}.input2.input2X'.format(multiplydivide))
    cmds.connectAttr('{}.output.outputX'.format(multiplydivide),'{}_{}_ik_translateX.input'.format(char_name,item))
#arms
for side in ('l','r'):
    for item in listArm:
        cmds.disconnectAttr('Max_{}_should01_jnt_DistShape.distance'.format(side),'{}_{}_{}_ik_translateX.input'.format(char_name,side,item))
        multiplydivide = cmds.createNode('multiplyDivide', n='{}_{}_multiplyDivide_scale'.format(char_name, item))
        cmds.setAttr('{}.operation'.format(multiplydivide),2)
        cmds.connectAttr('Max_{}_should01_jnt_DistShape.distance'.format(side),'{}.input1.input1X'.format(multiplydivide))
        cmds.connectAttr('Max_trs_ctrl.scale.scaleX','{}.input2.input2X'.format(multiplydivide))
        cmds.connectAttr('{}.output.outputX'.format(multiplydivide),'{}_{}_{}_ik_translateX.input'.format(char_name,side,item))
        
        if side == 'r':
            cmds.disconnectAttr('{}_{}_{}_ik_DistShape.distance'.format(char_name,side,item),'{}_{}_{}_ik_multiplyDivide.input1.input1X'.format(char_name,side,item))
            multiplydivide_bc = cmds.createNode('multiplyDivide', n='{}_{}_multiplyDivide_bc_scale'.format(char_name, item))
            cmds.setAttr('{}.operation'.format(multiplydivide_bc),2)
            cmds.connectAttr('{}_{}_{}_ik_DistShape.distance'.format(char_name,side,item),'{}.input1.input1X'.format(multiplydivide_bc))
            cmds.connectAttr('Max_trs_ctrl.scale.scaleX','{}.input2.input2X'.format(multiplydivide_bc))
            #multiplydivide_bc_r = cmds.createNode('multiplyDivide', n='{}_{}_multiplyDivide_bc_rside_scale'.format(char_name, item))
            cmds.connectAttr('{}.output.outputX'.format(multiplydivide_bc),'{}_{}_{}_ik_multiplyDivide.input1.input1X'.format(char_name,side,item))
            #cmds.setAttr('{}.input2X'.format(multiplydivide_bc_r),-1)
            #cmds.connectAttr('{}.output.outputX'.format(multiplydivide_bc_r),'{}_{}_{}_ik_blendColor.color1R'.format(char_name,side,item))
        else:
            cmds.disconnectAttr('{}_{}_{}_ik_DistShape.distance'.format(char_name,side,item),'{}_{}_{}_ik_blendColor.color1R'.format(char_name,side,item))
            multiplydivide_bc = cmds.createNode('multiplyDivide', n='{}_{}_multiplyDivide_bc_scale'.format(char_name, item))
            cmds.setAttr('{}.operation'.format(multiplydivide_bc),2)
            cmds.connectAttr('{}_{}_{}_ik_DistShape.distance'.format(char_name,side,item),'{}.input1.input1X'.format(multiplydivide_bc))
            cmds.connectAttr('Max_trs_ctrl.scale.scaleX','{}.input2.input2X'.format(multiplydivide_bc))
            cmds.connectAttr('{}.output.outputX'.format(multiplydivide_bc),'{}_{}_{}_ik_blendColor.color1R'.format(char_name,side,item))
        
#legs
for side in ('l','r'):
    for item in listLeg:
        cmds.disconnectAttr('Max_{}_upperLeg01_jnt_ik_DistShape.distance'.format(side),'{}_{}_{}_ik_pullvector_translateX.input'.format(char_name,side,item))
        multiplydivide = cmds.createNode('multiplyDivide', n='{}_{}_multiplyDivide_scale'.format(char_name, item))
        cmds.setAttr('{}.operation'.format(multiplydivide),2)
        cmds.connectAttr('Max_{}_upperLeg01_jnt_ik_DistShape.distance'.format(side),'{}.input1.input1X'.format(multiplydivide))
        cmds.connectAttr('Max_trs_ctrl.scale.scaleX','{}.input2.input2X'.format(multiplydivide))
        cmds.connectAttr('{}.output.outputX'.format(multiplydivide),'{}_{}_{}_ik_pullvector_translateX.input'.format(char_name,side,item))
        
        if side == 'r':
            cmds.disconnectAttr('{}_{}_{}_ik_pullvector_DistShape.distance'.format(char_name,side,item),'{}_{}_{}_ik_pullvector_multiplyDivide.input1.input1X'.format(char_name,side,item))
            multiplydivide_bc = cmds.createNode('multiplyDivide', n='{}_{}_multiplyDivide_bc_scale'.format(char_name, item))
            cmds.setAttr('{}.operation'.format(multiplydivide_bc),2)
            cmds.connectAttr('{}_{}_{}_ik_pullvector_DistShape.distance'.format(char_name,side,item),'{}.input1.input1X'.format(multiplydivide_bc))
            cmds.connectAttr('Max_trs_ctrl.scale.scaleX','{}.input2.input2X'.format(multiplydivide_bc))
            #multiplydivide_bc_r = cmds.createNode('multiplyDivide', n='{}_{}_multiplyDivide_bc_rside_scale'.format(char_name, item))
            cmds.connectAttr('{}.output.outputX'.format(multiplydivide_bc),'{}_{}_{}_ik_pullvector_multiplyDivide.input1.input1X'.format(char_name,side,item))
            #cmds.setAttr('{}.input2X'.format(multiplydivide_bc_r),-1)
            #cmds.connectAttr('{}.output.outputX'.format(multiplydivide_bc_r),'{}_{}_{}_ik_blendColor.color1R'.format(char_name,side,item))
        else:
            cmds.disconnectAttr('{}_{}_{}_ik_pullvector_DistShape.distance'.format(char_name,side,item),'{}_{}_{}_ik_pullvector_blendColor.color1R'.format(char_name,side,item))
            multiplydivide_bc = cmds.createNode('multiplyDivide', n='{}_{}_multiplyDivide_bc_scale'.format(char_name, item))
            cmds.setAttr('{}.operation'.format(multiplydivide_bc),2)
            cmds.connectAttr('{}_{}_{}_ik_pullvector_DistShape.distance'.format(char_name,side,item),'{}.input1.input1X'.format(multiplydivide_bc))
            cmds.connectAttr('Max_trs_ctrl.scale.scaleX','{}.input2.input2X'.format(multiplydivide_bc))
            cmds.connectAttr('{}.output.outputX'.format(multiplydivide_bc),'{}_{}_{}_ik_pullvector_blendColor.color1R'.format(char_name,side,item))                   
        

### eyesocket 
multiplydivide_bc_eyesocket = cmds.createNode('multiplyDivide', n='{}_{}_multiplyDivide_eyesocket'.format(char_name, item))
cmds.connectAttr('{}.output'.format(multiplydivide_bc_eyesocket),'{}_l_eyesock_jnt_scaleConstraint1.offset'.format(char_name))
cmds.connectAttr('{}.output'.format(multiplydivide_bc_eyesocket),'{}_r_eyesock_jnt_scaleConstraint1.offset'.format(char_name))

