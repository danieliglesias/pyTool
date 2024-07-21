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
