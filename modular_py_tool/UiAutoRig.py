import maya.cmds as cmds
import os
import json

import modular_py_tool.auto_rig_fundation as fundation
#import pyTool.utilities as utili
import modular_py_tool.Utilities as utili
import modular_py_tool.FileClass as FileClass
import modular_py_tool.auto_rig_hip as hip
import modular_py_tool.auto_rig_torso as torso
import modular_py_tool.auto_rig_leg as leg

import importlib
importlib.reload(fundation)
importlib.reload(utili)
importlib.reload(FileClass)
importlib.reload(hip)
importlib.reload(leg)
importlib.reload(torso)




global _nested_dict_instance
_nested_dict_instance = FileClass.NestedDictionary()


def check_global_dict():
    return '_nested_dict_instance' in globals()

"""if check_global_dict():
    del _global_instance
else:"""


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
def arm_ui(limb_name = None,):
    clear_grid(grid='selected_grid')

    if constructor_limb_selected('lleg') == False:

        type_foot_option_menu = cmds.optionMenu('optionmenu_{}'.format(limb_name), label='Preset leg', parent='selected_grid')
        cmds.menuItem(label="human")
        cmds.menuItem(label="Digitigrade(Dog)")
        cmds.menuItem(label="Ungualigrade(horses)")
        cmds.menuItem(label="Invertebrate(Spider)")

        cmds.checkBoxGrp('arm_ik_fk_flag_{}'.format(limb_name), numberOfCheckBoxes=2, label='IK/FK',
                         labelArray2=['BOTH', 'FK'], parent='selected_grid',value1=True, value2=False)

        cmds.checkBoxGrp('arm_hand_flag_{}'.format(limb_name), numberOfCheckBoxes=2, label='Foot?',
                         labelArray2=['Yes', 'No'], parent='selected_grid',value1=True, value2=False)
        cmds.checkBoxGrp('arm_hand_digit_{}'.format(limb_name), numberOfCheckBoxes=3, label='Foot?',
                         labelArray3=['5', '3','2'], parent='selected_grid',value1=True, value2=False)
        cmds.checkBoxGrp('arm_hand_metacarpal_{}'.format(limb_name), numberOfCheckBoxes=2, label='Foot?',
                         labelArray2=['no', 'basic'], parent='selected_grid',value1=True, value2=False)

        data_row_lleg = cmds.rowColumnLayout(numberOfColumns=2,
                                            columnWidth=[(1, 100), (2, 400)],
                                            columnOffset=[(1, 'left', 5), (2, 'both', 5)],
                                            columnAlign=[(1, 'left'), (2, 'center')],
                                            parent='selected_grid', rowSpacing=[1, 5])



        cmds.text(align='center', height=30, label='name limb connection', parent=data_row_lleg)
        leg_cog_data = _nested_dict_instance.data.get('COG', {})
        leg_cog_keys = [key for key in leg_cog_data if key != 'general']
        default_parent = leg_cog_keys[0] if leg_cog_keys else 'None'
        hip_position = cmds.textField('name_limb_connection_{}'.format(limb_name) ,height=30, text=default_parent, parent=data_row_lleg) ### chest01 default connection to the body

        cmds.text(align='center', height=30, label='limb_name', parent=data_row_lleg)
        hip_position = cmds.textField(height=30, text='{}'.format(limb_name), parent=data_row_lleg, enable = False)



        data_row_lleg_a = cmds.rowColumnLayout(numberOfColumns=2,
                                                columnWidth=[(1, 400), (2, 100)],
                                                columnOffset=[(1, 'both', 5), (2, 'both', 5)],
                                                columnAlign=[(1, 'center'), (2, 'center')],
                                                parent='selected_grid', rowSpacing=[1, 5])






        cmds.button(label='{}'.format('Generate guide'), height=25, parent=data_row_lleg_a,
                    command=lambda x: leg.controller_leg_guide(char_name = cmds.textField('charactername', query=True, text=True),limb_name = limb_name, leg_type = cmds.optionMenu('optionmenu_{}'.format(limb_name),q=True, v=True),limb_connection =  cmds.textField('name_limb_connection_{}'.format(limb_name), query=True, text=True) ,
                                                               kinematic_mode = cmds.checkBoxGrp('leg_ik_fk_flag_{}'.format(limb_name), query=True, valueArray2=True), limb_end = cmds.checkBoxGrp('leg_foot_flag_{}'.format(limb_name), query=True, valueArray2=True) ))
        cmds.button(label='{}'.format('Update'), height=25, parent=data_row_lleg_a)

        cmds.button(label='{}'.format('Generate Jnt from guide'), height=25, parent=data_row_lleg_a,
                    command=lambda x: leg.controller_leg_jnt(char_name = cmds.textField('charactername', query=True, text=True),limb_name = limb_name, leg_type = cmds.optionMenu('optionmenu_{}'.format(limb_name),q=True, v=True),limb_connection =  cmds.textField('name_limb_connection_{}'.format(limb_name), query=True, text=True) ,
                                                             kinematic_mode = cmds.checkBoxGrp('leg_ik_fk_flag_{}'.format(limb_name), query=True, valueArray2=True), limb_end = cmds.checkBoxGrp('leg_foot_flag_{}'.format(limb_name), query=True, valueArray2=True) ))
        cmds.button(label='{}'.format('Update'), height=25, parent=data_row_lleg_a)



