import maya.cmds as cmds
import os
import json

import pyTool.modular_py_tool.auto_rig_fundation as fundation
import pyTool.utilities as utili
import importlib
importlib.reload(fundation)
importlib.reload(utili)


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


    cmds.button(label='R_WING', height=25, parent=head_grid_layout,command=lambda x: frame_collapse(button_name = 'wing_botton',frame = 'data_frame_wing'))


    #cmds.button('head_botton',label='HEAD', height=50, parent=head_grid_layout,command=lambda x: controller_eyebrow_mirror(button_name = 'head_botton',frame = data_frame_head ))

    head_layout = cmds.gridLayout( 'head_gridlayout',numberOfColumns=5, cellWidthHeight=(60, 50), parent=head_grid_layout)
    cmds.button('head_botton1',label='', enable=False, height=15, parent=head_layout)
    cmds.button('head_botton2',label='', enable=False, height=15, parent=head_layout)
    #cmds.button('head_botton3',label='Head', height=50, parent=head_layout,command=lambda x: frame_collapse(button_name = 'head_botton',frame = 'data_frame_head'))
    cmds.button('head_botton3', label='Head', height=50, parent=head_layout,
                command=lambda x: constructor_limb_selected(limb_selected = 'head selected'))

    cmds.button('head_botton4',label='', enable=False, height=15, parent=head_layout)
    cmds.button('head_botton5',label='', enable=False, height=15, parent=head_layout)

    cmds.button(label='L_WING', height=25, parent=head_grid_layout,command=lambda x: frame_collapse(button_name = 'wing_botton',frame = 'data_frame_wing'))
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
                command=lambda x: constructor_limb_selected(limb_selected = 'neck selected'))
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
    cmds.button(label='R_ARM', height=37.5, parent=rarm_layout,command=lambda x: frame_collapse(button_name = 'arm_botton',frame = 'data_frame_arm'))
    cmds.button(label='', enable=False, height=15, parent=rarm_layout)



    cmds.button(label='TORSO', height=75, parent=torso_grid_layout,command=lambda x: frame_collapse(button_name = 'torso_botton',frame = 'data_frame_torso'))

    larm_layout = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(100, 37.5), parent=torso_grid_layout)
    cmds.button(label='L_ARM', height=37.5, parent=larm_layout,command=lambda x: frame_collapse(button_name = 'arm_botton',frame = 'data_frame_arm'))
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
    cmds.button(label='HIP (1)', height=25, parent=hip_grid_layout ,command=lambda x: frame_collapse(button_name = 'hip_botton',frame = 'data_frame_hip'))
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
    cmds.button(label='R_LEG', height=75, parent=rleg_layout ,command=lambda x: frame_collapse(button_name = 'leg_botton',frame = 'data_frame_leg'))

    lleg_layout = cmds.gridLayout(numberOfColumns=5, cellWidthHeight=(20, 75), parent=leg_grid_layout)
    cmds.button(label='', enable=False, height=75, parent=lleg_layout)
    cmds.button(label='', enable=False, height=75, parent=lleg_layout)
    cmds.button(label='TAIL', height=75, parent=lleg_layout ,command=lambda x: frame_collapse(button_name = 'tail_botton',frame = 'data_frame_tail'))
    cmds.button(label='', enable=False, height=75, parent=lleg_layout)
    cmds.button(label='', enable=False, height=75, parent=lleg_layout)

    lleg_layout = cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(50, 75), parent=leg_grid_layout)
    cmds.button(label='L_LEG', height=75, parent=lleg_layout ,command=lambda x: frame_collapse(button_name = 'leg_botton',frame = 'data_frame_leg'))
    cmds.button(label='', enable=False, height=75, parent=lleg_layout)


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
    def clear_grid(grid = None):
        children = cmds.layout(grid, q=True, childArray=True)
        # Delete each child
        if children:
            for child in children:
                cmds.deleteUI(child)

    def constructor_limb_selected(limb_selected = None):
        clear_grid(grid = 'selected_grid')
        cmds.button(label='{}'.format(limb_selected), height=25, parent='selected_grid')

