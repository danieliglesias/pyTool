"""string $name = "Max";
float $width = 70;
float $length = ($width/($width*20));
float $surfaceDegree = 3; //// 3cubic
float $uPatches = 28;
float $vPatches = 1;
float $ribonSection = 2;





ribbonProc( $name,  $width,  $length,  $surfaceDegree,  $uPatches,  $vPatches);


float $cvPos[] = `xform -q -ws -t ("Max_l_tentacle1_jnt_mid")`;
select "nurbsPlane1";
move -rpr $cvPos[0] $cvPos[1] $cvPos[2];
setAttr "nurbsPlane1.rotateY" -67.5;


  lattice  -dv 15 2 2 -ldv 15 2 2 -ol 1 -oc true;


    for($i=1 ; $i<=(($uPatches/2)+1); ++$i)
    {

                select -r ("ffd1Lattice.pt["+($i-1)+"][0:1][1]") nurbsPlane1 ;
                select -tgl ("ffd1Lattice.pt["+($i-1)+"][0:1][0]") nurbsPlane1 ;

                    ///tracking object to get local distance
                    cluster;
                    string $clusterTrack[] = `ls -sl`;

                    spaceLocator;
                    string $loca1[] = `ls -sl`;

                    spaceLocator;
                    string $loca2[] = `ls -sl`;




                select -r $clusterTrack;
                select -add $loca1;
                delete `pointConstraint -weight 1`;

                 float $cvPos[] = `xform -q -ws -t ($name+"_l_tentacle1_"+($i)+"_jnt")`;

                select $loca2;
                move -r $cvPos[0] $cvPos[1] $cvPos[2] ;

                parent $loca2 $loca1;

                float $valX = (getAttr($loca2[0] + ".translateX"));
                float $valY = (getAttr($loca2[0] + ".translateY"));
                float $valZ = (getAttr($loca2[0] + ".translateZ"));

                delete $clusterTrack;
                delete $loca2;
                delete $loca1;

                select -r ("ffd1Lattice.pt["+($i-1)+"][0:1][1]") nurbsPlane1 ;
                select -tgl ("ffd1Lattice.pt["+($i-1)+"][0:1][0]") nurbsPlane1 ;

                move -r $valX $valY $valZ;

    }


    ///delete lattice;
    select -add nurbsPlane1;
     DeleteHistory;


     for($i=1 ; $i<=(($uPatches/2)+1); ++$i)
    {
       select  ($name+"_l_tentacle1_"+($i)+"_jnt") ;
    }

    select -add nurbsPlane1;
    skinCluster;

//// create nur

global proc ribbonProc(string $name, float $width, float $length, float $surfaceDegree, float $uPatches, float $vPatches) {

     int $ctrlMidPos;
     if((($uPatches+1)%2) == 1){

            $ctrlMidPos = ((($uPatches+1)/2)+1);

        }else {

            $ctrlMidPos = (($uPatches+1)/2);

        }



    string $nurbPlane[] = `nurbsPlane -p 0 0 0 -ax 0 1 0 -w $width -lr $length -d $surfaceDegree -u $uPatches -v $vPatches -ch 1`;
    //move -r -os -wd 0 10 0 ;
    createHair ($uPatches+1) 1 10 0 0 1 0 5 0 1 2 1;



    string $hairN[] = `ls -sl`;
    int $totSize = (`size $hairN[0]`);
    string $num = `substring $hairN[0] 16 ($totSize)`;
        delete ("pfxHair"+$num);
        delete ("hairSystem"+$num);
        delete ("nucleus"+$num);

    rename ("hairSystem"+$num+"Follicles") ($name+"ribbon_follicle"+$num+"_grp");

    select -r `listTransforms "-type follicle"`;
    string $follicleHira[] = `ls -sl`;

    int $i = 1;
    for($item in $follicleHira){

            select -cl  ;
            joint;
            string $joint[] = `ls -sl`;
            string $jnt = `rename $joint ($name+"_ribbon_"+$i+"_jnt_def")`;

            parent $jnt $item;

            setAttr ($name+"_ribbon_"+$i+"_jnt_def.translateX") 0;
            setAttr ($name+"_ribbon_"+$i+"_jnt_def.translateY") 0;
            setAttr ($name+"_ribbon_"+$i+"_jnt_def.translateZ") 0;

        delete ("curve"+$i);



          rename $item ("ribbon_follicle"+$i);
          ++$i;
        }




}


"""