def leg_ui(limb_name = None,):
    clear_grid(grid='selected_grid')

    if constructor_limb_selected('lleg') == False:

        type_foot_option_menu = cmds.optionMenu('optionmenu_{}'.format(limb_name), label='Preset leg', parent='selected_grid')
        cmds.menuItem(label="human")
        cmds.menuItem(label="Digitigrade(Dog)")
        cmds.menuItem(label="Ungualigrade(horses)")
        cmds.menuItem(label="Invertebrate(Spider)")

        cmds.checkBoxGrp('leg_ik_fk_flag_{}'.format(limb_name), numberOfCheckBoxes=2, label='IK/FK',
                         labelArray2=['BOTH', 'FK'], parent='selected_grid',value1=True, value2=False)

        cmds.checkBoxGrp('leg_foot_flag_{}'.format(limb_name), numberOfCheckBoxes=2, label='Foot?',
                         labelArray2=['Yes', 'No'], parent='selected_grid',value1=True, value2=False)

        data_row_lleg = cmds.rowColumnLayout(numberOfColumns=2,
                                            columnWidth=[(1, 100), (2, 400)],
                                            columnOffset=[(1, 'left', 5), (2, 'both', 5)],
                                            columnAlign=[(1, 'left'), (2, 'center')],
                                            parent='selected_grid', rowSpacing=[1, 5])



        cmds.text(align='center', height=30, label='name limb connection', parent=data_row_lleg)
        leg_cog_data = _nested_dict_instance.data.get('COG', {})
        leg_cog_keys = [key for key in leg_cog_data if key != 'general']
        default_parent = leg_cog_keys[0] if leg_cog_keys else 'None'
        hip_position = cmds.textField('name_limb_connection_{}'.format(limb_name) ,height=30, text=default_parent, parent=data_row_lleg) ### chest01 default connection to the body

        cmds.text(align='center', height=30, label='limb_name', parent=data_row_lleg)
        hip_position = cmds.textField(height=30, text='{}'.format(limb_name), parent=data_row_lleg, enable = False)



        data_row_lleg_a = cmds.rowColumnLayout(numberOfColumns=2,
                                                columnWidth=[(1, 400), (2, 100)],
                                                columnOffset=[(1, 'both', 5), (2, 'both', 5)],
                                                columnAlign=[(1, 'center'), (2, 'center')],
                                                parent='selected_grid', rowSpacing=[1, 5])






        cmds.button(label='{}'.format('Generate guide'), height=25, parent=data_row_lleg_a,
                    command=lambda x: leg.controller_leg_guide(char_name = cmds.textField('charactername', query=True, text=True),limb_name = limb_name, leg_type = cmds.optionMenu('optionmenu_{}'.format(limb_name),q=True, v=True),limb_connection =  cmds.textField('name_limb_connection_{}'.format(limb_name), query=True, text=True) ,
                                                               kinematic_mode = cmds.checkBoxGrp('leg_ik_fk_flag_{}'.format(limb_name), query=True, valueArray2=True), limb_end = cmds.checkBoxGrp('leg_foot_flag_{}'.format(limb_name), query=True, valueArray2=True) ))
        cmds.button(label='{}'.format('Update'), height=25, parent=data_row_lleg_a)

        cmds.button(label='{}'.format('Generate Jnt from guide'), height=25, parent=data_row_lleg_a,
                    command=lambda x: leg.controller_leg_jnt(char_name = cmds.textField('charactername', query=True, text=True),limb_name = limb_name, leg_type = cmds.optionMenu('optionmenu_{}'.format(limb_name),q=True, v=True),limb_connection =  cmds.textField('name_limb_connection_{}'.format(limb_name), query=True, text=True) ,
                                                             kinematic_mode = cmds.checkBoxGrp('leg_ik_fk_flag_{}'.format(limb_name), query=True, valueArray2=True), limb_end = cmds.checkBoxGrp('leg_foot_flag_{}'.format(limb_name), query=True, valueArray2=True) ))
        cmds.button(label='{}'.format('Update'), height=25, parent=data_row_lleg_a)



