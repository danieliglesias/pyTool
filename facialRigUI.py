import maya.cmds as cmds
import os
import json

import pyTool.facialRig as face
import pyTool.utilities as utili
import importlib
importlib.reload(face)
importlib.reload(utili)

### open windows
### select center main joint
### we will create a locator in the center to rotate the same sctructure over and over
### ask to add cluster as guides
### define mid and las controller and how many tentacles, and how many deggress for each tentacles.

def face_ui():
    if cmds.window('FaceToolUI', exists=True):
        cmds.deleteUI('FaceToolUI')
    window = cmds.window('FaceToolUI', title='Face Tool', width=500,
                         height=543)
    main_layout = cmds.columnLayout(adjustableColumn=True)
    data_dict = build_data_frame(window, main_layout)

    # add build/close buttons
    #button_grid(window, main_layout,data_dict)
    cmds.showWindow()


def build_data_frame(window, main_layout):
    ##############################################################################################################################
    ##GENERAL INFORMATION FOR THE CHARACTER
    #this will be used all over the tool
    data_frame_general = cmds.frameLayout(label='General parameters', width=500,
                                           collapsable=True, parent=main_layout)

    data_row_general = cmds.rowColumnLayout(numberOfColumns=2,
                                    columnWidth=[(1, 150), (2, 350)],
                                    columnOffset=[(1, 'left', 5), (2, 'left', 0)],
                                    columnAlign=[(1, 'left'), (2, 'center')],
                                    parent=data_frame_general, rowSpacing=[1, 5])
    #character name
    cmds.text(align='center', height=30, label='character name ***', parent=data_row_general)
    general_name = cmds.textField(height=30, text='Max', parent=data_row_general)

    ###########################################################
    baseobject = cmds.rowColumnLayout(numberOfColumns=3,
                                      columnWidth=[(1, 100), (2, 250), (3, 150)],
                                      columnOffset=[(1, 'both', 5), (2, 'both', 0),
                                                    (3, 'both', 5)],
                                      columnAlign=[(1, 'left'), (2, 'center'), (3, 'right')],
                                      parent=data_frame_general, rowSpacing=[1, 5])
    # This is the main object from the face rig will be build.
    cmds.text(align='left', height=30, label='Base object', parent=baseobject)
    base_objectname = cmds.textField(height=20, text='center_jnt', parent=baseobject)
    cmds.button(label='load object', parent=baseobject,
                command=lambda x: controller_create_mouth_plane_btn(general_name=general_name))

    ###########################################################
    # here we want to specify the if guides are save base on guide or joints

    guide_level = cmds.rowColumnLayout(numberOfColumns=2,
                                       columnWidth=[(1, 150), (2, 350)],
                                       columnOffset=[(1, 'left', 5), (2, 'left', 0)],
                                       columnAlign=[(1, 'left'), (2, 'center')],
                                       parent=data_frame_general, rowSpacing=[1, 5])

    cmds.text(align='center', height=30, label='save level', parent=guide_level)
    cmds.checkBoxGrp('row_checkbox_guide_level', numberOfCheckBoxes=3, columnAlign3=['right', 'right', 'right'],
                     labelArray3=['guides', 'joint', 'selected'],
                     parent=guide_level)
    ###########################################################
    guide_load = cmds.rowColumnLayout(numberOfColumns=3,
                                      columnWidth=[(1, 100), (2, 250), (3, 150)],
                                      columnOffset=[(1, 'both', 5), (2, 'both', 0),
                                                    (3, 'both', 5)],
                                      columnAlign=[(1, 'left'), (2, 'center'), (3, 'right')],
                                      parent=data_frame_general, rowSpacing=[1, 5])
    # guide load
    char_name = cmds.textField(general_name, query=True, text=True)

    # load save position
    cmds.text(align='left', height=30, label='Plane Pos', parent=guide_load)
    listPos_faceguides = cmds.textScrollList(numberOfRows=5, allowMultiSelection=False
                                             , showIndexedItem=4, parent=guide_load)
    utili.file_manage(section_dir='base/', action='show', field=listPos_faceguides)

    listPos_faceguides_btn = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(150, 25), parent=guide_load)
    cmds.button(label='load selected', parent=listPos_faceguides_btn,
                command=lambda x: controller_load_guides(listPos=listPos_faceguides))

    cmds.button(label='Save', parent=listPos_faceguides_btn,
                command=lambda x: controller_save_to_json_faceguides(general_name=char_name, checkbox='row_checkbox_guide_level'))
    cmds.button(label='delete', parent=listPos_faceguides_btn,
                command=lambda x: controller_delete_eyebrow_save(listPos=listPos_faceguides))
    cmds.button(label='Refresh list', parent=listPos_faceguides_btn,
                command=lambda x: utili.file_manage(section_dir='base/', action='show', field=listPos_faceguides))



    ##########################################################################
    #General face guides
    grid_layoutgeneral = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(500, 25), parent=data_frame_general)
    cmds.button(label='create outliner structure (TBA)', height=25, parent=grid_layoutgeneral,
                command=lambda x: controller_build_struct_outliner(general_name = general_name))
    cmds.button(label='create basic face guide', height=25, parent=grid_layoutgeneral,
                command=lambda x: controller_build_faceguide(general_name = char_name, base_obj = base_objectname))
    cmds.button(label='Build basic structure', height=25, parent=grid_layoutgeneral,
                command=lambda x: controller_build_facebasic(general_name = char_name))

    ##############################################################################################################################
    data_frame_eyebrows = cmds.frameLayout(label='Build Eyebrows', width=500,
                                  collapsable=True, parent=main_layout)


    data_row = cmds.rowColumnLayout(numberOfColumns=3,
                                    columnWidth = [(1,80),(2,270),(3,150)] ,
                                    columnOffset=[(1, 'both', 5), (2, 'both', 0),
                                             (3, 'both', 5)],
                                    columnAlign=[(1, 'left'), (2, 'center'), (3, 'right')],
                                    parent=data_frame_eyebrows , rowSpacing = [1,5] )

    # load surface
    cmds.text(align='left', height=30, label='side', parent=data_row)
    cmds.checkBoxGrp('side_checkbox',numberOfCheckBoxes=2, labelArray2=['L', 'R'], parent=data_row )

    cmds.button(label='Load Surface Plane', height=30, parent=data_row,
                command=lambda x: controllerLoadSurfacePlaneBtn(general_name = general_name, checkbox = 'side_checkbox'))


    #load save position
    cmds.text(align='left', height=30, label='Plane Pos', parent=data_row)
    listPos_eyebrow = cmds.textScrollList(numberOfRows=5, allowMultiSelection=False
                                  , showIndexedItem=4, parent=data_row)
    utili.file_manage(section_dir='eyebrows/', action='show', field=listPos_eyebrow)

    botton_layout = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(150, 25),parent=data_row)
    cmds.button(label='load selected', parent=botton_layout ,command=lambda x: controllerLoadPositionBtn(listPos = listPos_eyebrow))
    char_name = cmds.textField(general_name, query=True,text=True)
    cmds.button(label='Save', parent=botton_layout, command=lambda x: controller_save_to_json(general_name = general_name,checkbox = 'side_checkbox'))
    cmds.button(label='delete', parent=botton_layout,command=lambda x: controller_delete_eyebrow_save(listPos = listPos_eyebrow))
    cmds.button(label='Refresh list', parent=botton_layout,command=lambda x: utili.file_manage(section_dir =  'eyebrows/' ,action = 'show',field=listPos_eyebrow))

    #
    grid_layouteyebrow = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(500, 40),parent=data_frame_eyebrows)
    cmds.checkBoxGrp('row_checkbox', numberOfCheckBoxes=3, label='Joint Rows', labelArray3=['One', 'Two', 'Three'] ,parent=grid_layouteyebrow)
    cmds.button(label='Build eyebrow', height=40, parent=grid_layouteyebrow,command=lambda x: controller_build_eyebrow(general_name = general_name,
                                                                                                                       sidecheckbox = 'side_checkbox', rowcheckbox = 'row_checkbox'))
    cmds.button(label='Mirror opposite side', height=40, parent=grid_layouteyebrow,command=lambda x: controller_eyebrow_mirror(general_name = general_name,
                                                                                                                               sidecheckbox = 'side_checkbox' ))




    ##############################################################################################################################
    data_frame_eyelid = cmds.frameLayout(label='Build eyelid', width=500,
                                  collapsable=True,collapse = True, parent=main_layout)

    data_row_eyelid_general = cmds.rowColumnLayout(numberOfColumns=2,
                                            columnWidth=[(1, 150), (2, 350)],
                                            columnOffset=[(1, 'left', 5), (2, 'left', 0)],
                                            columnAlign=[(1, 'left'), (2, 'center')],
                                            parent=data_frame_eyelid, rowSpacing=[1, 5])

    # number of edge loops
    cmds.text(align='left', height=30, label='eye edge loops ***', parent=data_row_eyelid_general)
    eyelid_edgeloop = cmds.intField(height=30 ,parent=data_row_eyelid_general)



    data_row2 = cmds.rowColumnLayout(numberOfColumns=3,
                                    columnWidth=[(1,80),(2,270),(3,150)],
                                    columnOffset=[(1, 'both', 5), (2, 'both', 0),
                                                  (3, 'both', 5)],
                                    columnAlign=[(1, 'left'), (2, 'center'), (3, 'right')],
                                    parent=data_frame_eyelid, rowSpacing=[1, 5])

    # character name
    cmds.text(align='left', height=50, label='side', parent=data_row2)
    cmds.checkBoxGrp('side_checkbox_load_eyelid_guide',numberOfCheckBoxes=2, labelArray2=['L', 'R'],parent=data_row2)

    eyelidguides = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(150, 25), parent=data_row2)
    cmds.button(label='load eyelid guide', parent=eyelidguides,
                command=lambda x: controllerLoadEyelidGuideBtn(general_name = general_name,edgeloop = eyelid_edgeloop,side_checkbox = 'side_checkbox_load_eyelid_guide'))
    cmds.button(label='Create curve', parent=eyelidguides,
                command=lambda x: controllerCreateCurveBtn(general_name=general_name, edgeloop=eyelid_edgeloop,
                                                               side_checkbox='side_checkbox_load_eyelid_guide'))

    cmds.text(align='left', height=30, label='Curve cv pos', parent=data_row2)
    listpos_eyelid = cmds.textScrollList(numberOfRows=5, allowMultiSelection=False
                                  , showIndexedItem=4, parent=data_row2)
    utili.file_manage(section_dir='eyelid/', action='show', field=listpos_eyelid)

    bottonEyelid = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(150, 25),parent=data_row2)
    cmds.button(label='load selected', parent=bottonEyelid,command=lambda x: controller_load_from_json_eyelid(general_name = general_name,listPos = listpos_eyelid))
    char_name = cmds.textField(general_name, query=True, text=True)
    cmds.button(label='Save', parent=bottonEyelid, command=lambda x: controller_save_to_json_eyelid(general_name = general_name,
                                                                                                    checkbox = 'side_checkbox_load_eyelid_guide'))
    cmds.button(label='Delete', parent=bottonEyelid, command=lambda x: face.savePlanePosition(name=char_name))
    cmds.button(label='Refresh list', parent=bottonEyelid, command=lambda x: utili.file_manage(section_dir='eyelid/', action='show', field=listpos_eyelid))


    grid_layout_eyelid = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(500, 25),parent=data_frame_eyelid)
    cmds.checkBoxGrp('row_checkbox_guide_number', numberOfCheckBoxes=2, label='Number guide', labelArray2=['One', 'L and R side'],
                     parent=grid_layout_eyelid)

    cmds.button(label='Build eyelid', height=40, parent=grid_layout_eyelid,command=lambda x:  controllerCreateEyeLidBtn(general_name=general_name,
                                                                                                                        edgeloop=eyelid_edgeloop,checkbox='side_checkbox_load_eyelid_guide',checkbox_guides = 'row_checkbox_guide_number'))
    cmds.button(label='Mirror opposite side', height=40, parent=grid_layout_eyelid,command=lambda x: controllerMirrorEyeLidBtn(general_name=general_name, edgeloop=eyelid_edgeloop,checkbox='side_checkbox_load_eyelid_guide'))

    grid_layout_eyelid2 = cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(250, 25), parent=grid_layout_eyelid)

    cmds.button(label='Right guide', height=25, parent=grid_layout_eyelid2,command=lambda x: controllerMirrorEyeLidBtn(general_name=general_name, edgeloop=eyelid_edgeloop,checkbox='side_checkbox_load_eyelid_guide'))
    cmds.button(label='Left guide', height=25, parent=grid_layout_eyelid2,command=lambda x: controllerMirrorEyeLidBtn(general_name=general_name, edgeloop=eyelid_edgeloop,checkbox='side_checkbox_load_eyelid_guide'))



    data_row_guide_detail = cmds.rowColumnLayout(numberOfColumns=3,
                                     columnWidth=[(1, 80), (2, 270), (3, 150)],
                                     columnOffset=[(1, 'both', 5), (2, 'both', 0),
                                                   (3, 'both', 5)],
                                     columnAlign=[(1, 'left'), (2, 'center'), (3, 'right')],
                                     parent=data_frame_eyelid, rowSpacing=[1, 5])

    cmds.text(align='left', height=30, label='Curve cv pos', parent=data_row_guide_detail)
    listpos_eyelid_guides = cmds.textScrollList(numberOfRows=5, allowMultiSelection=False
                                         , showIndexedItem=4, parent=data_row_guide_detail)
    utili.file_manage(section_dir='eyelid/guide/', action='show', field=listpos_eyelid_guides)

    bottonEyelid_guide_detail = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(150, 25), parent=data_row_guide_detail)
    cmds.button(label='load selected', parent=bottonEyelid_guide_detail,
                command=lambda x: controller_load_guidenumbers_from_json_eyelid(general_name = general_name, listPos= listpos_eyelid_guides))


    char_name = cmds.textField(general_name, query=True, text=True)
    cmds.button(label='Save', parent=bottonEyelid_guide_detail,
                command=lambda x: controller_save_to_json_eyelidguides(general_name=general_name))
    cmds.button(label='Delete', parent=bottonEyelid_guide_detail, command=lambda x: face.savePlanePosition(name=char_name))
    cmds.button(label='Refresh list', parent=bottonEyelid_guide_detail,
                command=lambda x: utili.file_manage(section_dir='eyelid/guide/', action='show', field=listpos_eyelid_guides))

    ##############################################################################################################################
    data_frame_eyeball = cmds.frameLayout(label='Build eyeball system', width=500,
                                         collapsable=True,collapse = True, parent=main_layout)
    data_row3 = cmds.rowColumnLayout(numberOfColumns=3,
                                     columnWidth=[(1, 100), (2, 200), (3, 200)],
                                     columnOffset=[(1, 'both', 5), (2, 'both', 0),
                                                   (3, 'both', 5)],
                                     columnAlign=[(1, 'left'), (2, 'center'), (3, 'right')],
                                     parent=data_frame_eyeball, rowSpacing=[1, 5])

    # character name
    cmds.text(align='left', height=30, label='side', parent=data_row3)
    cmds.checkBoxGrp('side_checkbox_eyeball', numberOfCheckBoxes=2, labelArray2=['L', 'R'], parent=data_row3)

    cmds.button(label='Build eyeball SYS', height=30, parent=data_row3,
                command=lambda x: controllerBuildEyeBallSysBtn(general_name=general_name, checkbox='side_checkbox_eyeball'))


    ##############################################################################################################################
    data_frame_socket = cmds.frameLayout(label='Build eye socket system', width=500,
                                          collapsable=True,collapse = True, parent=main_layout)
    data_row4 = cmds.rowColumnLayout(numberOfColumns=3,
                                     columnWidth=[(1, 100), (2, 200), (3, 200)],
                                     columnOffset=[(1, 'both', 5), (2, 'both', 0),
                                                   (3, 'both', 5)],
                                     columnAlign=[(1, 'left'), (2, 'center'), (3, 'right')],
                                     parent=data_frame_socket, rowSpacing=[1, 5])

    # side
    cmds.text(align='left', height=30, label='side', parent=data_row4)
    cmds.checkBoxGrp('side_checkbox_socket', numberOfCheckBoxes=2, labelArray2=['L', 'R'], parent=data_row4)
    cmds.separator(height=30, style = 'none', parent=data_row4)

    # size
    cmds.text(align='left', height=30, label='ctrl size', parent=data_row4)
    socket_size = cmds.intField(height=30 ,parent=data_row4)
    cmds.separator(height=30, style='none', parent=data_row4)



    grid_layout = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(500, 40),
                                  parent=data_frame_socket)



    cmds.floatFieldGrp('ctrl_vector_socket_move',height=30, numberOfFields=3, label='Move vector', extraLabel='unit',
                       value1=0, value2=0,value3=10, parent=grid_layout)
    cmds.button(label='Build Eyesocket system', height=40, parent=grid_layout,
                command=lambda x: controllerBuildEyeSocketSysBtn(general_name=general_name, checkbox='side_checkbox_socket',
                                                                 socketsize=socket_size,floatgrp = 'ctrl_vector_socket_move')
                )

