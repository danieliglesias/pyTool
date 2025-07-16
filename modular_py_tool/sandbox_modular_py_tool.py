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



auto_rig_ui._nested_dict_instance.update_limb( limb_name = 'torso', list = ['spine','chest'],suffix = 'jnt')



auto_rig_ui._nested_dict_instance.show_dictionary()


auto_rig_ui._nested_dict_instance.data['torso'] = {}

component =auto_rig_ui._nested_dict_instance.data['torso']


auto_rig_ui._nested_dict_instance.create_joints_from_limb()


print(auto_rig_ui._nested_dict_instance.data['COG']['general']['type'])


result = utili.check_existing_joints(auto_rig_ui._nested_dict_instance.data)

print( result)

self.data.keys()


    
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