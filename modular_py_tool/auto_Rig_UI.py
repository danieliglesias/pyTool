import maya.cmds as cmds
import os
import json

import pyTool.modular_py_tool.auto_rig_fundation as fundation
import pyTool.utilities as utili
import importlib
importlib.reload(fundation)
importlib.reload(utili)


def check_global_dict():
    return "global_dict" in globals()

def clear_grid(grid=None):
    children = cmds.layout(grid, q=True, childArray=True)
    # Delete each child
    if children:
        for child in children:
            cmds.deleteUI(child)


def constructor_limb_selected(limb_selected=None):
    clear_grid(grid='selected_grid')
    ###check if a save file is selected
    ### return exist or not
    return False


def build_lleg_layout(leg_grid_layout = None):

    if check_global_dict():
        ### lets figure out how many llegs are created
        lleg_amount = 3

        lleg_layout = cmds.gridLayout(numberOfColumns=lleg_amount + 1, cellWidthHeight=(100 / (lleg_amount + 1), 75),
                                      parent=leg_grid_layout)

        for i in range(lleg_amount):
            vertical_label = '\n'.join('leg0{}'.format(i))
            cmds.button(label='{}'.format(vertical_label), height=75, parent=lleg_layout,
                        command=lambda x: constructor_limb_selected(limb_selected='lleg{}'.format(i)))


    else:
        lleg_layout = cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(50, 75), parent=leg_grid_layout)
        vertical_label = '\n'.join('leg01')
        cmds.button(label=vertical_label, height=75, parent=lleg_layout ,
                    command=lambda x: constructor_limb_selected(limb_selected = 'lleg'))
        cmds.button(label='', enable=False, height=75, parent=lleg_layout)


def modular_ui():
    if cmds.window('ModularToolUI', exists=True):
        cmds.deleteUI('ModularToolUI')
    window = cmds.window('ModularToolUI', title='Modular Tool', menuBar=True, width=500,
                         height=800)

    cmds.menu(label='File', tearOff=True)
    cmds.menuItem(label='load guide file')
    cmds.menuItem(label='Save guide')
    cmds.menuItem(divider=True)
    cmds.menuItem(label='Quit')
    cmds.menu(label='Help', helpMenu=True)
    cmds.menuItem('Application..."', label='"About')

    main_layout = cmds.columnLayout(adjustableColumn=True)
    data_dict = build_data_frame(window, main_layout)


    # add build/close buttons
    #button_grid(window, main_layout,data_dict)
    cmds.showWindow()


