import maya.cmds as cmds
import modular_py_tool.Utilities as utili

import importlib
importlib.reload(utili)

def controller_chest_guide():
    #############################################################################################
    sphere_name = cmds.sphere(name='C_chest_BIND_guide', r=1)[0]
    shader, shading_group = utili.create_shader_guide()
    shape = cmds.listRelatives(sphere_name, shapes=True, fullPath=True)[0]
    cmds.sets(shape, edit=True, forceElement=shading_group)

    distance_value = cmds.getAttr('heightDistance.distance') / 1.3
    cmds.move(0, distance_value, 0, sphere_name)
    """annotate = cmds.annotate(sphere_name, tx='chest', p=(0, distance_value, 0))
    cmds.parent(annotate, sphere_name )"""
    annotate = cmds.annotate(sphere_name, tx='chest', p=(0, distance_value, 0))
    annotate_transform = cmds.listRelatives(annotate, parent=True)[0]
    cmds.parent(annotate_transform, sphere_name)

    # cmds.rename(annotate, "hip_annotation")
    cmds.setAttr(annotate + '.overrideEnabled', 1)
    cmds.setAttr(annotate + '.overrideColor', 6)





def controller_torso_guide(spine_num = None):

    print(spine_num)
    print(cmds.getAttr('heightDistance.distance'))
    print(cmds.getAttr('heightDistance.distance') / spine_num )


    #############################################################################################
    sphere_name_skip01 = cmds.sphere(name='C_skips01_guide', r=1)[0]
    """shape = cmds.listRelatives(sphere_name_skip01, shapes=True, fullPath=True)[0]
    cmds.sets(shape, edit=True, forceElement=shading_group)"""

    #############################################################################################
    sphere_name_skip02 = cmds.sphere(name='C_skips02_guide', r=1)[0]
    """shape = cmds.listRelatives(sphere_name_skip02, shapes=True, fullPath=True)[0]
    cmds.sets(shape, edit=True, forceElement=shading_group)"""



    mid_pos = utili.get_midpoint('C_chest_BIND_guide','C_COG_BIND_guide')

    loc = cmds.spaceLocator(absolute=True, name='mid_guide_loc')[0]
    #guidePos = cmds.xform(loc, t=True, ws=True, q=True)
    cmds.xform(loc, t=mid_pos)

    top_mid_pos = utili.get_midpoint('C_chest_BIND_guide', 'mid_guide_loc')
    cmds.xform(sphere_name_skip02, t=top_mid_pos)

    bot_mid_pos = utili.get_midpoint('mid_guide_loc', 'C_COG_BIND_guide')
    cmds.xform(sphere_name_skip01, t=bot_mid_pos)



    list_curve_pos = ['C_chest_BIND_guide','C_skips02_guide','C_skips01_guide', 'C_COG_BIND_guide']
    positions = [cmds.xform(obj, q=True, ws=True, translation=True) for obj in list_curve_pos]
    torso_curve = cmds.curve(d=3, p=positions, name='C_torso_curve_guide')
    curve_shape = cmds.listRelatives(torso_curve, shapes=True)[0]



    """ sphere_name = cmds.sphere(name='C_chest_BIND_guide', r=1)[0]
    cmds.connectAttr('{}.translate'.format(loc), '{}.controlPoints[{}]'.format(shape, cv))
    """
    cmds.delete(loc)
    cmds.connectAttr('{}.translate'.format(sphere_name_skip01), '{}.controlPoints[2]'.format(curve_shape))
    cmds.connectAttr('{}.translate'.format(sphere_name_skip02), '{}.controlPoints[1]'.format(curve_shape))


    print(curve_shape)
    """
    float $cvPos[] = `xform -q -ws -t "curve1.cv[1]"`;
    string $torsoGuide[] = `sphere -radius 0.5`;
    print $torsoGuide[0];
    move -rpr $cvPos[0] $cvPos[1] $cvPos[2];
    connectAttr -f ($torsoGuide[0] +".translate")  curveShape1.controlPoints[1];
    setAttr ($torsoGuide[0]+".overrideEnabled") 1;
    setAttr ($torsoGuide[0]+".overrideColor") 4;
    rename $torsoGuide[0] ("skips01_c_curve01_guide");
    
    float $cvPos2[] = `xform -q -ws -t "curve1.cv[2]"`;
    string $torsoGuide[] = `sphere -radius 0.5`;
    move -rpr $cvPos2[0] $cvPos2[1] $cvPos2[2];
    connectAttr -f ($torsoGuide[0] +".translate")  curveShape1.controlPoints[2];
    setAttr ($torsoGuide[0]+".overrideEnabled") 1;
    setAttr ($torsoGuide[0]+".overrideColor") 4;
    rename $torsoGuide[0] ("skips02_c_curve02_guide");
    """
    ## commment


def controller_torso_jnt(spine_num = None):
    position = 2 + 2
    value = 1 / (position - 1)

    for i in range(0, position):
        if i != 0 and i != (position - 1):
            print(i * value)