def build_layout(option_menu = None,grid_layout = None,reload = None,limb_number = 1):



    #### HERE WE CHECK IF ALREADY EXIST A LAYOUT INSIDE THE LAYOUT FRAMER, IF EXISTE WE DELETE EVETHING INSIDE
    if cmds.layout('{}_layout_frame'.format(option_menu), exists=True):
        # List all children of the layout
        children = cmds.layout('{}_layout_frame'.format(option_menu), query=True, childArray=True)

        if children:
            for child in children:
                cmds.deleteUI(child)
        else:
            print("No children found to delete.")
    if cmds.layout('{}_layout'.format(option_menu), exists=True):
        cmds.deleteUI('{}_layout'.format(option_menu))


    limb_amount = limb_number
    if option_menu[1:] == 'leg':
        limb_layout = cmds.gridLayout('{}_layout'.format(option_menu) ,numberOfColumns=limb_amount + 1, cellWidthHeight=(100 / (limb_amount + 1), 75),
                                      parent='{}_layout_frame'.format(option_menu))

    if (option_menu == 'rleg'):
        cmds.button(label='', enable=False, height=15, parent='{}_layout'.format(option_menu))

    for i in range(limb_amount):
        create_button(option_menu,i)

    if (option_menu == 'lleg'):
        cmds.button(label='', enable=False, height=15, parent='{}_layout'.format(option_menu))




def create_button(option_menu,i):
    print('we enter to create button')
    vertical_label = '\n'.join('{}{}'.format(option_menu, i+1))
        # This matches your print statement logic
    # Create the button with the correct label and the correct limb_name
    #if (option_menu == 'lleg'):

    if option_menu[1:] == 'leg':
        cmds.button('{}{}'.format(option_menu, i ), label=vertical_label, height=75,
                    parent='{}_layout'.format(option_menu),
                    command=lambda x: leg_ui(limb_name='{}{:02d}'.format(option_menu, i+1 )))
    #cmds.button(label='', enable=False, height=75, parent='{}_layout'.format(option_menu))
    if option_menu[1:] == 'arm':
        cmds.button('{}{}'.format(option_menu, i), label='{}{:02d}'.format(option_menu, i+1), height=20,
                    parent='{}_layout_frame'.format(option_menu),
                    command=lambda x: arm_ui(limb_name='{}{:02d}'.format(option_menu, i + 1)))




    """if (option_menu == 'rleg'):
        #cmds.button(label='', enable=False, height=75, parent='{}_layout'.format(option_menu))


        cmds.button('{}{}'.format(option_menu,i), label=vertical_label , height=75, parent='{}_layout'.format(option_menu),
                    command=lambda x: leg_ui(limb_name='{}{:02d}'.format(option_menu,i+1)))
"""

