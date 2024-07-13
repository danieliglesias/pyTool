
import maya.cmds as cmds
import importlib

import pyRigging.utilities as utili
importlib.reload(utili)

def tentacleBuild(name = 'character',mainjoint = 'joint', spacing = 45.0, midpos = 7, lastpos = 14
                                    ,listGuide = None  ):

    """print('{}\n'.format(name))
    print('{}\n'.format(mainjoint))
    print('{}\n'.format(spacing))
    print('{}\n'.format(midpos))
    print('{}\n'.format(lastpos))
    print(listGuide)"""

    for x in range(1,9):

        loc = cmds.spaceLocator(absolute=True,name = '{}_{}_loc'.format(name,x))
        cmds.delete(cmds.parentConstraint(mainjoint, loc))
        curve_list = []
        for i,guide in enumerate(listGuide):
            jnt = cmds.joint(name = '{}_tentacle{}_{:02d}_joint'.format(name,x,(i+1)))
            cmds.delete(cmds.pointConstraint(guide, jnt))
            if (i+1) <= int(lastpos):
                curve_list.append(jnt)

        cmds.joint('{}_tentacle{}_01_joint'.format(name,x), edit=True, zso=True, oj='xyz', secondaryAxisOrient='yup', children=True)
        cmds.joint('{}_tentacle{}_{}_joint'.format(name,x,len(listGuide)), edit=True, oj='none', children=True, zso=True)
        positions = [cmds.xform(obj, q=True, ws=True, translation=True) for obj in curve_list]

        #LETS CREATE A CURVE
        curve = cmds.curve(d=3,p=positions, name = '{}_tentacle{}_curve'.format(name,x))
        ##parenting the curve will multiply transformation
        #cmds.parent(curve, loc)

        ###creating joint controller and ik handle
        #lets create 3 joint
        ik_list = ['{}_tentacle{}_{}_joint'.format(name,x,obj) for obj in ('01_sta','0{}_mid'.format(str(midpos)),'{}_end'.format(str(lastpos)))]

        for i,item in enumerate(ik_list):
            cmds.select(clear=True)
            jnt_ctrl =cmds.joint(name = item, component = False)
            cmds.delete(cmds.parentConstraint('{}_joint'.format(item[:-10]) ,jnt_ctrl,maintainOffset = False))
            cmds.setAttr('{}.radius'.format(jnt_ctrl),2)
            cmds.parent(jnt_ctrl, loc)
            print('target: {}_____ name for controller: {}'.format(jnt_ctrl,'{}'.format(item[:-6])))
            ctrl = utili.createController(name='{}'.format(item[:-6]), shape='square', target=jnt_ctrl, contraint_target=None, facing='x',
                                    offsetnumber=2,
                                    type='fk', size=6-i)
            cmds.parent('{}_off'.format(ctrl), loc)
        #skin controller joints to the curve
        cmds.skinCluster(ik_list, curve, tsb=True)
        ik_handle = cmds.ikHandle(n='{}_tentacle{}_ikhandle'.format(name,x), sj='{}_tentacle{}_01_joint'.format(name,x),
                      ee='{}_tentacle{}_{}_joint'.format(name,x,int(lastpos)),
                      curve = curve , solver= 'ikSplineSolver',createCurve = False, parentCurve = False, numSpans = 3 )[0]
        #cmds.parent(ik_handle, loc)
        #here we create the fk controllers for the tip of the tentacles
        list_fk = ['{}_tentacle{}_{:02d}_joint'.format(name,x,int(i)) for i in range(int(lastpos)+1, len(listGuide))]
        for i,item in enumerate(list_fk):
            ctrl = utili.createController(name='{}'.format(item[:-6]), shape='circle', target=item, contraint_target=None,
                                   facing='x',
                                   offsetnumber=2,
                                   type='fk', size=5-(i*0.5))
            #here we group the controllers of the fk controller
            if i >= 1:
                cmds.parent('{}_off'.format(ctrl),'{}_ctrl'.format((list_fk[i-1])[:-6]) )


        cmds.parent('{}_tentacle{}_{:02d}_ctrl_off'.format(name,x,(int(lastpos)+1)),loc)
        cmds.parentConstraint(ik_list[2],'{}_tentacle{}_{:02d}_ctrl_off'.format(name,x,(int(lastpos)+1)), maintainOffset = True)

        arc1 = cmds.arclen(curve)
        cmds.setAttr('{}_ctrl.translateX'.format((ik_list[2])[:-6]), 20)
        arc2 = cmds.arclen(curve)
        cmds.setAttr('{}_ctrl.translateX'.format((ik_list[2])[:-6]), 0)


        arc = cmds.arclen(curve, ch=True)
        set_driven_key_tentacles(curve_list, ('{}_ctrl'.format((ik_list[2])[:-6])), 0, arc,curve,0)
        set_driven_key_tentacles(curve_list, ('{}_ctrl'.format((ik_list[2])[:-6])), 20, arc,curve,(arc2-arc1))

        #NOW WE CREATE THE RIBBON SYSTEM
        #we may want to customise more this funtion later for other tools
        listRibbonJnt = ['{}_tentacle{}_{:02d}_joint'.format(name, x, int(i)) for i in
                   range(1, int(lastpos) + 1)]
        utili.createRibbon(list=listRibbonJnt,name='{}_tentacle{}_ribbon'.format(name,x),target = ('{}_ctrl'.format((ik_list[1])[:-6])),ikhandle = ik_handle,
                           sta_ctrl = '{}_ctrl'.format((ik_list[0])[:-6]), mid_ctrl = '{}_ctrl'.format((ik_list[1])[:-6]) , end_ctrl = '{}_ctrl'.format((ik_list[2])[:-6]),
                           midpos = midpos)
    ###Finally we rotate loc to place everything in place.
    for x in range(1, 8):
        #val = x*spacing
        cmds.setAttr('{}.rotateY'.format('{}_{}_loc'.format(name, x)), x * 45.0)




"""
    setAttr ($name+"_c_pelvis01_jnt_ik_ikhandle.dTwistControlEnable") 1;
    setAttr ($name+"_c_pelvis01_jnt_ik_ikhandle.dWorldUpType") 4;
    connectAttr -f ($name+"_c_pelvis01_jnt_spinedef_ctrl.worldMatrix[0]") ($name+"_c_pelvis01_jnt_ik_ikhandle.dWorldUpMatrix");
    connectAttr -f ($name+"_c_chest01_jnt_spinedef_ctrl.worldMatrix[0]") ($name+"_c_pelvis01_jnt_ik_ikhandle.dWorldUpMatrixEnd");
"""

def set_driven_key_tentacles(list=None, ctrl=None, unit=None, arc=None, curve = None,diff = None):
    if not list:
        cmds.error('Must provide list of joints.')
    if not ctrl:
        cmds.error('Must provide main controller.')

    # move controller

    cmds.setAttr('{}.translateX'.format(ctrl), unit)

    for i, item in enumerate(list):
        value = cmds.getAttr('{}.translateX'.format(item))
        cmds.setAttr('{}.translateX'.format(item), value + (diff / (len(list)-1)))
        #arc = cmds.arclen(curve, ch=True)
        cmds.setDrivenKeyframe('{}.translateX'.format(item),cd = '{}.arcLength'.format(arc) )
        cmds.selectKey('{}.translateX'.format(item) ,addTo = True,keyframe = True )
    cmds.keyTangent( inTangentType='spline' , outTangentType='spline')
    cmds.setInfinity(pri='linear', poi='linear')
    cmds.setAttr('{}.translateX'.format(ctrl) ,0)
