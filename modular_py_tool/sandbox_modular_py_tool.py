import maya.cmds as cmds
import pyTool.modular_py_tool.UiAutoRig as auto_rig_ui
import pyTool.utilities as utili
import pyTool.modular_py_tool.UiUtilities as uiutili
import importlib
import pyTool.modular_py_tool.FileClass as FileClass
#from  pyTool.modular_py_tool.nested_dictionary import NestedDictionary as dict
import os
import json
import math
import sys

importlib.reload(auto_rig_ui)    
importlib.reload(utili)    
importlib.reload(uiutili)
importlib.reload(FileClass)


auto_rig_ui.modular_ui()

