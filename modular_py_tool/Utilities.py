import maya.cmds as cmds
import maya.mel as mel
import math
import json
import sys
import os
import re
import importlib

def ScrollListFileManage(section_dir = None,action = None,field = None,dictionary = None,windows = None):
    if sys.platform == 'darwin':
        local = '/Users/danieliglesiasvalenzuela/Library/Preferences/Autodesk/maya/2026/prefs/scripts/guide/{}'.format(section_dir)

    else:
        local = 'C:/Users/danie/Documents/maya/2026/scripts/modular_py_tool/save/'

    #####################################################################################################

    if action == 'show':
        list_to_show = os.listdir(local)
        #return filter(lambda k: '.json' in k, list)
        cmds.textScrollList(field, edit=True, removeAll=True)
        cmds.textScrollList(field, edit=True, append=filter(lambda k: '.json' in k, list_to_show))

    elif action == 'write':

        name = cmds.textField(field, query=True, text=True)

        print(name)
        print(local)
        print(section_dir)
        with open('{}{}'.format(local, name), 'w') as outfile:
            json.dump(dictionary, outfile)
        cmds.deleteUI(windows)

    """    elif action == 'load':
        f = open(local)
        data = json.load(f)
        f.close()
        return data"""


def generate_height_guides(pos1 = [0, 0, 0],pos2 = [0, 200, 0]):
    ### first we check to make sure that the unit scale in maya is the best one
    linear_units = cmds.currentUnit(query=True, linear=True)
    if linear_units != 'cm':
        errorMessage('Please change unit to centimeter')
    else:
        ### lets validate if guide already exist.
        if cmds.objExists('height') == True:
            cmds.delete('height')

        ### if the scale is in centimeters then we create a distance tool, this will provide scale to controllers
        distance_shape = cmds.distanceDimension(sp=(pos1[0], pos1[1], pos1[2]), ep=(pos2[0], pos2[1], pos2[2]))
        transform_node = cmds.listRelatives(distance_shape, parent=True)[0]
        locators = cmds.listConnections(distance_shape, type='locator')
        print(cmds.listConnections(distance_shape, type='distanceDimShape'))
        cmds.rename(transform_node, 'heightDistance')
        for i, loc in enumerate(locators):
            if i == 0:
                cmds.rename(loc, 'heightLocA')
            else:
                cmds.rename(loc, 'heightLocB')

        emptyGrp = createEmptyGroup(name='height')
        [cmds.parent(object1, emptyGrp) for object1 in ('heightDistance', 'heightLocA', 'heightLocB')]



def createController(name='controller',character_name = None, shape='circle', target = None, contraint_target=None, facing='x', offsetnumber=2,
                          type='fk', size=1,side = 'l' , move = None):


    char_height = cmds.getAttr('{}.distance'.format('heightDistanceShape'))
    print(char_height)
    if size == 'root':
        dynamic_size = char_height / 3


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
        ctrl = cmds.circle(nr=nr_value, c=(0, 0, 0), r=dynamic_size, name='{}_ctrl'.format(name))[0]
    elif shape == 'square':
        ctrl = cmds.circle(nr=nr_value, c=(0, 0, 0), r=dynamic_size, sections=4, degree=1, name='{}_ctrl'.format(name))[0]
    elif shape == 'sphere':
        ctrl = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), r=dynamic_size, name='{}_ctrl'.format(name))[0]
        shape02 = cmds.listHistory(cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), r=dynamic_size, name='Cicle_02_shape')[0])[0]
        shape03 = cmds.listHistory(cmds.circle(nr=(1, 0, 0), c=(0, 0, 0), r=dynamic_size, name='Cicle_03_shape')[0])[0]
        list = (ctrl, shape02, shape03)
        cmds.parent(list[1:], list[0], relative=True, shape=True)
        cmds.delete('Cicle_*_shape')
    elif shape == 'eyefk':
        size = 0.5
        ctrl = cmds.curve(p=[(0, 0, 0), (0, 0, 5), (0, 0, 10), (0, 0, 15), (0, 0, 20)], k=[0, 0, 0, 1, 2, 2, 2],
                          name='{}_ctrl'.format(name))
        # ctrl = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), r=size, name='{}_ctrl'.format(name))[0]
        circle01 = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), r=dynamic_size, name='Cicle_01_shape')[0]
        circle02 = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), r=dynamic_size, name='Cicle_02_shape')[0]
        circle03 = cmds.circle(nr=(1, 0, 0), c=(0, 0, 0), r=dynamic_size, name='Cicle_03_shape')[0]
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
        off = cmds.group(ctrl, name='{}_off'.format(name))
        constrain = cmds.group(off, name='{}_constrain'.format(off))
    else:
        #changed to our own function to keep center pivot on the group
        #off = cmds.group(ctrl, name='{}_off'.format(ctrl))
            off = cmds.group(ctrl, name='{}_off'.format(name))


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

"""def groupObject(object=None, offset=2):
    empty_grp =createEmptyGroup(name='{}_off'.format(object))
    cmds.parent( object,empty_grp)
    #off = cmds.group(object, name='{}_off'.format(object), relative = True)
    return empty_grp
"""

def createEmptyGroup(name=None):
    emptygroup = cmds.spaceLocator(absolute=True, name=name)[0]
    cmds.delete('{}Shape'.format(emptygroup))
    return emptygroup

