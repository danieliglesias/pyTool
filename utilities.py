import maya.cmds as cmds
import maya.mel as mel
import math
import json
import sys
import os

#distance between 2 points
def getdistance(object1, object2):
    if not object1 or not object2:
        cmds.error('Make sure to send 2 object into get distance function')
    obj1 = cmds.xform(object1, q=True, t=True, ws=True)
    obj2 = cmds.xform(object2, q=True, t=True, ws=True)

    distance = math.sqrt(pow(obj1[0] - obj2[0], 2) + pow(obj1[1] - obj2[1], 2)+pow(obj1[2] - obj2[2], 2))

    return distance

#this function will create a rect line between 2 points, normally used for controller curve like the shoulders
#utili.create_curve_line(position1='locator1', position2='locator2',name = 'l_shouldercurve',side = 'l')
#utili.create_curve_line(position1='locator1', position2='locator3',name = 'r_shouldercurve',side = 'r')
def create_curve_line(position1=None, position2=None, name=None, squaresize=3, side=None):
    positions = []
    positions.append(cmds.xform(position1, q=True, ws=True, translation=True))
    positions.append(cmds.xform(position2, q=True, ws=True, translation=True))
    positions.append(get_midpoint(position1=position1, position2=position2))
    loc = cmds.spaceLocator(absolute=True, name='loc')[0]
    cmds.xform(loc, t=(positions[2]))
    positions.append(get_midpoint(position1=position1, position2=loc))
    positions.append(get_midpoint(position1=loc, position2=position2))
    cmds.curve(d=3, name=name, p=[positions[0], positions[3], positions[2], positions[4], positions[1]])
    print(positions[0])
    cmds.xform(name, objectSpace=True, pivots=positions[0])
    square_ctrl(position=position2, name='{}_shoulder'.format(side), line=name, size=squaresize, side=side)


def square_ctrl(position=None, name=None, line=None, size=None, side=None):
    if side == 'l':
        cmds.nurbsSquare(name=name, nr=(0, 0, 1), d=1, c=((size / 2), (size / 2), 0), sl1=size, sl2=size)
    else:
        cmds.nurbsSquare(name=name, nr=(0, 0, 1), d=1, c=((size / 2) * -1, (size / 2), 0), sl1=size, sl2=size)
    list = (name, 'top{}Shape'.format(name), 'left{}Shape'.format(name), 'bottom{}Shape'.format(name),
            'right{}Shape'.format(name))
    cmds.parent(list[1:], list[0], relative=True, shape=True)
    [cmds.delete('{}{}'.format(sides, name)) for sides in ['top', 'left', 'bottom', 'right']]
    pos = cmds.xform(position, q=True, ws=True, translation=True)
    cmds.xform(name, t=(pos), ws=True)
    cmds.makeIdentity(name, apply=True)
    cmds.DeleteHistory(name)
    cmds.parent(list[1:], line, relative=True, shape=True)
    cmds.delete(name)


#this function will return the mid point between 2 vectors
def get_midpoint(position1=None, position2=None):

    Xaxis = (cmds.getAttr('{}.translateX'.format(position1)) + cmds.getAttr('{}.translateX'.format(position2))) / 2
    Yaxis = (cmds.getAttr('{}.translateY'.format(position1)) + cmds.getAttr('{}.translateY'.format(position2))) / 2
    Zaxis = (cmds.getAttr('{}.translateZ'.format(position1)) + cmds.getAttr('{}.translateZ'.format(position2))) / 2
    return [Xaxis, Yaxis, Zaxis]

def locOnCenterObject(object = None , name = None , number = 0):
    loc = cmds.spaceLocator(absolute=True, name='{}_{}_loc'.format(name, number))
    cmds.delete(cmds.parentConstraint(object, loc))
    return loc

def clearObject(object,scope = None):
    print('Call to clearObject function usin object: {} and scope is set to: {}'.format(object,scope))
    if not scope:
        cmds.DeleteHistory(cmds.select(object))
        cmds.makeIdentity(object, apply=True)
    elif scope == 'hist':
        cmds.DeleteHistory(cmds.select(object))
    elif scope == 'freeze':
        cmds.makeIdentity(object, apply=True)
    #here we will delete history and freeze trasnformation
    return 0