##############################################################################################################################

    data_frame_mouth = cmds.frameLayout(label='Build mouth system', width=500,
                                              collapsable=True,collapse = True, parent=main_layout)
    data_row5 = cmds.rowColumnLayout(numberOfColumns=3,
                                     columnWidth=[(1, 100), (2, 250), (3, 150)],
                                     columnOffset=[(1, 'both', 5), (2, 'both', 0),
                                                   (3, 'both', 5)],
                                     columnAlign=[(1, 'left'), (2, 'center'), (3, 'right')],
                                     parent=data_frame_mouth, rowSpacing=[1, 5])
    #mouth edgeloops
    mouthguides_name = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(350, 25), parent=data_row5)
    cmds.text(align='left', height=30, label='guides/edgeloop', parent=mouthguides_name)
    cmds.separator(height=30, style='none', parent=mouthguides_name)

    mouthguides_field = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(350, 25), parent=data_row5)
    mouth_edgeloop = cmds.intField(height=20,value=10, parent=mouthguides_field)
    cmds.separator(height=30, style='none', parent=mouthguides_field)


    mouthguides2 = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(150, 25), parent=data_row5)
    cmds.button(label='create plane', parent=mouthguides2,
                command=lambda x: controller_create_mouth_plane_btn(general_name=general_name))
    cmds.button(label='create mouth guide', parent=mouthguides2,
                command=lambda x: controller_create_mouth_guides_btn(general_name=general_name, edgeloop=mouth_edgeloop))



    cmds.text(align='left', height=30, label='Curve cv pos', parent=data_row5)
    listpos_mouth = cmds.textScrollList(numberOfRows=5, allowMultiSelection=False
                                         , showIndexedItem=4, parent=data_row5)
    utili.file_manage(section_dir='mouth/', action='show', field=listpos_mouth)

    bottonMouth = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(150, 25), parent=data_row5)
    cmds.button(label='load selected', parent=bottonMouth,
                command=lambda x: controller_load_from_json_mouth(general_name = general_name, listPos= listpos_mouth))
    char_name = cmds.textField(general_name, query=True, text=True)
    cmds.button(label='Save', parent=bottonMouth,
                command=lambda x: controller_save_to_json_mouth(general_name=general_name,edgeloop=mouth_edgeloop))
    cmds.button(label='Delete', parent=bottonMouth, command=lambda x: face.savePlanePosition(name=char_name))
    cmds.button(label='Refresh list', parent=bottonMouth, command=lambda x: utili.file_manage(section_dir='mouth/', action='show', field=listpos_mouth))

    grid_layout_mouth = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(500, 40),
                                  parent=data_frame_mouth)

    cmds.checkBoxGrp('row_checkbox_mounth_detail', numberOfCheckBoxes=3, label='Control detail(TBA)', labelArray3=['Standar', 'level 2', 'level 3'],
                     parent=grid_layout_mouth)
    cmds.button(label='Build mouth system', height=40, parent=grid_layout_mouth,
                command=lambda x: controller_build_mouth_system_btn(general_name=general_name,edgeloop=mouth_edgeloop)
                )





    data_row6 = cmds.rowColumnLayout(numberOfColumns=3,
                                     columnWidth=[(1, 100), (2, 250), (3, 150)],
                                     columnOffset=[(1, 'both', 5), (2, 'both', 0),
                                                   (3, 'both', 5)],
                                     columnAlign=[(1, 'left'), (2, 'center'), (3, 'right')],
                                     parent=data_frame_mouth, rowSpacing=[1, 5])

    cmds.text(align='left', height=30, label='Guide Values', parent=data_row6)
    listpos_jay_guide= cmds.textScrollList(numberOfRows=5, allowMultiSelection=False
                                         , showIndexedItem=4, parent=data_row6)
    utili.file_manage(section_dir='mouth/guide/', action='show', field=listpos_jay_guide)

    botton_mouth2 = cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(150, 25), parent=data_row6)
    cmds.button(label='load selected', parent=botton_mouth2,
                command=lambda x: controller_load_values_from_json_mouthjawguide(general_name=general_name, listPos=listpos_jay_guide))
    char_name = cmds.textField(general_name, query=True, text=True)
    cmds.button(label='Save', parent=botton_mouth2,
                command=lambda x: controller_save_values_from_json_mouthjawguide(general_name=general_name))
    cmds.button(label='Delete', parent=botton_mouth2, command=lambda x: face.savePlanePosition(name=char_name))
    cmds.button(label='Refresh list', parent=botton_mouth2, command=lambda x: utili.file_manage(section_dir='mouth/guide/', action='show', field=listpos_mouth))

