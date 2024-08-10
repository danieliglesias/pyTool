import maya.cmds as cmds
import json
import pyTool.utilities as utili
import importlib
import math
import sys
importlib.reload(utili)

def createEyebrowsPlane(name = None, sides = None,u= 1,v = 1):
    #validations

    if not sides:
        utili.errorMessage('No side was selected')
    if len(sides) == 2:
        side = 'both'
    else:
        side = sides
    #end validations
    planes = []
    #position reference base on the head joint
    cvPos = cmds.xform('{}_head01_jnt'.format(name), t=True, ws=True, q=True)
    if side == 'l':
        planes = cmds.nurbsPlane(u=u, v=v, w=10, d=3 , name = '{}_l_eyebrows_surface'.format(name) ,axis= [0,0,1])[0]
        cmds.xform(planes, t=(cvPos[0]+3, cvPos[1], cvPos[2] + 20))
        utili.clearObject(planes, scope='freeze')
    elif side == 'r':
        planes = cmds.nurbsPlane(u=u, v=v, w=10, d=3, name='{}_r_eyebrows_surface'.format(name), axis=[0, 0, 1])[0]
        cmds.xform(planes, t=(cvPos[0]-3, cvPos[1], cvPos[2] + 20))
        utili.clearObject(planes, scope='freeze')
        cmds.reverseSurface('{}.v[0.1]'.format(planes), ch=True)
    elif side == 'both':
        planes = [cmds.nurbsPlane(u=u, v=v, w=10, d=3, name='{}_{}_eyebrows_surface'.format(name,side), axis=[0, 0, 1])[0] for side in ('r','l')]
        [cmds.xform(planes, t=(cvPos[0], cvPos[1], cvPos[2] + 20)) for i,side in enumerate((planes))]
        [utili.clearObject(planes, scope='freeze') for side in (planes)]
        cmds.reverseSurface('{}.v[0.1]'.format(planes[0]), ch=True)
        #planes = [r_eyebrow_surface,l_eyebrow_surface]


    return planes


def load_plane_position(file_name = None):

    if not file_name:
        utili.errorMessage('nothing was selected')
        cmds.error('nothing was selected')

    if len(file_name) > 1:
        utili.errorMessage('More than one object selected')
        cmds.error('More than one object selected')


    data = utili.file_manage(section_dir = 'eyebrows/{}'.format(file_name[0]),action = 'load')
    #f = open('/Users/danieliglesiasvalenzuela/Library/Preferences/Autodesk/maya/2022/prefs/scripts/pyTool/guide/eyebrows/{}'.format(file_name[0]))
    #data = json.load(f)

    for item in data:
        cmds.xform(item, t=data[item],ws=True)
    utili.clearObject('Max_l_eyebrows_surface', scope='freeze')


def savePlanePosition(name = None ,side = None):

    if not side:
        utili.errorMessage('No side was selected')
    if len(side) == 2:
        side = 'both'
    else:
        side = side

    emptyDict = dict()

    if side == 'both':
        for sides in ('r','l'):
            for u in range(0, 4):
                for v in range(0, 4):
                    cvPos = cmds.xform('{}.cv[{}][{}]'.format('{}_{}_eyebrows_surface'.format(name,sides), u, v), t=True, ws=True, q=True)
                    emptyDict.update({'{}.cv[{}][{}]'.format('{}_{}_eyebrows_surface'.format(name,sides), u, v): cvPos})
    else:
            for u in range(0, 4):
                for v in range(0, 4):
                    cvPos = cmds.xform('{}.cv[{}][{}]'.format('{}_{}_eyebrows_surface'.format(name,side), u, v), t=True, ws=True, q=True)
                    emptyDict.update({'{}.cv[{}][{}]'.format('{}_{}_eyebrows_surface'.format(name,side), u, v): cvPos})

    directory = 'eyebrows/'
    utili.nameInputWindow( section_dir=directory, dictionary = emptyDict )

def mirrorEyebrowsPlane(name = None,side_selected = None,u = 1, v = 1 ):

    if not side_selected:
        utili.errorMessage('No side was selected')

    if side_selected == 'l':
        side_opposite = 'r'

    else:
        side_opposite = 'l'

    if side_selected == 'l' and cmds.objExists('{}_r_eyebrows_surface'.format(name)):

        for u in range(0, 4):
            for v in range(0, 4):
                cvPos = cmds.xform('{}.cv[{}][{}]'.format('{}_l_eyebrows_surface'.format(name), u, v), t=True, ws=True, q=True)
                cmds.xform('{}.cv[{}][{}]'.format('{}_r_eyebrows_surface'.format(name), u, v), t=(cvPos[0] * -1, cvPos[1], cvPos[2]),
                           ws=True)


    elif side_selected == 'r' and cmds.objExists('{}_l_eyebrows_surface'.format(name)):

        for u in range(0, 4):
            for v in range(0, 4):
                cvPos = cmds.xform('{}.cv[{}][{}]'.format('{}_r_eyebrows_surface'.format(name), u, v), t=True, ws=True,
                                   q=True)
                cmds.xform('{}.cv[{}][{}]'.format('{}_l_eyebrows_surface'.format(name), u, v),t=(cvPos[0] * -1, cvPos[1], cvPos[2]),
                           ws=True)

    else:

        surface_exists = '{}_{}_eyebrows_surface'.format(name,side_selected)
        surface_no_exist = '{}_{}_eyebrows_surface'.format(name,side_opposite)
        surface_opposite = cmds.nurbsPlane(u=u, v=v, w=10, d=3, name=surface_no_exist, axis=[0, 0, 1])[0]
        if '_r_' in surface_opposite:
            cmds.reverseSurface('{}.v[0.1]'.format(surface_opposite), ch=True)

        for u in range(0, 4):
            for v in range(0, 4):
                cvPos = cmds.xform('{}.cv[{}][{}]'.format(surface_exists,u, v), t=True, ws=True, q=True)
                cmds.xform('{}.cv[{}][{}]'.format(surface_opposite,u, v), t=(cvPos[0] * -1, cvPos[1], cvPos[2]),
                           ws=True)

        utili.clearObject(surface_opposite, scope='freeze')




def createEyebrows(name=None,side = None, joint_row = None):

    if not joint_row:
        utili.errorMessage('You must select one of the 3 checkbox')
    if not side:
        utili.errorMessage('No side was selected')


    #checking surface and sides
    if len(side) == 2 and cmds.objExists('{}_l_eyebrows_surface'.format(name)) and cmds.objExists('{}_r_eyebrows_surface'.format(name)):
        sides = 'both'
        nurbplanes = ['{}_l_eyebrows_surface'.format(name), '{}_r_eyebrows_surface'.format(name)]
    elif side == 'l' and cmds.objExists('{}_l_eyebrows_surface'.format(name)):
        sides = side
        nurbplanes = ['{}_l_eyebrows_surface'.format(name)]
    elif side == 'r' and cmds.objExists('{}_r_eyebrows_surface'.format(name)):
        sides = side
        nurbplanes = ['{}_r_eyebrows_surface'.format(name)]
    else:
        utili.errorMessage('One of the surfaces are missing, check your selection')


    if joint_row == 1:
        rows = ['low']
    elif joint_row == 2:
        rows = ['low','bet']
    elif joint_row == 3:
        rows = ['low','bet','upp']


    for nurbplane in nurbplanes:

        # CREATE MAIN CONTROLLER
        main_ctrl=utili.createController(name='{}_main'.format(nurbplane.replace('_surface','')), character_name=None, shape='circle', target=None, contraint_target=None,
                         facing='z', offsetnumber=3,
                         type='face', size=2, move=[0,0,0.8])
        # lets keep controller in the same space with the plane
        cmds.parent('{}_off_constrain'.format(main_ctrl), nurbplane)

        # CREATE 3 ROW OF CONTROLLERS FOR THE OCTOPUS
        for u in ('inn', 'mid', 'out'):
            for v in rows:

                ctrl = utili.createController(name='{}_{}{}_ctrl'.format( nurbplane.replace('_surface',''), u, v),
                                                   character_name=None, shape='circle', target=None, contraint_target=None,
                                                   facing='z', offsetnumber=3,
                                                   type='face', size=1, move=[0, 0, 1])
                #lets keep controller in the same space with the plane
                cmds.parent('{}_off_constrain'.format(ctrl), nurbplane)
                # double linear
                addDoubleLinearU = cmds.createNode('addDoubleLinear', n='{}_{}{}_addDoubleLinearU'.format(nurbplane.replace('_surface',''), u, v))
                addDoubleLinearV = cmds.createNode('addDoubleLinear', n='{}_{}{}_addDoubleLinearV'.format(nurbplane.replace('_surface',''), u, v))
                cmds.connectAttr('{}.translateX'.format(main_ctrl), '{}.input1'.format(addDoubleLinearU), force=True)
                cmds.connectAttr('{}.translateY'.format(main_ctrl), '{}.input1'.format(addDoubleLinearV), force=True)
                cmds.connectAttr('{}.translateX'.format(ctrl), '{}.input2'.format(addDoubleLinearU), force=True)
                cmds.connectAttr('{}.translateY'.format(ctrl), '{}.input2'.format(addDoubleLinearV), force=True)
                # joint
                jnt = cmds.joint(name='{}_{}{}_jnt'.format(nurbplane.replace('_surface',''), u, v))
                cmds.parent(jnt, nurbplane)
                # point on surface
                pointOnSurfaceInfo = cmds.createNode('pointOnSurfaceInfo', n='{}_{}{}_pointOnSurfaceInfo'.format(nurbplane.replace('_surface',''), u, v))
                # four by four matrix
                fourByFourMatrix = cmds.createNode('fourByFourMatrix', n='{}_{}{}_fourByFourMatrix'.format(nurbplane.replace('_surface',''), u, v))
                # matrix
                for count, x in enumerate(('normalizedTangentU', 'normalizedTangentV', 'normalizedNormal', 'position')):
                    for i, axis in enumerate('XYZ'):
                        cmds.connectAttr('{}.{}{}'.format(pointOnSurfaceInfo, x, axis), '{}.in{}{}'.format(fourByFourMatrix, count, i),force=True)
                #descompose matrix
                decomposeMatrix = cmds.createNode('decomposeMatrix', n='{}_{}{}_inputMatrix'.format(nurbplane.replace('_surface',''), u, v))
                cmds.connectAttr('{}.output'.format(fourByFourMatrix), '{}.inputMatrix'.format(decomposeMatrix), force=True)
                cmds.connectAttr('{}.outputRotate'.format(decomposeMatrix), '{}.rotate'.format(jnt), force=True)
                cmds.connectAttr('{}.outputScale'.format(decomposeMatrix), '{}.scale'.format(jnt), force=True)
                cmds.connectAttr('{}.outputTranslate'.format(decomposeMatrix), '{}.translate'.format(jnt), force=True)
                # multi double linear
                multDoubleLinear = cmds.createNode('multDoubleLinear', n='{}_{}{}_multDoubleLinearU'.format(nurbplane.replace('_surface',''), u, v))
                cmds.setAttr('{}.input2'.format(multDoubleLinear), 0.020)  # <----- check this
                # add double linear
                addDoubleLinear = cmds.createNode('addDoubleLinear', n='{}_{}{}_addDoubleLinear'.format(nurbplane.replace('_surface',''), u, v))
                if u == 'inn':
                    cmds.setAttr('{}.input2'.format(addDoubleLinear), 0.2)
                elif u == 'mid':
                    cmds.setAttr('{}.input2'.format(addDoubleLinear), 0.5)
                elif u == 'out':
                    cmds.setAttr('{}.input2'.format(addDoubleLinear), 0.8)

                #remap value
                remapValue = cmds.createNode('remapValue',
                                                   n='{}_{}{}_remapValueV'.format(nurbplane.replace('_surface', ''),
                                                                                         u, v))
                if v == 'low':
                    cmds.setAttr('{}.inputMin'.format(remapValue), -10)
                    cmds.setAttr('{}.inputMax'.format(remapValue), 10)
                    cmds.setAttr('{}.value[2].value_FloatValue'.format(remapValue), 0.4)
                    cmds.setAttr('{}.value[2].value_Position'.format(remapValue), 0.4)
                    cmds.setAttr('{}.value[2].value_Interp'.format(remapValue), 1)
                elif v == 'upp':
                    cmds.setAttr('{}.inputMin'.format(remapValue), -18)
                    cmds.setAttr('{}.inputMax'.format(remapValue), 2)
                    cmds.setAttr('{}.value[2].value_FloatValue'.format(remapValue), 0.9)
                    cmds.setAttr('{}.value[2].value_Position'.format(remapValue), 0.9)
                    cmds.setAttr('{}.value[2].value_Interp'.format(remapValue), 1)

                    cmds.setAttr('{}.value[0].value_FloatValue'.format(remapValue), 0.8)
                    cmds.setAttr('{}.value[0].value_Position'.format(remapValue), 0.8)
                elif v == 'bet':
                    cmds.setAttr('{}.inputMin'.format(remapValue), -14)
                    cmds.setAttr('{}.inputMax'.format(remapValue), 6)
                    cmds.setAttr('{}.value[2].value_FloatValue'.format(remapValue), 0.7)
                    cmds.setAttr('{}.value[2].value_Position'.format(remapValue), 0.7)
                    cmds.setAttr('{}.value[2].value_Interp'.format(remapValue), 1)

                    cmds.setAttr('{}.value[0].value_FloatValue'.format(remapValue), 0.4)
                    cmds.setAttr('{}.value[0].value_Position'.format(remapValue), 0.4)

                cmds.connectAttr('{}Shape.local'.format(nurbplane), '{}.inputSurface'.format(pointOnSurfaceInfo), force=True)
                cmds.connectAttr('{}.position'.format(pointOnSurfaceInfo), '{}.translate'.format(jnt), force=True)

                cmds.connectAttr('{}.output'.format(addDoubleLinearU), '{}.input1'.format(multDoubleLinear), force=True)
                cmds.connectAttr('{}.output'.format(addDoubleLinearV), '{}.inputValue'.format(remapValue), force=True)

                cmds.connectAttr('{}.outValue'.format(remapValue), '{}.parameterV'.format(pointOnSurfaceInfo), force=True)
                cmds.connectAttr('{}.output'.format(multDoubleLinear), '{}.input1'.format(addDoubleLinear), force=True)
                cmds.connectAttr('{}.output'.format(addDoubleLinear), '{}.parameterU'.format(pointOnSurfaceInfo), force=True)

                cmds.parentConstraint(jnt, '{}_off_constrain'.format(ctrl),  maintainOffset = False)

                multiplyDivideOff = cmds.createNode('multiplyDivide',
                                                  n='{}_{}{}_multiplyDivideCtrlOff'.format(nurbplane.replace('_surface', ''), u,
                                                                                      v))

                [cmds.setAttr('{}.input2{}'.format(multiplyDivideOff,axis), -1) for axis in 'XYZ']
                cmds.connectAttr('{}.translate'.format(ctrl), '{}.input1'.format(multiplyDivideOff), force=True)
                cmds.connectAttr('{}.output'.format(multiplyDivideOff), '{}.translate'.format('{}_off'.format(ctrl)), force=True)

        cmds.parentConstraint('{}_{}{}_jnt'.format(nurbplane.replace('_surface',''), 'mid', 'low'), '{}_off_constrain'.format(main_ctrl))



