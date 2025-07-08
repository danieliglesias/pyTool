import maya.cmds as cmds
import maya.mel as mel
import math
import json
import sys
import os

def file_manage(section_dir = None,action = None,field = None,dictionary = None,windows = None):
    if sys.platform == 'darwin':
        local = '/Users/danieliglesiasvalenzuela/Library/Preferences/Autodesk/maya/2022/prefs/scripts/pyTool/guide/{}'.format(section_dir)

    else:
        local = 'C:/Users/danie/Documents/maya/2022/scripts/pyTool/modular_py_tool/save/'

    #####################################################################################################

    if action == 'load':
        f = open(local)
        data = json.load(f)
        f.close()
        return data
    elif action == 'write':

        name = cmds.textField(field, query=True, text=True)

        print(name)
        print(local)
        print(section_dir)
        with open('{}{}'.format(local, name), 'w') as outfile:
            json.dump(dictionary, outfile)
        cmds.deleteUI(windows)

    elif action == 'show':
        listtoshow = os.listdir(local)
        #return filter(lambda k: '.json' in k, list)
        cmds.textScrollList(field, edit=True, removeAll=True)
        cmds.textScrollList(field, edit=True, append=filter(lambda k: '.json' in k, listtoshow))


