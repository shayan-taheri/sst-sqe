###################################################
## sst-sqe Build/Test Scenario
###################################################
# This scenario is a testing scenario for testing the build 
# We will put more info here...
###################################################

###################################################
# Identify the dependancies needed for this scenario 
###################################################
SCENARIO_NAME="SCENARIO_3"
echo "DEBUG: INSIDE FILE $SCENARIO_NAME"

## Identify Dependencies
SCENARIO_NUM_DEPENCENCY=3

SCENARIO_DEPENCENCY_NAME[1]="openmpi"
SCENARIO_DEPENCENCY_VER[1]="1.8"
                        
SCENARIO_DEPENCENCY_NAME[2]="zoltan"
SCENARIO_DEPENCENCY_VER[2]="3.83"

SCENARIO_DEPENCENCY_NAME[3]="goblinhmc"
SCENARIO_DEPENCENCY_VER[3]="3.0"
                        
SCENARIO_DEPENCENCY_NAME[4]="pin"
SCENARIO_DEPENCENCY_VER[4]="2.14-71313"


###################################################
# Identify the SUT's needed for this scenario 
###################################################
## Identify SUTS 
SCENARIO_NUM_SUTS=2

SCENARIO_SUT_NAME[1]="sst-core"
SCENARIO_SUT_SETUP[1]="autogen"
SCENARIO_SUT_CONFIG[1]=""
SCENARIO_SUT_MAKE[1]="make"
SCENARIO_SUT_INSTALL[1]="make install"
            
SCENARIO_SUT_NAME[2]="sst-elements"
SCENARIO_SUT_SETUP[2]=
SCENARIO_SUT_CONFIG[2]=
SCENARIO_SUT_MAKE[2]=
SCENARIO_SUT_INSTALL[2]=
            
SCENARIO_SUT_NAME[3]="sst-macro"
SCENARIO_SUT_SETUP[3]=
SCENARIO_SUT_CONFIG[3]=
SCENARIO_SUT_MAKE[3]=
SCENARIO_SUT_INSTALL[3]=
            
SCENARIO_SUT_NAME[4]="juno"
SCENARIO_SUT_SETUP[4]=
SCENARIO_SUT_CONFIG[4]=
SCENARIO_SUT_MAKE[4]=
SCENARIO_SUT_INSTALL[4]=