########################################################################################################################
########################################################################################################################
########################################################################################################################

def generateEyeLitGuide(name = None, side = 'l',eye_guide = 'l_eyeball_cluster'):

    for sides in side:
        if sides == 'l':
            multi = 2
        else:
            multi = -2
        guideList = []
        # using locator to get cluster position
        loc = cmds.spaceLocator(absolute=True, name='guide_loc')[0]
        cmds.delete(cmds.pointConstraint('{}_{}_eyeball_jnt'.format(name,sides), loc))
        for y in ('upp', 'low'):
            for i,x in enumerate(('inn_corner','inn','mid','out','out_corner')):
                if x in ('inn_corner','out_corner') and y == 'low':
                    continue
                if x in ('inn_corner','out_corner') and y == 'upp':
                    guide = cmds.sphere(radius=0.2, name='{}_{}_eyelit_guide'.format(sides, x))
                else:
                    guide = cmds.sphere(radius= 0.2, name = '{}_{}_{}_eyelit_guide'.format(sides,y,x))
                #guideList.append(guide)
                guidePos = cmds.xform(loc, t=True, ws=True, q=True)
                if y=='upp':
                    cmds.xform(guide, t=(guidePos[0]+(i*multi), guidePos[1], guidePos[2] + 20))
                else:
                    cmds.xform(guide, t=(guidePos[0] + (i*multi), guidePos[1]-5, guidePos[2] + 20))

        cmds.delete(loc)
        #return guideList





def createEyeLidCurve(name = None,l_eye_guide=None,r_eye_guide=None,side=None):

    """cmds.select(clear=True)
    for item in l_eye_guide:
        jnt = cmds.joint(name='{}_{}_jnt_def'.format(name, item[:-8] ))
        cmds.delete(cmds.parentConstraint(item, jnt))

    cmds.select(clear=True)
    for item in r_eye_guide:
        jnt = cmds.joint(name='{}_{}_jnt_def'.format(name,item[:-8]))
        cmds.delete(cmds.parentConstraint(item, jnt))"""



    #lets create eyeball grp and parent it to the socket
    """cmds.select(clear=True)
    [cmds.joint(name='{}_{}_eyeball_grp'.format(name, z)) for z in 'lr']
    [cmds.delete(cmds.parentConstraint('{}_eyeball_cluster'.format(z), '{}_{}_eyeball_grp'.format(name, z))) for z in 'lr']
    [cmds.parent('{}_{}_eyeball_grp'.format(name, z),'{}_{}_socket_jnt_def'.format(name,z) ) for z in 'lr']
    """

    #CREATE TOP AND LOW CURVE

    for sides in side:

        uppCurveList = ['{}_inn_corner_eyelit_guide'.format(sides), '{}_upp_inn_eyelit_guide'.format(sides),
                        '{}_upp_mid_eyelit_guide'.format(sides),'{}_upp_out_eyelit_guide'.format(sides),'{}_out_corner_eyelit_guide'.format(sides)]
        uppCurveListPos = [cmds.xform(obj, q=True, ws=True, translation=True) for obj in uppCurveList]
        upp_curve = cmds.curve(d=3,p=uppCurveListPos, name = '{}_eyelit_upp_curve'.format(sides))

        lowCurveList = ['{}_inn_corner_eyelit_guide'.format(sides), '{}_low_inn_eyelit_guide'.format(sides),
                        '{}_low_mid_eyelit_guide'.format(sides),'{}_low_out_eyelit_guide'.format(sides),'{}_out_corner_eyelit_guide'.format(sides)]
        lowCurveListPos = [cmds.xform(obj, q=True, ws=True, translation=True) for obj in lowCurveList]
        low_curve = cmds.curve(d=3,p=lowCurveListPos, name = '{}_eyelit_low_curve'.format(sides))

        #empty group that will contrain everything

        loc = cmds.spaceLocator(absolute=True, name='{}_{}_eyelid_grp'.format(name,sides))[0]
        cmds.delete('{}Shape'.format(loc))

        cmds.delete(cmds.pointConstraint('{}_{}_eyeball_jnt'.format(name,sides), loc))
        cmds.parent(upp_curve,low_curve,loc)

def saveCurveCvPosition(name = None ,side = None):
    directory = 'C:/Users/danie/Documents/maya/2022/scripts/pyTool/guide/eyelid/'
    if not side:
        utili.errorMessage('No side was selected')
    if len(side) == 2:
        side = 'both'
    else:
        side = side

    emptyDict = dict()

    if side == 'both':
        for sides in ('r','l'):
            for cv in range(0, 5):
                for portion in ('upp','low'):
                    cvPos = cmds.xform('{}_eyelit_{}_curve.cv[{}]'.format(sides,portion, cv), t=True, ws=True, q=True)
                    emptyDict.update({'{}_eyelit_{}_curve.cv[{}]'.format(sides,portion, cv): cvPos})
    else:
            for cv in range(0, 5):
                for portion in ('upp', 'low'):
                    cvPos = cmds.xform('{}_eyelit_{}_curve.cv[{}]'.format(side, portion, cv), t=True, ws=True, q=True)
                    emptyDict.update({'{}_eyelit_{}_curve.cv[{}]'.format(side, portion, cv): cvPos})

    utili.nameInputWindow( directory=directory, dictionary = emptyDict )

