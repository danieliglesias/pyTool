
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
    tentacle_guide = utili.createEmptyGroup(name='{}_tentacle_rotation_guide'.format(name))

    for x in range(1,5):
        for side in ('l','r'):

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
            for i, item in enumerate(curve_list):
                if (i + 1) % 2 != 0:
                    cv_curve_list.append(item)
            positions = [cmds.xform(obj, q=True, ws=True, translation=True) for obj in cv_curve_list]

            # LETS CREATE A CURVE
            tentacle_curve = cmds.curve(d=3, p=positions, name='{}_{}_tentacle{}_curve'.format(name, side, x))
            cmds.parent(tentacle_curve, loc)

            ##parenting the curve will multiply transformation
            # cmds.parent(curve, loc)

            ###creating joint controller and ik handle
            # lets create 3 joint
            print('{:02d}_sub'.format(int(int(midpos) / 2) + 1))
            ik_list = ['{}_{}_tentacle{}_{}_joint'.format(name, side, x, obj) for obj in
                       ('01_sta', '{:02d}_sub'.format(int(int(midpos) / 2) + 1), '{:02d}_mid'.format(int(midpos)),
                        '{:02d}_bet'.format(int(int(midpos) + ((int(lastpos) - int(midpos)) / 2)) - 1),
                        '{:02d}_end'.format(int(lastpos)))]

            for i, item in enumerate(ik_list):
                cmds.select(clear=True)
                jnt_ctrl = cmds.joint(name=item, component=False)
                cmds.delete(cmds.parentConstraint('{}_joint'.format(item[:-10]), jnt_ctrl, maintainOffset=False))
                cmds.setAttr('{}.radius'.format(jnt_ctrl), 2)
                cmds.parent(jnt_ctrl, loc)
                ctrl = utili.createController(name='{}'.format(item[:-6]), shape='square', target=jnt_ctrl,
                                              contraint_target=None, facing='x',
                                              offsetnumber=2,
                                              type='fk', size=7 - (i * 0.5))
                cmds.parent('{}_off'.format(ctrl), loc)

            # skin controller joints to the curve


            """ik_handle = cmds.ikHandle(n='{}_{}_tentacle{}_ikhandle'.format(name, side, x),
                                      sj='{}_{}_tentacle{}_01_joint'.format(name, side, x),
                                      ee='{}_{}_tentacle{}_{}_joint'.format(name, side, x, int(lastpos)),
                                      curve=curve, solver='ikSplineSolver', createCurve=False, parentCurve=False,
                                      numSpans=3)[0]
            """
            # cmds.parent(ik_handle, loc)
            # here we create the fk controllers for the tip of the tentacles
            list_fk = ['{}_{}_tentacle{}_{:02d}_joint_def'.format(name, side, x, int(i)) for i in
                       range(int(lastpos), len(listGuide))]

            for i, item in enumerate(list_fk):
                ctrl = utili.createController(name='{}'.format(item[:-10]), shape='circle', target=item,
                                                contraint_target = None,
                                                facing = 'x',
                                                offsetnumber = 2,
                                                type = 'fk', size = 4.5 - (i * 0.4))
                # here we group the controllers of the fk controller
                if i >= 1:
                    cmds.parent('{}_off'.format(ctrl), '{}_ctrl'.format((list_fk[i - 1])[:-10]))
            ## here we connect the ribbon system with the FK
            cmds.parent('{}_{}_tentacle{}_{:02d}_ctrl_off'.format(name, side, x, (int(lastpos))), loc)
            cmds.parentConstraint(ik_list[-1],
                                  '{}_{}_tentacle{}_{:02d}_ctrl_off'.format(name, side, x, (int(lastpos))),
            maintainOffset = True)

            #we rotate automatically the first controller base on %
            multiplyDivide = cmds.createNode('multiplyDivide',
                                             n='{}_{}_tentacle{}_{:02d}_ctrl_multiplyDivide'.format(name, side, x, (int(lastpos)+1)))
            cmds.connectAttr('{}_{}_tentacle{}_{:02d}_ctrl.rotate'.format(name, side, x, (int(lastpos)+1)),'{}.input1'.format(multiplyDivide), force=True)
            cmds.connectAttr('{}.output'.format(multiplyDivide),'{}_{}_tentacle{}_{:02d}_ctrl.rotate'.format(name, side, x, (int(lastpos))), force=True)
            [cmds.setAttr('{}.input2{}'.format(multiplyDivide, axis), 0.5) for  axis in 'XYZ']

            cmds.setAttr('{}_{}_tentacle{}_{:02d}_ctrlShape.visibility'.format(name, side, x, (int(lastpos))), 0)

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
            target = ('{}_ctrl'.format((ik_list[1])[:-6])),
            sta_ctrl = '{}_ctrl'.format((ik_list[0])[:-6]), mid_ctrl = '{}_ctrl'.format((ik_list[1])[:-6]),
            end_ctrl = '{}_ctrl'.format((ik_list[2])[:-6]),
            midpos = midpos, u_parches = 28)
            cmds.parent(ribbon, loc)




            ##LETS WORK ON ROTATIONS

            ik_list = [('01_sta'),
                       #('{:02d}_sub'.format(int(int(midpos) / 2) + 1)),
                       ('{:02d}_mid'.format(int(midpos))),
                       #('{:02d}_bet'.format(int(int(midpos) + ((int(lastpos) - int(midpos)) / 2)) - 1)),
                       ('{:02d}_end'.format(int(lastpos)))]



            for i, item in enumerate(listGuide):
                if i + 1 <= int(lastpos):
                    animBlendNodeAdditiveRotation = cmds.createNode('animBlendNodeAdditiveRotation',
                                                            n='{}_{}_tentacle{}_animBlendNodeAdditiveRotation{:02d}'.format(name,
                                                                                                                            side, x,
                                                                                                                            (
                                                                                                                                        i + 1)))
                    cmds.connectAttr('{}.output.outputX'.format(animBlendNodeAdditiveRotation),
                                     '{}_{}_tentacle{}_ribbon_{:02d}_joint_def_ctrl_off.rotate.rotateX'.format(name, side, x,
                                                                                                  (i + 1)), force=True)

            for i, item in enumerate(ik_list):
                if i == 0:
                    for i in range(2, (int(int(midpos) / 2))):
                        #if (i + 1) % 2 != 0:
                        exist = cmds.attributeQuery('sta_{:02d}'.format((i)), node='{}_tentacle_rotation_guide'.format(name), ex=True)
                        if not exist:
                            cmds.addAttr(tentacle_guide, longName='sta_{:02d}'.format((i)), defaultValue=0, minValue=0,
                                         maxValue=1,
                                         keyable=1)
                        multiplyDivide = cmds.createNode('multiplyDivide',
                                                         n='{}_{}_tentacle{}_multiplyDivide{:02d}'.format(name, side, x, (i)))
                        cmds.connectAttr('{}.outputX'.format(multiplyDivide),
                                         '{}_{}_tentacle{}_animBlendNodeAdditiveRotation{:02d}.inputAX'.format(name, side, x, (i)))
                        cmds.connectAttr('{}_tentacle_rotation_guide.sta_{:02d}'.format(name,(i)), '{}.input2X'.format(multiplyDivide))
                        cmds.connectAttr('{}_{}_tentacle{}_{:02d}_sta_ctrl.rotateX'.format(name, side, x, 1),
                                         '{}.input1X'.format(multiplyDivide))

                if i == 1:
                    cmds.connectAttr('{}_{}_tentacle{}_{:02d}_sub_ctrl.rotate.rotateX'.format(name, side, x, (int(int(midpos) / 2) + 1)),
                                     '{}_{}_tentacle{}_animBlendNodeAdditiveRotation{}.inputB.inputBX'.format(name, side, x, item[:2]))
                    for i in range(1, int(midpos) - 1):
                        if (i + 1) != (int(int(midpos) / 2) + 1):
                            exist = cmds.attributeQuery('sub_{:02d}'.format((i + 1)),
                                                        node='{}_tentacle_rotation_guide'.format(name), ex=True)
                            if not exist:
                                cmds.addAttr(tentacle_guide, longName='sub_{:02d}'.format((i + 1)), defaultValue=0,
                                             minValue=0,
                                             maxValue=1,
                                             keyable=1)
                            multiplyDivide = cmds.createNode('multiplyDivide',
                                                             n='{}_{}_tentacle{}_multiplyDivide{:02d}'.format(name, side, x, (i + 1)))
                            cmds.connectAttr('{}.outputX'.format(multiplyDivide),
                                             '{}_{}_tentacle{}_animBlendNodeAdditiveRotation{:02d}.inputBX'.format(name, side, x, (i + 1)))
                            cmds.connectAttr('{}_tentacle_rotation_guide.sub_{:02d}'.format(name,(i + 1)), '{}.input2X'.format(multiplyDivide))
                            cmds.connectAttr('{}_{}_tentacle{}_{:02d}_sub_ctrl.rotateX'.format(name, side, x, (int(int(midpos) / 2) + 1)),
                                             '{}.input1X'.format(multiplyDivide))

                if i == 2:
                    cmds.connectAttr('{}_{}_tentacle{}_{:02d}_mid_ctrl.rotate.rotateX'.format(name, side, x, int(midpos)),
                                     '{}_{}_tentacle{}_animBlendNodeAdditiveRotation{}.inputA.inputAX'.format(name, side, x, item[:2]))
                    for i in range((int(int(midpos) / 2) + 1),(int(int(midpos) + ((int(lastpos) - int(midpos)) / 2)) - 2)):
                        if (i + 1) != int(midpos):
                            exist = cmds.attributeQuery('mid_{:02d}'.format((i + 1)),
                                                        node='{}_tentacle_rotation_guide'.format(name), ex=True)
                            if not exist:
                                cmds.addAttr(tentacle_guide, longName='mid_{:02d}'.format((i + 1)), defaultValue=0,
                                             minValue=0,
                                             maxValue=1,
                                             keyable=1)
                            multiplyDivide = cmds.createNode('multiplyDivide',
                                                             n='{}_{}_tentacle{}_multiplyDivide{:02d}'.format(name, side, x, (i + 1)))
                            cmds.connectAttr('{}.outputX'.format(multiplyDivide),
                                             '{}_{}_tentacle{}_animBlendNodeAdditiveRotation{:02d}.inputAX'.format(name, side, x, (i + 1)))
                            cmds.connectAttr('{}_tentacle_rotation_guide.mid_{:02d}'.format(name,(i + 1)), '{}.input2X'.format(multiplyDivide))
                            cmds.connectAttr('{}_{}_tentacle{}_{:02d}_mid_ctrl.rotateX'.format(name, side, x, int(midpos)),
                                             '{}.input1X'.format(multiplyDivide))

                if i == 3:
                    cmds.connectAttr('{}_{}_tentacle{}_{:02d}_bet_ctrl.rotate.rotateX'.format(name, side, x, int(int(midpos) + (
                                (int(lastpos) - int(midpos)) / 2)) - 1),
                                     '{}_{}_tentacle{}_animBlendNodeAdditiveRotation{}.inputB.inputBX'.format(name, side, x, item[:2]))
                    for i in range(int(midpos), int(lastpos) - 1):
                        if i + 1 != (int(int(midpos) + ((int(lastpos) - int(midpos)) / 2)) - 1):
                            exist = cmds.attributeQuery('bet_{:02d}'.format((i + 1)),
                                                        node='{}_tentacle_rotation_guide'.format(name), ex=True)
                            if not exist:
                                cmds.addAttr(tentacle_guide, longName='bet_{:02d}'.format((i + 1)), defaultValue=0,
                                             minValue=0,
                                             maxValue=1,
                                             keyable=1)
                            multiplyDivide = cmds.createNode('multiplyDivide',
                                                             n='{}_{}_tentacle{}_multiplyDivide{:02d}'.format(name, side, x, (i + 1)))
                            cmds.connectAttr('{}.outputX'.format(multiplyDivide),
                                             '{}_{}_tentacle{}_animBlendNodeAdditiveRotation{:02d}.inputBX'.format(name, side, x, (i + 1)))
                            cmds.connectAttr('{}_tentacle_rotation_guide.bet_{:02d}'.format(name,(i + 1)), '{}.input2X'.format(multiplyDivide))
                            cmds.connectAttr(
                                '{}_{}_tentacle{}_{:02d}_bet_ctrl.rotateX'.format(name, side, x, int(int(midpos) + ((int(lastpos) - int(midpos)) / 2)) - 1),
                                '{}.input1X'.format(multiplyDivide))

                if i == 4:
                    cmds.connectAttr('{}_{}_tentacle{}_{:02d}_end_ctrl.rotate.rotateX'.format(name, side, x, int(lastpos)),
                                     '{}_{}_tentacle{}_animBlendNodeAdditiveRotation{}.inputA.inputAX'.format(name, side, x, item[:2]))
                    for i in range((int(int(midpos) + ((int(lastpos) - int(midpos)) / 2)) - 1), int(lastpos) - 1):
                        #if (i + 1) % 2 != 0:
                        exist = cmds.attributeQuery('end_{:02d}'.format((i + 1)),
                                                    node='{}_tentacle_rotation_guide'.format(name), ex=True)
                        if not exist:
                            cmds.addAttr(tentacle_guide, longName='end_{:02d}'.format((i + 1)), defaultValue=0,
                                         minValue=0,
                                         maxValue=1,
                                         keyable=1)
                        multiplyDivide = cmds.createNode('multiplyDivide',
                                                         n='{}_{}_tentacle{}_multiplyDivide{:02d}'.format(name, side, x, (i + 1)))
                        cmds.connectAttr('{}.outputX'.format(multiplyDivide),
                                         '{}_{}_tentacle{}_animBlendNodeAdditiveRotation{:02d}.inputAX'.format(name, side, x, (i + 1)))
                        cmds.connectAttr('{}_tentacle_rotation_guide.end_{:02d}'.format(name,(i + 1)), '{}.input2X'.format(multiplyDivide))
                        cmds.connectAttr('{}_{}_tentacle{}_{:02d}_end_ctrl.rotateX'.format(name, side, x, int(lastpos)),
                                     '{}.input1X'.format(multiplyDivide))

                # print('{}_{}_tentacle{}_{}_joint.rotateX'.format(name, side, x, item))
                # print('{}_{}_tentacle{}_ribbon_ribbon_{}_joint_def_ctrl_off.rotateX'.format(name, side, x,item[:2]))
            cmds.parent('{}_{}_tentacle{}_{:02d}_joint_def'.format(name, side, x, int(lastpos)), loc)
            cmds.delete('{}_{}_tentacle{}_01_joint'.format(name, side, x))

            # scale
            for item in range(1, 300):
                if cmds.objExists('follicle{}'.format(item)):
                    [cmds.connectAttr('Octopus_trs_ctrl_multiplydividefollicle_trs.output{}'.format(axis),
                                      'follicle{}.scale{}'.format(item, axis), force=True) for axis in 'XYZ']


            """### here we connect the scale of the main controller to the follicle, THIS WILL FAIL we need to set up the ribbon follicle names!
            for item in range(1, 233):
                [cmds.connectAttr('Octopus_trs_ctrl_multiplydividefollicle_trs.output{}'.format(axis),
                              'follicle{}.scale{}'.format(item, axis), force=True) for axis in 'XYZ']

            ### here we want to connect the scale of the main controller with the tentacles
            for item in range(1, lastpos + 1):
                multiplyDivideTRS = cmds.createNode('multiplyDivide',
                                                    n='{}_{}_tentacle{}_{:02d}_joint_multiplydivide_trs'.format(name,
                                                                                                                side, x,
                                                                                                                item))
                cmds.setAttr('{}.operation'.format(multiplyDivideTRS), 2)
                cmds.connectAttr('Octopus_trs_ctrl.scaleX',
                                 '{}_{}_tentacle{}_{:02d}_joint_multiplydivide_trs.input2X'.format(name, side, x, item),
                                 force=True)
                cmds.connectAttr('{}_{}_tentacle{}_curveinfo.arcLength'.format(name, side, x),
                                 '{}_{}_tentacle{}_{:02d}_joint_multiplydivide_trs.input1X'.format(name, side, x, item),
                                 force=True)
                cmds.connectAttr('{}_{}_tentacle{}_{:02d}_joint_multiplydivide_trs.outputX'.format(name, side, x, item),
                                 '{}_{}_tentacle{}_{:02d}_joint_translateX.input'.format(name, side, x, item),
                                 force=True)"""

    ###Finally we rotate loc to place everything in place. AND fix
    for x in range(1, 5):
        for side in ('l','r'):
            #val = x*spacing

            ik_list = ['{}_{}_tentacle{}_{}_joint'.format(name, side, x, obj) for obj in
                       ('01_sta', '{:02d}_sub'.format(int(int(midpos) / 2) + 1), '{:02d}_mid'.format(int(midpos)),
                        '{:02d}_bet'.format(int(int(midpos) + ((int(lastpos) - int(midpos)) / 2)) - 1),
                        '{:02d}_end'.format(int(lastpos)))]


            if side == 'l':
                cmds.setAttr('{}.rotateY'.format('{}_{}_{}_loc'.format(name,side, x)), (x-1) * 45.0)
            else:
                cmds.setAttr('{}.rotateY'.format('{}_{}_{}_loc'.format(name, side, x)), (360 - (x * 45.0)))

            cmds.wire('{}_{}_tentacle{}'.format(name, side, x), w='{}_{}_tentacle{}_curve'.format(name, side, x), dds=[(0, 50)])
            cmds.skinCluster(ik_list, '{}_{}_tentacle{}_curve'.format(name, side, x), tsb=True,
                             name='{}_{}_tentacle{}_skincluster'.format(name, side, x))

            """cmds.skinPercent('{}_{}_tentacle{}_skincluster'.format(name, side, x),
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