##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

def controllerLoadSurfacePlaneBtn(general_name = None , checkbox = None):

    if cmds.checkBoxGrp(checkbox, q=True, value1=True) == False and cmds.checkBoxGrp(checkbox, q=True, value2=True) == False:
        utili.errorMessage('Nothing was selected')
    else:
        if cmds.checkBoxGrp(checkbox, q=True, value1=True) == True and cmds.checkBoxGrp(checkbox, q=True, value2=True) == True:
            sides = ['l','r']
        elif cmds.checkBoxGrp(checkbox, q=True, value1=True) == True:
            sides = 'l'
        else:
            sides = 'r'
        name = cmds.textField(general_name, query=True, text=True)
        face.createEyebrowsPlane(name=name, sides=sides)
def controllerLoadPositionBtn(listPos = None):

    file_name = cmds.textScrollList(listPos, q=1, si=1)
    face.load_plane_position(file_name=file_name)


def controller_save_to_json(general_name = None,checkbox = None):
    if cmds.checkBoxGrp(checkbox, q=True, value1=True) == False and cmds.checkBoxGrp(checkbox, q=True, value2=True) == False:
        utili.errorMessage('Nothing was selected')
    else:
        if cmds.checkBoxGrp(checkbox, q=True, value1=True) == True and cmds.checkBoxGrp(checkbox, q=True, value2=True) == True:
            sides = ['l','r']
        elif cmds.checkBoxGrp(checkbox, q=True, value1=True) == True:
            sides = 'l'
        else:
            sides = 'r'
    name = cmds.textField(general_name, query=True, text=True)
    face.savePlanePosition(name = name ,side = sides)