def loadCurvePosition(name = None ,file_name = None ,l_eye_guide = None,r_eye_guide = None):

    f = open('C:/Users/danie/Documents/maya/2022/scripts/pyTool/guide/eyelid/{}'.format(file_name[0]))

    data = json.load(f)
    side_flag = []
    l_side_flag = False
    r_side_flag = False

    """
    for item in data:
        if 'l_' in item and l_side_flag == False:
            side_flag.append('l')
            l_side_flag = True

            if cmds.objExists('l_socket_cluster') == False or cmds.objExists('l_eyeball_cluster') == False:
                utili.errorMessage('Must create a left cluster in the center of the eyes and in the socket')
            if cmds.objExists('{}_l_socket_jnt_def'.format(name)) == False and cmds.objExists(
                    '{}_l_eyeball_jnt_def'.format(name)) == False:
                l_eye_guide = ['l_socket_cluster', 'l_eyeball_cluster']
                cmds.select(clear=True)
                for item in l_eye_guide:

                    jnt = cmds.joint(name='{}_{}_jnt_def'.format(name, item[:-8]))
                    cmds.delete(cmds.parentConstraint(item, jnt))

        elif 'r_' in item and r_side_flag == False:
            side_flag.append('r')
            r_side_flag = True

            if cmds.objExists('r_socket_cluster') == False or cmds.objExists('r_eyeball_cluster') == False:
                utili.errorMessage('Must create a right cluster in the center of the eyes and in the socket')
            if cmds.objExists('{}_r_socket_jnt_def'.format(name)) == False and cmds.objExists(
                    '{}_r_eyeball_jnt_def'.format(name)) == False:
                r_eye_guide = ['r_socket_cluster', 'r_eyeball_cluster']
                cmds.select(clear=True)
                for item in r_eye_guide:

                    jnt = cmds.joint(name='{}_{}_jnt_def'.format(name, item[:-8]))
                    cmds.delete(cmds.parentConstraint(item, jnt))"""
    for item in data:
        if 'l_' in item and l_side_flag == False:
            side_flag.append('l')
            l_side_flag = True
        elif 'r_' in item and r_side_flag == False:
            side_flag.append('r')
            r_side_flag = True


    l_low_pos = []
    l_upp_pos = []
    r_low_pos = []
    r_upp_pos = []

    for item in data:
        if 'l_' in item and 'low' in item:
            l_low_pos.append(data[item])
        if 'l_' in item and 'upp' in item:
            l_upp_pos.append(data[item])
        if 'r_' in item and 'low' in item:
            r_low_pos.append(data[item])
        if 'r_' in item and 'upp' in item:
            r_upp_pos.append(data[item])

    for side in side_flag:
        #lets create a empty group as a parent of the curves by side
        if cmds.objExists('{}_{}_eyelid_grp'.format(name, side)) == False:
            loc = cmds.spaceLocator(absolute=True, name='{}_{}_eyelid_grp'.format(name, side))[0]
            cmds.delete('{}Shape'.format(loc))
            cmds.delete(cmds.pointConstraint('{}_{}_eyeball_jnt'.format(name, side), loc))

        for section in ('upp', 'low'):
            if cmds.objExists('{}_eyelit_{}_curve'.format(side, section)):
                utili.errorMessage('Curve {} already exist'.format('{}_eyelit_{}_curve'.format(side, section)))
            if side == 'l' and section == 'upp':
                curve = cmds.curve(d=3, p=l_upp_pos, name='{}_eyelit_{}_curve'.format(side, section))
                cmds.parent(curve, loc)
            elif side == 'l' and section == 'low':
                curve = cmds.curve(d=3, p=l_low_pos, name='{}_eyelit_{}_curve'.format(side, section))
                cmds.parent(curve, loc)
            elif side == 'r' and section == 'upp':
                curve = cmds.curve(d=3, p=r_upp_pos, name='{}_eyelit_{}_curve'.format(side, section))
                cmds.parent(curve, loc)
            elif side == 'r' and section == 'low':
                curve = cmds.curve(d=3, p=r_low_pos, name='{}_eyelit_{}_curve'.format(side, section))
                cmds.parent(curve, loc)

    """cmds.select(clear=True)
    # lets create eyeball grp and parent it to the socket
    [cmds.joint(name='{}_{}_eyeball_grp'.format(name, z)) for z in 'lr']
    [cmds.delete(cmds.parentConstraint('{}_eyeball_cluster'.format(z), '{}_{}_eyeball_grp'.format(name, z))) for z in
     'lr']
    [cmds.parent('{}_{}_eyeball_grp'.format(name, z), '{}_{}_socket_jnt_def'.format(name, z)) for z in 'lr']
    """

def mirrorEyelid(name = None, mirror_side = None,edgeloop = None):

    if mirror_side == 'l':
        side = 'r'
        """if cmds.objExists('r_socket_cluster') == False or cmds.objExists('r_eyeball_cluster') == False:
            utili.errorMessage('Must create a right cluster in the center of the eyes and in the socket')
        if cmds.objExists('{}_r_socket_jnt_def'.format(name)) == False and cmds.objExists('{}_r_eyeball_jnt_def'.format(name)) == False:
            r_eye_guide = ['r_socket_cluster', 'r_eyeball_cluster']
            cmds.select(clear=True)
            for item in r_eye_guide:
                jnt = cmds.joint(name='{}_{}_jnt_def'.format(name, item[:-8]))
                cmds.delete(cmds.parentConstraint(item, jnt))"""
    else:
        side = 'l'
        """if cmds.objExists('l_socket_cluster') == False or cmds.objExists('l_eyeball_cluster') == False:
            utili.errorMessage('Must create a left cluster in the center of the eyes and in the socket')
        if cmds.objExists('{}_l_socket_jnt_def'.format(name)) == False and cmds.objExists('{}_l_eyeball_jnt_def'.format(name)) == False:
            l_eye_guide = ['l_socket_cluster', 'l_eyeball_cluster']
            print(l_eye_guide)
            for item in l_eye_guide:
                jnt = cmds.joint(name='{}_{}_jnt_def'.format(name, item[:-8]))
                cmds.delete(cmds.parentConstraint(item, jnt))"""

    if not '{}_eyelit_upp_curve'.format(side) or not '{}_eyelit_low_curve'.format(side):
        utili.errorMessage('No curve for the {} side'.format(mirror_side))

    """if cmds.objExists('{}_{}_eyelid_grp'.format(name, side)) == False:
        loc = cmds.spaceLocator(absolute=True, name='{}_{}_eyelid_grp'.format(name, side))[0]
        cmds.delete('{}Shape'.format(loc))
        cmds.delete(cmds.pointConstraint('{}_{}_eyeball_jnt'.format(name, side), loc))"""
    # create curve
    # for each
    for portion in ('low','upp'):
        list = []
        for i in range(0, 5):
            pos = cmds.xform('{}_eyelit_{}_curve.cv[{}]'.format(mirror_side,portion,i), q=True, ws=True, translation=True)
            list.append([pos[0] * -1, pos[1], pos[2]])
        curve = cmds.curve(d=3, p=list, name='{}_eyelit_{}_curve'.format(side,portion))
        cmds.parent(curve, '{}_{}_eyelid_grp'.format(name, side))

    createEyeLid(name = name,side=side,edgeloop = edgeloop)




