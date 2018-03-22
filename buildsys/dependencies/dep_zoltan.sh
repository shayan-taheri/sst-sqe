###################################################
## sst-sqe Dependancy 
###################################################
# This Dependancy file provides description on how
# to build/load the Zoltan dependancy on the test 
# machine
###################################################

DEPENDENCY_NAME="Zoltan"

echo "DEBUG: INSIDE FILE $DEPENDENCY_NAME"

# Identify the Loading Subroutine for this dependancy
# This is the name of a subroutine in this file with a 
# UNIQUE NAME that will be called to build/install 
# the dependancy.
DEPENDANCY_LOAD_FCN="Load_dep_zoltan"

###################################################
# This is the main entry point called by the 
# sst-build script (identified by the DEPENDANCY_LOAD_FCN)
# variable.  This will build/load the dependancy
# $1 = Dependancy Version
###################################################
Load_dep_zoltan() {
    OPTLOADMETHOD=$1
    OPTVER=$2
    
    echo "RUNNING Load_dep_zoltan() with version $OPTVER"
    
    # At this point, we have multiple ways we can load the dependancy
    # Modules, Download and Compile, Assume its on machine, etc. its 
    # Up to this function on how to be sophisticated in loading the dependancy.

    # NOTE: Load Methods are generic strings, but the initial set are
    #       "deps_build"  - Use the old legacy bamboo deps file to load the dependancy
    #       "modules"     - Use the environment-modules pre-built module to load the dependancy
    #       "clean_build" - Download and build the dependancy
    case "$OPTLOADMETHOD" in
        "deps_build") # Build/Install using the legacy deps_build system
            ${DEPENDENCY_NAME}_Load_dep_via_deps_build $OPTVER
            ;;
        "modules") # Install using pre-built modules
            ${DEPENDENCY_NAME}_Load_dep_via_modules $OPTVER
            ;;
        "clean_build") # Install using pre-built modules
            ${DEPENDENCY_NAME}_Load_dep_via_clean_build $OPTVER
            ;;
        *) 
            echo "# Unknown Load Method argument '$OPTLOADMETHOD', will not build/Install $DEPENDENCY_NAME"
            ;;
    esac
}    

###################################################

# Load via modules
Zoltan_Load_dep_via_modules() {
    OPTVER=$1
    
    echo "RUNNING ${DEPENDENCY_NAME}_Load_dep_via_modules() with version $OPTVER"
    
    echo "ERROR: Cannot Build/Install $DEPENDENCY_NAME via modules"
}

###################################################

# Load via deps_build
Zoltan_Load_dep_via_deps_build() {
    OPTVER=$1
    
    echo "RUNNING ${DEPENDENCY_NAME}_Load_dep_via_deps_build() with version $OPTVER"

    case "$OPTVER" in
        default|3.8) # build default Zoltan
            echo "# (default) 3.8: will build Zoltan 3.8"
            . ${SST_DEPS_BIN}/sstDep_zoltan_3.8.sh
            ;;
        3.83) # build Zoltan 3.83
            echo "#  will build Zoltan 3.83"
            . ${SST_DEPS_BIN}/sstDep_zoltan_3.83.sh
            ;;
        3.2) # build default Zoltan
            echo "#  will build Zoltan 3.2"
            . ${SST_DEPS_BIN}/sstDep_zoltan_3.2.sh
            ;;
        none) # do not build (explicit)
            echo "# none: will not build Zoltan"
            ;;
        *) # unknown Zoltan argument
            echo "# Unknown argument '$OPTVER', will not build Zoltan"
            ;;
    esac
    
    # Stage the Build
    sstDepsStage_zoltan

#    # Patch the Build (only for specific versions)
#    sstDepsPatch_zoltan
    
    # Deploy the Build
    sstDepsDeploy_zoltan    
}

###################################################

# Load via modules
Zoltan_Load_dep_via_clean_build() {
    OPTVER=$1
    
    echo "RUNNING ${DEPENDENCY_NAME}_Load_dep_via_clean_build() with version $OPTVER"
    
    echo "ERROR: Cannot Build/Install $DEPENDENCY_NAME via clean_build"
}

###################################################

