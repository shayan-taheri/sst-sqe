###################################################
## sst-sqe Dependancy 
###################################################
# This Dependancy file provides description on how
# to build/load the openmpi dependancy on the test 
# machine
###################################################

DEPENDENCY_NAME="openmpi"

echo "DEBUG: INSIDE FILE $DEPENDENCY_NAME"

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
    OPTLOADMETHOD=$1
    OPTVER=$2
    
    echo "DEBUG: RUNNING Load_dep_openmpi() with version $OPTVER"
    
    # At this point, we have multiple ways we can load the dependancy
    # Modules, Download and Compile, Assume its on machine, etc. its 
    # Up to this function on how to be sophisticated in loading the dependancy.

    # NOTE: Load Methods are generic strings, but the initial set are
    #       "deps_build" - Use the old legacy bamboo deps file to load the dependancy
    #       "modules" - Use the environmet-modules pre-built module to load the dependancy
    case "$OPTLOADMETHOD" in
        "deps_build") # Build/Install using the legacy deps_build system
            ${DEPENDENCY_NAME}_Load_dep_via_deps_build $OPTVER
            ;;
        "modules") # Install using pre-built modules
            ${DEPENDENCY_NAME}_Load_dep_via_modules $OPTVER
            ;;
        *) 
            echo "# Unknown Load Method argument '$OPTLOADMETHOD', will not build/Install $DEPENDENCY_NAME"
            ;;
    esac
}    

###################################################

# Load via modules
openmpi_Load_dep_via_modules() {
#${DEPENDENCY_NAME}_openmpi_Load_dep_via_modules() {
    OPTVER=$1
    
    echo "DEBUG: RUNNING openmpi_Load_dep_via_modules() with version $OPTVER"
    
   # load MPI
   case $OPTVER in
       openmpi-1.6.5)
           echo "OpenMPI (openmpi-1.6.5) selected"
           ModuleEx unload mpi # unload any default to avoid conflict error
           ModuleEx load mpi/$OPTVER
           ;;
       openmpi-1.8)
           echo "OpenMPI (openmpi-1.8) selected"
           ModuleEx unload mpi # unload any default to avoid conflict error
           ModuleEx load mpi/$OPTVER
           ;;
        openmpi-1.10)
           echo "OpenMPI (openmpi-1.10) selected"
           ModuleEx unload mpi # unload any default to avoid conflict error
           ModuleEx load mpi/$OPTVER
           ;;
       none)
           echo "MPI requested as \"none\".    No MPI loaded"
           ModuleEx unload mpi # unload any default 
           ;;
       *)
           echo "Default MPI option, loading mpi/${desiredMPI}"
           ModuleEx unload mpi # unload any default to avoid conflict error
           ModuleEx load mpi/$OPTVER 2>catch.err
           if [ -s catch.err ] 
           then
               cat catch.err
               exit 1
           fi
           ;;
   esac
}

###################################################

# Load via deps_build
openmpi_Load_dep_via_deps_build() {
    OPTVER=$1
    
    echo "DEBUG: RUNNING openmpi_Load_dep_via_deps_build() with version $OPTVER"

    echo "ERROR: Cannot Build/Install $DEPENDENCY_NAME via deps_build"
}

