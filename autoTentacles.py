
import maya.cmds as cmds
import importlib

import pyTool.utilities as utili
importlib.reload(utili)

def tentacleBuild(name = 'character',mainjoint = 'joint', spacing = 45.0, midpos = 7, lastpos = 14
                                    ,listGuide = None  ):

    """print('{}\n'.format(name))
    print('{}\n'.format(mainjoint))
    print('{}\n'.format(spacing))
    print('{}\n'.format(midpos))
    print('{}\n'.format(lastpos))
    print(listGuide)"""

    for x in range(1,5):
        for side in ('l','r'):

            loc = cmds.spaceLocator(absolute=True,name = '{}_{}_{}_loc'.format(name,side,x))
            cmds.delete(cmds.parentConstraint(mainjoint, loc))
            curve_list = []
            for i,guide in enumerate(listGuide):
                if i <= int(lastpos)-1:
                    jnt = cmds.joint(name = '{}_{}_tentacle{}_{:02d}_joint'.format(name,side,x,(i+1)))
                    cmds.delete(cmds.pointConstraint(guide, jnt))
                if i >= int(lastpos)-1:
                    jnt_fk = cmds.joint(name='{}_{}_tentacle{}_{:02d}_joint_def'.format(name, side, x, (i + 1)))
                    cmds.delete(cmds.pointConstraint(guide, jnt_fk))

                if (i+1) <= int(lastpos):
                    curve_list.append(jnt)

            cmds.joint('{}_{}_tentacle{}_01_joint'.format(name,side,x), edit=True, zso=True, oj='xyz', secondaryAxisOrient='yup', children=True)
            cmds.joint('{}_{}_tentacle{}_{}_joint_def'.format(name,side,x,len(listGuide)), edit=True, oj='none', children=True, zso=True)
            positions = [cmds.xform(obj, q=True, ws=True, translation=True) for obj in curve_list]

            #LETS CREATE A CURVE
            curve = cmds.curve(d=3,p=positions, name = '{}_{}_tentacle{}_curve'.format(name,side,x))
            ##parenting the curve will multiply transformation
            #cmds.parent(curve, loc)

            ###creating joint controller and ik handle
            #lets create 3 joint
            ik_list = ['{}_{}_tentacle{}_{}_joint'.format(name,side,x,obj) for obj in ('01_sta','0{}_mid'.format(str(midpos)),'{}_end'.format(str(lastpos)))]

            for i,item in enumerate(ik_list):
                cmds.select(clear=True)
                jnt_ctrl =cmds.joint(name = item, component = False)
                cmds.delete(cmds.parentConstraint('{}_joint'.format(item[:-10]) ,jnt_ctrl,maintainOffset = False))
                cmds.setAttr('{}.radius'.format(jnt_ctrl),2)
                cmds.parent(jnt_ctrl, loc)
                ctrl = utili.createController(name='{}'.format(item[:-6]), shape='square', target=jnt_ctrl, contraint_target=None, facing='x',
                                        offsetnumber=2,
                                        type='fk', size=6-i)
                cmds.parent('{}_off'.format(ctrl), loc)
            #skin controller joints to the curve
            cmds.skinCluster(ik_list, curve, tsb=True , name = '{}_{}_tentacle{}_skincluster'.format(name,side,x))
            ik_handle = cmds.ikHandle(n='{}_{}_tentacle{}_ikhandle'.format(name,side,x), sj='{}_{}_tentacle{}_01_joint'.format(name,side,x),
                          ee='{}_{}_tentacle{}_{}_joint'.format(name,side,x,int(lastpos)),
                          curve = curve , solver= 'ikSplineSolver',createCurve = False, parentCurve = False, numSpans = 3 )[0]
            #cmds.parent(ik_handle, loc)
            #here we create the fk controllers for the tip of the tentacles
            list_fk = ['{}_{}_tentacle{}_{:02d}_joint_def'.format(name,side,x,int(i)) for i in range(int(lastpos), len(listGuide))]
            for i,item in enumerate(list_fk):
                ctrl = utili.createController(name='{}'.format(item[:-10]), shape='circle', target=item, contraint_target=None,
                                       facing='x',
                                       offsetnumber=2,
                                       type='fk', size=3-(i*0.5))
                #here we group the controllers of the fk controller
                if i >= 1:
                    cmds.parent('{}_off'.format(ctrl),'{}_ctrl'.format((list_fk[i-1])[:-10]) )


            cmds.parent('{}_{}_tentacle{}_{:02d}_ctrl_off'.format(name,side,x,(int(lastpos))),loc)
            cmds.parentConstraint(ik_list[2],'{}_{}_tentacle{}_{:02d}_ctrl_off'.format(name,side,x,(int(lastpos))), maintainOffset = True)

            arc1 = cmds.arclen(curve)
            cmds.setAttr('{}_ctrl.translateX'.format((ik_list[2])[:-6]), 20)
            arc2 = cmds.arclen(curve)
            cmds.setAttr('{}_ctrl.translateX'.format((ik_list[2])[:-6]), 0)


            arc = cmds.arclen(curve, ch=True)
            set_driven_key_tentacles(curve_list, ('{}_ctrl'.format((ik_list[2])[:-6])), 0, arc,curve,0)
            set_driven_key_tentacles(curve_list, ('{}_ctrl'.format((ik_list[2])[:-6])), 20, arc,curve,(arc2-arc1))

            #NOW WE CREATE THE RIBBON SYSTEM
            #we may want to customise more this funtion later for other tools
            listRibbonJnt = ['{}_{}_tentacle{}_{:02d}_joint'.format(name,side, x, int(i)) for i in
                       range(1, int(lastpos) + 1)]
            utili.createRibbon(list=listRibbonJnt,name='{}_{}_tentacle{}_ribbon'.format(name,side,x),target = ('{}_ctrl'.format((ik_list[1])[:-6])),ikhandle = ik_handle,
                               sta_ctrl = '{}_ctrl'.format((ik_list[0])[:-6]), mid_ctrl = '{}_ctrl'.format((ik_list[1])[:-6]) , end_ctrl = '{}_ctrl'.format((ik_list[2])[:-6]),
                               midpos = midpos)


    ###Finally we rotate loc to place everything in place.
    for x in range(1, 5):
        for side in ('l','r'):
            #val = x*spacing


            if side == 'l':
                cmds.setAttr('{}.rotateY'.format('{}_{}_{}_loc'.format(name,side, x)), (x-1) * 45.0)
            else:
                cmds.setAttr('{}.rotateY'.format('{}_{}_{}_loc'.format(name, side, x)), (360 - (x * 45.0)))

            cmds.skinPercent('{}_{}_tentacle{}_skincluster'.format(name, side, x),
                             '{}_{}_tentacle{}_curve.cv[7]'.format(name, side, x),
                             transformValue=[('{}_{}_tentacle{}_07_mid_joint'.format(name, side, x), 0.8)])
            cmds.skinPercent('{}_{}_tentacle{}_skincluster'.format(name, side, x),
                             '{}_{}_tentacle{}_curve.cv[8]'.format(name, side, x),
                             transformValue=[('{}_{}_tentacle{}_07_mid_joint'.format(name, side, x), 0.5)])
            cmds.skinPercent('{}_{}_tentacle{}_skincluster'.format(name, side, x),
                             '{}_{}_tentacle{}_curve.cv[9]'.format(name, side, x),
                             transformValue=[('{}_{}_tentacle{}_07_mid_joint'.format(name, side, x), 0.25)])
            cmds.skinPercent('{}_{}_tentacle{}_skincluster'.format(name, side, x),
                             '{}_{}_tentacle{}_curve.cv[10]'.format(name, side, x),
                             transformValue=[('{}_{}_tentacle{}_07_mid_joint'.format(name, side, x), 0.1)])
            cmds.skinPercent('{}_{}_tentacle{}_skincluster'.format(name, side, x),
                             '{}_{}_tentacle{}_curve.cv[11]'.format(name, side, x),
                             transformValue=[('{}_{}_tentacle{}_07_mid_joint'.format(name, side, x), 0.03)])

            cmds.skinPercent('{}_{}_tentacle{}_skincluster'.format(name, side, x),
                             '{}_{}_tentacle{}_curve.cv[6]'.format(name, side, x),
                             transformValue=[('{}_{}_tentacle{}_07_mid_joint'.format(name, side, x), 0.9),
                                             ('{}_{}_tentacle{}_01_sta_joint'.format(name, side, x), 0.05),
                                             ('{}_{}_tentacle{}_14_end_joint'.format(name, side, x), 0.05)])

            cmds.skinPercent('{}_{}_tentacle{}_skincluster'.format(name, side, x),
                             '{}_{}_tentacle{}_curve.cv[5]'.format(name, side, x),
                             transformValue=[('{}_{}_tentacle{}_07_mid_joint'.format(name, side, x), 0.8)])
            cmds.skinPercent('{}_{}_tentacle{}_skincluster'.format(name, side, x),
                             '{}_{}_tentacle{}_curve.cv[4]'.format(name, side, x),
                             transformValue=[('{}_{}_tentacle{}_07_mid_joint'.format(name, side, x), 0.5)])
            cmds.skinPercent('{}_{}_tentacle{}_skincluster'.format(name, side, x),
                             '{}_{}_tentacle{}_curve.cv[3]'.format(name, side, x),
                             transformValue=[('{}_{}_tentacle{}_07_mid_joint'.format(name, side, x), 0.25)])
            cmds.skinPercent('{}_{}_tentacle{}_skincluster'.format(name, side, x),
                             '{}_{}_tentacle{}_curve.cv[2]'.format(name, side, x),
                             transformValue=[('{}_{}_tentacle{}_07_mid_joint'.format(name, side, x), 0.03)])


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