def build_data_frame(window, main_layout):
    ###GENERAL###########################################################################################################################
    data_frame_general = cmds.frameLayout(label='General parameters', width=500,
                                          collapsable=True, parent=main_layout)

    data_row_general_seg_01 = cmds.rowColumnLayout(numberOfColumns=2,
                                            columnWidth=[(1, 100), (2, 400)],
                                            columnOffset=[(1, 'left', 5), (2, 'both', 5)],
                                            columnAlign=[(1, 'left'), (2, 'center')],
                                            parent=data_frame_general, rowSpacing=[1, 5])
    # character name
    cmds.text(align='center', height=30, label='Json name:', parent=data_row_general_seg_01)
    general_name = cmds.textField(height=30, text='New json name...', parent=data_row_general_seg_01)
    cmds.text(align='center', height=30, label='character name:', parent=data_row_general_seg_01)
    general_name = cmds.textField(height=30, text='New name...', parent=data_row_general_seg_01)
    ###########################################################

    data_row_general_seg_02 = cmds.rowColumnLayout(numberOfColumns=1,
                                           columnWidth=[(1, 500)],
                                           columnOffset=[(1, 'both', 5)],
                                           columnAlign=[(1, 'left')],
                                           parent=data_frame_general, rowSpacing=[1,5])
    # Lets calculate the height of the character
    cmds.button(label='Generate Height guide', parent=data_row_general_seg_02,command=lambda x: generate_height_guides())

    ##########################################################################
    # General face guides
    """grid_layoutgeneral = cmds.gridLayout(numberOfColumns=3,
                                         cellWidthHeight=(500, 25), 
                                         parent=data_frame_general)"""
    head_grid_layout = cmds.rowColumnLayout(numberOfColumns=7,
                                                   columnWidth=[(1, 100),(2, 300),(3, 100)],
                                                   columnOffset=[(1, 'both', 2),(2, 'both', 2),(3, 'both', 2)],
                                                   columnAlign=[(1, 'left'),(2, 'left'),(3, 'left')],
                                                   parent=data_frame_general, rowSpacing=[1, 5])


    cmds.button(label='R_WING', height=25, parent=head_grid_layout,
                command=lambda x: constructor_limb_selected(limb_selected = 'rwing'))


    #cmds.button('head_botton',label='HEAD', height=50, parent=head_grid_layout,command=lambda x: controller_eyebrow_mirror(button_name = 'head_botton',frame = data_frame_head ))

    head_layout = cmds.gridLayout( 'head_gridlayout',numberOfColumns=5, cellWidthHeight=(60, 50), parent=head_grid_layout)
    cmds.button('head_botton1',label='', enable=False, height=15, parent=head_layout)
    cmds.button('head_botton2',label='', enable=False, height=15, parent=head_layout)
    #cmds.button('head_botton3',label='Head', height=50, parent=head_layout,command=lambda x: frame_collapse(button_name = 'head_botton',frame = 'data_frame_head'))
    cmds.button('head_botton3', label='Head', height=50, parent=head_layout,
                command=lambda x: constructor_limb_selected(limb_selected = 'head'))

    cmds.button('head_botton4',label='', enable=False, height=15, parent=head_layout)
    cmds.button('head_botton5',label='', enable=False, height=15, parent=head_layout)

    cmds.button(label='L_WING', height=25, parent=head_grid_layout,
                command=lambda x: constructor_limb_selected(limb_selected = 'lwing'))
    #########

    neck_grid_layout = cmds.rowColumnLayout(numberOfColumns=5,
                                            columnWidth=[(1, 100), (2, 100), (3, 100), (4, 100), (5, 100)],
                                            columnOffset=[(1, 'both', 2), (2, 'both', 2), (3, 'both', 2),
                                                          (4, 'both', 2), (5, 'both', 2)],
                                            columnAlign=[(1, 'left'), (2, 'left'), (3, 'left'), (4, 'left'),
                                                         (5, 'left')],
                                            parent=data_frame_general, rowSpacing=[1, 5])

    cmds.button(label='', enable=False, height=15, parent=neck_grid_layout)
    cmds.button(label='', enable=False, height=15, parent=neck_grid_layout)

    neck_layout = cmds.gridLayout(numberOfColumns=3, cellWidthHeight=(33.33, 15),parent=neck_grid_layout)
    cmds.button(label='', enable=False, height=15, parent=neck_layout)
    cmds.button(label='NECK', height=25, parent=neck_layout,
                command=lambda x: constructor_limb_selected(limb_selected = 'neck'))
    cmds.button(label='', enable=False, height=15, parent=neck_layout)

    cmds.button(label='', enable=False, height=15, parent=neck_grid_layout)
    cmds.button(label='', enable=False, height=15, parent=neck_grid_layout)
    #########

    torso_grid_layout = cmds.rowColumnLayout(numberOfColumns=5,
                                            columnWidth=[(1, 100), (2, 100), (3, 100), (4, 100), (5, 100)],
                                            columnOffset=[(1, 'both', 2), (2, 'both', 2), (3, 'both', 2),
                                                          (4, 'both', 2), (5, 'both', 2)],
                                            columnAlign=[(1, 'left'), (2, 'left'), (3, 'left'), (4, 'left'),
                                                         (5, 'left')],
                                            parent=data_frame_general, rowSpacing=[1, 5])

    cmds.button(label='',enable=False, height=25, parent=torso_grid_layout)

    rarm_layout = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(100, 37.5), parent=torso_grid_layout)
    cmds.button(label='R_ARM', height=37.5, parent=rarm_layout,
                command=lambda x: constructor_limb_selected(limb_selected = 'rarm'))
    cmds.button(label='', enable=False, height=15, parent=rarm_layout)



    cmds.button(label='TORSO', height=75, parent=torso_grid_layout,
                command=lambda x: torso_ui())

    larm_layout = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(100, 37.5), parent=torso_grid_layout)
    cmds.button(label='L_ARM', height=37.5, parent=larm_layout,
                command=lambda x: constructor_limb_selected(limb_selected = 'larm'))
    cmds.button(label='', enable=False, height=15, parent=larm_layout)

    cmds.button(label='',enable=False, height=25, parent=torso_grid_layout)
    #########

    hip_grid_layout = cmds.rowColumnLayout(numberOfColumns=5,
                                             columnWidth=[(1, 100), (2, 100), (3, 100), (4, 100), (5, 100)],
                                             columnOffset=[(1, 'both', 2), (2, 'both', 2), (3, 'both', 2),
                                                           (4, 'both', 2), (5, 'both', 2)],
                                             columnAlign=[(1, 'left'), (2, 'left'), (3, 'left'), (4, 'left'),
                                                          (5, 'left')],
                                             parent=data_frame_general, rowSpacing=[1, 5])

    cmds.button(label='', enable=False, height=25, parent=hip_grid_layout)
    cmds.button(label='', enable=False, height=25, parent=hip_grid_layout)
    cmds.button(label='HIP (1)', height=25, parent=hip_grid_layout ,
                command=lambda x: hip_ui())
    cmds.button(label='', enable=False, height=25, parent=hip_grid_layout)
    cmds.button(label='', enable=False, height=25, parent=hip_grid_layout)
    #########

    leg_grid_layout = cmds.rowColumnLayout(numberOfColumns=5,
                                           columnWidth=[(1, 100), (2, 100), (3, 100), (4, 100), (5, 100)],
                                           columnOffset=[(1, 'both', 2), (2, 'both', 2), (3, 'both', 2),
                                                         (4, 'both', 2), (5, 'both', 2)],
                                           columnAlign=[(1, 'left'), (2, 'left'), (3, 'left'), (4, 'left'),
                                                        (5, 'left')],
                                           parent=data_frame_general, rowSpacing=[1, 5])

    cmds.button(label='', enable=False, height=75, parent=leg_grid_layout)

    rleg_layout = cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(50, 75), parent=leg_grid_layout)
    cmds.button(label='', enable=False, height=75, parent=rleg_layout)
    cmds.button(label='R_LEG', height=75, parent=rleg_layout ,
                command=lambda x: constructor_limb_selected(limb_selected = 'rleg'))

    lleg_layout = cmds.gridLayout(numberOfColumns=5, cellWidthHeight=(20, 75), parent=leg_grid_layout)
    cmds.button(label='', enable=False, height=75, parent=lleg_layout)
    cmds.button(label='', enable=False, height=75, parent=lleg_layout)
    cmds.button(label='TAIL', height=75, parent=lleg_layout ,
                command=lambda x: constructor_limb_selected(limb_selected = 'tail'))
    cmds.button(label='', enable=False, height=75, parent=lleg_layout)
    cmds.button(label='', enable=False, height=75, parent=lleg_layout)

    build_lleg_layout(leg_grid_layout = leg_grid_layout)


    cmds.button(label='', enable=False, height=75, parent=leg_grid_layout)



    ##############################################################################################################################
    #############SELECTED##################################SELECTED#########SELECTED##############################################
    ##############################################################################################################################
    data_frame_selected = cmds.frameLayout(label='limb selected', width=500,
                                          collapsable=False, parent=main_layout)


    selected_grid_layout = cmds.rowColumnLayout('selected_grid',numberOfColumns=1,
                                            columnWidth=[(1, 500)],
                                            columnOffset=[(1, 'both', 2)],
                                            columnAlign=[(1, 'left')],
                                            parent=data_frame_selected, rowSpacing=[1, 5])

    cmds.button(label='Name', height=25, parent=selected_grid_layout)

    """###HIP###########################################################################################################################

    data_frame_hip = cmds.frameLayout('data_frame_hip',label='Build Hip', width=500,
                                        collapsable=True, collapse=True, parent=main_layout)
    data_row_hip_seg_01 = cmds.rowColumnLayout(numberOfColumns=2,
                                                 columnWidth=[(1, 500)],
                                                 columnOffset=[(1, 'both', 5)],
                                                 columnAlign=[(1, 'left')],
                                                 parent=data_frame_hip, rowSpacing=[1, 5])

    cmds.button(label='test', parent=data_row_hip_seg_01)

    ###TORSO###########################################################################################################################

    data_frame_torso = cmds.frameLayout('data_frame_torso',label='Build Torso', width=500,
                                           collapsable=True,collapse = True, parent=main_layout)
    data_row_torso_seg_01 = cmds.rowColumnLayout(numberOfColumns=2,
                                           columnWidth=[(1, 500)],
                                           columnOffset=[(1, 'both', 5)],
                                           columnAlign=[(1, 'left')],
                                           parent=data_frame_torso, rowSpacing=[1, 5])

    cmds.button(label='test', parent=data_row_torso_seg_01)

    ###TORSO###########################################################################################################################

    data_frame_leg = cmds.frameLayout('data_frame_leg',label='Build Leg', width=500,
                                        collapsable=True,collapse = True, parent=main_layout)
    data_row_leg_seg_01 = cmds.rowColumnLayout(numberOfColumns=2,
                                                 columnWidth=[(1, 500)],
                                                 columnOffset=[(1, 'both', 5)],
                                                 columnAlign=[(1, 'left')],
                                                 parent=data_frame_leg, rowSpacing=[1, 5])

    cmds.button(label='test', parent=data_row_leg_seg_01)

    ###ARMS###########################################################################################################################

    data_frame_arm = cmds.frameLayout('data_frame_arm',label='Build Arm', width=500,
                                      collapsable=True,collapse = True, parent=main_layout)
    data_row_arm_seg_01 = cmds.rowColumnLayout(numberOfColumns=2,
                                               columnWidth=[(1, 500)],
                                               columnOffset=[(1, 'both', 5)],
                                               columnAlign=[(1, 'left')],
                                               parent=data_frame_arm, rowSpacing=[1, 5])

    cmds.button(label='test', parent=data_row_arm_seg_01)
    ###NECK###########################################################################################################################

    data_frame_neck = cmds.frameLayout('data_frame_neck', label='Build neck', width=500,
                                       collapsable=True, collapse=True, parent=main_layout)
    data_row_neck_seg_01 = cmds.rowColumnLayout(numberOfColumns=2,
                                                columnWidth=[(1, 500)],
                                                columnOffset=[(1, 'both', 5)],
                                                columnAlign=[(1, 'left')],
                                                parent=data_frame_neck, rowSpacing=[1, 5])

    cmds.button(label='test', parent=data_row_neck_seg_01)
    ###HEAD###########################################################################################################################

    data_frame_head = cmds.frameLayout('data_frame_head',label='Build Head', width=500,
                                      collapsable=True,collapse = True, parent=main_layout)
    data_row_head_seg_01 = cmds.rowColumnLayout(numberOfColumns=2,
                                               columnWidth=[(1, 500)],
                                               columnOffset=[(1, 'both', 5)],
                                               columnAlign=[(1, 'left')],
                                               parent=data_frame_head, rowSpacing=[1, 5])

    cmds.button(label='test', parent=data_row_head_seg_01,command=lambda x: controller_refresh_head(grid = 'head_gridlayout'))

    ###TAIL###########################################################################################################################

    data_frame_tail = cmds.frameLayout('data_frame_tail', label='Build Tail', width=500,
                                       collapsable=True, collapse=True, parent=main_layout)
    data_row_tail_seg_01 = cmds.rowColumnLayout(numberOfColumns=2,
                                                columnWidth=[(1, 500)],
                                                columnOffset=[(1, 'both', 5)],
                                                columnAlign=[(1, 'left')],
                                                parent=data_frame_tail, rowSpacing=[1, 5])

    cmds.button(label='Generate Tail', parent=data_row_tail_seg_01)

    ###WING###########################################################################################################################

    data_frame_wing = cmds.frameLayout('data_frame_wing', label='Build Wing', width=500,
                                       collapsable=True, collapse=True, parent=main_layout)
    data_row_wing_seg_01 = cmds.rowColumnLayout(numberOfColumns=2,
                                                columnWidth=[(1, 500)],
                                                columnOffset=[(1, 'both', 5)],
                                                columnAlign=[(1, 'left')],
                                                parent=data_frame_wing, rowSpacing=[1, 5])

    cmds.button(label='Generate Tail', parent=data_row_wing_seg_01)"""



    #=================================================================================================================================
    # =================================================================================================================================
    # ==================================================CONTROLLER==========================================================
    # =================================================================================================================================
    # =================================================================================================================================
    #lets check from all global variables if there is one called global dict




    def check_global_dict():
        return "global_dict" in globals()

    def generate_height_guides():
        ### first we check to make sure that the unit scale in maya is the best one
        linear_units = cmds.currentUnit(query=True, linear=True)
        if linear_units != 'cm':
            utili.errorMessage('Please change unit to centimeter')
        else:
            ### lets validate if guide already exist.
            if cmds.objExists('height') == True:
                utili.errorMessage('height guide already exist')
            else:
                ### if the scale is in centimeters then we create a distance tool, this will provide scale to controllers
                distance_shape = cmds.distanceDimension(sp=(0, 0, 0), ep=(0, 2, 0))
                transform_node = cmds.listRelatives(distance_shape, parent=True)[0]
                locators = cmds.listConnections(distance_shape, type='locator')

                cmds.rename(transform_node, 'heightDistance')
                for i, loc in enumerate(locators):
                    if i == 0:
                        cmds.rename(loc, 'heightLocA')
                    else:
                        cmds.rename(loc, 'heightLocB')

                emptyGrp = utili.createEmptyGroup(name='height')
                [cmds.parent(object1, emptyGrp) for object1 in ('heightDistance', 'heightLocA', 'heightLocB')]

    def frame_collapse(button_name = None,frame = None):

        list = ['data_frame_hip', 'data_frame_torso', 'data_frame_leg', 'data_frame_arm',
                'data_frame_neck', 'data_frame_head', 'data_frame_tail', 'data_frame_wing']

        for item in list:
            if item == frame:

                cmds.frameLayout(item, edit=True, collapse=False)
            else:

                cmds.frameLayout(item, edit=True, collapse=True)


        ##cmds.deleteUI(button_name, control=True)


    def hip_ui():

        if constructor_limb_selected('hip') == False:

            data_row_hip = cmds.rowColumnLayout(numberOfColumns=2,
                                                columnWidth=[(1, 100), (2, 400)],
                                                columnOffset=[(1, 'left', 5), (2, 'both', 5)],
                                                columnAlign=[(1, 'left'), (2, 'center')],
                                                parent='selected_grid', rowSpacing=[1, 5])

            cmds.checkBoxGrp('root_jnt', numberOfCheckBoxes=2, label='Root Jnt (Game)',
                             labelArray2=['YES', 'NO'], parent='selected_grid')

            cmds.text(align='center', height=30, label='position', parent=data_row_hip)
            hip_position = cmds.textField(height=30, text='C', parent=data_row_hip)

            cmds.text(align='center', height=30, label='Body part', parent=data_row_hip)
            hip_bodypart = cmds.textField(height=30, text='hip', parent=data_row_hip)

            cmds.text(align='center', height=30, label='Function', parent=data_row_hip)
            hip_function = cmds.textField(height=30, text='BIND', parent=data_row_hip)

            cmds.button(label='{}'.format('Generate Hip Guide'), height=25, parent='selected_grid',
                command=lambda x: hip_guide_creating())

    def hip_guide_creating():

        sphere_name = cmds.sphere(name = 'hip_guide',r=1)[0]
        material_name = cmds.shadingNode('lambert', asShader=True)
        cmds.rename(material_name, "shaderrigger")  # Rename the material to "shaderrigger"
        # Step 3: Set the color of the material (e.g., Red color)
        shading_group = cmds.setAttr("shaderrigger.color", 1, 0.3921, 0.4232, type="double3")  # Red color
        # Step 5: Assign the material to the sphere
        cmds.select(sphere_name)
        cmds.hyperShade(assign='shaderrigger')

        distance_value = cmds.getAttr('heightDistance.distance')/2
        cmds.move(0, distance_value, 0, sphere_name)
        annotate = cmds.annotate(sphere_name, tx='hip', p=(0, distance_value, 0))
        cmds.parent(annotate, sphere_name)
        #cmds.rename(annotate, "hip_annotation")
        cmds.setAttr(annotate + '.overrideEnabled', 1)
        cmds.setAttr(annotate + '.overrideColor', 6)

    def torso_ui():
        if constructor_limb_selected('torso') == False:

            data_row_torso = cmds.rowColumnLayout(numberOfColumns=2,
                                                           columnWidth=[(1, 100), (2, 400)],
                                                           columnOffset=[(1, 'left', 5), (2, 'both', 5)],
                                                           columnAlign=[(1, 'left'), (2, 'center')],
                                                           parent='selected_grid', rowSpacing=[1, 5])

            cmds.text(align='center', height=30, label='number of spine:', parent=data_row_torso)
            int_field_name = cmds.intField(minValue=3, maxValue=5, value=3, parent=data_row_torso )

            cmds.text(align='center', height=30, label='group name', parent=data_row_torso)
            torso_grp = cmds.textField(height=30, text='torso', parent=data_row_torso)

            cmds.text(align='center', height=30, label='position', parent=data_row_torso)
            torso_position = cmds.textField(height=30, text='C', parent=data_row_torso)

            cmds.text(align='center', height=30, label='Body part', parent=data_row_torso)
            torso_bodypart = cmds.textField(height=30, text='torso', parent=data_row_torso)

            cmds.text(align='center', height=30, label='Function', parent=data_row_torso)
            torso_function = cmds.textField(height=30, text='BIND', parent=data_row_torso)

            cmds.button(label='{}'.format('Generate Hip Guide'), height=25, parent='selected_grid',
                command=lambda x: generate_chain_guide(int_field_name))



            data_row_torso02 = cmds.rowColumnLayout(numberOfColumns=2,
                                                  columnWidth=[(1, 100), (2, 400)],
                                                  columnOffset=[(1, 'left', 5), (2, 'both', 5)],
                                                  columnAlign=[(1, 'left'), (2, 'center')],
                                                  parent='selected_grid', rowSpacing=[1, 5])




            cmds.button(label='{}'.format('Generate torso jnt'), height=25, parent='selected_grid',
                        command=lambda x: generate_chain_guide(int_field_name))



            option_menu = cmds.optionMenu(label="Select jnt orientation",parent='selected_grid')
            cmds.menuItem(label="Option 1")
            cmds.menuItem(label="Option 2")
            cmds.menuItem(label="Option 3")

            cmds.button(label='{}'.format('change jnt orientation'), height=25, parent='selected_grid',
                        command=lambda x: generate_chain_guide(int_field_name))

            cmds.checkBoxGrp('ctrl_level', numberOfCheckBoxes=3, label='Control level',
                             labelArray3=['FK', 'FK/IK', 'TBA'], parent='selected_grid')

            data_row_torso03 = cmds.rowColumnLayout(numberOfColumns=2,
                                                    columnWidth=[(1, 100), (2, 400)],
                                                    columnOffset=[(1, 'left', 5), (2, 'both', 5)],
                                                    columnAlign=[(1, 'left'), (2, 'center')],
                                                    parent='selected_grid', rowSpacing=[1, 5])

            cmds.text(label="Pick a color:", parent=data_row_torso03)
            color_slider = cmds.colorSliderGrp(label="Color", rgb=(1.0, 0.0, 0.0), parent=data_row_torso03)

            cmds.button(label='{}'.format('Generate controller'), height=25, parent='selected_grid',
                        command=lambda x: generate_chain_guide(int_field_name))


    def generate_chain_guide(name_field = None):
        int_value = cmds.intField(name_field, query=True, value=True)
        print(int_value)


    def change_color_controller(color_slider = None,controller = None):
        color = cmds.colorSliderGrp(color_slider, query=True, rgb=True)
        cmds.setAttr('{}.overrideEnabled'.format(controller), 1)
        cmds.setAttr('{}.overrideColorRGB'.format(controller), color[0], color[1], color[2])