def createController(name='controller',character_name = None, shape='circle', target = None, contraint_target=None, facing='x', offsetnumber=2,
                          type='fk', size=1,side = 'l' , move = None):

    ### target constraint
    if not contraint_target:
        contraint_target = target

    ###FACING
    if facing == 'x':
        nr_value = (1, 0, 0)
    elif facing == 'y':
        nr_value = (0, 1, 0)
    else:
        nr_value = (0, 0, 1)
    ###SHAPE
    if shape == 'circle':
        ctrl = cmds.circle(nr=nr_value, c=(0, 0, 0), r=size, name='{}_ctrl'.format(name))[0]
    elif shape == 'square':
        ctrl = cmds.circle(nr=nr_value, c=(0, 0, 0), r=size, sections=4, degree=1, name='{}_ctrl'.format(name))[0]
    elif shape == 'sphere':
        ctrl = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), r=size, name='{}_ctrl'.format(name))[0]
        shape02 = cmds.listHistory(cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), r=size, name='Cicle_02_shape')[0])[0]
        shape03 = cmds.listHistory(cmds.circle(nr=(1, 0, 0), c=(0, 0, 0), r=size, name='Cicle_03_shape')[0])[0]
        list = (ctrl, shape02, shape03)
        cmds.parent(list[1:], list[0], relative=True, shape=True)
        cmds.delete('Cicle_*_shape')
    elif shape == 'eyefk':
        size = 0.5
        ctrl = cmds.curve(p=[(0, 0, 0), (0, 0, 5), (0, 0, 10), (0, 0, 15), (0, 0, 20)], k=[0, 0, 0, 1, 2, 2, 2],
                          name='{}_ctrl'.format(name))
        # ctrl = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), r=size, name='{}_ctrl'.format(name))[0]
        circle01 = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), r=size, name='Cicle_01_shape')[0]
        circle02 = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), r=size, name='Cicle_02_shape')[0]
        circle03 = cmds.circle(nr=(1, 0, 0), c=(0, 0, 0), r=size, name='Cicle_03_shape')[0]
        shape01 = cmds.listHistory(circle01)[0]
        shape02 = cmds.listHistory(circle02)[0]
        shape03 = cmds.listHistory(circle03)[0]

        cmds.setAttr('{}.centerZ'.format(cmds.listHistory(circle01)[1]), 20)
        cmds.setAttr('{}.centerZ'.format(cmds.listHistory(circle02)[1]), 20)
        cmds.setAttr('{}.centerZ'.format(cmds.listHistory(circle03)[1]), 20)

        list = (ctrl, shape01, shape02, shape03)
        cmds.parent(list[1:], list[0], relative=True, shape=True)
        cmds.delete('Cicle_*_shape')
    else:
        ctrl = cmds.circle(nr=nr_value, c=(0, 0, 0), r=size, name='{}_ctrl'.format(name))[0]

    ###GROUP
    if offsetnumber == 3:
        off = cmds.group(ctrl, name='{}_off'.format(ctrl))
        constrain = cmds.group(off, name='{}_constrain'.format(off))
    else:
        #changed to our own function to keep center pivot on the group
        #off = cmds.group(ctrl, name='{}_off'.format(ctrl))
        off = groupObject(object='{}'.format(ctrl), offset=2)


    ###MOVE
    if move:
        cmds.move(move[0], move[1], move[2], '{}.cv[0:7]'.format(ctrl), r=True, os=True, wd=True)


    ###GROUP
    if target and offsetnumber == 3:
        cmds.delete(cmds.parentConstraint(target, constrain))
    elif target and offsetnumber == 2:
        cmds.delete(cmds.parentConstraint(target, off))
    #target_pos = cmds.xform(target, t=True, ws=True, q=True)
    #cmds.xform(moving, t=(target_pos[0], target_pos[1], target_pos[2]))




    ###TYPE
    if type == 'simple':  # WE SHOULD JUST PARENT CONTRAINT WITH THE TARGET
        print('simple')

    if type == 'fk':  # WE SHOULD JUST PARENT CONTRAINT WITH THE TARGET
        print('entramos a FK')
        cmds.parentConstraint(ctrl,target)

    elif type == 'ik_pole':  # POINT CONSTRAINT FOR THE END
        cmds.delete(cmds.parentConstraint(ctrl, target))
        cmds.poleVectorConstraint(ctrl, contraint_target)

    elif type == 'ik_point':  # POINT CONSTRAINT FOR THE END
        cmds.delete(cmds.parentConstraint(ctrl, target))
        cmds.pointConstraint(ctrl, contraint_target)


    #face should be always 3 off set numbers
    elif type == 'face':  # SUBSTRACT CONTROLLER TO THE OFF
        if target:
            cmds.parentConstraint(ctrl, target)
        # we want to substract the movement of this controller so me can keep the ctl on position.
        multiplyDivideOff = cmds.createNode('multiplyDivide', n='{}_multiplyDivide'.format(ctrl))

        for x in 'XYZ':
            cmds.setAttr('{}.input2{}'.format(multiplyDivideOff, x), -1)

        cmds.connectAttr('{}.translate'.format(ctrl), '{}.input1'.format(multiplyDivideOff), force=True)
        cmds.connectAttr('{}.output'.format(multiplyDivideOff), '{}.translate'.format(off), force=True)

        #here we flip the position of the controller
        if '_r_' in name:
            cmds.setAttr('{}_constrain.scaleZ'.format(off), -1)


    elif type == 'eye_target':
        ### converge eyes system
        cmds.addAttr(ctrl, longName='converge', defaultValue=0, minValue=0, maxValue=1, keyable=1)
        cmds.addAttr(ctrl, longName='space', at='enum', en='local:world:', keyable=1)

        jntPos = cmds.xform(target[0], t=True, ws=True, q=True)
        cmds.xform(off, t=(0, jntPos[1], jntPos[2] + 10))

        #here we spect a list for target for the left and right side
        for emptyGrp in target:

            remapNode = cmds.createNode('remapValue', n='{}_remapValue'.format(emptyGrp))
            cmds.setAttr('{}.inputMin'.format(remapNode), 1)
            cmds.setAttr('{}.inputMax'.format(remapNode), 0)
            cmds.setAttr('{}.outputMin'.format(remapNode), 0)

            if '_r_' in emptyGrp:
                rjntPos = cmds.xform('{}_r_eyesock_jnt'.format(character_name), t=True, ws=True, q=True)
                cmds.setAttr('{}.outputMax'.format(remapNode), rjntPos[0])
            if '_l_' in emptyGrp:
                ljntPos = cmds.xform('{}_l_eyesock_jnt'.format(character_name), t=True, ws=True, q=True)
                cmds.setAttr('{}.outputMax'.format(remapNode), ljntPos[0])

            cmds.connectAttr('{}.converge'.format(ctrl), '{}.inputValue'.format(remapNode))
            cmds.connectAttr('{}.outValue'.format(remapNode), '{}.translateX'.format(emptyGrp))




    return ctrl


