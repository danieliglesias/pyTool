import maya.cmds as cmds
import os
import json

import pyTool.modular_py_tool.auto_rig_fundation as fundation
#import pyTool.utilities as utili
import pyTool.modular_py_tool.Utilities as utili
import pyTool.modular_py_tool.FileClass as FileClass

import importlib
importlib.reload(fundation)
importlib.reload(utili)
importlib.reload(FileClass)



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



def lleg_ui(limb_name = None):
    clear_grid(grid='selected_grid')
    print("entramos")
    if constructor_limb_selected('lleg') == False:

        type_foot_option_menu = cmds.optionMenu(label='Preset leg', parent='selected_grid')
        cmds.menuItem(label="Select a option")
        cmds.menuItem(label="Plantigrade(biped)")
        cmds.menuItem(label="Digitigrade(Dog)")
        cmds.menuItem(label="Ungualigrade(horses)")
        cmds.menuItem(label="Invertebrate(Spider)")

        cmds.checkBoxGrp('leg_ik_fk_flag', numberOfCheckBoxes=2, label='IK/FK',
                         labelArray2=['BOTH', 'FK'], parent='selected_grid')

        cmds.checkBoxGrp('leg_foot_flag', numberOfCheckBoxes=2, label='Foot?',
                         labelArray2=['Yes', 'No'], parent='selected_grid')

        data_row_lleg = cmds.rowColumnLayout(numberOfColumns=2,
                                            columnWidth=[(1, 100), (2, 400)],
                                            columnOffset=[(1, 'left', 5), (2, 'both', 5)],
                                            columnAlign=[(1, 'left'), (2, 'center')],
                                            parent='selected_grid', rowSpacing=[1, 5])



        cmds.text(align='center', height=30, label='guide limb connection', parent=data_row_lleg)
        hip_position = cmds.textField(height=30, text='C_COG_BIND_jnt', parent=data_row_lleg) ### chest01 default connection to the body

        cmds.text(align='center', height=30, label='limb_name', parent=data_row_lleg)
        hip_position = cmds.textField(height=30, text='{}'.format(limb_name), parent=data_row_lleg, enable = False)

        cmds.text(align='center', height=30, label='position', parent=data_row_lleg)
        hip_position = cmds.textField(height=30, text='L', parent=data_row_lleg)

        cmds.text(align='center', height=30, label='Body part', parent=data_row_lleg)
        hip_bodypart = cmds.textField(height=30, text='leg', parent=data_row_lleg)

        cmds.text(align='center', height=30, label='Function', parent=data_row_lleg)
        hip_function = cmds.textField(height=30, text='BIND', parent=data_row_lleg)



        cmds.button(label='{}'.format('Generate lleg Guide'), height=25, parent='selected_grid')

def build_layout(option_menu = None,grid_layout = None,reload = None,limb_number = 1):

    if cmds.layout('{}_layout'.format(option_menu), exists=True):
        # List all children of the layout
        children = cmds.layout('{}_layout'.format(option_menu), query=True, childArray=True)

        if children:
            for child in children:
                cmds.deleteUI(child)
        else:
            print("No children found to delete.")

        cmds.deleteUI('{}_layout'.format(option_menu))

    if check_global_dict() or reload == True:
        ### lets figure out how many llegs are created
        limb_amount = limb_number

        limb_layout = cmds.gridLayout('{}_layout'.format(option_menu) ,numberOfColumns=limb_amount + 1, cellWidthHeight=(100 / (limb_amount + 1), 75),
                                      parent='{}_layout_frame'.format(option_menu))



        for i in range(limb_amount):
            create_button(option_menu,i)

            """vertical_label = '\n'.join('leg0{}'.format(i))
            print('lleg0{}'.format(i+1))
            cmds.button('lleg0{}'.format(i) , label='{}'.format(vertical_label), height=75, parent='lleg_layout',
                        command=lambda x: lleg_ui(limb_name='leg0{}'.format(i+1)))"""


    else:
        limb_layout = cmds.gridLayout( '{}_layout'.format(option_menu) ,numberOfColumns=2, cellWidthHeight=(50, 75), parent='{}_layout_frame'.format(option_menu))
        vertical_label = '\n'.join('{}1'.format(option_menu))
        button01 = cmds.button(label=vertical_label, height=75, parent=limb_layout ,
                    command=lambda x: lleg_ui(limb_name = '{}1'.format(option_menu)))
        button02 = cmds.button(label='', enable=False, height=75, parent=limb_layout)


