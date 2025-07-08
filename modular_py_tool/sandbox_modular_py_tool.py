import maya.cmds as cmds
import pyTool.modular_py_tool.auto_Rig_UI as auto_rig_ui
import pyTool.utilities as utili
import importlib
import pyTool.modular_py_tool.nested_dictionary as dict
#from  pyTool.modular_py_tool.nested_dictionary import NestedDictionary as dict
import os
import json
import math
import sys

importlib.reload(auto_rig_ui)
importlib.reload(utili)
importlib.reload(dict)


auto_rig_ui.modular_ui()

# Create an instance of the class
nested_dict_instance = NestedDictionary()


print(nested_dict_instance.get_all_limb())

sub_dict_key1 = nested_dict_instance.get_limb('torso01')
print("Sub-dictionary for 'key1':", sub_dict_key1)

keys = nested_dict_instance.get_all_limb()
print("All top-level keys:", keys)

print(nested_dict_instance.get_item('key1')) 

#calculate height character



f = open('C:/Users/danie/Desktop/Rigging/python_tool/test.json')


global global_dict
#data = json.load(f)
global_dict = json.load(f)
side_flag = []
l_side_flag = False
r_side_flag = False


print(global_dict)


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