def controller_delete_eyebrow_save(listPos = None):
    utili.errorMessage('Work in progress')



def controller_build_eyebrow(general_name = None,sidecheckbox = None, rowcheckbox = None):
    if cmds.checkBoxGrp(sidecheckbox, q=True, value1=True) == False and cmds.checkBoxGrp(sidecheckbox, q=True, value2=True) == False:
        utili.errorMessage('Nothing was selected from the side checkbox')
    elif cmds.checkBoxGrp(rowcheckbox, q=True, value1=True) == False and cmds.checkBoxGrp(rowcheckbox, q=True, value2=True) == False and cmds.checkBoxGrp(rowcheckbox, q=True, value3=True) == False:
        utili.errorMessage('Nothing was selected from the row checkbox')
    else:
        if cmds.checkBoxGrp(sidecheckbox, q=True, value1=True) == True and cmds.checkBoxGrp(sidecheckbox, q=True,value2=True) == True:
            sides = ['l', 'r']
        elif cmds.checkBoxGrp(sidecheckbox, q=True, value1=True) == True:
            sides = 'l'
        else:
            sides = 'r'
        name = cmds.textField(general_name, query=True, text=True)
        testlist = cmds.checkBoxGrp(rowcheckbox, q=True, valueArray3=True)

        if testlist.count(True) >=2:
            utili.errorMessage('You must select only one checkbox from the row checkbox')
        else:
            joint_row=(testlist.index(True)+1)
            face.createEyebrows(name=name, side= sides, joint_row=joint_row)