def colorObject(objectList = None, color = None):
    if not color:
    	color = 4
    if not objectList:
        objectList = cmds.ls(sl=True)
        if not objectList:
          	errorMessage('Nothing is selected')
        else:
            for item in objectList:
            #guide = cmds.sphere(radius= 0.2, name = '{}_guide'.format(item))[0]
                cmds.setAttr('{}.overrideEnabled'.format(item), 1)
                cmds.setAttr('{}.overrideColor'.format(item), color)

def closedObject(object):
    #will be interesting to create a type of collision system
    return 0

def toPythonListFormat(objectsList = None):
    if not objectsList:
        objectsList = cmds.ls(selection=True)
    for i,item in enumerate(objectsList):
        if i == 0:
            print('[\''+item+'\'')
        elif item == objectsList[-1]:
            print(',\''+item+'\']')
        else:
            print(',\''+item+'\'')

def checkOpositePos():
    #check if after rigging process joint position match
    return 0

def checkMesh():
    #check symmetry, flipped faces or open quads
    return 0
def createSimpleFkController(objectList = None,align = 'x',size = 1):
    #create simple FK rig usually for simple thinks like hair
    #this should work with any type of guide, like nurb cirle or clusters
    #after this delete clusters.
    if not objectList:
        selected = cmds.ls(sl=True)
        if not selected:
            errorMessage('Nothing is selected')
        #else:
            #renameListObjectsUi(objects=selected)
            #for obj in selected:
            # then we send the list of joint to the change name function
    for i,item in enumerate(selected):
        ctrl = createController(name='{}'.format(item), shape='circle', target=item, contraint_target=None,
                                facing=align,
                                offsetnumber=2,
                                type='fk', size=size)
        # here we group the controllers of the fk controller
        if i >= 1:
            cmds.parent('{}_off'.format(ctrl), '{}_ctrl'.format(selected[i - 1]))



                #here fist we create the joint chain base on the selected clusters
                #joint_list = createJntChain(objects = selected)