def createEyeLid(name = None,portion='upp',side='l',curve= None,edgeloop = None,spread_control = 'normal'):
    if spread_control == 'normal':

        spread_guide = cmds.group(em=True, name='{}_eyelid_guide'.format(name))
        for edges in range(0, edgeloop):
            cmds.addAttr(spread_guide, longName='guide{}'.format(edges), defaultValue=(edges * (1.0 / (21 - 1))),
                         keyable=1)

    elif spread_control == 'side':

        l_spread_guide = cmds.group(em=True, name='{}_l_eyelid_guide'.format(name))
        r_spread_guide = cmds.group(em=True, name='{}_r_eyelid_guide'.format(name))

        for edges in range(0, edgeloop):
            cmds.addAttr(l_spread_guide, longName='guide{}'.format(edges), defaultValue=(edges * (1.0 / (21 - 1))),
                         keyable=1)
            cmds.addAttr(r_spread_guide, longName='guide{}'.format(edges), defaultValue=(edges * (1.0 / (21 - 1))),
                         keyable=1)


    for sides in side:
        for portion in ('low','upp'):
            if sides == 'l':
                if portion == 'upp':
                    move = [0,1,0.5]
                else:
                    move = [0,-1,0.5]
            else:
                if portion == 'upp':
                    move = [0,1,-0.5]
                else:
                    move = [0,-1,-0.5]
            ctrl = utili.createController(name='{}_{}_global_eyelit_{}'.format(name,sides,portion), shape='circle', target=None, contraint_target=None, facing='z',
                                          offsetnumber=3, type='face', size=1 , move =move)

            #cmds.delete(cmds.aimConstraint('{}_{}_eyelid_grp'.format(name, side), '{}_off_constrain'.format(ctrl), aimVector=[0, 0, -1], upVector=[0, 1, 0],worldUpType='objectrotation', worldUpVector=[0, 1, 0],worldUpObject='{}_{}_eyelid_grp'.format(name, side)))

            #let set attributes
            [cmds.addAttr(ctrl, longName=i, defaultValue=0, minValue=-5, maxValue=10, keyable=1) for i in ('inn','mid','out') ]
            plusMinusAverageoff = cmds.createNode('plusMinusAverage', n='{}_plusMinusAverage'.format(ctrl))
            [cmds.connectAttr('{}.translateY'.format(ctrl),'{}.input3D[0].input3D{}'.format(plusMinusAverageoff,axis)) for axis in 'xyz']
            for axis,item in enumerate(('inn','mid','out')):
                if axis == 0:
                    cmds.connectAttr('{}.{}'.format(ctrl,item), '{}.input3D[1].input3D{}'.format(plusMinusAverageoff,'x'))
                elif axis == 1:
                    cmds.connectAttr('{}.{}'.format(ctrl, item), '{}.input3D[1].input3D{}'.format(plusMinusAverageoff, 'y'))
                else:
                    cmds.connectAttr('{}.{}'.format(ctrl, item), '{}.input3D[1].input3D{}'.format(plusMinusAverageoff, 'z'))
            #lets create a locator for each cv of the curve
            for cv in range(0,5):
                loc = cmds.spaceLocator(absolute=True, name='{}_{}_{}_{}_eyelid_loc'.format(name, sides,portion,cv))[0]
                shape = cmds.listRelatives('{}_eyelit_{}_curve'.format(sides,portion), shapes = True)[0]
                print(shape)
                pos = cmds.xform('{}.controlPoints[{}]'.format(shape,cv),query=True, ws=True, translation=True)
                cmds.xform(loc, t=(pos[0], pos[1], pos[2]))
                cmds.parent(loc,'{}_{}_eyelid_grp'.format(name,sides))
                cmds.connectAttr('{}.translate'.format(loc),'{}.controlPoints[{}]'.format(shape,cv))

            for i,remap in enumerate(('inn','mid','out')):
                i = i + 1
                remapNode = cmds.createNode('remapValue', n='{}_{}_eyelid_{}_{}_remapValueV'.format(name, sides,portion,remap))


                if remap == 'mid':
                    cmds.setAttr('{}.inputMin'.format(remapNode), -10)
                    cmds.setAttr('{}.inputMax'.format(remapNode), 10)
                    cmds.setAttr('{}.outputMin'.format(remapNode), -10)
                    cmds.setAttr('{}.outputMax'.format(remapNode), 10)
                    cmds.setAttr('{}.value[2].value_FloatValue'.format(remapNode), 0.45)
                    cmds.setAttr('{}.value[2].value_Position'.format(remapNode), 0.5)
                    cmds.setAttr('{}.value[2].value_Interp'.format(remapNode), 1)
                else:
                    cmds.setAttr('{}.inputMin'.format(remapNode), -10)
                    cmds.setAttr('{}.inputMax'.format(remapNode), 10)
                    cmds.setAttr('{}.outputMin'.format(remapNode), -5)
                    cmds.setAttr('{}.outputMax'.format(remapNode), 5)
                    cmds.setAttr('{}.value[2].value_FloatValue'.format(remapNode), 0.40)
                    cmds.setAttr('{}.value[2].value_Position'.format(remapNode), 0.5)
                    cmds.setAttr('{}.value[2].value_Interp'.format(remapNode), 1)

                if remap == 'inn':
                    cmds.connectAttr('{}.output3Dx'.format(plusMinusAverageoff),'{}.inputValue'.format(remapNode))
                elif remap == 'mid':
                    cmds.connectAttr('{}.output3Dy'.format(plusMinusAverageoff), '{}.inputValue'.format(remapNode))
                else:
                    cmds.connectAttr('{}.output3Dz'.format(plusMinusAverageoff), '{}.inputValue'.format(remapNode))

                cmds.connectAttr('{}.outValue'.format(remapNode),'{}.controlPoints[{}].yValue'.format(shape,i))

            [cmds.setAttr('{}.translate{}'.format('{}_eyelit_{}_curve'.format(sides,portion),axis),0) for axis in 'XYZ']



            #joint creation
            #spread_guide = cmds.group(em=True, name='{}_{}_{}_eyelid_guide'.format(name,sides,portion))
            for edges in range(0 , edgeloop):

                #cmds.addAttr(spread_guide, longName='guide{}'.format(edges), defaultValue=(edges * (1.0 / (21 - 1))),keyable=1)

                pointoncurveinfo = cmds.createNode('pointOnCurveInfo', n='{}_{}_eyelid_{}_pointOnCurveInfo'.format(name, sides, portion))
                cmds.connectAttr('{}.local'.format('{}_eyelit_{}_curve'.format(sides,portion)), '{}.inputCurve'.format(pointoncurveinfo))

                #cmds.connectAttr('{}.guide{}'.format(spread_guide,edges), '{}.parameter'.format(pointoncurveinfo))
                #cmds.setAttr('{}.parameter'.format(pointoncurveinfo),(edges * (1.0/(edgeloop-1))))
                if spread_control == 'normal':
                    cmds.connectAttr('{}.guide{}'.format(spread_guide, edges), '{}.parameter'.format(pointoncurveinfo))
                elif spread_control == 'side':
                    cmds.connectAttr('{}.guide{}'.format('{}_{}_eyelid_guide'.format(name, sides, portion), edges),
                                     '{}.parameter'.format(pointoncurveinfo))


                cmds.setAttr('{}.turnOnPercentage'.format(pointoncurveinfo),1)

                vectorproduct = cmds.createNode('vectorProduct', n='{}_{}_eyelid_{}_vectorProduct'.format(name, sides, portion))
                cmds.setAttr('{}.operation'.format(vectorproduct),0)
                cmds.setAttr('{}.normalizeOutput'.format(vectorproduct), 1)
                cmds.connectAttr('{}.position'.format(pointoncurveinfo),'{}.input1'.format(vectorproduct))

                multiplydivide = cmds.createNode('multiplyDivide', n='{}_{}_eyelid_{}_multiplyDivide'.format(name, sides, portion))
                cmds.connectAttr('{}.output'.format(vectorproduct),'{}.input1'.format(multiplydivide))

                if edges == 0:
                    dist = utili.getdistance(loc, '{}_{}_eyelid_grp'.format(name, sides))

                [cmds.setAttr('{}.input2{}'.format(multiplydivide,axis), dist) for axis in 'XYZ']
                cmds.select(clear=True)
                jnt = cmds.joint(name='{}_{}_eyelid_{}_{}_jnt_def'.format(name, sides, portion, edges))
                cmds.parent(jnt,'{}_{}_eyelid_grp'.format(name,sides))
                cmds.connectAttr('{}.output'.format(multiplydivide),'{}.translate'.format(jnt))
                cmds.aimConstraint('{}_{}_eyelid_grp'.format(name,sides), jnt , aimVector = [0 ,0,-1], upVector = [0,1,0],worldUpType = 'objectrotation',worldUpVector = [0,1,0],worldUpObject = '{}_{}_eyelid_grp'.format(name,sides))


            #lets position the eyelit controller in position
            #we may have to set up he postion of the controller in a better way

            cmds.pointConstraint('{}_{}_eyelid_{}_{}_jnt_def'.format(name, sides, portion, int((edgeloop-1)/2)), '{}_off_constrain'.format(ctrl) )

            ##WORLD SPACE SWITCH
            if not ('{}_eyetarget_world'.format(name)):
                emptyGrp = utili.createEmptyGroup(name='{}_eyetarget_world'.format(name))
                reverse = cmds.createNode('reverse', n='{}_reverse'.format(ctrl))
                cmds.parentConstraint((jnt, emptyGrp), '{}_off'.format(ctrl))
                cmds.connectAttr('{}.space'.format(ctrl), '{}_off_parentConstraint1.{}_eyetarget_worldW1'.format(ctrl, name))
                cmds.connectAttr('{}.space'.format(ctrl), '{}.inputX'.format(reverse))
                cmds.connectAttr('{}.outputX'.format(reverse), '{}_off_parentConstraint1.{}_c_midface_jntW0'.format(ctrl, name))

            #here we aim back to the center of the eye so our controller look parallelo to the surface
            """loc = cmds.spaceLocator(absolute=True, name='{}_{}_{}_eyelid_grp_dummy'.format(name, sides, portion))[0]
            pos_eyelid_grp = cmds.xform('{}_{}_eyelid_grp'.format(name, sides), query=True, ws=True, translation=True)
            pos_eyelid_off = cmds.xform('{}_off'.format(ctrl), query=True, ws=True, translation=True)

            cmds.xform(loc, t=(pos_eyelid_grp[0], pos_eyelid_off[1], pos_eyelid_grp[2]))"""



            """cmds.aimConstraint('{}_{}_{}_eyelid_grp_dummy'.format(name, sides, portion), '{}'.format(ctrl),
                               aimVector=[0, 0, -1], upVector=[0, 1, 0],
                               worldUpType='objectrotation', worldUpVector=[0, 1, 0],
                               worldUpObject='{}_{}_eyelid_grp'.format(name, sides))"""
            #cmds.orientConstraint('{}_{}_eyelid_{}_{}_jnt_def'.format(name, sides, portion, int((edgeloop-1)/2)), '{}_off_constrain'.format(ctrl))

            ### here we aim the controller back to the center off the eye
            cmds.aimConstraint('{}_{}_eyeball_jnt'.format(name, sides), '{}_off_constrain'.format(ctrl), aimVector=[0, 0, -1],
                               upVector=[0, 1, 0], worldUpType='objectrotation', worldUpVector=[0, 1, 0],
                               worldUpObject='{}_{}_eyeball_jnt'.format(name, sides))

            #cmds.aimConstraint('{}_{}_eyelid_grp'.format(name, sides), ctrl, aimVector=[0, 0, -1], upVector=[0, 1, 0], worldUpType='objectrotation',worldUpVector=[0, 1, 0], worldUpObject=jnt)



            # lets delete all locators
            for cv in range(0, 5):
                cmds.delete('{}_{}_{}_{}_eyelid_loc'.format(name, sides, portion, cv))

            # this was move from the createEyeSocketCtrl() function
            for i in range(0, int(edgeloop)):
                [cmds.parent('{}_{}_eyelid_{}_{}_jnt_def'.format(name, side, position, i),
                             '{}_{}_eyeball_grp'.format(name, side)) for position in ('upp', 'low')]
            cmds.setAttr('{}_{}_eyeball_jnt.segmentScaleCompensate'.format(name, side), 0)
            cmds.setAttr('{}_{}_eyeball_grp.segmentScaleCompensate'.format(name, side), 0)

########################################################################################################################
########################################################################################################################
########################################################################################################################
def createEyeballController(name=None, sides='l', targetoff=30):
    if not name:
        cmds.error('createEyeballController must get a name prefix')
    for side in sides:
        fkcurve = cmds.curve(d=3, p=[(0,0,0),(0,0,20)], name='{}_{}_eyelid_fk_ctrl'.format(name, side))
        utili.clearObject(fkcurve)
        off = utili.groupObject(object=fkcurve)

        jntPos = cmds.xform('{}_{}_eyeball_jnt'.format(name, side), t=True, ws=True, q=True)
        cmds.xform(off, t=(jntPos[0], jntPos[1], jntPos[2]))
        cmds.parentConstraint(fkcurve, '{}_{}_eyeball_jnt'.format(name, side))

        cmds.select(clear=True)

        if cmds.objExists('{}_eyetarget_ctrl'.format(name)):
            ctrl = '{}_eyetarget_ctrl'.format(name)
            jnt = '{}_eyelid_center_jnt'.format(name)
            emptyGrp = '{}_{}_eyetarget'.format(name, side)
        else:
            # create empty group
            emptyGrp = utili.createEmptyGroup(name='{}_{}_eyetarget'.format(name, side))
            cmds.xform(emptyGrp, t=(jntPos[0], jntPos[1], jntPos[2] + targetoff))

            # create empty group
            emptyGrp2 = utili.createEmptyGroup(name='{}_r_eyetarget'.format(name))
            cmds.xform(emptyGrp2, t=(jntPos[0]*-1, jntPos[1], jntPos[2] + targetoff))

            ## joint between 2 eyes
            cmds.select(clear=True)
            jnt = cmds.joint(name='{}_eyelid_center_jnt'.format(name))
            cmds.xform(jnt, t=(0, jntPos[1], jntPos[2]))
            # create controller
            ctrl = utili.createController(name='{}_eyetarget'.format(name),character_name = 'Max', shape='circle', target=[emptyGrp,emptyGrp2],
                                          contraint_target=None, facing='z', offsetnumber=2, type='eye_target', size=5)
            cmds.parent( '{}_off'.format(ctrl),jnt)

        cmds.parent(emptyGrp, ctrl)
        cmds.aimConstraint(emptyGrp,off, aimVector=[0, 0, 1], upVector=[0, 1, 0],worldUpType='objectrotation', worldUpVector=[0, 1, 0], worldUpObject=jnt)

########################################################################################################################
########################################################################################################################
########################################################################################################################

def createEyeSocketCtrl(name= None, sides='l',size = 5, facing  = 'x',move=[0,0,10], fk_ctrl = 'Max_r_eyelid_fk_ctrl_off'):

    for side in sides:
        fk_ctrl = '{}_{}_eyelid_fk_ctrl_off'.format(name,side)
        #lets calculate the edge loop by using all the conection to the eyelid group
        conn_list = cmds.listConnections('{}_{}_eyelid_grp'.format(name,side), t='aimConstraint', scn=True)
        dist_list = list(set(conn_list))
        edgeloop = ((len(dist_list)/2))

        ctrl = utili.createController(name='{}_{}_socket'.format(name,side), character_name=None, shape='circle', target='{}_{}_eyesock_jnt'.format(name, side), contraint_target=None,
                               facing=facing, offsetnumber=2, type='fk', size=size, side='l', move= move)

        cmds.parentConstraint(ctrl, '{}_{}_eyesock_jnt'.format(name, side))
        cmds.scaleConstraint(ctrl, '{}_{}_eyesock_jnt'.format(name, side))

        #keep controller separed from the main rig for unreal
        cmds.parent(fk_ctrl,ctrl)

        """ 
        for i in range(0,int(edgeloop)):
                [cmds.parent('{}_{}_eyelid_{}_{}_jnt_def'.format(name, side,position,i),'{}_{}_eyeball_grp'.format(name, side)) for position in ('upp','low')]
        cmds.setAttr('{}_{}_eyeball_jnt.segmentScaleCompensate'.format(name,side),0)
        cmds.setAttr('{}_{}_eyeball_grp.segmentScaleCompensate'.format(name,side), 0)"""



