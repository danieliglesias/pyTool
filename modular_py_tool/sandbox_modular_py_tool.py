import maya.cmds as cmds
import pyTool.modular_py_tool.UiAutoRig as auto_rig_ui
import pyTool.modular_py_tool.Utilities as utili
import importlib
import pyTool.modular_py_tool.FileClass as FileClass
import pyTool.modular_py_tool.auto_rig_torso as torso
import pyTool.modular_py_tool.auto_rig_hip as hip
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

sphere_name = cmds.sphere(name='C_COG_BIND_guide', r=1)[0]
shader_name = utili.create_shader_guide()
# Step 5: Assign the material to the sphere
#cmds.select(sphere_name)
#cmds.hyperShade(assign='{}'.format(shader_name))
shape = cmds.listRelatives(sphere_name, shapes=True, fullPath=True)[0]
cmds.sets(shape, edit=True, forceElement='{}SG'.format(shader_name))


distance_value = cmds.getAttr('heightDistance.distance') / 2
cmds.move(0, distance_value, 0, sphere_name)
annotate = cmds.annotate(sphere_name, tx='COG', p=(0, distance_value, 0))
cmds.parent(annotate, sphere_name)
# cmds.rename(annotate, "hip_annotation")
cmds.setAttr(annotate + '.overrideEnabled', 1)
cmds.setAttr(annotate + '.overrideColor', 6)
    
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