def create_fk_system(objects = None,general_name = None,obname = None):

    name = cmds.textField(general_name, query=True, text=True)
    objectName = cmds.textField(obname, query=True, text=True)

    result = check_list_type(list_object=objects)

    if result[0]:
        ### lets add controller and rename if object are already joints
        if result[1] == 'joint':
            cmds.joint(objects[0], edit=True, zso=True, oj='xyz', secondaryAxisOrient='yup',
                       children=True)
            cmds.joint(objects[-1], edit=True, oj='none', children=True, zso=True)
            list_joints = []
            for i, item in enumerate(objects):
                newname = cmds.rename(objects[i], '{}_{}_{:02d}_jnt'.format(name, objectName, (i + 1)))
                list_joints.append(newname)
                print(list_joints)
                print('rename of joint: {}'.format(newname))

                ctrl = createController(name='{}'.format(newname), shape='circle', target=newname, contraint_target=None,
                                        facing='x',
                                        offsetnumber=2,
                                        type='fk', size=5)
                print('control name: {}'.format(ctrl))
                if i >= 1:
                    print('child is equal: {}'.format('{}_ctrl'.format(list_joints[i - 1])))
                    cmds.parent('{}_off'.format(ctrl), '{}_ctrl'.format(list_joints[i - 1]))


        ### if reference are not joint create joint chain and controller
        else:
            jnt_list = []
            # create joint chain for all the clusters
            for i, guide in enumerate(objects):
                cmds.select(clear=True)
                jnt = cmds.joint(name='{}_{}_{:02d}_jnt'.format(name, objectName, (i + 1)))
                print('este es el jont" {}'.format(jnt))
                cmds.delete(cmds.pointConstraint(guide, jnt))
                if i > 0:
                    cmds.parent(jnt, jnt_list[i - 1])
                jnt_list.append(jnt)

            cmds.joint(jnt_list[0], edit=True, zso=True, oj='xyz', secondaryAxisOrient='yup',
                       children=True)
            cmds.joint(jnt_list[-1], edit=True, oj='none', children=True, zso=True)
            # create fk controller for the entire joint chain

            for i, item in enumerate(jnt_list):
                ctrl = createController(name='{}'.format(item), shape='circle', target=item, contraint_target=None,
                                        facing='x',
                                        offsetnumber=2,
                                        type='fk', size=5)
                # here we group the controllers of the fk controller
                if i >= 1:
                    cmds.parent('{}_off'.format(ctrl), '{}_ctrl'.format(jnt_list[i - 1]))

    else:
        errorMessage('No all object selected are the same')





def renameListObjectsUi(objects = None):
    if cmds.window('renameObjectList', exists=True):
        cmds.deleteUI('renameObjectList')
    renameObjectListWindow = cmds.window('renameObjectList', title='Input file name', width=500 ,height = 100)

    data_frame_name_input = cmds.columnLayout(adjustableColumn=True)

    data_row = cmds.rowColumnLayout(numberOfColumns=2,
                                     columnWidth=[(1, 200), (2, 300)],
                                     columnOffset=[(1, 'both', 5), (2, 'both', 0)],
                                     columnAlign=[(1, 'left'), (2, 'center')],
                                     parent=data_frame_name_input, rowSpacing=[1, 5])

    cmds.text(align='center', height=30, label='Character Name:', parent=data_row)
    general_name = cmds.textField(height=30, parent=data_row)


    cmds.text(align='center', height=30, label='Object_name:', parent=data_row)
    obname = cmds.textField(height=30, parent=data_row)

    nameInputWin2 = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(500, 40),parent=data_frame_name_input)
    cmds.button(label='Continue', height=40, parent=nameInputWin2, command=lambda x: create_fk_system(objects =objects,general_name =general_name,obname = obname))
    cmds.button(label='Close', height=40, parent=nameInputWin2,command=lambda x: cmds.deleteUI(renameObjectListWindow))

    cmds.showWindow(renameObjectListWindow)