########################################################################################################################
########################################################################################################################
########################################################################################################################
def createMouthPlane(name = None,u= 1,v = 1):
    #validations
    if not cmds.objExists('{}_c_head01_jnt'.format(name)):
        utili.errorMessage('Head join does not exist')

    #end validations

    #position reference base on the head joint
    cvPos = cmds.xform('{}_c_head01_jnt'.format(name), t=True, ws=True, q=True)
    plane = cmds.nurbsPlane(u=u, v=v, w=10, d=3, name='{}_mouth_surface'.format(name), axis=[0, 0, 1])[0]
    cmds.xform(plane, t=(cvPos[0], cvPos[1], cvPos[2] + 20))
    utili.clearObject(plane, scope='freeze')


    return plane
def generateMouthGuide(name = None, mouth_edgeloop = None):

    if not cmds.objExists('{}_c_head01_jnt'.format(name)) :
        utili.errorMessage('Head join does not exist')

    for sides in ('l','r'):
        if sides == 'l':
            multi = 0.5
        else:
            multi = -0.5
        guideList = []

        for y in ('upp', 'low'):
            for x in range(0,mouth_edgeloop):
                if x == 0:
                    if cmds.objExists('c_{}_{:02d}_mouth_guide'.format( y, x)):
                        continue
                    else:
                        guide = cmds.sphere(radius=0.1, name='c_{}_{:02d}_mouth_guide'.format( y, x))
                else:
                    if x == mouth_edgeloop-1 and y == 'low':
                        continue
                    if x == mouth_edgeloop-1 and y == 'upp':
                        guide = cmds.sphere(radius=0.1, name='{}_cor_{:02d}_mouth_guide'.format(sides, x))
                    else:
                        guide = cmds.sphere(radius= 0.1, name = '{}_{}_{:02d}_mouth_guide'.format(sides,y,x))
                    #guideList.append(guide)
                guidePos = cmds.xform('{}_c_head01_jnt'.format(name), t=True, ws=True, q=True)
                if y=='upp':
                    cmds.xform(guide, t=(guidePos[0]+(x*multi), guidePos[1], guidePos[2] + 20))
                else:
                    cmds.xform(guide, t=(guidePos[0] + (x*multi), guidePos[1]-1, guidePos[2] + 20))


        #return guideList

def save_mouth_guide_position(name=None, guide_list = None, surface = None):

    directory = 'C:/Users/danie/Documents/maya/2022/scripts/pyTool/guide/mouth/'

    emptyDict = dict()
    #lets save the surface position first
    if surface:
        for u in range(0, 4):
            for v in range(0, 4):
                cvPos = cmds.xform('{}.cv[{}][{}]'.format(surface, u, v),t=True, ws=True, q=True)
                emptyDict.update({'{}.cv[{}][{}]'.format(surface, u, v): cvPos})
    if len(guide_list) > 0:
        for item in guide_list:
            cvPos = cmds.xform(item, t=True, ws=True, q=True)
            emptyDict.update({item: cvPos})

    utili.nameInputWindow(directory=directory, dictionary=emptyDict)


def load_mouth_guide_position(name = None ,file_name = None):
    f = open(
        'C:/Users/danie/Documents/maya/2022/scripts/pyTool/guide/mouth/{}'.format(file_name[0]))

    data = json.load(f)

    all_exist = True
    for item in data:
        if not utili.objectExist(item):
            all_exist = False

    if all_exist:
        for item in data:
            cmds.xform(item, t=data[item])
    else:
        utili.errorMessage('Not all object listed in the this file exist')

def build_mouth_system(name = None ,guide_list = None,edgeloop = None,detail = 1):
    #lets create the jaw guides
    empty_jaw_grp = build_jaw_guide(name=name, edgeloop=edgeloop)

    #lets create
    # now we are going to create a locator to calculate the closes point on surface for each joint
    loc = cmds.spaceLocator(absolute=True, name='guide_loc')[0]
    loc_closestPointOnSurface = cmds.createNode('closestPointOnSurface',n='{}_closestPointOnSurface_del'.format(loc))

    cmds.connectAttr('{}.translate'.format(loc), '{}.inPosition'.format(loc_closestPointOnSurface))
    cmds.connectAttr('{}.worldSpace[0]'.format('{}_mouth_surface'.format(name)),'{}.inputSurface'.format(loc_closestPointOnSurface))

    lip_joint_list = []
    for guide in guide_list:
        cmds.select(clear=True)
        lip_jnt = cmds.joint(name='{}_{}_lip_jnt_def'.format(name,guide[:-12]))
        lip_joint_list.append(lip_jnt)
        cmds.select(clear=True)
        jaw_jnt = cmds.joint(name='{}_{}_jaw_jnt'.format(name, guide[:-12]))

        #lip is children of jaw
        cmds.parent(lip_jnt,jaw_jnt)
        #move jaw joint to the position of the guides
        guidePos = cmds.xform(guide, t=True, ws=True, q=True)
        cmds.xform(jaw_jnt, t=(guidePos[0], guidePos[1], guidePos[2]))

        #lets hide jaw joints
        cmds.setAttr('{}.drawStyle'.format(jaw_jnt),2)

        # add structure for facial
        add_join_lip_structure(name, lip_jnt, loc, loc_closestPointOnSurface)

        #parent constrain to split weight between lowface joint and jaw joint using are guide
        jaw_constrain = cmds.parentConstraint(('{}_c_lowface_jnt'.format(name),'{}_c_jaw_jnt'.format(name)),jaw_jnt, maintainOffset=True)[0]

        #connect this constrain to the weight guides
        assign_jaw_weight_guide(name = name,jaw_constrain=jaw_constrain,jaw_jnt = jaw_jnt,guide = guide[:-12],num_guides =edgeloop)



    if detail == 1:
        controller_list = ['c_glo_00', 'l_cor_{:02d}'.format(edgeloop-1), 'r_cor_{:02d}'.format(edgeloop-1), 'c_upp_00', 'c_low_00', 'l_upp_{:02d}'.format(math.ceil(edgeloop/2)), 'l_low_{:02d}'.format(math.ceil(edgeloop/2)),
                           'r_upp_{:02d}'.format(math.ceil(edgeloop/2)), 'r_low_{:02d}'.format(math.ceil(edgeloop/2))]


    #controller_list = ['c_glo_00','l_cor_09','r_cor_09','c_upp_00','c_low_00','l_upp_05','l_low_05','r_upp_05','r_low_05']
    #controller_list = ['c_glo_00','l_cor_09','r_cor_09','c_upp_00','c_low_00','l_upp_05','l_low_05','r_upp_05','r_low_05']
    # create basic controller structure
    build_mouth_controller(name  = name,controller_list = controller_list, lip_joint_list = lip_joint_list, edgeloop = edgeloop)





def add_join_lip_structure(name = None,lip_jnt = None,loc = None, loc_closestPointOnSurface = None):
    plusMinusAverage = cmds.createNode('plusMinusAverage',n= '{}_plusMinusAverageStart'.format(lip_jnt))
    pointOnSurfaceInfo = cmds.createNode('pointOnSurfaceInfo',n='{}_pointOnSurfaceInfo'.format(lip_jnt))
    #connections
    cmds.connectAttr('{}.output2Dx'.format(plusMinusAverage),'{}.parameterU'.format(pointOnSurfaceInfo))
    cmds.connectAttr('{}.output2Dy'.format(plusMinusAverage), '{}.parameterV'.format(pointOnSurfaceInfo))

    #four by four matrix
    fourByFourMatrix = cmds.createNode('fourByFourMatrix', n='{}_fourByFourMatrix'.format(lip_jnt))
    #connections
    for count, x in enumerate(('normalizedTangentU', 'normalizedTangentV', 'normalizedNormal', 'position')):
        for i, axis in enumerate('XYZ'):
            cmds.connectAttr('{}.{}{}'.format(pointOnSurfaceInfo, x, axis),
                             '{}.in{}{}'.format(fourByFourMatrix, count, i), force=True)
    #descompose matrix
    decomposeMatrix = cmds.createNode('decomposeMatrix',n='{}_decomposeMatrix'.format(lip_jnt))
    #connections
    cmds.connectAttr('{}.output'.format(fourByFourMatrix), '{}.inputMatrix'.format(decomposeMatrix), force=True)

    # animBlendNodeAdditiveRotation
    animBlendNodeAdditiveRotation = cmds.createNode('animBlendNodeAdditiveRotation', n='{}_animBlendNodeAdditiveRotation'.format(lip_jnt))
    plusMinusAverageEnd = cmds.createNode('plusMinusAverage',n='{}_plusMinusAverageEnd'.format(lip_jnt))
    cmds.setAttr('{}.operation'.format(plusMinusAverageEnd),2)
    ### connections
    cmds.connectAttr('{}.outputRotateX'.format(decomposeMatrix),'{}.inputAX'.format(animBlendNodeAdditiveRotation))
    cmds.connectAttr('{}.outputTranslate'.format(decomposeMatrix), '{}.input3D[0]'.format(plusMinusAverageEnd))
    cmds.connectAttr('{}.inputAX'.format(animBlendNodeAdditiveRotation), '{}.rotateX'.format(lip_jnt))
    cmds.connectAttr('{}.outputRotateY'.format(decomposeMatrix), '{}.rotateY'.format(lip_jnt))
    cmds.connectAttr('{}.outputRotateZ'.format(decomposeMatrix), '{}.rotateZ'.format(lip_jnt))
    cmds.connectAttr('{}.output3D'.format(plusMinusAverageEnd), '{}.translate'.format(lip_jnt))

    #from here lets add the offset for the joints base on the surface using this locator as a dummy guide
    cmds.delete(cmds.pointConstraint(lip_jnt,loc))

    u_value = cmds.getAttr('{}.parameterU'.format(loc_closestPointOnSurface))
    v_value = cmds.getAttr('{}.parameterV'.format(loc_closestPointOnSurface))

    positions = cmds.getAttr('{}.result.position'.format(loc_closestPointOnSurface))[0]

    [cmds.setAttr('{}.input3D[1].input3D{}'.format(plusMinusAverageEnd,axis),positions[i]) for i,axis in enumerate('xyz')]

    cmds.setAttr('{}.input2D[0].input2Dx'.format(plusMinusAverage), u_value)
    cmds.setAttr('{}.input2D[0].input2Dy'.format(plusMinusAverage), v_value)

    cmds.connectAttr('{}.worldSpace[0]'.format('{}_mouth_surface'.format(name)),'{}.inputSurface'.format(pointOnSurfaceInfo))




