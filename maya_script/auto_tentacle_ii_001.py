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
name = 'Max'
mainjoint = 'center_jnt'
spacing = 45.0
midpos = 13
lastpos = 27

for i in range(2, (int(int(midpos) / 2))):
    print(i)

listGuide = cmds.ls(sl=True)

side = 'l'
x = 1



loc = cmds.spaceLocator(absolute=True, name='{}_{}_{}_loc'.format(name, side, x))







cmds.delete(cmds.parentConstraint(mainjoint, loc))
curve_list = []
for i, guide in enumerate(listGuide):
    if i <= int(lastpos) - 1:
        jnt = cmds.joint(name='{}_{}_tentacle{}_{:02d}_joint'.format(name, side, x, (i + 1)))
        cmds.delete(cmds.pointConstraint(guide, jnt))
    if i >= int(lastpos) - 1:
        jnt_fk = cmds.joint(name='{}_{}_tentacle{}_{:02d}_joint_def'.format(name, side, x, (i + 1)))
        cmds.delete(cmds.pointConstraint(guide, jnt_fk))

    if (i + 1) <= int(lastpos):
        curve_list.append(jnt)

cmds.joint('{}_{}_tentacle{}_01_joint'.format(name, side, x), edit=True, zso=True, oj='xyz',
           secondaryAxisOrient='yup', children=True)
cmds.joint('{}_{}_tentacle{}_{}_joint_def'.format(name, side, x, len(listGuide)), edit=True, oj='none',
           children=True, zso=True)
           

           
cv_curve_list = []
for i,item in enumerate(curve_list):
    if (i+1) % 2 != 0:
        cv_curve_list.append(item)
positions = [cmds.xform(obj, q=True, ws=True, translation=True) for obj in cv_curve_list]



# LETS CREATE A CURVE
tentacle_curve = cmds.curve(d=3, p=positions, name='{}_{}_tentacle{}_curve'.format(name, side, x))
##parenting the curve will multiply transformation
# cmds.parent(curve, loc)

###creating joint controller and ik handle
# lets create 3 joint
ik_list = ['{}_{}_tentacle{}_{}_joint'.format(name, side, x, obj) for obj in
           ('01_sta','{:02d}_sub'.format(int(midpos/2)+1) ,'{:02d}_mid'.format(int(midpos)),'{:02d}_bet'.format(int(midpos + ((lastpos-midpos)/2))-1), '{:02d}_end'.format((lastpos)))]



for i, item in enumerate(ik_list):
    cmds.select(clear=True)
    jnt_ctrl = cmds.joint(name=item, component=False)
    cmds.delete(cmds.parentConstraint('{}_joint'.format(item[:-10]), jnt_ctrl, maintainOffset=False))
    cmds.setAttr('{}.radius'.format(jnt_ctrl), 2)
    cmds.parent(jnt_ctrl, loc)
    ctrl = utili.createController(name='{}'.format(item[:-6]), shape='square', target=jnt_ctrl,
                                  contraint_target=None, facing='x',
                                  offsetnumber=2,
                                  type='fk', size=7 - (i *0.5))
    cmds.parent('{}_off'.format(ctrl), loc)
# skin controller joints to the curve


cmds.skinCluster(ik_list, curve, tsb=True, name='{}_{}_tentacle{}_skincluster'.format(name, side, x))


"""ik_handle = cmds.ikHandle(n='{}_{}_tentacle{}_ikhandle'.format(name, side, x),
                          sj='{}_{}_tentacle{}_01_joint'.format(name, side, x),
                          ee='{}_{}_tentacle{}_{}_joint'.format(name, side, x, int(lastpos)),
                          curve=curve, solver='ikSplineSolver', createCurve=False, parentCurve=False,
                          numSpans=3)[0]
"""
# cmds.parent(ik_handle, loc)
# here we create the fk controllers for the tip of the tentacles
list_fk = ['{}_{}_tentacle{}_{:02d}_joint_def'.format(name, side, x, int(i)) for i in
           range(int(lastpos)+1, len(listGuide))]
           )

for i, item in enumerate(list_fk):
    ctrl = utili.createController(name='{}'.format(item[:-10]), shape='circle', target=item,
                                  contraint_target=None,
                                  facing='x',
                                  offsetnumber=2,
                                  type='fk', size=4.5 - (i * 0.4))
    # here we group the controllers of the fk controller
    if i >= 1:
        cmds.parent('{}_off'.format(ctrl), '{}_ctrl'.format((list_fk[i - 1])[:-10]))


cmds.parent('{}_{}_tentacle{}_{:02d}_ctrl_off'.format(name, side, x, (int(lastpos)+1)), loc)
cmds.parentConstraint(ik_list[-1], '{}_{}_tentacle{}_{:02d}_ctrl_off'.format(name, side, x, (int(lastpos)+1)),
                      maintainOffset=True)