def renameListObjects(objects = None, general_name = None, obname = None):
    name = cmds.textField(general_name, query=True, text=True)
    objectName = cmds.textField(obname, query=True, text=True)



    return 0



def createRibbon(list = None, name = None , width = 70, length = (0.05), surface_degree = 3,u_parches = 28,v_patches = 1,
                 ribbon_section = 2,target = None,ikhandle = None,sta_ctrl = None,mid_ctrl=None,end_ctrl = None,midpos = None):
    lattice , plane = createNurbPlane(name = name, add_rot=22.5, lattice=True,target = target)

    #### HAIR SYSTEM FOR THE THE RIBBON
    val = 1.0 / u_parches
    grp=cmds.group(em=True, n='{}_follicle_grp'.format(name))
    for i in range(0, (u_parches+1)):
        foll = cmds.createNode('follicle')
        cmds.parent(foll.replace('Shape', ''), grp, s=True)
        cmds.setAttr('{}.simulationMethod'.format(foll), 0)
        cmds.setAttr('{}.parameterV'.format(foll), 0.5)
        cmds.setAttr('{}.parameterU'.format(foll), i * val)
        cmds.connectAttr('{}Shape.local'.format(plane), '{}.inputSurface'.format(foll))
        cmds.connectAttr('{}Shape.worldMatrix[0]'.format(plane), '{}.inputWorldMatrix'.format(foll))
        cmds.connectAttr('{}.outRotate'.format(foll), '{}.rotate'.format(foll.replace('Shape', '')))
        cmds.connectAttr('{}.outTranslate'.format(foll), '{}.translate'.format(foll.replace('Shape', '')))

        jnt = cmds.joint(name='{}_ribbon_{:02d}_joint_def'.format(name, (i + 1)))

        cmds.delete(cmds.parentConstraint(foll.replace('Shape', ''), jnt))


    #HERE WE ARE SNAPING THE LATTICE TO THE JOINTS
    for i in range(0,int(u_parches/2)):
        #create cluster each 2 pair of lattice pt
        cluster =cmds.cluster('{}.pt[{}][0:1][1]'.format(lattice,i), '{}.pt[{}][0:1][0]'.format(lattice,i), rel=True,name='{}_cluster{}'.format(lattice,i))
        #we create 2 locator as a guide to snap and get local position
        loc1 = cmds.spaceLocator(absolute=True, name='loc1')[0]
        loc2 = cmds.spaceLocator(absolute=True, name='loc2')[0]
        cmds.delete(cmds.pointConstraint(cluster, loc1))
        cvPos = cmds.xform(list[i], t=True, ws=True, q=True)
        cmds.xform(loc2, t=(cvPos[0], cvPos[1], cvPos[2]))
        cmds.parent(loc2, loc1)
        locPos = [cmds.getAttr('{}.translate{}'.format(loc2, i)) for i in 'XYZ']
        cmds.delete(cluster, loc1, loc2)

        [cmds.move(locPos[0], locPos[1], locPos[2], '{}.pt[{}][0:1][{}]'.format(lattice,i,x), r=True) for x in
         range(0, 2)]
    clearObject(object = plane,scope = 'hist')
    cmds.skinCluster(list, plane, tsb=True)
    # ROTATIONS
    cmds.setAttr('{}.dTwistControlEnable'.format(ikhandle), 1)
    cmds.setAttr('{}.dWorldUpType'.format(ikhandle), 4)
    cmds.connectAttr('{}.worldMatrix[0]'.format(sta_ctrl),
                     '{}.dWorldUpMatrix'.format(ikhandle))
    cmds.connectAttr('{}.worldMatrix[0]'.format(end_ctrl),
                     '{}.dWorldUpMatrixEnd'.format(ikhandle))
    #MID ROTATION
    midmultiplyDivide = cmds.createNode('multiplyDivide', n='{}_multiplyDivide'.format(mid_ctrl))
    cmds.setAttr('{}.input2X'.format(midmultiplyDivide), -1)
    cmds.connectAttr('{}.outputX'.format(midmultiplyDivide),
                     '{}.rotateX'.format('{}_ribbon_{:02d}_joint_def'.format(name, (int(u_parches / 2)))))

    elsemultiplyDivide = cmds.createNode('multiplyDivide', n='{}_multiplyDivide'.format(mid_ctrl))

    for i,x in enumerate('XYZ'):
        i=i+1
        cmds.setAttr('{}.input2{}'.format(elsemultiplyDivide,x), (1 - (i*0.25)))
        cmds.connectAttr('{}.rotateX'.format(mid_ctrl),'{}.input1{}'.format(elsemultiplyDivide,x))
        cmds.connectAttr('{}.output{}'.format(elsemultiplyDivide,x),'{}.rotateX'.format('{}_ribbon_{:02d}_joint_def'.format(name, (int(u_parches/2)+i))))
        cmds.connectAttr('{}.output{}'.format(elsemultiplyDivide,x),'{}.rotateX'.format('{}_ribbon_{:02d}_joint_def'.format(name, (int(u_parches/2)-i))))