def limb_option_menu_change( option_menu = None ,selected_value = None):

    build_layout(option_menu = option_menu, reload=True, limb_number=int(selected_value))
    """if option_menu == 'lleg':
        build_lleg_layout(leg_grid_layout='lleg_layout_frame', reload=True,limb_number = int(selected_value))
    elif option_menu == 'rleg':
        return 0
    elif option_menu == 'tail':
        return 1
    elif option_menu == 'head':
        return 1
    elif option_menu == 'rarm':
        return 0
    elif option_menu == 'larm':
        return 0"""
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
    # File name
    cmds.text(align='center', height=30, label='Json name:', parent=data_row_general_seg_01)
    json_file_name = cmds.textField('filename', height=30, text='file name', parent=data_row_general_seg_01)

    # Character name
    cmds.text(align='center', height=30, label='character name:', parent=data_row_general_seg_01)
    char_name = cmds.textField('charactername', height=30, text='max', parent=data_row_general_seg_01)



    ###########################################################

    data_row_general_seg_02 = cmds.rowColumnLayout(numberOfColumns=1,
                                           columnWidth=[(1, 500)],
                                           columnOffset=[(1, 'both', 5)],
                                           columnAlign=[(1, 'left')],
                                           parent=data_frame_general, rowSpacing=[1,5])
    # Lets calculate the height of the character
    cmds.button(label='FILE MANAGEMENT (Save,Load, Delete)', parent=data_row_general_seg_02, command=lambda x: ScrollListUi())
    cmds.button(label='Generate Height guide', parent=data_row_general_seg_02,command=lambda x: utili.generate_height_guides())

    type_rig_option_menu = option_menu = cmds.optionMenu('type_rig_option_menu',label='Fundation rig', parent=data_row_general_seg_02)
    cmds.menuItem(label="Select a option")
    cmds.menuItem(label="Game")
    cmds.menuItem(label="Cinematic")
    cmds.menuItem(label="Other")
    #this trigger a function call any time we change something in the option menu
    cmds.optionMenu(type_rig_option_menu, e=True, cc=lambda *args: fundation.type_rig_option_menu_change(cmds.optionMenu(type_rig_option_menu,
                                                                                                     q=True, v=True),cmds.textField(char_name, query=True, text=True)))

    data_row_general_seg_03 = cmds.rowColumnLayout(numberOfColumns=3,
                                                   columnWidth=[(1, 125), (2, 125), (3, 125), (4, 125)],
                                                   columnOffset=[(1, 'both', 5), (2, 'both', 5), (3, 'both', 5), (4, 'both', 5)],
                                                   columnAlign=[(1, 'center'), (2, 'center'), (3, 'center'), (4, 'center')],
                                                   parent=data_frame_general, rowSpacing=[1, 5])

    option_menu = cmds.optionMenu(label='head',parent= data_row_general_seg_03)
    cmds.menuItem(label="1")
    cmds.menuItem(label="2")
    cmds.menuItem(label="3")

    larm_option_menu = cmds.optionMenu('larm',label='larm ',parent= data_row_general_seg_03)
    cmds.menuItem(label="1")
    cmds.menuItem(label="2")
    cmds.menuItem(label="3")
    # this trigger a function call any time we changge something in the option menu
    cmds.optionMenu(larm_option_menu, e=True, cc=lambda *args: limb_option_menu_change(
        option_menu='larm', selected_value=cmds.optionMenu(larm_option_menu, q=True, v=True)))

    option_menu = cmds.optionMenu(label='rarm', parent=data_row_general_seg_03)
    cmds.menuItem(label="1")
    cmds.menuItem(label="2")
    cmds.menuItem(label="3")

    lleg_option_menu = cmds.optionMenu( 'lleg',label='lleg ', parent=data_row_general_seg_03)
    cmds.menuItem(label="1")
    cmds.menuItem(label="2")
    cmds.menuItem(label="3")
    # this trigger a function call any time we changge something in the option menu
    cmds.optionMenu(lleg_option_menu, e=True, cc=lambda *args: limb_option_menu_change(
        option_menu = 'lleg' ,selected_value = cmds.optionMenu(lleg_option_menu, q=True, v=True)))



    rleg_option_menu = cmds.optionMenu('rleg',label='rleg', parent=data_row_general_seg_03)
    cmds.menuItem(label="1")
    cmds.menuItem(label="2")
    cmds.menuItem(label="3")

    # this trigger a function call any time we changge something in the option menu
    cmds.optionMenu(rleg_option_menu, e=True, cc=lambda *args: limb_option_menu_change( option_menu = 'rleg',
                                                                                     selected_value = cmds.optionMenu(rleg_option_menu,
                                                                                                     q=True, v=True)))

    option_menu = cmds.optionMenu(label='tail ', parent=data_row_general_seg_03)
    cmds.menuItem(label="1")
    cmds.menuItem(label="2")
    cmds.menuItem(label="3")

    ##########################################################################
    data_frame_limbview = cmds.frameLayout(label='visual structure rig', width=500,
                                          collapsable=True, parent=main_layout)

    # General face guides
    """grid_layoutgeneral = cmds.gridLayout(numberOfColumns=3,
                                         cellWidthHeight=(500, 25), 
                                         parent=data_frame_general)"""
    head_grid_layout = cmds.rowColumnLayout(numberOfColumns=7,
                                                   columnWidth=[(1, 100),(2, 300),(3, 100)],
                                                   columnOffset=[(1, 'both', 2),(2, 'both', 2),(3, 'both', 2)],
                                                   columnAlign=[(1, 'left'),(2, 'left'),(3, 'left')],
                                                   parent=data_frame_limbview, rowSpacing=[1, 5])


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
                                            parent=data_frame_limbview, rowSpacing=[1, 5])

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
                                            parent=data_frame_limbview, rowSpacing=[1, 5])

    cmds.button(label='',enable=False, height=25, parent=torso_grid_layout)

    rarm_layout = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(100, 37.5), parent=torso_grid_layout)
    cmds.button(label='R_ARM', height=37.5, parent=rarm_layout,
                command=lambda x: constructor_limb_selected(limb_selected = 'rarm'))
    cmds.button(label='', enable=False, height=15, parent=rarm_layout)



    cmds.button(label='TORSO', height=75, parent=torso_grid_layout,
                command=lambda x: torso_ui())

    larm_gridLayout_frame = cmds.gridLayout('larm_layout_frame', numberOfColumns=1, cellWidthHeight=(100, 20), parent=torso_grid_layout)
    build_layout(option_menu='larm', grid_layout='larm_layout_frame')

    cmds.button(label='',enable=False, height=25, parent=torso_grid_layout)
    #########

    hip_grid_layout = cmds.rowColumnLayout(numberOfColumns=5,
                                             columnWidth=[(1, 100), (2, 100), (3, 100), (4, 100), (5, 100)],
                                             columnOffset=[(1, 'both', 2), (2, 'both', 2), (3, 'both', 2),
                                                           (4, 'both', 2), (5, 'both', 2)],
                                             columnAlign=[(1, 'left'), (2, 'left'), (3, 'left'), (4, 'left'),
                                                          (5, 'left')],
                                             parent=data_frame_limbview, rowSpacing=[1, 5])

    cmds.button(label='', enable=False, height=25, parent=hip_grid_layout)
    cmds.button(label='', enable=False, height=25, parent=hip_grid_layout)
    cmds.button(label='HIP (1)', height=25, parent=hip_grid_layout ,
                command=lambda x: hip_ui())
    cmds.button(label='', enable=False, height=25, parent=hip_grid_layout)
    cmds.button(label='', enable=False, height=25, parent=hip_grid_layout)


    ######### LEG ROW #########

    leg_grid_rowColumnlayout = cmds.rowColumnLayout( 'leg_grid_rowColumnlayout' ,numberOfColumns=5,
                                       columnWidth=[(1, 100), (2, 100), (3, 100), (4, 100), (5, 100)],
                                       columnOffset=[(1, 'both', 2), (2, 'both', 2), (3, 'both', 2),
                                                     (4, 'both', 2), (5, 'both', 2)],
                                       columnAlign=[(1, 'left'), (2, 'left'), (3, 'left'), (4, 'left'),
                                                    (5, 'left')],
                                       parent=data_frame_limbview, rowSpacing=[1, 5])

    cmds.button(label='', enable=False, height=75, parent=leg_grid_rowColumnlayout)

    rleg_gridLayout_frame = cmds.gridLayout('rleg_layout_frame', numberOfColumns=1, cellWidthHeight=(100, 75),
                                            parent=leg_grid_rowColumnlayout)
    build_layout(option_menu='rleg', grid_layout='rleg_layout_frame')



    """cmds.button(label='', enable=False, height=75, parent=rleg_layout)
    cmds.button(label='R_LEG', height=75, parent=rleg_layout ,
                command=lambda x: constructor_limb_selected(limb_selected = 'rleg'))"""

    tail_gridLayout_frame = cmds.gridLayout('tail_gridLayout_frame', numberOfColumns=1, cellWidthHeight=(100, 75),
                                            parent=leg_grid_rowColumnlayout)

    tail_layout = cmds.gridLayout(numberOfColumns=5, cellWidthHeight=(20, 75), parent=tail_gridLayout_frame)
    cmds.button(label='', enable=False, height=75, parent=tail_layout)
    cmds.button(label='', enable=False, height=75, parent=tail_layout)
    cmds.button(label='TAIL', height=75, parent=tail_layout ,
                command=lambda x: constructor_limb_selected(limb_selected = 'tail'))
    cmds.button(label='', enable=False, height=75, parent=tail_layout)
    cmds.button(label='', enable=False, height=75, parent=tail_layout)

    lleg_gridLayout_frame = cmds.gridLayout('lleg_layout_frame', numberOfColumns=1, cellWidthHeight=(100, 75), parent=leg_grid_rowColumnlayout)
    build_layout(option_menu= 'lleg',grid_layout = 'lleg_layout_frame')

    cmds.button(label='', enable=False, height=75, parent=leg_grid_rowColumnlayout)



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

    #cmds.button(label='Name', height=25, parent=selected_grid_layout)


    #=================================================================================================================================
    # =================================================================================================================================
    # ==================================================CONTROLLER==========================================================
    # =================================================================================================================================
    # =================================================================================================================================
    #lets check from all global variables if there is one called global dict





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

            data_row_hip_a = cmds.rowColumnLayout(numberOfColumns=2,
                                                  columnWidth=[(1, 100), (2, 400)],
                                                  columnOffset=[(1, 'both', 5), (2, 'both', 5)],
                                                  columnAlign=[(1, 'center'), (2, 'center')],
                                                  parent='selected_grid', rowSpacing=[1, 5])

            cmds.text(align='center', height=30, label='parent', parent=data_row_hip_a)

            fundation_data = _nested_dict_instance.data.get('fundation', {})
            fundation_keys = [key for key in fundation_data if key != 'general']
            default_parent = fundation_keys[0] if fundation_keys else 'None'
            parent_name = cmds.textField('cog_parent_name', height=30,text=default_parent,parent=data_row_hip_a)


            """ if [key for key in _nested_dict_instance.data.get('fundation', {}) if key != 'general'][0] is not None:
                parent_name = cmds.textField('cog_parent_name', height=30, text=_nested_dict_instance.data['COG']['general']['parent'],
                                             parent=data_row_hip_a)  ### chest01 default connection to the body
            else:
                parent_name = cmds.textField('cog_parent_name',height=30, text='root_jnt',
                                             parent=data_row_hip_a)  ### chest01 default connection to the body"""

            data_row_hip = cmds.rowColumnLayout(numberOfColumns=2,
                                                columnWidth=[(1, 400), (2, 100)],
                                                columnOffset=[(1, 'both', 5), (2, 'both', 5)],
                                                columnAlign=[(1, 'center'), (2, 'center')],
                                                parent='selected_grid', rowSpacing=[1, 5])



            cmds.button(label='{}'.format('Generate COG Guide'), height=25, parent=data_row_hip,
                command=lambda x: hip.controller_hip_guide(char_name = cmds.textField(char_name, query=True, text=True),parent_name = cmds.textField('cog_parent_name', query=True, text=True)))
            cmds.button(label='{}'.format('Update'), height=25, parent=data_row_hip, command=lambda x: _nested_dict_instance.update_limb(char_name = cmds.textField(char_name, query=True, text=True), limb_name = 'COG',parent = cmds.textField(parent_name, query=True, text=True), list = ['COG'],suffix = 'guide'))

            cmds.button(label='{}'.format('Generate Jnt from guide'), height=25, parent=data_row_hip,
                        command=lambda x: hip.controller_hip_jnt(char_name = cmds.textField(char_name, query=True, text=True),parent_name = cmds.textField('cog_parent_name', query=True, text=True)))
            cmds.button(label='{}'.format('Update'), height=25, parent=data_row_hip, command=lambda x: _nested_dict_instance.update_limb(char_name = cmds.textField(char_name, query=True, text=True), limb_name = 'COG',parent = cmds.textField(parent_name, query=True, text=True), list = ['COG'],suffix = 'jnt'))


    def torso_ui():
        if constructor_limb_selected('torso') == False:

            data_row_torso = cmds.rowColumnLayout(numberOfColumns=2,
                                                           columnWidth=[(1, 100), (2, 400)],
                                                           columnOffset=[(1, 'both', 5), (2, 'both', 5)],
                                                           columnAlign=[(1, 'center'), (2, 'center')],
                                                           parent='selected_grid', rowSpacing=[1, 5])

            cmds.text(align='center', height=30, label='parent', parent=data_row_torso)
            cog_data = _nested_dict_instance.data.get('COG', {})
            cog_keys = [key for key in cog_data if key != 'general']
            default_parent = cog_keys[0] if cog_keys else 'None'
            parent_name = cmds.textField(height=30, text=default_parent,
                                          parent=data_row_torso)  ### chest01 default connection to the body


            cmds.text(align='center', height=30, label='number of spine:', parent=data_row_torso)
            #cmds.text(align='center', height=30, label='number of spine:', parent=data_row_torso)
            int_field_name = cmds.intField(minValue=1, maxValue=5, value=3,step=1, parent=data_row_torso )

            data_row_torso01 = cmds.rowColumnLayout(numberOfColumns=2,
                                                  columnWidth=[(1, 400), (2, 100)],
                                                  columnOffset=[(1, 'both', 5), (2, 'both', 5)],
                                                  columnAlign=[(1, 'center'), (2, 'center')],
                                                  parent='selected_grid', rowSpacing=[1, 5])



            cmds.button(label='{}'.format('Generate Chest guide'), height=25, parent=data_row_torso01,
                        command=lambda x: torso.controller_chest_guide(char_name = cmds.textField(char_name, query=True, text=True),parent_name = cmds.textField(parent_name, query=True, text=True)))
            cmds.button(label='{}'.format('Update'), height=25, parent=data_row_torso01, command=lambda x: _nested_dict_instance.update_limb(char_name = cmds.textField(char_name, query=True, text=True), limb_name = 'torso',parent = cmds.textField(parent_name, query=True, text=True), list = ['spine','chest'],suffix = 'guide'))

            cmds.button(label='{}'.format('Generate torso Guides'), height=25, parent=data_row_torso01 , command=lambda x: torso.controller_torso_guide(char_name = cmds.textField(char_name, query=True, text=True),parent_name = cmds.textField(parent_name, query=True, text=True),spine_num = cmds.intField(int_field_name, query=True, value=True) ))
            cmds.button(label='{}'.format('Update'), height=25, parent=data_row_torso01, command=lambda x: _nested_dict_instance.update_limb(char_name = cmds.textField(char_name, query=True, text=True), limb_name = 'torso',parent = cmds.textField(parent_name, query=True, text=True), list = ['spine','chest'],suffix = 'guide'))

            cmds.button(label='{}'.format('Generate torso jnt'), height=25, parent=data_row_torso01, command=lambda x: torso.controller_torso_jnt(char_name = cmds.textField(char_name, query=True, text=True),parent_name = cmds.textField(parent_name, query=True, text=True),spine_num = cmds.intField(int_field_name, query=True, value=True) ))
            cmds.button(label='{}'.format('Update'), height=25, parent=data_row_torso01, command=lambda x: _nested_dict_instance.update_limb(char_name = cmds.textField(char_name, query=True, text=True), limb_name = 'torso',parent = cmds.textField(parent_name, query=True, text=True), list = ['spine','chest'],suffix = 'jnt'))

            data_row_torso02 = cmds.rowColumnLayout(numberOfColumns=1,
                                                    columnWidth=[(1, 500)],
                                                    #columnOffset=[(1, 'left', 5), (2, 'both', 5)],
                                                    columnAlign=[(1, 'center')],
                                                    parent='selected_grid', rowSpacing=[1, 5])



            option_menu = cmds.optionMenu(label="Select jnt orientation",parent=data_row_torso02)
            cmds.menuItem(label="Option 1")
            cmds.menuItem(label="Option 2")
            cmds.menuItem(label="Option 3")

            cmds.button(label='{}'.format('change jnt orientation'), height=25, parent=data_row_torso02)

            cmds.checkBoxGrp('ctrl_level', numberOfCheckBoxes=2, label='IK/FK',
                             labelArray2=['Both', 'FK'], parent=data_row_torso02)

            data_row_torso03 = cmds.rowColumnLayout(numberOfColumns=2,
                                                    columnWidth=[(1, 100), (2, 400)],
                                                    columnOffset=[(1, 'left', 5), (2, 'both', 5)],
                                                    columnAlign=[(1, 'left'), (2, 'center')],
                                                    parent='selected_grid', rowSpacing=[1, 5])

            cmds.text(label="Pick a color:", parent=data_row_torso03)
            color_slider = cmds.colorSliderGrp(label="Color", rgb=(1.0, 0.0, 0.0), parent=data_row_torso03)

            cmds.button(label='{}'.format('Generate controller'), height=25, parent='selected_grid')


    def generate_chain_guide(name_field = None,torso_grp = None):
        int_value = cmds.intField(name_field, query=True, value=True)
        group_value = cmds.textField(torso_grp, query=True, text=True)
        for number in range(int_value):
            print('{}{:02d}'.format(group_value,number+1))

    """def generate_chain_guide(int_value=None, group_value=None):

        for number in range(int_value):
            print('{}{:02d}'.format(group_value,number+1))"""



    def change_color_controller(color_slider = None,controller = None):
        color = cmds.colorSliderGrp(color_slider, query=True, rgb=True)
        cmds.setAttr('{}.overrideEnabled'.format(controller), 1)
        cmds.setAttr('{}.overrideColorRGB'.format(controller), color[0], color[1], color[2])

    def save_limb_json():
        my_dict = {}
        sub_dict = {}


    def ScrollListUi(*args):
        if cmds.window("mySecondWindow", exists=True):
            cmds.deleteUI("mySecondWindow", window=True)

        second_window = cmds.window("mySecondWindow", title="Second Window", widthHeight=(500, 150))

        main_layout2 = cmds.columnLayout(adjustableColumn=True)

        json_load = cmds.rowColumnLayout(numberOfColumns=3,
                                          columnWidth=[(1, 100), (2, 250), (3, 150)],
                                          columnOffset=[(1, 'both', 5), (2, 'both', 0),
                                                        (3, 'both', 5)],
                                          columnAlign=[(1, 'left'), (2, 'center'), (3, 'right')],
                                          parent=main_layout2, rowSpacing=[1, 5])
        # guide load
        ##char_name = cmds.textField(general_name, query=True, text=True)

        # load save position
        cmds.text(align='left', height=30, label='Plane Pos', parent=json_load)
        file_name = cmds.textScrollList(numberOfRows=5, allowMultiSelection=False
                                                 , showIndexedItem=4, parent=json_load)
        utili.ScrollListFileManage( action='show', field=file_name)

        jsonload_btn_gridl = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(150, 25), parent=json_load)

        cmds.button(label='Load selected', parent=jsonload_btn_gridl, command=lambda x: _nested_dict_instance.LoadDictionary(file_name=file_name))
        cmds.button(label='Delete', parent=jsonload_btn_gridl)
        cmds.button(label='Save', parent=jsonload_btn_gridl, command=lambda x: _nested_dict_instance.SaveDictionary(file_name = cmds.textField('filename', query=True, text=True), char_name = cmds.textField('charactername', query=True, text=True) ))
        cmds.button(label='Refresh list', parent=jsonload_btn_gridl,
                    command=lambda x: utili.file_manage( action='show', field=file_name))


        cmds.button(label="Close", command=lambda *x: cmds.deleteUI("mySecondWindow", window=True))
        cmds.showWindow(second_window)


def NameInputUi(section_dir=None, dictionary=None):
    if cmds.window('InputName', exists=True):
        cmds.deleteUI('InputName')
    InputName = cmds.window('InputName', title='Input file name', width=500, height=100)

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
                command=lambda x: utili.ScrollListFileManage(section_dir=section_dir, action='write',
                                                               field=textfields, dictionary=dictionary,
                                                               windows=InputName))

    nameInputWin2 = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(500, 40), parent=data_frame_name_input)
    cmds.button(label='Close', height=40, parent=nameInputWin2, command=lambda x: cmds.deleteUI(InputName))

    cmds.showWindow(InputName)