"""
arc1 = cmds.arclen(curve)
cmds.setAttr('{}_ctrl.translateX'.format((ik_list[2])[:-6]), 20)
arc2 = cmds.arclen(curve)
cmds.setAttr('{}_ctrl.translateX'.format((ik_list[2])[:-6]), 0)

arc = cmds.arclen(curve, ch=True, n='{}_{}_tentacle{}_curveinfo'.format(name, side, x))
set_driven_key_tentacles(curve_list, ('{}_ctrl'.format((ik_list[2])[:-6])), 0, arc, curve, 0)
set_driven_key_tentacles(curve_list, ('{}_ctrl'.format((ik_list[2])[:-6])), 20, arc, curve, (arc2 - arc1))
"""
# NOW WE CREATE THE RIBBON SYSTEM
# we may want to customise more this funtion later for other tools
listRibbonJnt = ['{}_{}_tentacle{}_{:02d}_joint'.format(name, side, x, int(i)) for i in
                 range(1, int(lastpos) + 1)]
                 
         
                 
ribbon = utili.createRibbon(list=listRibbonJnt, name='{}_{}_tentacle{}'.format(name, side, x),
                   target=('{}_ctrl'.format((ik_list[1])[:-6])),
                   sta_ctrl='{}_ctrl'.format((ik_list[0])[:-6]), mid_ctrl='{}_ctrl'.format((ik_list[1])[:-6]),
                   end_ctrl='{}_ctrl'.format((ik_list[2])[:-6]),
                   midpos=midpos,u_parches = 28)
                
###let wire the curve to the ribbon system
#wire -gw false -en 1.000000 -ce 0.000000 -li 0.000000 -dds 0 50 -w Max_l_tentacle1_curve Max_l_tentacle1_ribbon; 

cmds.wire(ribbon,w=tentacle_curve,dds=[(0, 50)])
                  
##LETS WORK ON ROTATIONS


ik_list = ['{}_{}_tentacle{}_{}_joint'.format(name, side, x, obj) for obj in
           ('01_sta','{:02d}_sub'.format(int(midpos/2)+1) ,'{:02d}_mid'.format(int(midpos)),'{:02d}_bet'.format(int(midpos + ((lastpos-midpos)/2))-1), '{:02d}_end'.format((lastpos)))]
ik_list = [('01_sta'),('{:02d}_sub'.format(int(midpos/2)+1)),('{:02d}_mid'.format(int(midpos))),('{:02d}_bet'.format(int(midpos + ((lastpos-midpos)/2))-1)),('{:02d}_end'.format((lastpos)))]


for i, item in enumerate(listGuide):
    if (i+1) % 2 != 0 and i+1 <= lastpos: 
        animBlendNodeAdditiveRotation = cmds.createNode('animBlendNodeAdditiveRotation', n='{}_{}_tentacle{}_animBlendNodeAdditiveRotation{:02d}'.format(name, side, x,(i+1)))    
        cmds.connectAttr('{}.output.outputX'.format(animBlendNodeAdditiveRotation),'{}_{}_tentacle{}_ribbon_ribbon_{:02d}_joint_def_ctrl_off.rotate.rotateX'.format(name, side, x,(i+1)),force = True)
    

