import maya.cmds as cmds

import pyRigging.autoTentacles as autoTentacles
import importlib
importlib.reload(autoTentacles)

### open windows
### select center main joint
### we will create a locator in the center to rotate the same sctructure over and over
### ask to add cluster as guides
### define mid and las ctroller and how many tentacles, and how many deggress for each tentacles.

def tentacle_ui():
    if cmds.window('TentacleToolUI', exists=True):
        cmds.deleteUI('TentacleToolUI')
    window = cmds.window('TentacleToolUI', title='Tentacle Tool', width=503,
                         height=543)
    main_layout = cmds.columnLayout(adjustableColumn=True)
    data_dict = build_data_frame(window, main_layout)

    # add build/close buttons
    button_grid(window, main_layout,data_dict)
    cmds.showWindow()
def build_data_frame(window, main_layout):
    data_frame = cmds.frameLayout(label='Build Data', width=500, height=210,
                                  collapsable=True, parent=main_layout)
    data_row = cmds.rowColumnLayout(numberOfColumns=3,
                                    columnWidth = [(1,100),(2,300),(3,100)] ,columnOffset=[(1, 'both', 5), (2, 'both', 0),
                                             (3, 'both', 5)],
                                    parent=data_frame , rowSpacing = [1,5] )
    cmds.separator( height=2, style = 'none', parent=data_row)
    cmds.separator(height=2, style = 'none', parent=data_row)
    cmds.separator(height=2, style = 'none', parent=data_row)

    #cmds.text(label='Variables', align  = 'left', font= 'boldLabelFont',height = 30, parent =data_row)
    #cmds.text(label='Define', align  = 'left', font= 'boldLabelFont',height = 30, parent =data_row)
    #cmds.text(label='Load', align  = 'left', font= 'boldLabelFont',height = 30, parent =data_row)
#character name
    cmds.text(align  = 'center' , height = 30, label ='character name', parent = data_row)
    names = cmds.textField(height=30,text = 'Max', parent=data_row)
    cmds.button(label='load selected', height=30, parent = data_row)
#main joint
    cmds.text(align='center', height=30, label='main joint', parent=data_row)
    joint = cmds.textField(height=30,text = 'center_jnt' , parent=data_row)
    cmds.button(label='load selected', height=30, parent=data_row)
#spacing %
    cmds.text(align='center', height=30, label='spacing %', parent=data_row)
    spacing =cmds.textField(height=30,text = '45' , parent=data_row)
    cmds.button(label='load selected', height=30, parent=data_row)
# mid ik %
    cmds.text(align='center', height=30, label='mid ik pos', parent=data_row)
    midpos = cmds.textField(height=30,text = '7' , parent=data_row)
    cmds.button(label='load selected', height=30, parent=data_row)
# end ik %
    cmds.text(align='center', height=30, label='end ik pos', parent=data_row)
    lastpos = cmds.textField(height=30,text = '14' , parent=data_row)
    cmds.button(label='load selected', height=30, parent=data_row)

    #cmds.separator( height=40, style='out' , parent=data_row)
    data_frame2 = cmds.frameLayout(label='Build List', width=500, height=120,
                                  collapsable=True, parent=main_layout)

    data_rowlist = cmds.rowColumnLayout(numberOfColumns=3,
                                    columnWidth=[(1, 100), (2, 300), (3, 100)],
                                    columnOffset=[(1, 'both', 5), (2, 'both', 0)],
                                    parent=data_frame2, rowSpacing = [2,5] )

    cmds.separator( height=2, style = 'none', parent=data_rowlist)
    cmds.separator(height=2, style = 'none', parent=data_rowlist)
    cmds.separator(height=2, style = 'none', parent=data_rowlist)

    cmds.text(align='center', height=30, label='Guides List', parent=data_rowlist)
    listGuide = cmds.textScrollList(numberOfRows=5, allowMultiSelection=True,
                        selectItem='six', showIndexedItem=4 , parent=data_rowlist, append=['cluster_handle_1'
,'cluster_handle_2'
,'cluster_handle_3'
,'cluster_handle_4'
,'cluster_handle_5'
,'cluster_handle_6'
,'cluster_handle_7'
,'cluster_handle_8'
,'cluster_handle_9'
,'cluster_handle_10'
,'cluster_handle_11'
,'cluster_handle_12'
,'cluster_handle_13'
,'cluster_handle_14'
,'cluster_handle_15'
,'cluster_handle_16'
,'cluster_handle_17'
,'cluster_handle_18'
,'cluster_handle_19'
,'cluster_handle_20'
,'cluster_handle_21'
,'cluster_handle_22'])
    cmds.button(label='load selected', height=30, parent=data_rowlist,command=lambda x: load_sel(listGuide))


    #append cmds.textScrollList(listGuide, edit=True, append = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
                                                            # 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen'] )
    #query listGuide2 = cmds.textScrollList(listGuide, query=True , allItems = True)

    #remove cmds.textScrollList(listGuide,edit=True, removeAll=True)
    return_dict = {'name': names,
                   'mainjoint': joint,
                   'spacing': spacing,
                   'midpos': midpos,
                   'lastpos': lastpos,
                   'listguide': listGuide
                   }

    return return_dict

def load_sel(text_field):
    sel = cmds.ls(sl=True)
    if len(sel):
        #cmds.textField(text_field, edit=True, text=sel[0])
        cmds.textScrollList(text_field, edit=True, append=sel )


def button_grid(window, main_layout, command_dict):
    btn_col = cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, 500)],
                                   columnOffset=[(1, 'both', 0)],
                                   parent=main_layout)
    grid_layout = cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(250, 40),
                                  parent=btn_col)
    cmds.button(label='Build Tentacles', height=40, parent=grid_layout,
                            command=lambda x: build_tentacles_cmd( command_dict )
                            )
    cmds.button(label='Close', height=40, parent=grid_layout,
                            command=lambda x: cmds.deleteUI(window)
                            )

def build_tentacles_cmd(dictionary):
    #lets add some validations before sending everything
    name = cmds.textField(dictionary['name'], query=True,
                                  text=True)
    mainjoint = cmds.textField(dictionary['mainjoint'], query=True,
                         text=True)
    spacing = cmds.textField(dictionary['spacing'], query=True,
                          text=True)
    midpos = cmds.textField(dictionary['midpos'], query=True,
                          text=True)
    lastpos = cmds.textField(dictionary['lastpos'], query=True,
                          text=True)
    listGuide = cmds.textScrollList(dictionary['listguide'], query=True, allItems=True)


    autoTentacles.tentacleBuild(name = name,mainjoint = mainjoint, spacing = spacing, midpos = midpos, lastpos = lastpos
                                ,listGuide = listGuide  )

