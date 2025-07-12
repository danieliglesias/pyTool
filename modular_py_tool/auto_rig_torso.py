import maya.cmds as cmds
import pyTool.modular_py_tool.Utilities as utili

import importlib
importlib.reload(utili)

def controller_torso_guide():

    sphere_name = cmds.sphere(name='C_chest_BIND_guide', r=1)[0]
    shader, shading_group  = utili.create_shader_guide()
    # Step 5: Assign the material to the sphere
    #cmds.select(sphere_name)
    #cmds.hyperShade(assign='{}'.format(shader_name))

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



    mid_pos = utili.get_midpoint('C_chest_BIND_guide','C_COG_BIND_guide')

    loc = cmds.spaceLocator(absolute=True, name='mid_guide_loc')[0]
    #guidePos = cmds.xform(loc, t=True, ws=True, q=True)
    cmds.xform(loc, t=mid_pos)

    top_mid_pos = utili.get_midpoint('C_chest_BIND_guide', 'mid_guide_loc')

    loc2 = cmds.spaceLocator(absolute=True, name='top_guide_loc')[0]
    # guidePos = cmds.xform(loc, t=True, ws=True, q=True)

    cmds.xform(loc2, t=top_mid_pos)

    bot_mid_pos = utili.get_midpoint('mid_guide_loc', 'C_COG_BIND_guide')

    loc3 = cmds.spaceLocator(absolute=True, name='bot_guide_loc')[0]
    # guidePos = cmds.xform(loc, t=True, ws=True, q=True)
    cmds.xform(loc3, t=bot_mid_pos)



    list_curve_pos = ['C_chest_BIND_guide','top_guide_loc','bot_guide_loc', 'C_COG_BIND_guide']
    positions = [cmds.xform(obj, q=True, ws=True, translation=True) for obj in list_curve_pos]
    torso_curve = cmds.curve(d=3, p=positions, name='C_torso_curve_guide')
    curve_shape = cmds.listRelatives(torso_curve, shapes=True)[0]



    """ sphere_name = cmds.sphere(name='C_chest_BIND_guide', r=1)[0]
    cmds.connectAttr('{}.translate'.format(loc), '{}.controlPoints[{}]'.format(shape, cv))
    """
    cmds.delete(loc)
    cmds.delete(loc2)
    cmds.delete(loc3)

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


