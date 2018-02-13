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
    
    echo "DEBUG: RUNNING Load_dep_goblinhmc() with version $OPTVER"
   
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
GoblinHMC_Load_dep_via_modules() {
    OPTVER=$1
    
    echo "DEBUG: RUNNING GoblinHMC_Load_dep_via_modules() with version $OPTVER"
    
    echo "ERROR: Cannot Build/Install $DEPENDENCY_NAME via modules"
}

###################################################

# Load via deps_build
GoblinHMC_Load_dep_via_deps_build() {
    OPTVER=$1
    
    echo "DEBUG: RUNNING GoblinHMC_Load_dep_via_deps_build() with version $OPTVER"

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
    
    # Stage the Goblin HMC Sim
    sstDepsStage_goblin_hmcsim

#    # Patch the Goblin HMC Sim
#    sstDepsPatch_goblin_hmcsim
    
    # Deploy the Goblin HMC Sim
    sstDepsDeploy_goblin_hmcsim    
}
