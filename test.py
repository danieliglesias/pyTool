def save_mainstructure_guide(name=None, objectList=None):
    final_dict = dict()
    if not objectList:
        selected = cmds.ls(sl=True)
        if not selected:
          	errorMessage('Nothing is selected')
    	
    
    if len(objectList) >= 2:

        
        for item in objectList:
        	emptyDict = dict()
        	#lets get the parent name
            parent = cmds.listRelatives(item, parent = True)
            if not parent:
            	parent = 'none'
            #position
           	xform = cmds.xform(item, t=True, ws=True, q=True)
             
            emptyDict.update({'parent': parent})
            emptyDict.update({'xform': xform})
            
            final_dict.update({item: emptyDict})
    
    directory = 'base/guide/'
    utili.nameInputWindow(section_dir=directory, dictionary=final_dict)
    
def load_save_mainstructure_guide(name=None, file_name=None):
    data = utili.file_manage(section_dir='eyelid/guide/{}'.format(file_name[0]), action='load')

    for guide_name, obj in data.items():
        if not utili.objectExist(guide_name):
            utili.errorMessage('Guide with the name of {} does not exist')
        else:
        	guide = cmds.sphere(radius=0.2, name=guide_name)[0]
            	
	 for guide_name, obj in data.items():
        if not utili.objectExist(guide_name):
            utili.errorMessage('Guide with the name of {} does not exist')
        else:
            for y in obj:
            	
                cmds.xform(guide, t=obj[y])
                if y == 'parent' and obj[y] != 'none'
                	cmds.parent(obj[y], guide_name)	
def build_face_structure(name = None,guide_list = None,eye_guide_list = None):
  f = open(
          'C:/Users/danie/Documents/maya/2022/scripts/pyTool/guide/base/{}'.format(file_name[0]))

      data = json.load(f)

      all_exist = True
      for item in data:
          if not utili.objectExist(item):
              all_exist = False

      if all_exist:
          for item in data:
              cmds.xform(item, t=data[item])
      else:
          utili.errorMessage('Not all object listed in the this file exist')
                      cmds.parent(obj[y], guide_name)	
                                