def controller_eyebrow_mirror(general_name = None,sidecheckbox = None ):

    if cmds.checkBoxGrp(sidecheckbox, q=True, value1=True) == False and cmds.checkBoxGrp(sidecheckbox, q=True, value2=True) == False:
        utili.errorMessage('Nothing was selected from the side checkbox')

    checklist = cmds.checkBoxGrp(sidecheckbox, q=True, valueArray2=True)
    if checklist.count(True) >= 2:
        utili.errorMessage('You must select only one checkbox from the row checkbox')
    else:
        side_val = (checklist.index(True) + 1)
        if side_val == 1:
            side_selected = 'l'
        else:
            side_selected = 'r'
        name = cmds.textField(general_name, query=True, text=True)

        face.mirrorEyebrowsPlane(name=name, side_selected=side_selected)

##############################################################################################################################

def controllerLoadEyelidGuideBtn(general_name = None,edgeloop = None,side_checkbox = None):
    name = cmds.textField(general_name, query=True, text=True)
    if cmds.checkBoxGrp(side_checkbox, q=True, value1=True) == False and cmds.checkBoxGrp(side_checkbox, q=True, value2=True) == False:
        utili.errorMessage('Nothing was selected from the side checkbox of load eyelid guide')
    if cmds.checkBoxGrp(side_checkbox, q=True, value1=True) == True and cmds.objExists('{}_l_eyeball_jnt'.format(name)) == False:
        utili.errorMessage('There is no eyeball jnt in the center of the eye named {}'.format('{}_l_eyeball_jnt'.format(name)))
    if cmds.checkBoxGrp(side_checkbox, q=True, value2=True) == True and cmds.objExists('{}_r_eyeball_jnt'.format(name)) == False:
        utili.errorMessage('There is no eyeball jnt in the center of the eye named {}'.format('{}_r_eyeball_jnt'.format(name)))

    testlist = cmds.checkBoxGrp(side_checkbox, q=True, valueArray2=True)

    if testlist.count(True) >= 2:
        sides = ['l', 'r']
        cluster = ['{}_l_eyeball_jnt'.format(name),'{}_r_eyeball_jnt'.format(name)]
    elif cmds.checkBoxGrp(side_checkbox, q=True, value1=True) == True:
        sides = 'l'
        cluster = '{}_l_eyeball_jnt'.format(name)
    else:
        sides = 'r'
        cluster = '{}_r_eyeball_jnt'.format(name)


    face.generateEyeLitGuide(name = name, side = sides,eye_guide = cluster)

def controllerCreateCurveBtn(general_name=None, edgeloop=None,side_checkbox=None):
    name = cmds.textField(general_name, query=True, text=True)
    if cmds.checkBoxGrp(side_checkbox, q=True, value1=True) == False and cmds.checkBoxGrp(side_checkbox, q=True, value2=True) == False:
        utili.errorMessage('Nothing was selected from the side checkbox of load eyelid guide')
    if cmds.checkBoxGrp(side_checkbox, q=True, value1=True) == True and (cmds.objExists('{}_l_eyesock_jnt'.format(name)) == False or cmds.objExists('{}_l_eyeball_jnt'.format(name)) == False):
        cmds.error('Must create a left cluster in the center of the eyes and in the socket')
    if cmds.checkBoxGrp(side_checkbox, q=True, value2=True) == True and (cmds.objExists('{}_r_eyesock_jnt'.format(name)) == False or cmds.objExists('{}_r_eyeball_jnt'.format(name)) == False):
        cmds.error('Must create a right cluster in the center of the eyes and in the socket')

    l_eye_guide = ['{}_l_eyesock_jnt'.format(name), '{}_l_eyeball_jnt'.format(name)]
    r_eye_guide = ['{}_r_eyesock_jnt'.format(name), '{}_r_eyeball_jnt'.format(name)]

    testlist = cmds.checkBoxGrp(side_checkbox, q=True, valueArray2=True)

    if testlist.count(True) >= 2:
        sides = ['l', 'r']

    elif cmds.checkBoxGrp(side_checkbox, q=True, value1=True) == True:
        sides = 'l'

    else:
        sides = 'r'


    face.createEyeLidCurve(name = name,l_eye_guide=l_eye_guide,r_eye_guide=r_eye_guide,side=sides)

