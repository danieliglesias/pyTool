import maya.cmds as cmds
import json
import os

#import pyTool.utilities as utili
import pyTool.modular_py_tool.UiAutoRig as UiAutoRig
import pyTool.modular_py_tool.Utilities as utili
import importlib
importlib.reload(utili)
importlib.reload(UiAutoRig)

class NestedDictionary:
    def __init__(self):
        #self.data = data
        self.data = {
            'general':{
                'file': 'Nombre Json Array',
                'char_name': 'Character Name'
            }

        }
    def PrintTest(self):

        return list(self.data.keys())

    def LoadDictionary(self, file_name):

        file_name = cmds.textScrollList(file_name, q=1, si=1)
        if not file_name:
            utili.errorMessage('nothing was selected')
            cmds.error('nothing was selected')

        elif len(file_name) > 1:
            utili.errorMessage('More than one object selected')
            cmds.error('More than one object selected')
        else:
            #face.load_mainstructure_guide(file_name=file_name)
            f = open('C:/Users/danie/Documents/maya/2026/scripts/pyTool/modular_py_tool/save/{}'.format(file_name[0]))
            loaded_dict = {}
            loaded_dict = json.load(f)

            for key,value in loaded_dict.items():

                self.data[key] = value

            #print(self.data['torso01'].values())

            #keys = list(self.data['torso01'].keys())
            keys = [k for k in self.data['torso01'] if k != 'general']

            for item in keys:
                print(item)
                print(self.data['torso01'][item]['position'])
            """
                if item != 'general':
                    del loaded_dict[item]
            print(loaded_dict)"""

        """print(filename)

        f = open('C:/Users/danie/Desktop/Rigging/python_tool/test.json')

        try:
            with open(filename, 'r') as json_file:
                self.data = json.load(json_file)
            print('Data loaded from {}'.format(filename))
        except Exception as e:
            print('Error loading from JSON: {}'.format(e))"""


    def SaveDictionary(self):

        directory = 'C:/Users/danie/Documents/maya/2026/scripts/pyTool/modular_py_tool/save/'
        UiAutoRig.NameInputUi(section_dir=directory, dictionary=self.data)
        ##utili.errorMessage('Make sure that the selection is in hierarchy order from parent to children')

    def GuideNumber(self, limb_name = 'torso01'):

        keys = [k for k in self.data['torso01'] if k != 'general']


        for item in keys:
            print(keys)
            print(self.data['torso01'][keys]['position'])


    def GuidePositioner(self):
        return 0
    def JntCreation(self):
        return 0

    def AddLimb(self):

        return 0

    def UpdateLimb(self):

        return 0

    def ValidationValues(self):

        return 0




    """
    def add_item(self, key, subkey, value):
        if key not in self.data:
            self.data[key] = {}
        self.data[key][subkey] = value

    def get_item(self, key, subkey):
        return self.data.get(key, {}).get(subkey, None)

        # New method to get the entire sub-dictionary for a given key

    # this method return a specific limb
    def get_limb(self, key):
        # Return the entire sub-dictionary for the given key
        return self.data.get(key, None)

    # this method return all limb
    def get_all_limb(self):
        return list(self.data.keys())

    def add_new_limb(self, key, limb_dict=None):
        # Adds a new key that maps to a nested dictionary (or provided data)
        if key not in self.data:
            self.data[key] = limb_dict if limb_dict is not None else {}
        else:
            print('Key {} already exists.'.format(key))

    def remove_limb(self, key):
        # Removes a top-level key (and its associated data)
        if key in self.data:
            del self.data[key]
            print('Key {} has been removed.'.format(key))
        else:
            print('Key {} not found.'.format(key))

    # New method to save the dictionary to a JSON file
    def save_to_json(self, filename):
        #Save the current data dictionary to a JSON file with overwrite check.
        if os.path.exists(filename):
            # Ask the user if they want to overwrite the file
            user_input = input('The file {} already exists. Do you want to overwrite it? (y/n): '.format(filename))
            if user_input.lower() != 'y':
                print('File not overwritten.')
                return  # Do not proceed with saving if the user does not want to overwrite

        try:
            with open(filename, 'w') as json_file:
                json.dump(self.data, json_file, indent=4)  # Pretty print with indentation
            print('Data saved to {}'.format(filename))
        except Exception as e:
            print('Error saving to JSON: {}'.format(e))

    # New method to load the dictionary from a JSON file
    def load_from_json(self, filename):

        #lets clear the dictionary before loading.
        self.data = {}
        #Load data from a JSON file into the dictionary.
        try:
            with open(filename, 'r') as json_file:
                self.data = json.load(json_file)
            print('Data loaded from {}'.format(filename))
        except Exception as e:
            print('Error loading from JSON: {}'.format(e))

    #this method will return file name and character name
    def get_general_info(self):
        
        Returns the values of 'file' and 'char_name' under the 'general' key.
        
        general_info = self.data.get('general', {})
        file_value = general_info.get('file', None)
        char_name = general_info.get('char_name', None)
        return file_value, char_name

    #this method will update the info values for the file name and character name
    def update_general_info(self, file_value=None, char_name=None):
        
        Updates the 'file' and 'char_name' values under the 'general' key.

        Args:
            file_value (str): New value for 'file' (optional).
            char_name (str): New value for 'char_name' (optional).
        
        if 'general' not in self.data:
            self.data['general'] = {}

        if file_value is not None:
            self.data['general']['file'] = file_value
        if char_name is not None:
            self.data['general']['char_name'] = char_name

        ## here the rest of the nested structure 
            'torso01': {
                'general': {
                'exist': True,
                'parent': 'hip'
                },'guide1': {
                'position': [1, 0, 0],
                'bone_ori': 'XYZ',
                'parent': 'hip01',
                'bone_name': 'spine01_BIND'
                },'guide2': {
                'position': [1, 0, 0],
                'bone_ori': 'XYZ',
                'parent': 'Guide1',
                'bone_name': 'spine02_BIND'
                }
            },
            'lfarm01': {
                'general': {
                    'exist': True,
                    'parent': 'torso'
                },
                'subkey1': 'value3',
                'subkey2': 'value4'
            },
            'rfarm01': {
                'subkey1': 'value3',
                'subkey2': 'value4'
            },
            'head01': {
                'subkey1': 'value3',
                'subkey2': 'value4'
            }"""