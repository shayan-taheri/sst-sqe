###################################################
## sst-sqe Dependancy 
###################################################
# This Dependancy file provides description on how
# to build/load the GoblinHMC dependancy on the test 
# machine
###################################################

# THIS IS THE NAME OF THE DEPENDANCY.  Load Routines
# Must be prefixed with the actual name here
DEPENDENCY_NAME="GoblinHMC"

echo "DEBUG: INSIDE FILE $DEPENDENCY_NAME"

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
    OPTLOADMETHOD=$1
    OPTVER=$2
    
    echo "RUNNING Load_dep_goblinhmc() with version $OPTVER"
   
    # At this point, we have multiple ways we can load the dependancy
    # Modules, Download and Compile, Assume its on machine, etc. its 
    # Up to this function on how to be sophisticated in loading the dependancy.

    # NOTE: Load Methods are generic strings, but the initial set are
    #       "clean_build" - Download and build the dependancy
    #       "deps_build"  - Use the old legacy bamboo deps file to load the dependancy
    #       "modules"     - Use the environment-modules pre-built module to load the dependancy
    #       "spack"       - Use the spack engine to downlod & build/load the module
    
    case "$OPTLOADMETHOD" in
        "clean_build") # Download and build the dependancy
            ${DEPENDENCY_NAME}_Load_dep_via_clean_build $OPTVER
            ;;
        "deps_build") # Build/Install using the legacy deps_build system
            ${DEPENDENCY_NAME}_Load_dep_via_deps_build $OPTVER
            ;;
        "modules") # Install using pre-built modules
            ${DEPENDENCY_NAME}_Load_dep_via_modules $OPTVER
            ;;
        "spack") # Install using pre-built modules
            ${DEPENDENCY_NAME}_Load_dep_via_spack $OPTVER
            ;;
        *) 
            echo "# Unknown Load Method argument '$OPTLOADMETHOD', will not build/Install $DEPENDENCY_NAME"
            ;;
    esac
}    

###################################################

# Load via clean build
GoblinHMC_Load_dep_via_clean_build() {
    OPTVER=$1
    
    echo "RUNNING ${DEPENDENCY_NAME}_Load_dep_via_clean_build() with version $OPTVER"
    
    echo "ERROR: Cannot Build/Install $DEPENDENCY_NAME via clean_build"
}

###################################################

# Load via deps_build
GoblinHMC_Load_dep_via_deps_build() {
    OPTVER=$1
    
    echo "RUNNING ${DEPENDENCY_NAME}_Load_dep_via_deps_build() with version $OPTVER"

    case "$OPTVER" in
        default|stabledevel) # build latest Goblin_HMCSIM from repository ("stable development")
            echo "# (default) stabledevel: build latest Goblin_HMCSIM from repository"
            . ${SST_DEPS_BIN}/sstDep_goblin_hmcsim_stabledevel.sh
            ;;
        none) # do not build (explicit)
            echo "# none: will not build Goblin_HMCSIM"
            ;;
        *) # unknown Goblin_HMCSIM argument
            echo "# Unknown argument '$OPTVER', will not build Goblin_HMCSIM"
            ;;
    esac
    
    # Stage the Build
    sstDepsStage_goblin_hmcsim

#    # Patch the Build (only for specific versions)
#    sstDepsPatch_goblin_hmcsim
    
    # Deploy the Build
    sstDepsDeploy_goblin_hmcsim    
}

###################################################

# Load via modules
GoblinHMC_Load_dep_via_modules() {
    OPTVER=$1
    
    echo "RUNNING ${DEPENDENCY_NAME}_Load_dep_via_modules() with version $OPTVER"
    
    echo "ERROR: Cannot Build/Install $DEPENDENCY_NAME via modules"
}

###################################################

# Load via spack
GoblinHMC_Load_dep_via_spack() {
    OPTVER=$1
    
    echo "RUNNING ${DEPENDENCY_NAME}_Load_dep_via_spack() with version $OPTVER"
    
    echo "ERROR: Cannot Build/Install $DEPENDENCY_NAME via spack"
}

###################################################