def controller_save_to_json_eyelid(general_name=None, checkbox=None):
    if cmds.checkBoxGrp(checkbox, q=True, value1=True) == False and cmds.checkBoxGrp(checkbox, q=True,
                                                                                     value2=True) == False:
        utili.errorMessage('Nothing was selected')
    else:
        if cmds.checkBoxGrp(checkbox, q=True, value1=True) == True and cmds.checkBoxGrp(checkbox, q=True,
                                                                                        value2=True) == True:
            sides = ['l', 'r']
        elif cmds.checkBoxGrp(checkbox, q=True, value1=True) == True:
            sides = 'l'
        else:
            sides = 'r'


        name = cmds.textField(general_name, query=True, text=True)
        face.saveCurveCvPosition(name=name, side=sides)
        #post warning
        if cmds.objExists('{}_l_eyesock_jnt'.format(name)) == False or cmds.objExists('{}_l_eyeball_jnt'.format(name)) == False:
            cmds.error('Warning left eyesocket and eyeball does not exist')
        if cmds.objExists('{}_r_eyesock_jnt'.format(name)) == False or cmds.objExists('{}_r_eyeball_jnt'.format(name)) == False:
            cmds.error('Warning Right eyesocket and eyeball does not exist')
        if cmds.objExists('{}_l_eyeball_grp'.format(name)) == False or cmds.objExists('{}_l_eyeball_grp'.format(name)) == False:
            cmds.error('Warning eyeball_grp does not exist')




def controller_load_from_json_eyelid(general_name = None, listPos= None):

    file_name = cmds.textScrollList(listPos, q=1, si=1)

    if not file_name:
        utili.errorMessage('nothing was selected')
        cmds.error('nothing was selected')

    if len(file_name) > 1:
        utili.errorMessage('More than one object selected')
        cmds.error('More than one object selected')

    name = cmds.textField(general_name, query=True, text=True)
    face.loadCurvePosition(name = name ,file_name = file_name)

def controllerCreateEyeLidBtn(general_name=None, edgeloop=None,checkbox=None,checkbox_guides = None):
    name = cmds.textField(general_name, query=True, text=True)

    if cmds.checkBoxGrp(checkbox_guides, q=True, value1=True) == False and cmds.checkBoxGrp(checkbox_guides, q=True,
                                                                                     value2=True) == False:
        utili.errorMessage('No guide especification was selected.')
    else:
        if cmds.checkBoxGrp(checkbox, q=True, value1=True) == False and cmds.checkBoxGrp(checkbox, q=True,
                                                                                            value2=True) == True:
            spread = 'side'
        else:
            spread = 'normal'



    if cmds.checkBoxGrp(checkbox, q=True, value1=True) == False and cmds.checkBoxGrp(checkbox, q=True,
                                                                                     value2=True) == False:
        utili.errorMessage('Nothing was selected')
    else:
        if cmds.checkBoxGrp(checkbox, q=True, value1=True) == True and cmds.checkBoxGrp(checkbox, q=True,
                                                                                        value2=True) == True:
            sides = ['l', 'r']
        elif cmds.checkBoxGrp(checkbox, q=True, value1=True) == True:
            sides = 'l'
        else:
            sides = 'r'

        edgeloops = cmds.intField(edgeloop, query=True, v=1)
        if edgeloops == 0:
            utili.errorMessage('You must introduce a number of edge loops')
        else:
            face.createEyeLid(name = name,side=sides,curve= None,edgeloop = int(edgeloops),spread_control = spread)

def controllerMirrorEyeLidBtn(general_name=None, edgeloop=None,checkbox=None):

    ##test change 11:43
    if cmds.checkBoxGrp(checkbox, q=True, value1=True) == False and cmds.checkBoxGrp(checkbox, q=True, value2=True) == False:
        utili.errorMessage('Nothing was selected from the side checkbox')

    checklist = cmds.checkBoxGrp(checkbox, q=True, valueArray2=True)
    if checklist.count(True) >= 2:
        utili.errorMessage('You must select only one checkbox from the row checkbox')
    else:
        side_val = (checklist.index(True) + 1)
        if side_val == 1:
            side_selected = 'l'
        else:
            side_selected = 'r'


    edgeloops = cmds.intField(edgeloop, query=True, v=1)

    if edgeloops == 0:
        utili.errorMessage('You must introduce a number of edge loops')
    else:
        name = cmds.textField(general_name, query=True, text=True)
        face.mirrorEyelid(name=name, mirror_side=side_selected, edgeloop=edgeloops)
        # post warning
        if cmds.objExists('{}_l_eyesock_jnt'.format(name)) == False or cmds.objExists(
                '{}_l_eyeball_jnt'.format(name)) == False:
            cmds.error('Warning left eyesocket and eyeball does not exist')
        if cmds.objExists('{}_r_eyesock_jnt'.format(name)) == False or cmds.objExists(
                '{}_r_eyeball_jnt'.format(name)) == False:
            cmds.error('Warning Right eyesocket and eyeball does not exist')
        if cmds.objExists('{}_l_eyeball_grp'.format(name)) == False or cmds.objExists(
                '{}_l_eyeball_grp'.format(name)) == False:
            cmds.error('Warning eyeball_grp does not exist')