def assign_jaw_weight_guide(name = None,jaw_constrain=None, jaw_jnt= None,guide= None,num_guides= None):
    if guide[6:] == '00':
        if  guide[2:-3] == 'upp':
            cmds.setAttr('{}.{}_c_lowface_jntW0'.format(jaw_constrain,name),1)
            cmds.setAttr('{}.{}_c_jaw_jntW1'.format(jaw_constrain, name), 0)
        elif guide[2:-3] == 'low':
            cmds.setAttr('{}.{}_c_lowface_jntW0'.format(jaw_constrain, name), 0)
            cmds.setAttr('{}.{}_c_jaw_jntW1'.format(jaw_constrain, name), 1)
    elif guide[:1] == 'c':
        cmds.setAttr('{}.{}_c_lowface_jntW0'.format(jaw_constrain, name), 0.5)
        cmds.setAttr('{}.{}_c_jaw_jntW1'.format(jaw_constrain, name), 0.5)
    else:
        reverse_input = cmds.listConnections('{}_jaw_guide.weight_{:02d}'.format(name,int(guide[6:])), p=True,t='reverse')
        axis_output = reverse_input[0][-1:]
        reverse_node = reverse_input[0][:-7]
        if  guide[2:-3] == 'upp':
            # upp
            cmds.connectAttr('{}.output{}'.format(reverse_node,axis_output), '{}.{}_c_jaw_jntW1'.format(jaw_constrain,name))
            cmds.connectAttr('{}_jaw_guide.weight_{:02d}'.format(name,int(guide[6:])), '{}.{}_c_lowface_jntW0'.format(jaw_constrain, name))
        if  guide[2:-3] == 'low':
            # low
            print(reverse_node)
            cmds.connectAttr('{}.output{}'.format(reverse_node,axis_output), '{}.{}_c_lowface_jntW0'.format(jaw_constrain, name))
            cmds.connectAttr('{}_jaw_guide.weight_{:02d}'.format(name,int(guide[6:])),'{}.{}_c_jaw_jntW1'.format(jaw_constrain, name))


def build_jaw_guide(name = None,edgeloop = None):
    # lets create the jaw guides
    empty_jaw_grp = utili.createEmptyGroup(name='{}_jaw_guide'.format(name))
    # this value will define how many reverse node we need for this guide values
    num_reverse_node = math.floor((edgeloop - 1 / 3) + 0.9)
    for i in range(0, num_reverse_node):
        reverse = cmds.createNode('reverse', n='{}_{:02d}_reverse'.format(empty_jaw_grp, i))
        [cmds.addAttr(empty_jaw_grp, longName='weight_{:02d}'.format((i * 3) + y),
                      defaultValue=(1 - (((i * 3) + y) * 0.03)), at='double', keyable=1) for y in range(1, 4)]
        [cmds.connectAttr('{}.weight_{:02d}'.format(empty_jaw_grp, ((i * 3) + (x + 1))),
                          '{}.input{}'.format(reverse, axis)) for x, axis in enumerate(('X', 'Y', 'Z'))]


    for i in range (1, edgeloop -1):

        cmds.addAttr(empty_jaw_grp,longName='vFallOffRearange_{:02d}'.format(i),at='double', keyable=1)
        cmds.addAttr(empty_jaw_grp,longName='vFallOff_{:02d}'.format(i), at='double', keyable=1)
        multDoubleLinearU = cmds.createNode('multDoubleLinear', n='{}_guide_v_falloff_{:02d}_multDoubleLinearV'.format(name, i))
        cmds.setAttr('{}.input2'.format(multDoubleLinearU), 0.05)
        cmds.connectAttr('{}.vFallOff_{:02d}'.format(empty_jaw_grp,i),'{}.input1'.format(multDoubleLinearU))
        cmds.connectAttr('{}.output'.format(multDoubleLinearU), '{}.vFallOffRearange_{:02d}'.format(empty_jaw_grp,i))

    for i in range(1, edgeloop - 1):
        #mid rearange
        cmds.addAttr(empty_jaw_grp, longName='vFallOffMidRearange_{:02d}'.format(i), at='double', keyable=1)
        cmds.addAttr(empty_jaw_grp, longName='vFallOffMid_{:02d}'.format(i), at='double', keyable=1)
        multDoubleLinearUmid = cmds.createNode('multDoubleLinear',n='{}_guide_v_falloffmid_{:02d}_multDoubleLinearV'.format(name, i))
        cmds.setAttr('{}.input2'.format(multDoubleLinearUmid), 0.05)
        cmds.connectAttr('{}.vFallOffMid_{:02d}'.format(empty_jaw_grp, i), '{}.input1'.format(multDoubleLinearUmid))
        cmds.connectAttr('{}.output'.format(multDoubleLinearUmid), '{}.vFallOffMidRearange_{:02d}'.format(empty_jaw_grp, i))

    for i in range(0, edgeloop - 1):
        #deforme controller
        ##upp
        cmds.addAttr(empty_jaw_grp, longName='vFallOffUpCurveRearange_{:02d}'.format(i), at='double', keyable=1)
        cmds.addAttr(empty_jaw_grp, longName='vFallOffUpCurve_{:02d}'.format(i), at='double', keyable=1)
        multDoubleLinearUppcurve = cmds.createNode('multDoubleLinear',n='{}_guide_v_falloffUpCurve_{:02d}_multDoubleLinearV'.format(name, i))
        cmds.setAttr('{}.input2'.format(multDoubleLinearUppcurve), 0.05)
        cmds.connectAttr('{}.vFallOffUpCurve_{:02d}'.format(empty_jaw_grp, i), '{}.input1'.format(multDoubleLinearUppcurve))
        cmds.connectAttr('{}.output'.format(multDoubleLinearUppcurve),'{}.vFallOffUpCurveRearange_{:02d}'.format(empty_jaw_grp, i))
    for i in range(0, edgeloop - 1):
        ##low
        cmds.addAttr(empty_jaw_grp, longName='vFallOffLoCurveRearange_{:02d}'.format(i), at='double', keyable=1)
        cmds.addAttr(empty_jaw_grp, longName='vFallOffLoCurve_{:02d}'.format(i), at='double', keyable=1)
        multDoubleLinearLowCurve = cmds.createNode('multDoubleLinear',n='{}_guide_v_falloffLoCurve_{:02d}_multDoubleLinearV'.format(name, i))
        cmds.setAttr('{}.input2'.format(multDoubleLinearLowCurve), 0.05)
        cmds.connectAttr('{}.vFallOffLoCurve_{:02d}'.format(empty_jaw_grp, i), '{}.input1'.format(multDoubleLinearLowCurve))
        cmds.connectAttr('{}.output'.format(multDoubleLinearLowCurve),'{}.vFallOffLoCurveRearange_{:02d}'.format(empty_jaw_grp, i))

    ############################################################################################################################################

    for i in range(0, edgeloop - 1):
        ## U CONTROLLER SIDE
        cmds.addAttr(empty_jaw_grp, longName='vFallOff_ctrl_Rearange_{:02d}'.format(i), at='double', keyable=1)
        cmds.addAttr(empty_jaw_grp, longName='vFallOff_ctrl_{:02d}'.format(i), at='double', keyable=1)
        multDoubleLinear_ctrl = cmds.createNode('multDoubleLinear',n='{}_guide_v_falloff_ctrl_{:02d}_multDoubleLinearU'.format(name, i))
        cmds.setAttr('{}.input2'.format(multDoubleLinear_ctrl), 0.025)
        cmds.connectAttr('{}.vFallOff_ctrl_{:02d}'.format(empty_jaw_grp, i), '{}.input1'.format(multDoubleLinear_ctrl))
        cmds.connectAttr('{}.output'.format(multDoubleLinear_ctrl),'{}.vFallOff_ctrl_Rearange_{:02d}'.format(empty_jaw_grp, i))

    for i in range(0, edgeloop - 1):
        ## U CONTROLLER OPOSSITE SIDE
        cmds.addAttr(empty_jaw_grp, longName='vFallOff_ctrl_opposite_Rearange_{:02d}'.format(i), at='double', keyable=1)
        cmds.addAttr(empty_jaw_grp, longName='vFallOff_ctrl_opposite_{:02d}'.format(i), at='double', keyable=1)
        multDoubleLinear_ctrl_opposite = cmds.createNode('multDoubleLinear',n='{}_guide_v_falloff_ctrl_opposite_{:02d}_multDoubleLinearU'.format(name, i))
        cmds.setAttr('{}.input2'.format(multDoubleLinear_ctrl_opposite), 0.025)
        cmds.connectAttr('{}.vFallOff_ctrl_opposite_{:02d}'.format(empty_jaw_grp, i), '{}.input1'.format(multDoubleLinear_ctrl_opposite))
        cmds.connectAttr('{}.output'.format(multDoubleLinear_ctrl_opposite),'{}.vFallOff_ctrl_opposite_Rearange_{:02d}'.format(empty_jaw_grp, i))




    return empty_jaw_grp