"""
def create_shader_guide():
    shader_name = "shader_guide"

    # Check if the shader already exists
    if cmds.objExists(shader_name):
        return shader_name  # Return the name if it already exists

    # Create the Lambert shader
    material_name = cmds.shadingNode('lambert', asShader=True)
    print(material_name)
    cmds.rename(material_name, shader_name)

    # Set the color of the shader
    cmds.setAttr(f"{shader_name}.color", 1, 0.3921, 0.4232, type="double3")  # Specific color

    return shader_name  # Return the name of the newly created shader"""

def create_shader_guide():
    shader_name = "shader_guide"
    shading_group_name = "shader_guideSG"

    if cmds.objExists(shader_name) and cmds.objExists(shading_group_name):
        return shader_name, shading_group_name

    # Create the shader
    shader = cmds.shadingNode('lambert', asShader=True, name=shader_name)

    # Create the shading group and connect the shader to it
    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shading_group_name)
    cmds.connectAttr(f"{shader}.outColor", f"{shading_group}.surfaceShader", force=True)

    # Set the color
    cmds.setAttr(f"{shader}.color", 1, 0.3921, 0.4232, type="double3")

    return shader, shading_group

def get_midpoint(position1=None, position2=None):

    Xaxis = (cmds.getAttr('{}.translateX'.format(position1)) + cmds.getAttr('{}.translateX'.format(position2))) / 2
    Yaxis = (cmds.getAttr('{}.translateY'.format(position1)) + cmds.getAttr('{}.translateY'.format(position2))) / 2
    Zaxis = (cmds.getAttr('{}.translateZ'.format(position1)) + cmds.getAttr('{}.translateZ'.format(position2))) / 2
    return [Xaxis, Yaxis, Zaxis]



def get_position_on_curve(curve, normalized_param):
    # Get curve shape
    shape = cmds.listRelatives(curve, s=True)[0]

    # Total length of the curve
    length = cmds.arclen(curve)

    # Create a pointOnCurveInfo node
    poc = cmds.createNode('pointOnCurveInfo')
    curve_shape = cmds.listRelatives(curve, shapes=True)[0]
    cmds.connectAttr(f'{curve_shape}.worldSpace[0]', f'{poc}.inputCurve')

    # Enable parameter by length and set normalized position
    cmds.setAttr(f'{poc}.turnOnPercentage', 1)
    cmds.setAttr(f'{poc}.parameter', normalized_param)

    # Query world position
    position = cmds.getAttr(f'{poc}.position')[0]

    # Clean up
    cmds.delete(poc)

    return position



def find_named_objects(char_name = None, name_patterns =None, suffix="_jnt", node_types=("joint", "transform")):
    # Get all objects of the specified types

    print('inside find_named_objects')
    all_objects = []
    for node_type in node_types:
        all_objects.extend(cmds.ls(type=node_type) or [])

    # Join patterns and build regex
    name_group = "|".join(name_patterns)
    escaped_suffix = re.escape('_{}'.format(suffix))
    escaped_char_name = re.escape(char_name)
    pattern_str = r'^{}.*(?:{}).*{}$'.format(escaped_char_name, name_group, escaped_suffix)
    pattern = re.compile(pattern_str, re.IGNORECASE)

    # Filter by name pattern and suffix
    matching = [obj for obj in all_objects if pattern.match(obj)]
    return matching


def check_existing_joints(data):
    ### this get back all joint or guide that already exist
    existing_joints = []

    for component_name, component_data in data.items():
        if component_name == 'general':
            continue  # Skip global metadata

        for joint_key, joint_info in component_data.items():
            if joint_key == 'general':
                continue  # Skip per-component metadata

            bone_name = joint_info.get('bone_name')
            print(bone_name)
            if bone_name and cmds.objExists(bone_name):
                existing_joints.append(bone_name)

    return existing_joints

def create_guide_sphere(item, final_position):
    print('#### inside create_guide_sphere')
    # Get or create the shader once
    shader, shading_group = create_shader_guide()

    # Create sphere
    sphere_name = cmds.sphere(name=item, r=1)[0]
    shape = cmds.listRelatives(sphere_name, shapes=True, fullPath=True)[0]

    cmds.move(final_position[0],
              final_position[1],
              final_position[2],
              sphere_name)


    # Assign shader
    cmds.sets(shape, edit=True, forceElement=shading_group)

    # Create annotation
    label_text = "_".join(item.split("_")[1:])
    #y_offset = final_position[1] if rebuild else final_position[1] + final_position[1] / 30

    annotate = cmds.annotate(item, tx=label_text, p=(final_position[0], final_position[1]+ final_position[1]/30, final_position[2]))
    annotate_transform = cmds.listRelatives(annotate, parent=True)[0]
    cmds.parent(annotate_transform, item)

    # Set annotation color
    cmds.setAttr(annotate + '.overrideEnabled', 1)
    cmds.setAttr(annotate + '.overrideColor', 6)

    return sphere_name  # Optional: return if you need reference

def switch_side_prefix(limb_name):
    if limb_name.startswith('l'):
        return 'r' + limb_name[1:]
    elif limb_name.startswith('r'):
        return 'l' + limb_name[1:]
    elif limb_name.startswith('L'):
        return 'R' + limb_name[1:]
    elif limb_name.startswith('R'):
        return 'L' + limb_name[1:]
    else:
        return limb_name  # No change if doesn't start with l or r