def createNurbPlane(name=None, degree=3, axis=(0, 1, 0), width=70, length=0.05, u=26, v=1, target=None, add_rot=0.0, lattice = False):
    if not name:
        name = 'nurbplane'

    plane = cmds.nurbsPlane(d=degree, u=u, v=v, ax=axis, w=width, lr=length, n=name)[0]
    #THE BASIC ROTATION MAY NEED TO BE POSITIVE
    cmds.rotate(0, -90 + add_rot, 0, plane)
    if target:
        cvPos = cmds.xform(target, t=True, ws=True, q=True)
        cmds.xform(name, t=(cvPos[0], cvPos[1], cvPos[2]))
    if lattice:
       lattice = cmds.lattice(plane, dv=((u+2)/2, 2, 2),ldv=((u+2)/2, 2, 2),ol=1, oc=True , n = plane )[1]

    return lattice , plane


# move to utilities page
def groupObject(object=None, offset=2):
    empty_grp =createEmptyGroup(name='{}_off'.format(object))
    cmds.parent( object,empty_grp)
    #off = cmds.group(object, name='{}_off'.format(object), relative = True)
    return empty_grp


def createEmptyGroup(name=None):
    emptygroup = cmds.spaceLocator(absolute=True, name=name)[0]
    cmds.delete('{}Shape'.format(emptygroup))
    return emptygroup

def errorMessage(message = None):

    if  not message:
        cmds.error('for utilities.error() you most provide a message')
    if cmds.window('ErrorMessage', exists=True):
        cmds.deleteUI('ErrorMessage')
    window_error = cmds.window('Error message', title='Error message', width=500)

    grid_layouteyebrow = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(500, 40))

    cmds.text(align='center', height=30, label= message , font = 'boldLabelFont', parent=grid_layouteyebrow)

    cmds.button(label='Close', height=40, parent=grid_layouteyebrow,
                command=lambda x: cmds.deleteUI(window_error)
                )

    cmds.showWindow(window_error)

def nameInputWindow(section_dir = None, dictionary = None):

    print('We ge into nameInputWindow() function')

    if cmds.window('InputName', exists=True):
        cmds.deleteUI('InputName')
    InputName = cmds.window('InputName', title='Input file name', width=500 ,height = 100)

    data_frame_name_input = cmds.columnLayout(adjustableColumn=True)

    data_row = cmds.rowColumnLayout(numberOfColumns=3,
                                     columnWidth=[(1, 100), (2, 250), (3, 150)],
                                     columnOffset=[(1, 'both', 5), (2, 'both', 0),
                                                   (3, 'both', 5)],
                                     columnAlign=[(1, 'left'), (2, 'center'), (3, 'right')],
                                     parent=data_frame_name_input, rowSpacing=[1, 5])


    cmds.text(align='center', height=30, label='File Name:', parent=data_row)
    textfields = cmds.textField(height=30, parent=data_row)
    cmds.button(label='Save position', height=30, parent=data_row,
                command=lambda x: file_manage(section_dir=section_dir,action = 'write',
                                                    field=textfields, dictionary=dictionary, windows=InputName))

    nameInputWin2 = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(500, 40),parent=data_frame_name_input)
    cmds.button(label='Close', height=40, parent=nameInputWin2,command=lambda x: cmds.deleteUI(InputName))

    cmds.showWindow(InputName)

