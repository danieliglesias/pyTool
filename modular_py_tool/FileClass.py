import maya.cmds as cmds
import json
import os

#import pyTool.utilities as utili
import modular_py_tool.UiAutoRig as ui_autorig
import modular_py_tool.Utilities as utili
import modular_py_tool.auto_rig_hip as hip
import modular_py_tool.auto_rig_fundation as fundation
import modular_py_tool.auto_rig_torso as torso
import modular_py_tool.auto_rig_leg as leg
import importlib
importlib.reload(utili)
importlib.reload(hip)
importlib.reload(ui_autorig)
importlib.reload(leg)

class NestedDictionary:
    def __init__(self):
        #self.data = data
        self.data = {
            'general':{
                'file': 'Nombre Json Array',
                'char_name': 'Character Name',
                'dist_loc1': [0, 0, 0],
                'dist_loc2': [0, 200, 0]
            }

        }



    def show_dictionary(self, current_dict=None, indent=0, limb=None):
        """Recursively prints a nested dictionary in a readable format using .format().
        If a component name is provided, only that key will be shown."""
        if current_dict is None:
            # If filtering by component, start from that sub-dictionary if it exists
            if limb:
                current_dict = self.data.get(limb, {})
                if not current_dict:
                    print("Component '{}' not found.".format(limb))
                    return
                print("{}:".format(limb))
                indent += 1
            else:
                current_dict = self.data

        spacing = '    '  # 4 spaces

        for key, value in current_dict.items():
            if isinstance(value, dict):
                print("{0}{1}:".format(spacing * indent, key))
                self.show_dictionary(value, indent + 1)
            else:
                print("{0}{1}: {2}".format(spacing * indent, key, value))


    def LoadDictionary(self, file_name):

        file_name = cmds.textScrollList(file_name, q=1, si=1)
        if not file_name:
            utili.errorMessage('nothing was selected')
            cmds.error('nothing was selected')

        elif len(file_name) > 1:
            utili.errorMessage('More than one object selected')
            cmds.error('More than one object selected')
        else:
            file_path = 'C:/Users/danie/Documents/maya/2026/scripts/modular_py_tool/save/{}'.format(file_name[0])

            #try:
            with open(file_path, 'r') as f:
                self.data = json.load(f)  # ✅ Replace the entire self.data
                print('Loaded data from: {}'.format(file_path))
                self.rebuild_from_json()

            """except Exception as e:
                utili.errorMessage('Failed to load file: {}'.format(e))
                cmds.error('Failed to load file: {}'.format(e))
"""
            # Show the loaded dictionary
            self.show_dictionary()

    def rebuild_from_json(self):
        ### first we need a validation if any of the joint or guide exist
        existing = utili.check_existing_joints(self.data)
        print('inside rebuild_from_json')
        if existing:
            print('The following joints or guide already exist in the scene and need to be deleted to rebuild the rig:')
            for joint in existing:
                print('  - {}'.format(joint))
        else:
            # now we go limb by limb rebuilding
            char_name = self.data['general']['char_name']
            for limb in self.data.keys():
                if limb == 'general':
                    #set file and character name
                    file_name = self.data[limb]['file']
                    ui_autorig.cmds.textField('filename', edit=True, text=file_name)
                    ui_autorig.cmds.textField('charactername', edit=True, text=char_name)

                    #set distant measure tool
                    loc_pos1 = self.data[limb]['dist_loc1']
                    loc_pos2 = self.data[limb]['dist_loc2']
                    utili.generate_height_guides(loc_pos1,loc_pos2)


                else:
                    type_rebuild = self.data[limb]['general']['type']
                    if limb == 'fundation':
                        print('inside fundation rebuild')
                        type_rig = self.data[limb]['general']['parent']
                        if type_rig:
                            cmds.optionMenu('type_rig_option_menu', edit=True, value=type_rig)
                            fundation.type_rig_option_menu_change(type_rig = type_rig,char_name = char_name)




                    if limb == 'COG':
                        if type_rebuild == 'jnt':
                            hip.controller_hip_jnt(rebuild=True,char_name = char_name)
                        if type_rebuild == 'guide':
                            hip.controller_hip_guide(rebuild=True, char_name = char_name)
                        # check for joint or guide type
                        # for now fundation is just for games
                    if limb == 'torso':
                        if type_rebuild == 'jnt':
                            torso.controller_torso_jnt(rebuild=True,char_name = char_name)
                        if type_rebuild == 'guide':
                            torso_guides = self.data.get("torso", {})

                            spine_joints = [k for k in torso_guides if "spine" in k.lower()]
                            chest_joints = [k for k in torso_guides if "chest" in k.lower()]

                            if chest_joints:
                                torso.controller_chest_guide(rebuild=True,char_name = char_name)

                            if spine_joints:
                                torso.controller_torso_guide(rebuild=True,char_name = char_name)


                        # check for joint or guide type

                    if "lleg" in limb or "rleg" in limb:
                        kinematic_mode = self.data[limb]['general']['kinematic_mode']
                        limb_type = self.data[limb]['general']['limb_type']
                        limb_end = self.data[limb]['general']['limb_end']
                        if type_rebuild == 'jnt':
                            leg.controller_leg_jnt(limb_name=limb, char_name=char_name, rebuild=True,
                                                     kinematic_mode=kinematic_mode,
                                                     limb_end=limb_end, leg_type=limb_type)
                        if type_rebuild == 'guide':
                            leg.controller_leg_guide(limb_name = limb, char_name = char_name, rebuild=True, kinematic_mode = kinematic_mode,
                                                     limb_end = limb_end , leg_type = limb_type )



    def SaveDictionary(self,file_name = None, char_name = None):

        ###lets update general variables
        self.data['general']['file'] = "updated_file.json"
        self.data['general']['char_name'] = char_name
        self.data['general']['dist_loc1'] = cmds.xform('heightLocA', t=True, ws=True, q=True)
        self.data['general']['dist_loc2'] = cmds.xform('heightLocB', t=True, ws=True, q=True)


        directory = 'C:/Users/danie/Documents/maya/2026/scripts/modular_py_tool/save/'
        ui_autorig.NameInputUi(section_dir=directory, dictionary=self.data)
        ##utili.errorMessage('Make sure that the selection is in hierarchy order from parent to children')



    def GuideNumber(self, limb_name = 'torso01'):

        keys = [k for k in self.data['torso01'] if k != 'general']


        for item in keys:
            print(item)
            print(self.data['torso01'][item]['position'])


    def GuidePositioner(self):
        return 0
    def JntCreation(self):
        return 0

    def AddLimb(self):

        return 0

    def update_limb(self,char_name = None, limb_name = None,parent = None, list = None , suffix = None,priority = None,
                    kinematic_mode = None,limb_type = None,limb_end = None):

        guides = utili.find_named_objects(char_name = char_name, name_patterns=list, suffix=suffix)

        print(guides)

        #for comp in components.split('_')[1]:
        self.data[limb_name] = {}
        ##general
        self.data[limb_name]['general'] = {
            'parent': parent,
            'type': suffix,
            'rebuild_priority': priority,
            'kinematic_mode': kinematic_mode, ### IK FK controller
            'limb_type': limb_type, ### this could be a humand feet or a horse or dog leg etc
            'limb_end': limb_end, ### Do we include feet or hands?
            'limb_end_metacarpal': None, ### this could be None/simple/advance
            'limb_end_digit_number': 5 ### default 5/could be less too
                        
        }
        ###join or guide list

        print('updating limb before loop')
        for guide_name in guides:  # Let's say 3 guides per component
            if cmds.objectType(guide_name) == 'joint':
                rotate_orders = ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx']
                value_ori = cmds.getAttr('{}.rotateOrder'.format(guide_name))
                bone_ori = rotate_orders[value_ori]
            else:
                bone_ori = 'NA'
            self.data[limb_name][guide_name] = {
                'position': cmds.xform(guide_name, t=True, ws=True, q=True),
                'bone_ori'  : bone_ori,
                'parent': cmds.listRelatives(guide_name, parent=True),
                'bone_name': guide_name
            }
        print('updating limb after loop')
        ####finally we print the result on the console
        self.show_dictionary(limb=limb_name)


    def create_joints_from_limb(self, limb_name='torso'):
        #this part to separate the rebuild from joint and guides
        if self.data[limb_name]['general']['type'] == 'jnt':

            component = self.data.get(limb_name)
            if not component:
                print('Limb "{}" not found.'.format(limb_name))
                return

            joint_map = {}  # joint_key → bone_name

            # First pass: create joints
            for joint_key, info in component.items():
                cmds.select(clear=True)
                if joint_key == 'general':
                    continue

                bone_name = info.get('bone_name')
                position = info.get('position')

                if not isinstance(position, (list, tuple)) or len(position) != 3:
                    print('Invalid or missing position for \'{}\'. Defaulting to [0, 0, 0].'.format(bone_name))
                    position = [0, 0, 0]
                else:
                    print('Creating joint \'{}\': position = {}'.format(bone_name, position))

                if not cmds.objExists(bone_name):
                    joint = cmds.joint(name=bone_name, position=position)
                else:
                    print('Joint \'{}\' already exists. Skipping creation.'.format(bone_name))
                    joint = bone_name

                cmds.xform(joint, ws=True, t=position)
                joint_map[joint_key] = bone_name

            # Second pass: parent joints
            for joint_key, info in component.items():
                cmds.select(clear=True)
                if joint_key == 'general':
                    continue
                bone_name = info.get('bone_name')
                parent_key = info.get('parent')
                if not parent_key or parent_key == 'None':
                    continue  # No parent, skip

                if bone_name and parent_key:
                    try:
                        cmds.parent(bone_name, parent_key)
                        print('Parented "{}" → "{}"'.format(bone_name, parent_key))
                    except RuntimeError as e:
                        print('Error parenting \'{}\' to \'{}\': {}'.format(bone_name, parent_key, e))
                else:
                    print('Could not find child or parent for key: {}'.format(joint_key))


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
