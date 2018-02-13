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
    OPTARG=$1
    
    echo "DEBUG: RUNNING Load_dep_goblinhmc() with version $OPTARG"

    case "$OPTARG" in
        default|stabledevel) # build latest Goblin_HMCSIM from repository ("stable development")
            echo "# (default) stabledevel: build latest Goblin_HMCSIM from repository"
            . ${SST_DEPS_BIN}/sstDep_goblin_hmcsim_stabledevel.sh
            ;;
        none) # do not build (explicit)
            echo "# none: will not build Goblin_HMCSIM"
            ;;
        *) # unknown Goblin_HMCSIM argument
            echo "# Unknown argument '$OPTARG', will not build Goblin_HMCSIM"
            ;;
    esac
    
    # Stage the Goblin HMC Sim
    sstDepsStage_goblin_hmcsim

#    # Patch the Goblin HMC Sim
#    sstDepsPatch_goblin_hmcsim
    
    # Deploy the Goblin HMC Sim
    sstDepsDeploy_goblin_hmcsim    
}