for i,item in enumerate(ik_list):      
    if i == 0:
        for i in range(2 ,(int(midpos/2))):
            if (i+1) % 2 != 0:
                multiplyDivide = cmds.createNode('multiplyDivide',n='{}_{}_tentacle{}_multiplyDivide{:02d}'.format(name, side, x,(i+1)))
                cmds.connectAttr('{}.outputX'.format(multiplyDivide),'{}_{}_tentacle{}_animBlendNodeAdditiveRotation{:02d}.inputAX'.format(name, side, x,(i+1)))
                cmds.connectAttr('tentacle_rotation_guide.sta_{:02d}'.format((i+1)),'{}.input2X'.format(multiplyDivide))
                cmds.connectAttr('{}_{}_tentacle{}_{:02d}_sta_ctrl.rotateX'.format(name, side, x, 1),'{}.input1X'.format(multiplyDivide))
             
    if i == 1:
        cmds.connectAttr('{}_{}_tentacle{}_{:02d}_sub_ctrl.rotate.rotateX'.format(name, side, x, (int(midpos/2)+1)),'{}_{}_tentacle{}_animBlendNodeAdditiveRotation{}.inputB.inputBX'.format(name, side, x,item[:2]))
        for i in range(2 ,midpos-1):
            if (i+1) % 2 != 0 and (i+1) != (int(midpos/2)+1):
                print(i+1)
                multiplyDivide = cmds.createNode('multiplyDivide',n='{}_{}_tentacle{}_multiplyDivide{:02d}'.format(name, side, x,(i+1)))
                cmds.connectAttr('{}.outputX'.format(multiplyDivide),'{}_{}_tentacle{}_animBlendNodeAdditiveRotation{:02d}.inputBX'.format(name, side, x,(i+1)))
                cmds.connectAttr('tentacle_rotation_guide.sub_{:02d}'.format((i+1)),'{}.input2X'.format(multiplyDivide))
                cmds.connectAttr('{}_{}_tentacle{}_{:02d}_sub_ctrl.rotateX'.format(name, side, x, (int(midpos/2)+1)),'{}.input1X'.format(multiplyDivide))
                     
    if i == 2:
        cmds.connectAttr('{}_{}_tentacle{}_{:02d}_mid_ctrl.rotate.rotateX'.format(name, side, x, midpos),'{}_{}_tentacle{}_animBlendNodeAdditiveRotation{}.inputA.inputAX'.format(name, side, x,item[:2]))
        for i in range((int(midpos/2)+1) ,(int(midpos + ((lastpos-midpos)/2))-2)):
            if (i+1) % 2 != 0 and (i+1) != midpos:
                multiplyDivide = cmds.createNode('multiplyDivide',n='{}_{}_tentacle{}_multiplyDivide{:02d}'.format(name, side, x,(i+1)))
                cmds.connectAttr('{}.outputX'.format(multiplyDivide),'{}_{}_tentacle{}_animBlendNodeAdditiveRotation{:02d}.inputAX'.format(name, side, x,(i+1)))
                cmds.connectAttr('tentacle_rotation_guide.mid_{:02d}'.format((i+1)),'{}.input2X'.format(multiplyDivide))
                cmds.connectAttr('{}_{}_tentacle{}_{:02d}_mid_ctrl.rotateX'.format(name, side, x, midpos),'{}.input1X'.format(multiplyDivide))
                
    
    if i == 3:
        
        cmds.connectAttr('{}_{}_tentacle{}_{:02d}_bet_ctrl.rotate.rotateX'.format(name, side, x, int(midpos + ((lastpos-midpos)/2))-1),'{}_{}_tentacle{}_animBlendNodeAdditiveRotation{}.inputB.inputBX'.format(name, side, x,item[:2]))
        for i in range(midpos+1,lastpos-1):
            if (i+1) % 2 != 0 and i+1 != (int(midpos + ((lastpos-midpos)/2))-1):
                multiplyDivide = cmds.createNode('multiplyDivide',n='{}_{}_tentacle{}_multiplyDivide{:02d}'.format(name, side, x,(i+1)))
                cmds.connectAttr('{}.outputX'.format(multiplyDivide),'{}_{}_tentacle{}_animBlendNodeAdditiveRotation{:02d}.inputBX'.format(name, side, x,(i+1)))
                cmds.connectAttr('tentacle_rotation_guide.bet_{:02d}'.format((i+1)),'{}.input2X'.format(multiplyDivide))
                cmds.connectAttr('{}_{}_tentacle{}_{:02d}_bet_ctrl.rotateX'.format(name, side, x, int(midpos + ((lastpos-midpos)/2))-1),'{}.input1X'.format(multiplyDivide))
        
        
    if i == 4:
        cmds.connectAttr('{}_{}_tentacle{}_{:02d}_end_ctrl.rotate.rotateX'.format(name, side, x, lastpos),'{}_{}_tentacle{}_animBlendNodeAdditiveRotation{}.inputA.inputAX'.format(name, side, x,item[:2]))
        for i in range((int(midpos + ((lastpos-midpos)/2))-1),lastpos-1):
            if (i+1) % 2 != 0:
                print(i+1)
                multiplyDivide = cmds.createNode('multiplyDivide',n='{}_{}_tentacle{}_multiplyDivide{:02d}'.format(name, side, x,(i+1)))
                cmds.connectAttr('{}.outputX'.format(multiplyDivide),'{}_{}_tentacle{}_animBlendNodeAdditiveRotation{:02d}.inputAX'.format(name, side, x,(i+1)))
                cmds.connectAttr('tentacle_rotation_guide.end_{:02d}'.format((i+1)),'{}.input2X'.format(multiplyDivide))
                cmds.connectAttr('{}_{}_tentacle{}_{:02d}_end_ctrl.rotateX'.format(name, side, x, lastpos),'{}.input1X'.format(multiplyDivide))
        

        
    #print('{}_{}_tentacle{}_{}_joint.rotateX'.format(name, side, x, item))
    #print('{}_{}_tentacle{}_ribbon_ribbon_{}_joint_def_ctrl_off.rotateX'.format(name, side, x,item[:2]))



cmds.parent('{}_{}_tentacle{}_{:02d}_joint_def'.format(name, side,x,int(lastpos)+1),loc)
cmds.delete('{}_{}_tentacle{}_01_joint'.format(name, side,x))


#scale
for item in range(1, 233):
    if cmds.objExists('follicle{}'.format(item)):
        [cmds.connectAttr('Octopus_trs_ctrl_multiplydividefollicle_trs.output{}'.format(axis),
        'follicle{}.scale{}'.format(item, axis), force=True) for axis in 'XYZ']
    
        