def build_mouth_controller(name  = None,controller_list= None, lip_joint_list = None, edgeloop = None):
    #controller_list = ['c_glo_00','l_cor_09','r_cor_09','c_upp_00','c_low_00','l_upp_05','l_low_05','r_upp_05','r_low_05']
    for i,ctrl_prefix in enumerate(controller_list):
        print(ctrl_prefix)
        #we want to make sure this does not interfere with any other controller
        plusMinusAverage_start_POS = i+1
        if ctrl_prefix[:1] == 'l':
            move = [0, 0, 0.5]
        elif ctrl_prefix[:1] == 'c':
            move = [0, 0, 1]
        elif ctrl_prefix[:1] == 'r':
            move = [0, 0, -0.5]

        if ctrl_prefix[2:-3] == 'glo':
            joint_target = '{}_c_low_00_lip_jnt_def'.format(name)
            ctrl_size = 1
        elif ctrl_prefix[2:-3] == 'cor':
            joint_target = '{}_{}_cor_{:02d}_lip_jnt_def'.format(name,ctrl_prefix[:1],edgeloop-1)
            ctrl_size = 0.5

        elif ctrl_prefix[:1] == 'c' and ctrl_prefix[2:-3] != 'glo':
            joint_target = '{}_{}_{}_{}_lip_jnt_def'.format(name, ctrl_prefix[:1], ctrl_prefix[2:-3], ctrl_prefix[-2:])
            ctrl_size = 0.5
        else:
            joint_target = '{}_{}_{}_{}_lip_jnt_def'.format(name,ctrl_prefix[:1] ,ctrl_prefix[2:-3],ctrl_prefix[-2:])
            ctrl_size = 0.25

        ctrl = utili.createController(name='{}_{}_lip'.format(name,ctrl_prefix), shape='circle',target=None, contraint_target=None, facing='z',
                                      offsetnumber=3, type='face', size=ctrl_size, move = move)

        constrain = cmds.parentConstraint( joint_target,'{}_off_constrain'.format(ctrl),maintainOffset=False)[0]

        multDoubleLinearU = cmds.createNode('multDoubleLinear', n='{}_multDoubleLinearU'.format(joint_target))
        multDoubleLinearV = cmds.createNode('multDoubleLinear', n='{}_multDoubleLinearV'.format(joint_target))

        cmds.connectAttr('{}.translateY'.format(ctrl),'{}.input1'.format(multDoubleLinearV))
        cmds.connectAttr('{}.output'.format(multDoubleLinearV),'{}_plusMinusAverageStart.input2D[{}].input2Dy'.format(joint_target,plusMinusAverage_start_POS))
        cmds.connectAttr('{}.translateX'.format(ctrl), '{}.input1'.format(multDoubleLinearU))
        cmds.connectAttr('{}.output'.format(multDoubleLinearU),'{}_plusMinusAverageStart.input2D[{}].input2Dx'.format(joint_target,plusMinusAverage_start_POS))


        if ctrl[:1] == 'r':
            cmds.setAttr('{}.input2'.format(multDoubleLinearV),0.05)
            cmds.setAttr('{}.input2'.format(multDoubleLinearU), -0.025)
            cmds.setAttr('{}.target[0].targetOffsetRotateY'.format(constrain), 180)
        else:
            cmds.setAttr('{}.input2'.format(multDoubleLinearV),0.05)
            cmds.setAttr('{}.input2'.format(multDoubleLinearU), 0.025)

        for joint_lip in lip_joint_list:
            if joint_lip != joint_target:
                jnt_num = int((joint_lip[10:])[:2])
                u_val = 0.0
                if (joint_lip[:(len(name) + 2)])[-1:] == 'r':
                    u_val = (((1/(edgeloop - 1))* jnt_num ) * 0.025)
                elif (joint_lip[:(len(name) + 2)])[-1:] == 'l':
                    u_val = (((1/(edgeloop - 1)) * jnt_num) * 0.025)

                # corner controller
                if ctrl_prefix[2:-3] == 'cor'  and ctrl_prefix[:1] == (joint_lip[:(len(name) + 2)])[-1:]:

                    multDoubleLinearU = cmds.createNode('multDoubleLinear',n='{}_{}_multDoubleLinearU'.format(joint_lip, ctrl_prefix))
                    multDoubleLinearV = cmds.createNode('multDoubleLinear',n='{}_{}_multDoubleLinearV'.format(joint_lip, ctrl_prefix))
                    cmds.connectAttr('{}.translateX'.format(ctrl), '{}.input1'.format(multDoubleLinearU))
                    cmds.connectAttr('{}.output'.format(multDoubleLinearU),'{}_plusMinusAverageStart.input2D[{}].input2Dx'.format(joint_lip,plusMinusAverage_start_POS))
                    cmds.connectAttr('{}.translateY'.format(ctrl), '{}.input1'.format(multDoubleLinearV))
                    cmds.connectAttr('{}.output'.format(multDoubleLinearV),'{}_plusMinusAverageStart.input2D[{}].input2Dy'.format(joint_lip,plusMinusAverage_start_POS))
                    ### u value
                    cmds.setAttr('{}.input2'.format(multDoubleLinearU), u_val)
                    ### v value
                    cmds.connectAttr('{}.vFallOffRearange_{}'.format('{}_jaw_guide'.format(name),(joint_lip[10:])[:2]),'{}.input2'.format(multDoubleLinearV))

                if ctrl_prefix[:1] == 'c' and ctrl_prefix[2:-3] not in ['glo','cor'] and  ctrl_prefix[2:-3] == (joint_lip[6:])[:-15]:
                    multDoubleLinearU = cmds.createNode('multDoubleLinear',n='{}_{}_multDoubleLinearU'.format(joint_lip, ctrl_prefix))
                    multDoubleLinearV = cmds.createNode('multDoubleLinear',n='{}_{}_multDoubleLinearV'.format(joint_lip, ctrl_prefix))
                    cmds.connectAttr('{}.translateX'.format(ctrl), '{}.input1'.format(multDoubleLinearU))
                    cmds.connectAttr('{}.output'.format(multDoubleLinearU),'{}_plusMinusAverageStart.input2D[{}].input2Dx'.format(joint_lip,plusMinusAverage_start_POS))
                    cmds.connectAttr('{}.translateY'.format(ctrl), '{}.input1'.format(multDoubleLinearV))
                    cmds.connectAttr('{}.output'.format(multDoubleLinearV),'{}_plusMinusAverageStart.input2D[{}].input2Dy'.format(joint_lip,plusMinusAverage_start_POS))
                    ### u value
                    cmds.setAttr('{}.input2'.format(multDoubleLinearU), (u_val *-1) + 0.025)
                    ### v value
                    cmds.connectAttr('{}.vFallOffMidRearange_{}'.format('{}_jaw_guide'.format(name), (joint_lip[10:])[:2]),
                                     '{}.input2'.format(multDoubleLinearV))

                if ctrl_prefix[:1] == 'c' and ctrl_prefix[2:-3]  == 'glo':

                    multDoubleLinearU = cmds.createNode('multDoubleLinear',n='{}_{}_multDoubleLinearU'.format(joint_lip, ctrl_prefix))
                    multDoubleLinearV = cmds.createNode('multDoubleLinear',n='{}_{}_multDoubleLinearV'.format(joint_lip, ctrl_prefix))
                    cmds.connectAttr('{}.translateX'.format(ctrl), '{}.input1'.format(multDoubleLinearU))
                    cmds.connectAttr('{}.output'.format(multDoubleLinearU),'{}_plusMinusAverageStart.input2D[{}].input2Dx'.format(joint_lip,plusMinusAverage_start_POS))
                    cmds.connectAttr('{}.translateY'.format(ctrl), '{}.input1'.format(multDoubleLinearV))
                    cmds.connectAttr('{}.output'.format(multDoubleLinearV),'{}_plusMinusAverageStart.input2D[{}].input2Dy'.format(joint_lip,plusMinusAverage_start_POS))
                    ### u value
                    cmds.setAttr('{}.input2'.format(multDoubleLinearU), 0.025)
                    ### v value
                    cmds.setAttr('{}.input2'.format(multDoubleLinearV), 0.05)

                if ctrl_prefix[:1] in ['l','r'] and ctrl_prefix[2:-3] == 'upp' and ctrl_prefix[2:-3] == (joint_lip[6:])[:-15]:
                    print('upp if')
                    print(joint_lip)
                    multDoubleLinearU = cmds.createNode('multDoubleLinear',n='{}_{}_multDoubleLinearU'.format(joint_lip, ctrl_prefix))
                    multDoubleLinearV = cmds.createNode('multDoubleLinear',n='{}_{}_multDoubleLinearV'.format(joint_lip, ctrl_prefix))
                    cmds.connectAttr('{}.translateX'.format(ctrl), '{}.input1'.format(multDoubleLinearU))
                    cmds.connectAttr('{}.output'.format(multDoubleLinearU),'{}_plusMinusAverageStart.input2D[{}].input2Dx'.format(joint_lip,plusMinusAverage_start_POS))
                    cmds.connectAttr('{}.translateY'.format(ctrl), '{}.input1'.format(multDoubleLinearV))
                    cmds.connectAttr('{}.output'.format(multDoubleLinearV),'{}_plusMinusAverageStart.input2D[{}].input2Dy'.format(joint_lip,plusMinusAverage_start_POS))


                    if ctrl_prefix[:1] in ['l']:
                        if (joint_lip[4:])[:-19] == 'r':
                            ### v value
                            cmds.connectAttr(
                                '{}.vFallOffLoCurveRearange_{}'.format('{}_jaw_guide'.format(name),(joint_lip[10:])[:2]),
                                '{}.input2'.format(multDoubleLinearV))
                            ### u value
                            cmds.connectAttr('{}.vFallOff_ctrl_opposite_Rearange_{}'.format('{}_jaw_guide'.format(name),
                                                                                            (joint_lip[10:])[:2]),
                                             '{}.input2'.format(multDoubleLinearU))
                        elif (joint_lip[4:])[:-19] in ['l','c']:
                            ### v value
                            cmds.connectAttr(
                                '{}.vFallOffUpCurveRearange_{}'.format('{}_jaw_guide'.format(name), (joint_lip[10:])[:2]),
                                '{}.input2'.format(multDoubleLinearV))
                            ### u value
                            cmds.connectAttr('{}.vFallOff_ctrl_Rearange_{}'.format('{}_jaw_guide'.format(name),
                                                                                   (joint_lip[10:])[:2]),
                                             '{}.input2'.format(multDoubleLinearU))
                    elif ctrl_prefix[:1] in ['r']:
                        if (joint_lip[4:])[:-19] == 'l':
                            ### v value
                            cmds.connectAttr(
                                '{}.vFallOffLoCurveRearange_{}'.format('{}_jaw_guide'.format(name),
                                                                       (joint_lip[10:])[:2]),
                                '{}.input2'.format(multDoubleLinearV))
                            ### u value
                            cmds.connectAttr('{}.vFallOff_ctrl_opposite_Rearange_{}'.format('{}_jaw_guide'.format(name),
                                                                                            (joint_lip[10:])[:2]),
                                             '{}.input2'.format(multDoubleLinearU))
                        elif (joint_lip[4:])[:-19] in ['r','c']:
                            ### v value
                            cmds.connectAttr(
                                '{}.vFallOffUpCurveRearange_{}'.format('{}_jaw_guide'.format(name),
                                                                       (joint_lip[10:])[:2]),
                                '{}.input2'.format(multDoubleLinearV))
                            ### u value
                            cmds.connectAttr('{}.vFallOff_ctrl_Rearange_{}'.format('{}_jaw_guide'.format(name),
                                                                                   (joint_lip[10:])[:2]),
                                             '{}.input2'.format(multDoubleLinearU))

                if ctrl_prefix[:1] in ['l', 'r'] and ctrl_prefix[2:-3] == 'low' and ctrl_prefix[2:-3] == (joint_lip[6:])[:-15]:

                    multDoubleLinearU = cmds.createNode('multDoubleLinear',n='{}_{}_multDoubleLinearU'.format(joint_lip, ctrl_prefix))
                    multDoubleLinearV = cmds.createNode('multDoubleLinear',n='{}_{}_multDoubleLinearV'.format(joint_lip, ctrl_prefix))
                    cmds.connectAttr('{}.translateX'.format(ctrl), '{}.input1'.format(multDoubleLinearU))
                    cmds.connectAttr('{}.output'.format(multDoubleLinearU),'{}_plusMinusAverageStart.input2D[{}].input2Dx'.format(joint_lip,plusMinusAverage_start_POS))
                    cmds.connectAttr('{}.translateY'.format(ctrl), '{}.input1'.format(multDoubleLinearV))
                    cmds.connectAttr('{}.output'.format(multDoubleLinearV),'{}_plusMinusAverageStart.input2D[{}].input2Dy'.format(joint_lip,plusMinusAverage_start_POS))



                    if ctrl_prefix[:1] in ['l']:

                        if (joint_lip[4:])[:-19] == 'r':
                            ### v value
                            cmds.connectAttr('{}.vFallOffLoCurveRearange_{}'.format('{}_jaw_guide'.format(name),(joint_lip[10:])[:2]),'{}.input2'.format(multDoubleLinearV))
                            ### u value
                            #cmds.setAttr('{}.input2'.format(multDoubleLinearU), 0.025)
                            cmds.connectAttr('{}.vFallOff_ctrl_opposite_Rearange_{}'.format('{}_jaw_guide'.format(name),
                                                                                            (joint_lip[10:])[:2]),
                                             '{}.input2'.format(multDoubleLinearU))

                        elif (joint_lip[4:])[:-19] in ['l','c']:
                            ### v value
                            cmds.connectAttr('{}.vFallOffUpCurveRearange_{}'.format('{}_jaw_guide'.format(name),(joint_lip[10:])[:2]),'{}.input2'.format(multDoubleLinearV))
                            ### u value
                            #cmds.setAttr('{}.input2'.format(multDoubleLinearU), 0.025)
                            cmds.connectAttr('{}.vFallOff_ctrl_Rearange_{}'.format('{}_jaw_guide'.format(name),
                                                                                   (joint_lip[10:])[:2]),
                                             '{}.input2'.format(multDoubleLinearU))

                    elif ctrl_prefix[:1] in ['r']:

                        if (joint_lip[4:])[:-19] == 'l':
                            ### v value
                            cmds.connectAttr('{}.vFallOffLoCurveRearange_{}'.format('{}_jaw_guide'.format(name),(joint_lip[10:])[:2]),'{}.input2'.format(multDoubleLinearV))
                            ### u value
                            cmds.setAttr('{}.input2'.format(multDoubleLinearU), 0.025)
                            cmds.connectAttr('{}.vFallOff_ctrl_opposite_Rearange_{}'.format('{}_jaw_guide'.format(name),
                                                                                   (joint_lip[10:])[:2]),
                                             '{}.input2'.format(multDoubleLinearU))

                        elif (joint_lip[4:])[:-19] in ['r','c']:
                            ### v value
                            cmds.connectAttr('{}.vFallOffUpCurveRearange_{}'.format('{}_jaw_guide'.format(name),(joint_lip[10:])[:2]),'{}.input2'.format(multDoubleLinearV))
                            ### u value
                            #cmds.setAttr('{}.input2'.format(multDoubleLinearU), 0.025)
                            cmds.connectAttr('{}.vFallOff_ctrl_Rearange_{}'.format('{}_jaw_guide'.format(name),
                                                                                    (joint_lip[10:])[:2]),
                                             '{}.input2'.format(multDoubleLinearU))

