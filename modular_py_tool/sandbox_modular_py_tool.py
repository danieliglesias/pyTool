import maya.cmds as cmds
import modular_py_tool.UiAutoRig as auto_rig_ui
import modular_py_tool.Utilities as utili
import importlib
import modular_py_tool.FileClass as FileClass
import modular_py_tool.auto_rig_torso as torso
import modular_py_tool.auto_rig_hip as hip
#from  pyTool.modular_py_tool.nested_dictionary import NestedDictionary as dict
import os
import json
import math
import sys

importlib.reload(auto_rig_ui)    
importlib.reload(utili)    
importlib.reload(FileClass)
importlib.reload(torso)
importlib.reload(hip)



auto_rig_ui.modular_ui()

totalCtrlPoint = 3
cmds.rebuildCurve('C_torso_curve_guide', ch=1, rpo=1, rt=0, end=1, kr=1, kcp=0, kep=1, kt=0, s=totalCtrlPoint, d=3, tol=0.01)


cv_curve_list = ['C_chest_BIND_guide','C_skips02_guide','C_skips02_guide1','C_skips01_guide','C_COG_BIND_guide']
positions = [cmds.xform(obj, q=True, ws=True, translation=True) for obj in cv_curve_list]
positions_fixed = [positions[0]] * 2 + positions + [positions[-1]] * 2
cmds.curve(d=3, p=positions_fixed, name='test')


curve_name = 'test'  # Replace with your curve name
mid_pos = utili.get_position_on_curve('C_torso_curve_guide', 0.66666)

print(mid_pos)


position = 2 +2
test= 1/(position-1)




for i in range(0, position):
    if i != 0 and i != (position-1):    
        print(i*test)





















    
############################################################

distance_shapes = cmds.ls(type='distanceDimShape')
dist_shape = distance_shapes[0]
test = cmds.getAttr('{}.distance'.format('heightDistanceShape'))

print(test)
distance = cmds.getAttr(heightDistance.heightDistanceShape.distance)
print(cmds.getAttr(heightDistanceShape.distance))




#get name of dictionaries
print(list(data.keys()))

#get name of subdisctionaries
print(list(data['torso01'].keys()))

#get name of subdisctionaries filter by %guide%
print([key for key in data['torso01'].keys() if 'guide' in key])

#here we get the specific position 
print(data['torso01']['guide1']['position'])



##### now building the disctionary back #####

guide1 = {
    "position": [1, 0, 0],
    "bone_ori": "XYZ",
    "parent": "hip01",
    "bone_name": "spine01_BIND"
}

guide2 = {
    "position": [1, 0, 0],
    "bone_ori": "XYZ",
    "parent": "Guide1",
    "bone_name": "spine02_BIND"
}

guide3 = {
    "position": [1, 0, 0],
    "bone_ori": "XYZ",
    "parent": "Guide2",
    "bone_name": "chest01_BIND"
}

# Create the 'general' sub-dictionary
general = {
    "parent": "??"
}

# Now, build the final nested dictionary for 'torso01'
torso01 = {
    "general": general,
    "guide1": guide1,
    "guide2": guide2,
    "guide3": guide3
}

# Repeat the same process for 'lfarm01'
lfarm01 = {
    "general": general,
    "guide1": guide1,
    "guide2": guide2,
    "guide3": guide3
}

# Combine 'torso01' and 'lfarm01' into a final nested dictionary
nested_dict = {
    "torso01": torso01,
    "lfarm01": lfarm01
}


##### MODIFY GLOBAL DISCTIONARY

def modify_position():
    global global_dict  # Optional if you're reassigning the whole dictionary
    global_dict['torso01']['guide1']['position'] = [2, 1, 0]  # Modify existing value

# Function to add a new key-value pair to the global dictionary
def add_new_guide():
    global global_dict  # Optional if you're reassigning the whole dictionary
    global_dict['torso01']['guide2'] = {
        "position": [0, 1, 0],
        "bone_ori": "XYZ",
        "parent": "guide1",
        "bone_name": "spine02_BIND"
    }