def create_button(option_menu,i):
    vertical_label = '{}{}'.format(option_menu,i+1)  # This matches your print statement logic
    # Create the button with the correct label and the correct limb_name
    if option_menu == 'lleg':
        cmds.button('{}{}'.format(option_menu,i+1), label=vertical_label, height=75, parent='{}_layout'.format(option_menu),
                    command=lambda x: lleg_ui(limb_name='{}{}'.format(option_menu,i+1)))

def limb_option_menu_change( option_menu = None ,selected_value = None):

    build_layout(option_menu = option_menu,grid_layout='lleg_layout_frame', reload=True, limb_number=int(selected_value))
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
    json_file_name = cmds.textField(height=30, text='file name', parent=data_row_general_seg_01)

    # Character name
    cmds.text(align='center', height=30, label='character name:', parent=data_row_general_seg_01)
    char_name = cmds.textField(height=30, text='', parent=data_row_general_seg_01)



    ###########################################################

    data_row_general_seg_02 = cmds.rowColumnLayout(numberOfColumns=1,
                                           columnWidth=[(1, 500)],
                                           columnOffset=[(1, 'both', 5)],
                                           columnAlign=[(1, 'left')],
                                           parent=data_frame_general, rowSpacing=[1,5])
    # Lets calculate the height of the character
    cmds.button(label='FILE MANAGEMENT (Save,Load, Delete)', parent=data_row_general_seg_02, command=lambda x: ScrollListUi())
    cmds.button(label='Generate Height guide', parent=data_row_general_seg_02,command=lambda x: utili.generate_height_guides())

    type_rig_option_menu = option_menu = cmds.optionMenu(label='Type of rig', parent=data_row_general_seg_02)
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

    option_menu = cmds.optionMenu(label='larm ',parent= data_row_general_seg_03)
    cmds.menuItem(label="1")
    cmds.menuItem(label="2")
    cmds.menuItem(label="3")

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
        (lleg_option_menu.split('|')[-1]),cmds.optionMenu(lleg_option_menu, q=True, v=True)))

    rleg_option_menu = cmds.optionMenu('rleg',label='rleg', parent=data_row_general_seg_03)
    cmds.menuItem(label="1")
    cmds.menuItem(label="2")
    cmds.menuItem(label="3")

    # this trigger a function call any time we changge something in the option menu
    cmds.optionMenu(rleg_option_menu, e=True, cc=lambda *args: limb_option_menu_change((rleg_option_menu.split('|')[-1]),
                                                                                     cmds.optionMenu(rleg_option_menu,
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
                                             parent=data_frame_limbview, rowSpacing=[1, 5])

    cmds.button(label='', enable=False, height=25, parent=hip_grid_layout)
    cmds.button(label='', enable=False, height=25, parent=hip_grid_layout)
    cmds.button(label='HIP (1)', height=25, parent=hip_grid_layout ,
                command=lambda x: hip_ui())
    cmds.button(label='', enable=False, height=25, parent=hip_grid_layout)
    cmds.button(label='', enable=False, height=25, parent=hip_grid_layout)
    #########

    leg_grid_rowColumnlayout = cmds.rowColumnLayout( 'lleg_grid_rowColumnlayout' ,numberOfColumns=5,
                                           columnWidth=[(1, 100), (2, 100), (3, 100), (4, 100), (5, 100)],
                                           columnOffset=[(1, 'both', 2), (2, 'both', 2), (3, 'both', 2),
                                                         (4, 'both', 2), (5, 'both', 2)],
                                           columnAlign=[(1, 'left'), (2, 'left'), (3, 'left'), (4, 'left'),
                                                        (5, 'left')],
                                           parent=data_frame_limbview, rowSpacing=[1, 5])

    cmds.button(label='', enable=False, height=75, parent=leg_grid_rowColumnlayout)

    rleg_gridLayout_frame = cmds.gridLayout('rleg_layout_frame', numberOfColumns=1, cellWidthHeight=(100, 75),
                                            parent=leg_grid_rowColumnlayout)
    rleg_layout = cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(50, 75), parent=rleg_gridLayout_frame)
    cmds.button(label='', enable=False, height=75, parent=rleg_layout)
    cmds.button(label='R_LEG', height=75, parent=rleg_layout ,
                command=lambda x: constructor_limb_selected(limb_selected = 'rleg'))

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

    build_layout(option_menu = 'lleg',grid_layout = lleg_gridLayout_frame)


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



    def check_global_dict():
        return "global_dict" in globals()


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
                                                columnWidth=[(1, 400), (2, 100)],
                                                columnOffset=[(1, 'both', 5), (2, 'both', 5)],
                                                columnAlign=[(1, 'center'), (2, 'center')],
                                                parent='selected_grid', rowSpacing=[1, 5])



            cmds.button(label='{}'.format('Generate COG Guide'), height=25, parent=data_row_hip,
                command=lambda x: controller_hip_guide())
            cmds.button(label='{}'.format('Save'), height=25, parent=data_row_hip)

            cmds.button(label='{}'.format('Generate Jnt Guide'), height=25, parent=data_row_hip,
                        command=lambda x: controller_hip_guide())
            cmds.button(label='{}'.format('Save'), height=25, parent=data_row_hip)



    def controller_hip_guide(root_grp = None , isForGame = None):

        group_value = cmds.textField(root_grp, query=True, text=True)
        selected_item = cmds.optionMenu(isForGame, query=True, value=True)

        print(group_value)
        print(selected_item)

        if selected_item:
            for i in range(1,3):
                print('{}{:02d}'.format(group_value,i))
        else:
            print('nothing')

            sphere_name = cmds.sphere(name='hip_guide', r=1)[0]
            shader_name = create_shader_guide()
            # Step 5: Assign the material to the sphere
            cmds.select(sphere_name)
            cmds.hyperShade(assign='{}'.format(shader_name))

            distance_value = cmds.getAttr('heightDistance.distance') / 2
            cmds.move(0, distance_value, 0, sphere_name)
            annotate = cmds.annotate(sphere_name, tx='hip', p=(0, distance_value, 0))
            cmds.parent(annotate, sphere_name)
            # cmds.rename(annotate, "hip_annotation")
            cmds.setAttr(annotate + '.overrideEnabled', 1)
            cmds.setAttr(annotate + '.overrideColor', 6)


    def create_shader_guide():
        shader_name = "shader_guide"

        # Check if the shader already exists
        if cmds.objExists(shader_name):
            return shader_name  # Return the name if it already exists

        # Create the Lambert shader
        material_name = cmds.shadingNode('lambert', asShader=True)
        cmds.rename(material_name, shader_name)

        # Set the color of the shader
        cmds.setAttr(f"{shader_name}.color", 1, 0.3921, 0.4232, type="double3")  # Specific color

        return shader_name  # Return the name of the newly created shader

    def torso_ui():
        if constructor_limb_selected('torso') == False:

            data_row_torso = cmds.rowColumnLayout(numberOfColumns=2,
                                                           columnWidth=[(1, 100), (2, 400)],
                                                           columnOffset=[(1, 'both', 5), (2, 'both', 5)],
                                                           columnAlign=[(1, 'center'), (2, 'center')],
                                                           parent='selected_grid', rowSpacing=[1, 5])



            cmds.text(align='center', height=30, label='number of spine:', parent=data_row_torso)
            #cmds.text(align='center', height=30, label='number of spine:', parent=data_row_torso)
            int_field_name = cmds.intField(minValue=3, maxValue=5, value=3,step=1, parent=data_row_torso )

            data_row_torso01 = cmds.rowColumnLayout(numberOfColumns=2,
                                                  columnWidth=[(1, 400), (2, 100)],
                                                  columnOffset=[(1, 'both', 5), (2, 'both', 5)],
                                                  columnAlign=[(1, 'center'), (2, 'center')],
                                                  parent='selected_grid', rowSpacing=[1, 5])



            cmds.button(label='{}'.format('Generate torso Guides'), height=25, parent=data_row_torso01)
            cmds.button(label='{}'.format('Update'), height=25, parent=data_row_torso01)

            cmds.button(label='{}'.format('Generate torso jnt'), height=25, parent=data_row_torso01)
            cmds.button(label='{}'.format('Update'), height=25, parent=data_row_torso01)

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
        cmds.button(label='Save', parent=jsonload_btn_gridl, command=lambda x: _nested_dict_instance.SaveDictionary())
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