def save_mouth_jaw_guide_numbers(name = None,object=None):

    emptyDict = dict()
    attriburtes_list = cmds.listAttr(object, r=True, s=True, k=True)

    for att in attriburtes_list:
        if att not in ['visibility', 'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY',
                       'rotateZ',
                       'scaleX', 'scaleY', 'scaleZ'] and 'Rearange' not in att:
            value = cmds.getAttr('{}.{}'.format('{}_jaw_guide'.format(name), att))
            emptyDict.update({att: value})

    directory = '/mouth/guide/'
    utili.nameInputWindow(directory=directory, dictionary=emptyDict)

def load_mouth_jaw_guide_numbers(name=None, file_name=None):

    data = utili.file_manage(section_dir='mouth/guide/{}'.format(file_name[0]), action='load')
    #f = open('/Users/danieliglesiasvalenzuela/Library/Preferences/Autodesk/maya/2022/prefs/scripts/pyTool/guide/mouth/guide/{}'.format(file_name[0]))
    #data = json.load(f)
    all_exist = True
    for item in data:
        if not utili.objectExist('Max_jaw_guide.{}'.format(item)):
            all_exist = False

    if all_exist:
        for item in data:
            for item in data:
                cmds.setAttr('{}_jaw_guide.{}'.format(name,item), data[item])
    else:
        utili.errorMessage('Not all object listed in the this file exist')


def save_eyelit_guide_numbers(name=None, object=None):
    final_dict = dict()
    if not object:
        utili.errorMessage('save_eyelit_guide_numbers did not receive an object')
    if len(object) == 1:
        emptyDict1 = dict()

        attriburtes_list = cmds.listAttr(object[0], r=True, s=True, k=True)
        for att in attriburtes_list:
            if att not in ['visibility', 'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY',
                           'rotateZ',
                           'scaleX', 'scaleY', 'scaleZ'] and 'Rearange' not in att:
                value = cmds.getAttr('{}.{}'.format(object[0], att))
                emptyDict1.update({att: value})
        ## only one dictionary
        final_dict.update({object[0]: emptyDict1})

    elif len(object) >= 2:

        emptyDict = dict()
        for item in object:
            attriburtes_list = cmds.listAttr(item, r=True, s=True, k=True)

        for att in attriburtes_list:
            if att not in ['visibility', 'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY',
                           'rotateZ',
                           'scaleX', 'scaleY', 'scaleZ']:
                value = cmds.getAttr('{}.{}'.format(item, att))
                emptyDict.update({att: value})
            final_dict.update({item: emptyDict})

    directory = 'eyelid/guide/'
    utili.nameInputWindow(section_dir=directory, dictionary=final_dict)


def load_eyelit_guide_numbers(name=None, file_name=None):
    data = utili.file_manage(section_dir='eyelid/guide/{}'.format(file_name[0]), action='load')

    for x, obj in data.items():
        if not utili.objectExist(x):
            utili.errorMessage('Guide with the name of {} does not exist')
        else:
            for y in obj:
                cmds.setAttr('{}.{}'.format(x, y), obj[y])
            utili.errorMessage('Successfully loaded guide')


def build_face_guide(name = None,base_object = 'center_jnt',guide_list = None,eye_guide_list = None):
    if not guide_list and not eye_guide_list:
        guide_list = ['head01','facelow','facemid','faceupp','head02_end']
        eye_guide_list = [ 'eyeball','eyesock']
    guidePos = cmds.xform(base_object, t=True, ws=True, q=True)
    for i,item in enumerate(guide_list):
        guide = cmds.sphere(radius= 0.2, name = '{}_guide'.format(item))[0]
        cmds.setAttr('{}Shape.overrideEnabled'.format(guide), 1)
        cmds.setAttr('{}Shape.overrideColor'.format(guide), 4)

        if  guide_list in (guide_list[0],guide_list[-1]):
            cmds.xform(guide, t=(guidePos[0], guidePos[1] + (5 * i), guidePos[2]))
        else:
            cmds.xform(guide, t=(guidePos[0], guidePos[1] + (5 * i), guidePos[2]+5))

    guidePos = cmds.xform('facemid_guide', t=True, ws=True, q=True)
    for side in ('l', 'r'):
        for i,eye_item in enumerate(eye_guide_list):
            guide = cmds.sphere(radius=0.2, name='{}_{}_guide'.format(side,eye_item))[0]
            cmds.setAttr('{}Shape.overrideEnabled'.format(guide), 1)
            cmds.setAttr('{}Shape.overrideColor'.format(guide), 4)
            if side == 'l':
                cmds.xform(guide, t=(guidePos[0]+5, guidePos[1] , guidePos[2] + (5*(i+1))))
            else:
                cmds.xform(guide, t=(guidePos[0]-5, guidePos[1], guidePos[2] + (5 * (i + 1))))


def build_face_structure(name=None, guide_list=None, eye_guide_list=None):
    ### basic naming and parenting on a json file
    f = open(
        'C:/Users/danie/Documents/maya/2022/scripts/pyTool/guide/base/hierarchy/basic_face_structure_21072024.json')
    data = json.load(f)

    all_exist = True
    for item in data:

        if not utili.objectExist('{}_guide'.format(item)):
            all_exist = False

    if all_exist:
        for item in data:
            cmds.select(clear=True)
            jnt = cmds.joint(name='{}_{}_jnt'.format(name, item))

            guidePos = cmds.xform('{}_guide'.format(item), t=True, ws=True, q=True)
            cmds.xform(jnt, t=(guidePos[0], guidePos[1], guidePos[2]))
        for item in data:
            if data[item] != 'none':
                cmds.parent('{}_{}_jnt'.format(name, item), '{}_{}_jnt'.format(name, data[item]))
        for item in data:
            #lets get rid of guides after creating joints
            cmds.delete('{}_guide'.format(item))
    else:
        utili.errorMessage('Not all object listed  in the this file exist')


def save_mainstructure_guide(name=None,guide_type = 'guide'):
    print(guide_type)
    print(name)
    final_dict = dict()
    parent = None
    objectList = []
    guide_list = ['head01', 'facelow', 'facemid', 'faceupp', 'head02_end']
    eye_guide_list = ['eyeball', 'eyesock']


    if guide_type == 'guide':
        for item in guide_list:
            if cmds.objExists('{}_guide'.format(item)):
                objectList.append('{}_guide'.format(item))
        for item in eye_guide_list:
            for side in ('l', 'r'):
                if cmds.objExists('{}_{}_guide'.format(side, item)):
                    objectList.append('{}_{}_guide'.format(side, item))

    elif guide_type == 'joint':
        for item in guide_list:
            if cmds.objExists('{}_{}_jnt'.format(name, item)):
                objectList.append('{}_{}_jnt'.format(name, item))
        for item in eye_guide_list:
            for side in ('l', 'r'):
                if cmds.objExists('{}_{}_{}_jnt'.format(name, side, item)):
                    objectList.append('{}_{}_{}_jnt'.format(name, side, item))
    elif guide_type == 'selected': #for xfor we still need to know if this is
        objectList = cmds.ls(sl=True)
        if not objectList:
            utili.errorMessage('Nothing is selected')

    if len(objectList) >= 2:
        print(objectList)
        for item in objectList:
            emptyDict = dict()
            # lets get the parent name
            if (cmds.listRelatives(item, parent=True)) != None:
                parent = cmds.listRelatives(item, parent=True)[0]

            if not parent:
                parent = 'none'
                # position
            if guide_type == 'joint' or guide_type == 'selected':
                pos = cmds.xform(item, t=True, ws=True, q=True)
                #pos = cmds.xform(item, t=True, os=True, q=True)
                """pos = []
                posX = cmds.getAttr('{}.translateX'.format(item))
                posY = cmds.getAttr('{}.translateY'.format(item))
                posZ = cmds.getAttr('{}.translateZ'.format(item))
                pos.append(posX)
                pos.append(posY)
                pos.append(posZ)"""

                oriY = cmds.getAttr('{}.jointOrientY'.format(item))
                oriX = cmds.getAttr('{}.jointOrientX'.format(item))
                oriZ = cmds.getAttr('{}.jointOrientZ'.format(item))



            else:
                pos = cmds.xform(item, t=True, ws=True, q=True)

            emptyDict.update({'parent': parent})
            emptyDict.update({'pos': pos})
            emptyDict.update({'oriX': oriX})
            emptyDict.update({'oriY': oriY})
            emptyDict.update({'oriZ': oriZ})
            print('{}<<<<<<{}'.format(item,parent))

            final_dict.update({item: emptyDict})

    directory = 'base/'
    utili.nameInputWindow(section_dir=directory, dictionary=final_dict)
    utili.errorMessage('Make sure that the selection is in hierarchy order from parent to children')


def load_mainstructure_guide( file_name=None):
    data = utili.file_manage(section_dir='base/{}'.format(file_name[0]), action='load')

    for guide_name, obj in data.items():
        if cmds.objExists(guide_name):
            continue
        else:
            cmds.select(clear=True)
            jnt = cmds.joint(name=guide_name)
            # guide = cmds.sphere(radius=0.2, name=guide_name)[0]
    print(data)
    for guide_name, obj in data.items():
        cmds.select(clear=True)
        # print('{}  <<<< {}'.format(guide_name,obj.get('parent')))

        cmds.xform(guide_name, t=obj.get('pos'))



        if obj.get('parent') != 'none':
            print(guide_name)
            cmds.parent(guide_name, obj.get('parent'))

        cmds.setAttr('{}.jointOrientX'.format(guide_name), obj.get('oriX'))
        cmds.setAttr('{}.jointOrientY'.format(guide_name), obj.get('oriY'))
        cmds.setAttr('{}.jointOrientZ'.format(guide_name), obj.get('oriZ'))




