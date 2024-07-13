import maya.cmds as cmds
import pyTool.utilities as utili
import importlib

importlib.reload(utili)


def createEyeballController(name=None, side='l', targetoff=30):
    if not name:
        cmds.error('createEyeballController must get a name prefix')

    fkcurve = cmds.curve(d=3, p=uppCurveListPos, name='{}_{}_eyelid_fk_ctrl'.format(name, side))
    cmds.DeleteHistory(fkcurve)


off = utili.groupObject(object=fkcurve)
jntPos = cmds.xform('{}_{}_eyeball_jnt', format(name, side), t=True, ws=True, q=True)
cmds.xform(off, t=(jntPos[0], jntPos[1], jntPos[2]))
cmds.parentConstraint(fkcurve, '{}_{}_eyeball_jnt', format(name, side))

# create empty group
emptyGrp = createEmptyGroup(name='{}_{}_eyetarget'.format(name, side))
cmds.xform(emptyGrp, t=(jntPos[0], jntPos[1], jntPos[2]) + targetoff)

# create controller
#### maybe we should create a eyetarget controller

if not ('{}_eyetarget_ctrl'.format(name)):
    ctrl = utili.createController(name='{}_eyetarget_ctrl'.format(name), shape='circle', target=None,
                                  contraint_target=None, facing='z', offsetnumber=2, type='fk', size=5)
    ###### delete history
    ### converge eyes system
    cmds.addAttr(ctrl, longName='converge', defaultValue=0, minValue=0, maxValue=1, keyable=1)
    cmds.addAttr(ctrl, longName='space', at='enum', en='local:world:', keyable=1)

    remapNode = cmds.createNode('remapValue', n='{}_remapValue'.format(ctrl))
    cmds.setAttr('{}.inputMin'.format(remapNode), 1)
    cmds.setAttr('{}.inputMax'.format(remapNode), 0)
    cmds.setAttr('{}.outputMin'.format(remapNode), 0)
    if side = 'r':
        cmds.setAttr('{}.outputMax'.format(remapNode), -3.462)
        else
        cmds.setAttr('{}.outputMax'.format(remapNode), 3.462)

    cmds.connectAttr('{}.converge'.format(ctrl), '{}.inputValue'.format(remapNode))
    cmds.connectAttr('{}.outValue'.format(remapNode), '{}.translateX'.format(emptyGrp))

cmds.parent(ctrl, emptyGrp)

## joint between 2 eyes
jnt = cmds.joint(name='{}_{}_eyelid_{}_{}_jnt'.format(name, side, portion, edges))
cmds.xform(jnt, t=0, jntPos[1], jntPos[2]))

cmds.parent('{}_off'.format(ctrl), jnt)

cmds.aimConstraint('{}_off'.format(ctrl), emptyGrp, aimVector=[0, 0, 1], upVector=[0, 1, 0],
                   worldUpType='objectrotation', worldUpVector=[0, 1, 0], worldUpObject=jnt)

cmds.parentConstraint((join, emptyGrp), '{}_off'.format(ctrl))

##WORLD SPACE SWITCH
if not ('{}_eyetarget_world'.format(name):
emptyGrp = createEmptyGroup(name='{}_eyetarget_world'.format(name))
reverse = cmds.createNode('reverse', n='{}_reverse'.format(ctrl))

cmds.connectAttr('{}.space'.format(ctrl), '{}_off_parentConstraint1.{}_eyetarget_worldW1'.format(ctrl, name))
cmds.connectAttr('{}.space'.format(ctrl), '{}.inputX'.format(reverse))
cmds.connectAttr('{}.outputX'.format(reverse), '{}_off_parentConstraint1.{}_c_midface_jntW0'.format(ctrl, name))

cmds.aimConstraint(jnt, ctrl, aimVector=[0, 0, -1], upVector=[0, 1, 0], worldUpType='objectrotation',
                   worldUpVector=[0, 1, 0], worldUpObject=jnt)




# move to utilities page
def groupObject(object=None, offset=2):
    off = cmds.group(object, name='{}_off'.format(object))
    return off


def createEmptyGroup(name=None):
    emptygroup = cmds.spaceLocator(absolute=True, name=name)[0]
    cmds.delete('{}Shape'.format(emptygroup))

"""


/////// EYE SOCKET CONTROLLER PROC ///////
/////// EYE SOCKET CONTROLLER PROC ///////
/////// EYE SOCKET CONTROLLER PROC ///////

global proc eyeSocketCtrl(string $name , string $side, int
$numberJnt ){

CreateNURBSCircle;
string $eyeSocketCtl[] = `ls -sl`;
string $eyeSocketCtlHist[] = `listHistory

($eyeSocketCtl)`;

setAttr ($eyeSocketCtlHist[1]+".normalZ") 1;
setAttr ($eyeSocketCtlHist[1]+".normalY") 0;
string $eyeSocketCtrl = `rename $eyeSocketCtl[0]

($name+"_"+$side+"_socket_ctrl")`;

select -r ($eyeSocketCtrl+".cv[0:7]");
scale -r -p 0cm 0cm 0cm 2.5 2.5 2.5 ;
//move -r -cs -ls -wd 0 0 0.5 ;
if($side == "l"){
rotate -r -p 0cm 0cm 1.156123cm -os -fo 0 15 0 ;
move -r 1 0 0 ;
}
if($side == "r"){
rotate -r -p 0cm 0cm 1.156123cm -os -fo 0 -15 0 ;
move -r -1 0 0 ;
}
DeleteHistory;
string $eyeSocketCtrlGrp = `group -em ($eyeSocketCtrl)`;
string $eyeSocketCtrlOff = `rename $eyeSocketCtrlGrp

($eyeSocketCtrl+"_off")`;

parent $eyeSocketCtrl $eyeSocketCtrlOff;

float $scktJntPos[] = `xform -q -ws -t

($name+"_"+$side+"_socket_jnt")`;
select $eyeSocketCtrlOff;
move -rpr $scktJntPos[0] $scktJntPos[1] $scktJntPos[2];

select -r $eyeSocketCtrl ;
select -tgl ($name+"_"+$side+"_socket_jnt");
doCreateParentConstraintArgList 1 {
"1","0","0","0","0","0","0","0","1","","1" };
parentConstraint -mo -weight 1;
doCreateScaleConstraintArgList 1 {
"0","1","1","1","0","0","0","1","","1" };

scaleConstraint -offset 1 1 1 -weight 1;
//// keeping controllers seprated of the main rig for

game engine

parent ($name+"_"+$side+"_eyelid_fk_ctrl_off")

$eyeSocketCtrl;

for($i=1;$i<=$numberJnt;++$i){
parent ($name+"_"+$side+"_eyelid_upp_"+$i+"_jnt")

($name+"_"+$side+"_eyeball_grp");

parent ($name+"_"+$side+"_eyelid_low_"+$i+"_jnt")

($name+"_"+$side+"_eyeball_grp");

}
/// to make child eyelit joint work we need to turn of

compensate scale
setAttr

($name+"_"+$side+"_eyeball_jnt.segmentScaleCompensate") 0;

setAttr

($name+"_"+$side+"_eyeball_grp.segmentScaleCompensate") 0;
}// END PROC
