def saveGuidePositions(name='Mid size quadruped', listGuides=Null, export_location='/desktop', type='Biped'):
    if not listGuides:
        cmds.error('must provide a list off guides to get position and name')
        # lets create the empty slot to be save on a file on our python directory
        object = cmds.group(em=True, name='{}_{}'.format(name, type))

    ###we may want to add some variables like description, name of the character or type
    for attr in listGuides:
        cmds.addAttr(attr, dt='float3', object)
        position = cmds.xform(attr, q=True, t=True, ws=True)
        cmds.setAttr('{}.{}'.format(object, attr), position)

    # Use the file command to export the object
    cmds.file(export_location + "/" + object + ".ma", type='mayaAscii', exportSelected=True, force=True)


def getGuideBlueprintList():
    ### check this way to call the maya main directory
    list = cmds.getFileList(folder=cmds.internalVar(userScriptDir=True), filespec='*.ma')


def loadBlueprint(name=None):
    if not name:
        cmds.error('you must send the name of the file')

    cmds.file('{}.ma'.format(name), o=True)

    ###lets call the rebuildGuides
    buildGuides()