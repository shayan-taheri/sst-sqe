###################################################
## sst-sqe Dependancy 
###################################################
# This Dependancy file provides description on how
# to build/load the openmpi dependancy on the test 
# machine
###################################################

DEPANDANCY_NAME="openmpi"

echo "DEBUG: INSIDE FILE $DEPANDANCY_NAME"

# Identify the Loading Subroutine for this dependancy
# This is the name of a subroutine in this file with a 
# UNIQUE NAME that will be called to build/install 
# the dependancy.
DEPENDANCY_LOAD_FCN="Load_dep_openmpi"

###################################################
# This is the main entry point called by the 
# sst-build script (identified by the DEPENDANCY_LOAD_FCN)
# variable.  This will build/load the dependancy
# $1 = Dependancy Version
###################################################
Load_dep_openmpi() {
    DEP_VERSION=$1
    
    echo "DEBUG: RUNNING Load_dep_openmpi() with version $DEP_VERSION"
    
    # At this point, we have multiple ways we can load the dependancy
    # Modules, Download and Compile, Assume its on machine, etc. its 
    # Up to this function on how to be sophisticated in loading the dependancy.
}