def saveDicToJsonFile(section_dir = None,textfield = None,dictionary = None,windows = None):
    name = cmds.textField(textfield, query=True, text=True)

    with open( "{}{}".format(dir,name), 'w') as outfile:
        json.dump(dictionary, outfile)
    cmds.deleteUI(windows)

def objectExist(object = None):
    if not cmds.objExists(object):
        errorMessage('Object {} does not exist'.format(object))
        return False
    else:
        return True

def file_manage(section_dir = None,action = None,field = None,dictionary = None,windows = None):
    if sys.platform == 'darwin':
        local = '/Users/danieliglesiasvalenzuela/Library/Preferences/Autodesk/maya/2022/prefs/scripts/pyTool/guide/{}'.format(section_dir)

    else:
        local = 'C:/Users/danie/Documents/maya/2022/scripts/pyTool/guide/{}'.format(
            section_dir)

    if action == 'load':
        f = open(local)
        data = json.load(f)
        f.close()
        return data
    elif action == 'write':

        name = cmds.textField(field, query=True, text=True)

        print(name)
        print(local)
        print(section_dir)
        with open('{}{}'.format(local, name), 'w') as outfile:
            json.dump(dictionary, outfile)
        cmds.deleteUI(windows)

    elif action == 'show':
        listtoshow = os.listdir(local)
        #return filter(lambda k: '.json' in k, list)
        cmds.textScrollList(field, edit=True, removeAll=True)
        cmds.textScrollList(field, edit=True, append=filter(lambda k: '.json' in k, listtoshow))



def check_list_type(list_object=None):
    print(list_object)
    result = True
    selected_type = []
    for obj in list_object:
        selected_type.append(cmds.objectType(obj))
    if not list_object:
        errorMessage('check_list_type function need a list of objects')
    else:
        for i, obj in enumerate(selected_type):
            if i >= 1:
                if selected_type[0] != selected_type[i]:
                    result = False
                else:
                    continue
        if result:
            return True,selected_type[0]
        else:
            return False,'False'


