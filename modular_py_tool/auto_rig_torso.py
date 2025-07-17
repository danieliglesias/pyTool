import maya.cmds as cmds
import modular_py_tool.Utilities as utili
import modular_py_tool.UiAutoRig as ui_autorig
import re
import importlib
importlib.reload(utili)
importlib.reload(ui_autorig)

def controller_chest_guide(char_name = None,parent_name = None,rebuild=False):
    #############################################################################################
    sphere_name = cmds.sphere(name='C_chest_BIND_guide', r=1)[0]
    shader, shading_group = utili.create_shader_guide()
    shape = cmds.listRelatives(sphere_name, shapes=True, fullPath=True)[0]
    cmds.sets(shape, edit=True, forceElement=shading_group)

    final_position = None

    if rebuild:
        final_position = ui_autorig._nested_dict_instance.data['torso']['C_chest_BIND_guide']['position']
        cmds.xform(sphere_name, ws=True, t=final_position)

    else:
        final_position = [0,cmds.getAttr('heightDistance.distance') / 1.3,0]
        cmds.move(0, final_position[1], 0, sphere_name)
        ui_autorig._nested_dict_instance.update_limb(limb_name='torso',
                                                     parent=parent_name,
                                                     list=['chest'], suffix='guide')




    annotate = cmds.annotate(sphere_name, tx='chest', p=(0, final_position[1], 0))
    annotate_transform = cmds.listRelatives(annotate, parent=True)[0]
    cmds.parent(annotate_transform, sphere_name)
    cmds.setAttr(annotate + '.overrideEnabled', 1)
    cmds.setAttr(annotate + '.overrideColor', 6)





def controller_torso_guide(char_name = None,parent_name = None, spine_num = None, rebuild=False):
    cog_object = None
    if cmds.objExists("C_COG_BIND_jnt"):
        cog_object = "C_COG_BIND_jnt"
    elif cmds.objExists("C_COG_BIND_guide"):
        cog_object = "C_COG_BIND_guide"

    if cog_object:
        #############################################################################################
        sphere_name_spine01 = cmds.sphere(name='C_spine01_guide', r=1)[0]

        #############################################################################################
        sphere_name_spine02 = cmds.sphere(name='C_spine02_guide', r=1)[0]

        mid_pos = utili.get_midpoint('C_chest_BIND_guide',cog_object)

        loc = cmds.spaceLocator(absolute=True, name='mid_guide_loc')[0]
        #guidePos = cmds.xform(loc, t=True, ws=True, q=True)
        cmds.xform(loc, t=mid_pos)

        top_mid_pos = utili.get_midpoint('C_chest_BIND_guide', 'mid_guide_loc')
        cmds.xform(sphere_name_spine02, t=top_mid_pos)

        bot_mid_pos = utili.get_midpoint('mid_guide_loc', cog_object)
        cmds.xform(sphere_name_spine01, t=bot_mid_pos)
        cmds.delete(loc)


        list_curve_pos = [cog_object,'C_spine01_guide','C_spine02_guide','C_chest_BIND_guide']
        positions = [cmds.xform(obj, q=True, ws=True, translation=True) for obj in list_curve_pos]
        torso_curve = cmds.curve(d=3, p=positions, name='C_torso_curve_guide')
        curve_shape = cmds.listRelatives(torso_curve, shapes=True)[0]


        cmds.connectAttr('{}.translate'.format(sphere_name_spine02), '{}.controlPoints[2]'.format(curve_shape))
        cmds.connectAttr('{}.translate'.format(sphere_name_spine01), '{}.controlPoints[1]'.format(curve_shape))

        if rebuild == True:

            pos1 = ui_autorig._nested_dict_instance.data['torso']['C_spine01_guide']['position']
            cmds.xform(sphere_name_spine01, t= pos1)
            pos2 = ui_autorig._nested_dict_instance.data['torso']['C_spine02_guide']['position']
            cmds.xform(sphere_name_spine02, t= pos2)
        else:
            ui_autorig._nested_dict_instance.update_limb(limb_name='torso',
                                                         parent=parent_name,
                                                         list=['chest','spine'], suffix='guide')



def controller_torso_jnt(char_name = None,parent_name = None,rebuild = False, spine_num = None):

    if rebuild == False:

        position = spine_num + 2
        value = 1 / (position - 1)
        #for i in range(position,0,-1):
        for i in range(1,position):
            world_pos = utili.get_position_on_curve('C_torso_curve_guide', (i * value))
            cmds.select(clear=True)


            if i == (position-1):
                jnt = cmds.joint(p=world_pos, name='c_chest_BIND_jnt')
                cmds.parent( 'c_chest_BIND_jnt','c_spine{:02d}_BIND_jnt'.format(i-1))
            else:
                jnt = cmds.joint(p=world_pos, name='c_spine{:02d}_BIND_jnt'.format(i))

                if i >= 2:
                    cmds.parent(jnt,'c_spine{:02d}_BIND_jnt'.format(i-1))

        cmds.delete('C_chest_BIND_guide')
        cmds.delete('C_spine01_guide')
        cmds.delete('C_spine02_guide')
        cmds.delete('C_torso_curve_guide')
        #cmds.joint("rootJoint", edit=True, orientJoint="xyz", secondaryAxisOrient="yup", children=True)
        #cmds.joint(jnt_list[0], edit=True, zso=True, oj='xyz', secondaryAxisOrient='yup',children=True)
        #cmds.joint(jnt_list[-1], edit=True, oj='none', children=True, zso=True)

        ### update dictionary
        ui_autorig._nested_dict_instance.update_limb(limb_name='torso',
                                                     parent=parent_name,
                                                     list=['chest', 'spine'], suffix='jnt')

    else:
        ui_autorig._nested_dict_instance.create_joints_from_limb(limb_name='torso')


def controller_torso_jnt_rebuild():
    return 0
