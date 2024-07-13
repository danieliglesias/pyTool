biped_film_pos = {
  "ches_01": [0,0,0],
  "ches_02": [0,0,0],
  "neck_01": [0,0,0]
}

biped_game_pos = {
  "root_01": [0,0,0],
  "ches_01": [0,0,0],
  "ches_02": [0,0,0]
}

quadr_game_pos = {
  "root_01": [0,0,0],
  "ches_01": [0,0,0],
  "ches_02": [0,0,0]
}

quadr_film_pos = {
  "root_01": [0,0,0],
  "ches_01": [0,0,0],
  "ches_02": [0,0,0]
}

#global variables
##lets create 2 variables to determinate variables to be able to scale the controllers automaticly base on the distance of the center to top joint
ctrl_size = 1
scale_char = 2
top_jnt = None

def os_system():
	return os

def global_scale(data = None,ctrl_size = 1):
	ypos_list = []
    for item in data:
    	ypos_list.append(data[item][1])
   	if max(ypos_list) != 2:
    	scale_char = max(ypos_list)
    	
        ## this result need to be % as a decimal
    	difference = ((scale_char - 2) * 100) / 2
    	ctrl_size = ctrl_size * difference
    else:
    	ctrl_size = 1
    
    return ctrl_size    	
		


###auto_riggingUI
###auto_rigging_controller


###auto_rigging_general

def save_guide(name=None, type = None):

def load_guides(name = Name, filename = None):

def build_guides(name = None, dictionary = None):

	guide = cmds.sphere(radius=0.2, name='{}_{}_eyelit_guide'.format(sides, x))
	
	return 0
def build_joint():
	return 0
    
###auto_rigging_biped_chest

###auto_rigging_biped_arms
###auto_rigging_biped_hands
###auto_rigging_biped_legs

###auto_rigging_quadr_chest
###auto_rigging_quadr_legs
###auto_rigging_quadr_hands


###modular_rigging_arms
###modular_rigging_legs


############### EXTRAS ####################

def fk_ik_switch(ctrl):



#### 06 29 2024 



	

	