def createRibbonSystem (list_object=None,name = None):

    if not list_object:
        list_object = cmds.ls(sl=True)
        list_object.sort()
    if not name:
        errorMessage('createRibbonSystem function need a name to create ribbon system')

    #we get all joint positions to create a curve
    positions = [cmds.xform(obj, q=True, ws=True, translation=True) for obj in list_object]
    # LETS CREATE A CURVE
    curve = cmds.curve(d=3, p=positions, name='{}_curve'.format(name))
    ##parenting the curve will multiply transformation
    # cmds.parent(curve, loc)

    ###creating joint controller and ik handle
    # lets create 3 join
    ik_list = ['{}_ribbon'.format( obj) for obj in
               (list_object[0],list_object[-1])]
    #,list_object[(math.ceil(len(list_object)/2))]
    print(ik_list)
    for i, item in enumerate(ik_list):
        cmds.select(clear=True)
        jnt_ctrl = cmds.joint(name=item, component=False)
        cmds.delete(cmds.parentConstraint('{}'.format(item[:-7]), jnt_ctrl, maintainOffset=False))
        cmds.setAttr('{}.radius'.format(jnt_ctrl), 2)

        ctrl = createController(name='{}'.format(item), shape='square', target=jnt_ctrl,
                                      contraint_target=None, facing='x',
                                      offsetnumber=2,
                                      type='fk', size=15)

    # skin controller joints to the curve
    cmds.skinCluster(ik_list, curve, tsb=True, name='{}_skincluster'.format(name))
    #ik_handle = cmds.ikHandle(n='{}_ikhandle'.format(name),sj=list_object[0],ee=list_object[-1],curve=curve, solver='ikSplineSolver', createCurve=False, parentCurve=False, numSpans=3)[0]
    cmds.ikHandle(n='{}_ikhandle'.format(name), sj=list_object[0], ee=list_object[-1], curve=curve,
                  solver='ikSplineSolver', createCurve=False, parentCurve=False, numSpans=3)[0]


    arc1 = cmds.arclen(curve)
    cmds.setAttr('{}_ctrl.translateX'.format((ik_list[-1])), 20)
    arc2 = cmds.arclen(curve)
    cmds.setAttr('{}_ctrl.translateX'.format((ik_list[-1])), 0)

    arc = cmds.arclen(curve, ch=True)
    set_driven_key(list = list_object, ctrl = '{}_ctrl'.format((ik_list[-1])),unit = 0,arc =  arc, curve = curve,diff = 0)
    set_driven_key(list = list_object, ctrl = '{}_ctrl'.format((ik_list[-1])),unit = 20,arc = arc, curve = curve, diff =(arc2 - arc1))
    """
    # NOW WE CREATE THE RIBBON SYSTEM
    # we may want to customise more this funtion later for other tools
    listRibbonJnt = ['{}_{}_tentacle{}_{:02d}_joint'.format(name, side, x, int(i)) for i in
                     range(1, int(lastpos) + 1)]
    utili.createRibbon(list=listRibbonJnt, name='{}_{}_tentacle{}_ribbon'.format(name, side, x),
                       target=('{}_ctrl'.format((ik_list[1])[:-6])), ikhandle=ik_handle,
                       sta_ctrl='{}_ctrl'.format((ik_list[0])[:-6]), mid_ctrl='{}_ctrl'.format((ik_list[1])[:-6]),
                       end_ctrl='{}_ctrl'.format((ik_list[2])[:-6]),
                       midpos=midpos)"""

def set_driven_key(list=None, ctrl=None, unit=None, arc=None, curve = None,diff = None):
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

def build_struct_outliner(name=None):
    if not name:
        errorMessage('No Character name provided.')
    else:
        grp_list =  ['{}_all'.format(name),'{}_trs'.format(name),'{}_other'.format(name),'{}_geo'.format(name)]

        grpTRS_list = ['{}_ik'.format(name),'{}_loc'.format(name),'{}_ctrl'.format(name),'{}_jnt'.format(name)]

        for i,group in enumerate(grp_list):
            createEmptyGroup(name = group)
            if i>0:
                cmds.parent( group,grp_list[0])
        for group in grpTRS_list:
            createEmptyGroup(name=group)
            cmds.parent( group,'{}_trs'.format(name))


def visibilitySwitch(objectList=None, targetCtrl=None, targetVariable=None, direct=None,
                     reverse=None):
    if not objectList:
        objectList = cmds.ls(sl=True)
        if not objectList:
            errorMessage('Nothing is selected')
        else:
            if not targetVariable and not targetCtrl:
                errorMessage('You must define a variable and target controller')
            else:
                if not direct and not reverse:
                    for item in objectList:
                        cmds.connectAttr('{}.{}'.format(targetCtrl, targetVariable), '{}.visibility'.format(item), force = True)
                else:
                    for item in objectList:
                        print(direct)
                        print(item.find(direct))
                        if item.find(direct) != -1:
                            print('Entramos a direct con la variable {}'.format(item))
                            cmds.connectAttr('{}.{}'.format(targetCtrl, targetVariable), '{}.visibility'.format(item), force = True)
                        print(reverse)
                        print(item.find(reverse))
                        if item.find(reverse) != -1:
                            print('Entramos a reverse con la variable {}'.format(item))
                            reversenode = cmds.listConnections(targetCtrl, type='reverse')[0]
                            cmds.connectAttr('{}.output.outputX'.format(reversenode), '{}.visibility'.format(item), force = True)

def displayLocalAxis(display = True,objectList = None):
    if not objectList:
        objectList = cmds.ls(sl=True)

    for item in objectList:
        print(cmds.getAttr(item + ".displayLocalAxis"))
        if cmds.getAttr(item + ".displayLocalAxis") == True:
            cmds.setAttr(item + ".displayLocalAxis", False)