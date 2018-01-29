###################################################
## sst-sqe Dependancy 
###################################################
# This Dependancy file provides description on how
# to build/load the GoblinHMC dependancy on the test 
# machine
###################################################

DEPANDANCY_NAME="GoblinHMC"

echo "DEBUG: INSIDE FILE $DEPANDANCY_NAME"

# Identify the Loading Subroutine for this dependancy
# This is the name of a subroutine in this file with a 
# UNIQUE NAME that will be called to build/install 
# the dependancy.
DEPENDANCY_LOAD_FCN="Load_dep_goblinhmc"

###################################################
# This is the main entry point called by the 
# sst-build script (identified by the DEPENDANCY_LOAD_FCN)
# variable.  This will build/load the dependancy
# $1 = Dependancy Version
###################################################
Load_dep_goblinhmc() {
    DEP_VERSION=$1
    
    echo "DEBUG: RUNNING Load_dep_goblinhmc() with version $DEP_VERSION"
}