def controllerBuildEyeBallSysBtn(general_name=None, checkbox= None):
    if cmds.checkBoxGrp(checkbox, q=True, value1=True) == False and cmds.checkBoxGrp(checkbox, q=True, value2=True) == False:
        utili.errorMessage('Nothing was selected')
    else:
        if cmds.checkBoxGrp(checkbox, q=True, value1=True) == True and cmds.checkBoxGrp(checkbox, q=True, value2=True) == True:
            sides = ['l','r']
        elif cmds.checkBoxGrp(checkbox, q=True, value1=True) == True:
            sides = 'l'
        else:
            sides = 'r'
        name = cmds.textField(general_name, query=True, text=True)
        face.createEyeballController(name=name, sides=sides)

def controllerBuildEyeSocketSysBtn(general_name=None, checkbox=None, socketsize=None,floatgrp = None):
    if cmds.checkBoxGrp(checkbox, q=True, value1=True) == False and cmds.checkBoxGrp(checkbox, q=True,value2=True) == False:
        utili.errorMessage('No side was selected')
    else:
        if cmds.checkBoxGrp(checkbox, q=True, value1=True) == True and cmds.checkBoxGrp(checkbox, q=True, value2=True) == True:
            sides = ['l','r']
        elif cmds.checkBoxGrp(checkbox, q=True, value1=True) == True:
            sides = 'l'
        else:
            sides = 'r'
        name = cmds.textField(general_name, query=True, text=True)
        size = cmds.intField(socketsize, query=True, v=1)
        vector = cmds.floatFieldGrp(floatgrp, query=True, v=1)


        count = 0
        for pos in vector:
            if pos > 0:
                count = count + 1
        if count > 1:
            utili.errorMessage('More than one axis its set, must be only one')
        else:
            for i,pos in enumerate(vector):
                if pos > 0 and i == 0:
                    facing = 'x'
                elif pos > 0 and i == 1:
                    facing = 'y'
                elif pos > 0 and i == 2:
                    facing = 'z'

        face.createEyeSocketCtrl(name=name, sides=sides, size=size, facing=facing,move = vector)


def controller_create_mouth_plane_btn(general_name=None):

    name = cmds.textField(general_name, query=True, text=True)
    face.createMouthPlane(name=name, u=1, v=1)

def controller_create_mouth_guides_btn(general_name=None, edgeloop=None):

    name = cmds.textField(general_name, query=True, text=True)
    edgeloops = cmds.intField(edgeloop, query=True, v=1)
    if edgeloops == 0 or not name:
        utili.errorMessage('You must introduce a number of edge loops for the mouth')
    else:

        face.generateMouthGuide(name = name, mouth_edgeloop = edgeloops)

def controller_save_to_json_mouth(general_name=None,edgeloop=None):

    name = cmds.textField(general_name, query=True, text=True)
    edgeloops = cmds.intField(edgeloop, query=True, v=1)

    print('la cantidad edgeloop es: {}'.format(edgeloops))
    #check for edgeloops number
    if edgeloops == 0:
        utili.errorMessage('You must introduce a number of edge loops for the mouth, to save their position')

    #check for guides if they all exist
    guide_list = []
    for sides in ('l', 'r'):
        for y in ('upp', 'low'):
            for x in range(0, edgeloops):
                if x == 0:
                    if 'c_{}_{:02d}_mouth_guide'.format(y, x) in guide_list:
                        continue
                    else:
                        if utili.objectExist('c_{}_{:02d}_mouth_guide'.format(y, x)):
                            guide_list.append('c_{}_{:02d}_mouth_guide'.format(y, x))
                else:
                    if x == edgeloops - 1 and y == 'low':
                        continue
                    if x == edgeloops - 1 and y == 'upp':
                        if utili.objectExist('{}_cor_{:02d}_mouth_guide'.format(sides, x)):
                            guide_list.append('{}_cor_{:02d}_mouth_guide'.format(sides, x))
                    else:
                        if utili.objectExist('{}_{}_{:02d}_mouth_guide'.format(sides,y,x)):
                            guide_list.append('{}_{}_{:02d}_mouth_guide'.format(sides,y,x))

    #check if the mouth plane exists
    if utili.objectExist('{}_mouth_surface'.format(name)):
        surface = '{}_mouth_surface'.format(name)

    if not surface and len(guide_list) == 0:
        utili.errorMessage('There is nothing to save')

    face.save_mouth_guide_position(name=name, guide_list = guide_list, surface = surface)

def controller_load_from_json_mouth(general_name = None, listPos= None):

    file_name = cmds.textScrollList(listPos, q=1, si=1)

    if not file_name:
        utili.errorMessage('nothing was selected')
        cmds.error('nothing was selected')

    if len(file_name) > 1:
        utili.errorMessage('More than one object selected')
        cmds.error('More than one object selected')

    name = cmds.textField(general_name, query=True, text=True)
    face.load_mouth_guide_position(name = name ,file_name = file_name)


def controller_build_mouth_system_btn(general_name=None,edgeloop=None):
    name = cmds.textField(general_name, query=True, text=True)
    edgeloops = cmds.intField(edgeloop, query=True, v=1)

    if not utili.objectExist('{}_facelow_jnt'.format(name)) or not utili.objectExist('{}_facejaw_jnt'.format(name)):
        utili.errorMessage('low_face_jnt or jaw_jnt does not exist, check basic structure on general parameters')
    if not utili.objectExist('{}_mouth_surface'.format(name)):
        utili.errorMessage('No nurb plane was created for the face')
    else:
        guide_list = []
        for sides in ('l', 'r'):
            for y in ('upp', 'low'):
                for x in range(0, edgeloops):
                    if x == 0:
                        if 'c_{}_{:02d}_mouth_guide'.format(y, x) in guide_list:
                            continue
                        else:
                            if utili.objectExist('c_{}_{:02d}_mouth_guide'.format(y, x)):
                                guide_list.append('c_{}_{:02d}_mouth_guide'.format(y, x))
                    else:
                        if x == edgeloops - 1 and y == 'low':
                            continue
                        if x == edgeloops - 1 and y == 'upp':
                            if utili.objectExist('{}_cor_{:02d}_mouth_guide'.format(sides, x)):
                                guide_list.append('{}_cor_{:02d}_mouth_guide'.format(sides, x))
                        else:
                            if utili.objectExist('{}_{}_{:02d}_mouth_guide'.format(sides, y, x)):
                                guide_list.append('{}_{}_{:02d}_mouth_guide'.format(sides, y, x))

        face.build_mouth_system(name=name, guide_list=guide_list, edgeloop=edgeloops)

def controller_load_values_from_json_mouthjawguide(general_name = None, listPos= None):

    file_name = cmds.textScrollList(listPos, q=1, si=1)

    if not file_name:
        utili.errorMessage('nothing was selected')
        cmds.error('nothing was selected')

    if len(file_name) > 1:
        utili.errorMessage('More than one object selected')
        cmds.error('More than one object selected')

    name = cmds.textField(general_name, query=True, text=True)
    face.load_mouth_jaw_guide_numbers(name=name, file_name=file_name)
def controller_save_values_from_json_mouthjawguide(general_name = None):
    name = cmds.textField(general_name, query=True, text=True)
    if utili.objectExist('{}_jaw_guide'.format(name)):
        face.save_mouth_jaw_guide_numbers(name=name, object='Max_jaw_guide')
    else:
        utili.errorMessage('jaw_guide does not exist')




def controller_load_guidenumbers_from_json_eyelid(general_name = None, listPos= None):

    file_name = cmds.textScrollList(listPos, q=1, si=1)

    if not file_name:
        utili.errorMessage('nothing was selected')
        cmds.error('nothing was selected')

    if len(file_name) > 1:
        utili.errorMessage('More than one object selected')
        cmds.error('More than one object selected')

    name = cmds.textField(general_name, query=True, text=True)
    face.load_eyelit_guide_numbers(name=name, file_name=file_name)


def controller_save_to_json_eyelidguides(general_name=None):
    name = cmds.textField(general_name, query=True, text=True)
    if utili.objectExist('{}_eyelid_guide'.format(name)):
        object_list = ['{}_eyelid_guide'.format(name)]
        face.save_eyelit_guide_numbers(name=name, object=object_list)
    elif utili.objectExist('{}_l_eyelid_guide'.format(name)) and utili.objectExist('{}_r_eyelid_guide'.format(name)):
        object_list = ['{}_l_eyelid_guide'.format(name),'{}_r_eyelid_guide'.format(name)]
        face.save_eyelit_guide_numbers(name=name, object=object_list)
    else:
        utili.errorMessage('No guides exist to save')


def controller_build_faceguide(general_name = None, base_obj = None):
    #name = cmds.textField(general_name, query=True, text=True)
    #obj = cmds.textField(base_obj, query=True, text=True)

    base_obj_name = cmds.textField(base_obj, query=True, text=True)
    print(base_obj_name)
    if not cmds.objExists(base_obj_name):
        utili.errorMessage('base object does not exist')
    else:
        face.build_face_guide(name = general_name ,base_object = base_obj_name)
def controller_build_facebasic(general_name = None):
    #name = cmds.textField(general_name, query=True, text=True)
    face.build_face_structure(name=general_name)

def controller_save_to_json_faceguides(general_name=None, checkbox=None):
    if (cmds.checkBoxGrp(checkbox, q=True, value1=True) == False and
            cmds.checkBoxGrp(checkbox, q=True, value2=True) == False and
            cmds.checkBoxGrp(checkbox, q=True, value3=True) == False):

        utili.errorMessage('Nothing was selected')
    else:
        if (cmds.checkBoxGrp(checkbox, q=True, value1=True) == True and
            cmds.checkBoxGrp(checkbox, q=True, value2=True) == False and
            cmds.checkBoxGrp(checkbox, q=True, value3=True) == False):
            face.save_mainstructure_guide(name=general_name, guide_type='guide')
        elif (cmds.checkBoxGrp(checkbox, q=True, value2=True) == True and
            cmds.checkBoxGrp(checkbox, q=True, value1=True) == False and
            cmds.checkBoxGrp(checkbox, q=True, value3=True) == False):
            face.save_mainstructure_guide(name=general_name, guide_type='joint')
        elif (cmds.checkBoxGrp(checkbox, q=True, value3=True) == True and
            cmds.checkBoxGrp(checkbox, q=True, value1=True) == False and
            cmds.checkBoxGrp(checkbox, q=True, value2=True) == False):
            face.save_mainstructure_guide(name=general_name, guide_type='selected')
        else:
            utili.errorMessage('More than one level of save is  selected')


def controller_load_guides(listPos=None):
    file_name = cmds.textScrollList(listPos, q=1, si=1)
    if not file_name:
        utili.errorMessage('nothing was selected')
        cmds.error('nothing was selected')

    elif len(file_name) > 1:
        utili.errorMessage('More than one object selected')
        cmds.error('More than one object selected')
    else:
        face.load_mainstructure_guide( file_name=file_name)


def controller_build_struct_outliner(general_name=None):
    char_name = cmds.textField(general_name, query=True, text=True)
    utili.build_struct_outliner(name=char_name)