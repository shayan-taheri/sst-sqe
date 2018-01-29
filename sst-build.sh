#-------------------------------------------------------------------------
# Main - Main execution of the script - Called by script init (at bottom)
# $1 = <Name of this script>
# $2 = Build Scenario
#-------------------------------------------------------------------------
Main() {
    # Give the name of this script
    echo "Running Script $1 $2"
    echo "" 
    
    ## Save the Scenario Name into a var
    SCENARIO_NAME=$2
    
    # First figure out where we are running from and then setup some paths
    # Root of directory checked out, where this script should be found
    export WORKING_DIR=`pwd`
    export SQE_ROOT="$( cd "$( dirname "${1}" )" && pwd )"
    export SST_ROOT=$SQE_ROOT
    echo "WORKING_DIR = $WORKING_DIR"
    echo "SQE_ROOT = $SQE_ROOT"
    echo "SST_ROOT = $SST_ROOT"
    echo "" 
    
    ## Lets go into the SQE Directory for awhile
    echo "CHANGE TO SQE DIRECTORY @ $SQE_ROOT" 
    pushd $SQE_ROOT
    echo "" 
    
    echo "NOW WORKING IN SQE DIRECTORY @ `pwd`" 
    echo "Directory Contents:" 
    ls -la
    echo "" 
    
    SQE_SHA=`git rev-parse --short HEAD`
    SQE_BRANCH=`git rev-parse --abbrev-ref HEAD`
    echo "SQE VERSION INFORMATION:" 
    echo "SQE SHA    = $SQE_SHA"
    echo "SQE BRANCH = $SQE_BRANCH"
    echo ""

    ## Setup the Environment Paths and load various support files
    SetupEnvironment

    echo "PLATFORM INFORMATION"
    echo "KERNEL   = $SST_DEPS_OS_NAME"
    echo "CPU_ARCH = $SST_DEPS_CPU_ARCH"
    echo "OS_REL   = $SST_DEPS_OS_RELEASE"
    echo ""    

    # Dump the Environment that we have at the moment
## TODO: TURN THIS BACK ON    
###    DumpEnvironment "INITIAL"
    
    ############################################################################
    ## Load the Scenario 
    echo ""
    echo "############################################################################"
    echo "Loading the Scenario File"
    LoadSupportFile $SCENARIO_NAME "$SQE_ROOT/scenarios/" "scenario_" "scenario"
    echo ""
    echo ""

    ############################################################################
    # Load the Dependancy files
    echo ""
    echo "############################################################################"
    echo "Loading the Dependancy Files"
    echo ""
    echo "The Number of Dependancys to Load in Scenario $SCENARIO_NAME = $SCENARIO_NUM_DEPENCENCY"
    echo ""
    count=1 
    while [  $count -le $SCENARIO_NUM_DEPENCENCY ]; do
        echo ""
        echo "Loading DEPENCENCY #$count -- ${SCENARIO_DEPENCENCY_NAME[$count]} Version ${SCENARIO_DEPENCENCY_VER[$count]}"
        echo ""
        DEPENDANCY_LOAD_FCN=""
        LoadSupportFile ${SCENARIO_DEPENCENCY_NAME[$count]} "$SQE_ROOT/dependencies" "dep_" "dependancy"
        ## Get the name of the load function from the dependancy file
        SCENARIO_DEPENCENCY_LOAD_FCN[$count]=$DEPENDANCY_LOAD_FCN
        let count=count+1 
    done    
    
    ############################################################################
    # Load the SUT files
    echo ""
    echo "############################################################################"
    echo "Loading the SUT Files"
    echo ""
    echo "The Number of SUT's to Load in Scenario $SCENARIO_NAME = $SCENARIO_NUM_SUTS"
    echo ""
    count=1 
    while [  $count -le $SCENARIO_NUM_SUTS ]; do
        echo ""
        echo "Loading SUT #$count -- ${SCENARIO_SUT_NAME[$count]}"
        echo ""
        SUT_LOAD_FCN=""
        LoadSupportFile ${SCENARIO_SUT_NAME[$count]} "$SQE_ROOT/suts" "sut_" "SUT"
        ## Get the name of the load function from the sut file
        SCENARIO_SUT_LOAD_FCN[$count]=$SUT_LOAD_FCN
        let count=count+1 
    done    

    ############################################################################
    # Execute each actual Build / Install function in the dependancy file
    echo ""
    echo "############################################################################"
    echo "Performing the Build/Install function for the Dependancy Files"
    count=1 
    while [  $count -le $SCENARIO_NUM_DEPENCENCY ]; do
        if [[ ${SCENARIO_DEPENCENCY_LOAD_FCN[$count]} != "" ]]; then 
            echo ""
            echo "Building / Installing Dependancy #$count -- ${SCENARIO_DEPENCENCY_NAME[$count]} Version ${SCENARIO_DEPENCENCY_VER[$count]}"
            echo ""
            ## Run the load function defined by the dependancy file
            ${SCENARIO_DEPENCENCY_LOAD_FCN[$count]} ${SCENARIO_DEPENCENCY_VER[$count]}
            ret_code=$?
            if [ $ret_code -ne 0 ] ; then
                echo "ERROR: Failed call to function ${SCENARIO_DEPENCENCY_LOAD_FCN[$count]}"
                exit 1
            fi    
        else 
            echo ""
            echo "ERROR: Unable to call Load Function for ${SCENARIO_DEPENCENCY_NAME[$count]}; Is it defined correctly in the dependancy file?"
            exit 1
        fi     
        let count=count+1 
    done    
    
    
    
    echo ""
    echo ""
    echo ""
    echo "######################################"
    echo "### SCRIPT FINISHED WITH NO ERRORS ###"    
    echo "######################################"
}

#-------------------------------------------------------------------------
# Function: ScriptExitHandler
# Trap the exit command and perform end of script processing.
#-------------------------------------------------------------------------
ScriptExitHandler() {
    echo ""
    echo ""
    echo ""
    echo "SCRIPT FINISHED...."
    ## Exit back to the working dir
    echo "RETURING TO WORKING DIRECTORY @ $WORKING_DIR" 
    popd
    echo ""
}

#-------------------------------------------------------------------------
# Function: ScriptErrorHandler
# Trap the exit command and perform end of script processing.
#-------------------------------------------------------------------------
ScriptErrorHandler() {
    echo "ERROR ERROR ERROR in script ERROR ERROR ERROR ...."
    ## PUT ANY SCRIPT EXIT CODE HERE
    errcode=$? # save the exit code as the first thing done in the trap function
    echo "error $errorcode"
    echo "the command executing at the time of the error was"
    echo "$BASH_COMMAND"
    echo "on line ${BASH_LINENO[0]}"
    # do some error handling, cleanup, logging, notification
    # $BASH_COMMAND contains the command that was being executed at the time of the trap
    # ${BASH_LINENO[0]} contains the line number in the script of that command
    # exit the script or return to try again, etc.
    exit $errcode  # or use some other value or do return instead}
}

#-------------------------------------------------------------------------
# LoadSupportFile - Function to setup environment for build/testing
#                    and load any support files.
# $1 = Name to load
# $2 = File Path
# $3 = File Prefix
# $4 = Type Of File
#-------------------------------------------------------------------------
LoadSupportFile() {
    ## Save the Scenario Name into a var
    FILE_NAME=$1
    FILE_PATH=$2
    FILE_PREFIX=$3
    FILE_TYPE_STR=$4

    ## Load all the Scenario Files and make them available
    ## Load the Build/Test Scenario into the system
    echo "Looking for $FILE_TYPE_STR file with name $FILE_NAME"
    found_file=0
    for s_filename in $( ls $FILE_PATH/$FILE_PREFIX*.sh ); do
        basename=$(basename $s_filename)
        #echo "Debug: Found file $s_filename; basename = $basename"
        if [ "$FILE_PREFIX$FILE_NAME.sh" == $basename ]; then
            echo "Loading $FILE_TYPE_STR File $s_filename..."
            . $s_filename
            found_file=1
        fi
    done
    # Check that we loaded a scenario
    if [ $found_file == 0 ]; then
        echo "ERROR: Unable to load $FILE_TYPE_STR $FILE_NAME; NOT FOUND IN $FILE_PATH"
        exit 1
    fi
}
#-------------------------------------------------------------------------
# SetupEnvironment - Function to setup environment for build/testing
#                    and load any support files.
#-------------------------------------------------------------------------
SetupEnvironment() {
    ## Check to see if the user has set a directory for 
    ## where they want to put the installed versions
    echo "IDENTIFY WHERE SST WILL BE INSTALLED:"
    if [[ ${SST_DEPS_USER_MODE:+isSet} = isSet ]]
    then
        export SST_BASE=$SST_DEPS_USER_DIR
    else
        export SST_BASE=$HOME
    fi
    
    # Location of SST library dependencies (deprecated)
    export SST_DEPS=${SST_BASE}/local
    # Starting Location where SST files are installed
    export SST_INSTALL=${SST_BASE}/local

    echo "SST_BASE    = $SST_BASE"
    echo "SST_INSTALL = $SST_INSTALL"
    echo "this can be changed by setting environment:"
    echo "  'export SST_DEPS_USER_MODE=1'"
    echo "  'export SST_DEPS_USER_DIR=<path>'"
    echo ""
    
    
##    # Location where SST CORE files are installed
##    export SST_CORE_INSTALL=${SST_INSTALL}/sst-core
##    # Location where SST CORE build files are installed
##    export SST_CORE_INSTALL_BIN=${SST_CORE_INSTALL}/bin
##    
##    # Location where SST ELEMENTS files are installed
##    export SST_ELEMENTS_INSTALL=${SST_INSTALL}/sst-elements
##    # Location where SST ELEMENTS build files are installed
##    export SST_ELEMENTS_INSTALL_BIN=${SST_ELEMENTS_INSTALL}/bin
##    
##    # Location where SST MACRO files are installed
##    export SST_MACRO_INSTALL=${SST_INSTALL}/sst-macro
##    
##    # Final Location where SST executable files are installed
##    export SST_INSTALL=${SST_CORE_INSTALL}
##    # Location where SST build files are installed
##    export SST_INSTALL_BIN=${SST_CORE_INSTALL_BIN}
##    
##    # Setup the Location to find the sstsimulator.conf file
##    export SST_CONFIG_FILE_PATH=${SST_CORE_INSTALL}/etc/sst/sstsimulator.conf
##    
##    
##    # Location where SST dependencies are installed. This only specifies
##    # the root; dependencies may be installed in various locations under
##    # this directory. The user can override this value by setting the
##    # exporting the SST_INSTALL_DEPS_USER variable in their environment.
##    export SST_INSTALL_DEPS=${SST_BASE}/local
##    # Initialize build type to null
##    export SST_BUILD_TYPE=""

    echo "LOADING THE SQE depsDefinitions.sh FILE"
    #ls buildsys/deps/include
    # Load dependency definitions
    . buildsys/deps/include/depsDefinitions.sh
    echo ""
}

#-------------------------------------------------------------------------
# DumpEnvironment - Function to display the current environment settings
# $1 = <Name of the dump>
#-------------------------------------------------------------------------
DumpEnvironment() {
    echo "============================== $1 ENVIRONMENT DUMP STARTING ================="
    env|sort
    echo "============================== $1 ENVIRONMENT DUMP FINISHED ================="
    echo ""
}

function setupdefinitions {
    #=========================================================================
    # Definitions
    #=========================================================================
    
    # Check Environement variables that control what Repo and branch we are planning
    # to use.  Most of the time the defaults are used, but by setting the Environment
    # variables, we can control what (and from where) files are pulled.
    # This feature is critical for the autotesters as files may come from a different 
    # branch and/or fork
    
    # Which Repository to use for SQE (default is https://github.com/sstsimulator/sst-sqe)
    if [[ ${SST_SQEREPO:+isSet} != isSet ]] ; then
        SST_SQEREPO=https://github.com/sstsimulator/sst-sqe
    fi
    
    # Which Repository to use for CORE (default is https://github.com/sstsimulator/sst-core)
    if [[ ${SST_COREREPO:+isSet} != isSet ]] ; then
        SST_COREREPO=https://github.com/sstsimulator/sst-core
    fi
    
    # Which Repository to use for ELEMENTS (default is https://github.com/sstsimulator/sst-elements)
    if [[ ${SST_ELEMENTSREPO:+isSet} != isSet ]] ; then
        SST_ELEMENTSREPO=https://github.com/sstsimulator/sst-elements
    fi
    
    # Which Repository to use for MACRO (default is https://github.com/sstsimulator/sst-macro)
    if [[ ${SST_MACROREPO:+isSet} != isSet ]] ; then
        SST_MACROREPO=https://github.com/sstsimulator/sst-macro
    fi
    
    # Which Repository to use for EXTERNAL-ELEMENT (default is https://github.com/sstsimulator/sst-external-element)
    if [[ ${SST_EXTERNALELEMENTREPO:+isSet} != isSet ]] ; then
        SST_EXTERNALELEMENTREPO=https://github.com/sstsimulator/sst-external-element
    fi
    
    # Which Repository to use for JUNO (default is https://github.com/sstsimulator/juno)
    if [[ ${SST_JUNOREPO:+isSet} != isSet ]] ; then
        SST_JUNOREPO=https://github.com/sstsimulator/juno
    fi
    ###
    
    # Which branches to use for each repo (default is devel)
    if [[ ${SST_SQEBRANCH:+isSet} != isSet ]] ; then
        SST_SQEBRANCH=devel
        SST_SQEBRANCH="detached"
    else
        echo ' ' ;  echo ' ' ; echo ' ' ; echo ' ' 
        echo " Attempting to set SQE branch is a no op"
        echo " SQE branch is selected by configure in Jenkins"
        echo "  Ignoring SST_SQEBRANCH =  ${SST_SQEBRANCH}"
        echo ' ' ;  echo ' ' ; echo ' ' ; echo ' ' 
    fi
                            
    if [[ ${SST_COREBRANCH:+isSet} != isSet ]] ; then
        SST_COREBRANCH=devel
    fi
                            
    if [[ ${SST_ELEMENTSBRANCH:+isSet} != isSet ]] ; then
        SST_ELEMENTSBRANCH=devel
    fi
    
    if [[ ${SST_MACROBRANCH:+isSet} != isSet ]] ; then
        SST_MACROBRANCH=devel
    fi
    
    if [[ ${SST_EXTERNALELEMENTBRANCH:+isSet} != isSet ]] ; then
        SST_EXTERNALELEMENTBRANCH=master
    fi
    
    if [[ ${SST_JUNOBRANCH:+isSet} != isSet ]] ; then
        SST_JUNOBRANCH=master
    fi
    
    echo "#############################################################"
    echo "===== BAMBOO.SH PARAMETER SETUP INFORMATION ====="
    echo "  GitHub SQE Repository and Branch = $SST_SQEREPO $SST_SQEBRANCH"
    echo "  GitHub CORE Repository and Branch = $SST_COREREPO $SST_COREBRANCH"
    echo "  GitHub ELEMENTS Repository and Branch = $SST_ELEMENTSREPO $SST_ELEMENTSBRANCH"
    echo "  GitHub MACRO Repository and Branch = $SST_MACROREPO $SST_MACROBRANCH"
    echo "  GitHub EXTERNAL-ELEMENT Repository and Branch = $SST_EXTERNALELEMENTREPO $SST_EXTERNALELEMENTBRANCH"
    echo "  GitHub JUNO Repository and Branch = $SST_JUNOREPO $SST_JUNOBRANCH"
    echo "#############################################################"
}


other_stuff() {
    
##    cloneOtherRepos 
    
    
        case $1 in
            default|sstmainline_config|sstmainline_config_linux_with_ariel_no_gem5|sstmainline_config_no_gem5|sstmainline_config_static|sstmainline_config_static_no_gem5|sstmainline_config_clang_core_only|sstmainline_config_macosx|sstmainline_config_macosx_no_gem5|sstmainline_config_no_mpi|sstmainline_config_test_output_config|sstmainline_config_memH_Ariel|sstmainline_config_dist_test|sstmainline_config_make_dist_no_gem5|documentation|sstmainline_config_stream|sstmainline_config_openmp|sstmainline_config_diropenmp|sstmainline_config_diropenmpB|sstmainline_config_dirnoncacheable|sstmainline_config_diropenmpI|sstmainline_config_dir3cache|sstmainline_config_all|sstmainline_config_memH_wo_openMP|sstmainline_config_develautotester_linux|sstmainline_config_develautotester_mac|sstmainline_config_valgrind|sstmainline_config_valgrind_ES|sstmainline_config_valgrind_ESshmem|sstmainline_config_valgrind_memHA|sst-macro_withsstcore_mac|sst-macro_nosstcore_mac|sst-macro_withsstcore_linux|sst-macro_nosstcore_linux)
                #   Save Parameters $2, $3 and $4 in case they are need later
                SST_DIST_MPI=$2
                SST_DIST_BOOST=$3
                SST_DIST_PARAM4=$4
    
                # Configure MPI, Boost, and Compiler (Linux only)
                if [ $kernel != "Darwin" ]
                then
                    linuxSetBoostMPI $1 $2 $3 $4 
    
                else  # kernel is "Darwin", so this is MacOS
    
                    darwinSetBoostMPI $1 $2 $3 $4
                fi
           if [[  ${SST_WITHOUT_PIN:+isSet} == isSet ]] ; then
                echo "  This run is forced to be without PIN "
           else
                # if Intel PIN module is available, load 2.14 version
                #           ModuleEx puts the avail output on Stdout (where it belongs.)
                ModuleEx avail | egrep -q "pin/pin-2.14-71313"
                if [ $? == 0 ] 
                then
                # if `pin module is available, use 2.14.
                    if [ $kernel != "Darwin" ] ; then
    
                       echo "using Intel PIN environment module  pin-2.14-71313-gcc.4.4.7-linux"
                        #    Compiler is $4
                       if [[ "$4" != gcc-5* ]] ; then
                           echo "Loading Intel PIN environment module"
                           ModuleEx load pin/pin-2.14-71313-gcc.4.4.7-linux
                           echo  $INTEL_PIN_DIRECTORY
                           ls $INTEL_PIN_DIRECTORY
                       else 
                          echo " ################################################################"
                          echo " #"
                          echo " #  pin-2.14-71313-gcc.4.4.7-linux is incompatible with gcc-5.x"
                          echo " #"
                          echo " ################################################################"
                       fi
                    else        ##    MacOS   (Darwin)
                       echo "using Intel PIN environment module  pin-2.14-71313-clang.5.1-mac"
                       echo "Loading Intel PIN environment module"
                       ModuleEx load pin/pin-2.14-71313-clang.5.1-mac
                    fi
                else
                    echo "Intel PIN environment module not found on this host."
                fi
           fi
    
                echo "bamboo.sh: LISTING LOADED MODULES"
                ModuleEx list
    
                # Build type given as argument to this script
                export SST_BUILD_TYPE=$1
    
                if [ $SST_BUILD_TYPE = "documentation" ]
                then
                    # build sst-core documentation, create list of undocumented files
                    echo "Building SST-CORE Doxygen Documentation"
                    pushd $SST_ROOT/sst-core
                    ./autogen.sh
                    ./configure --disable-silent-rules --prefix=$SST_CORE_INSTALL
                    make html 2> ./doc/makeHtmlErrors.txt
                    egrep "is not documented" ./doc/makeHtmlErrors.txt | sort > ./doc/undoc.txt
                    test -d ./doc/html
                    retval=$?
                    if [ $retval -ne 0 ]
                    then
                        echo "HTML directory not found! - Documentation build has failed"
                        exit 1
                    fi
                    popd
                    
                else
                    # Perform the build
                    dobuild -t $SST_BUILD_TYPE -a $arch -k $kernel
                    retval=$?
                    if [[ ${SST_STOP_AFTER_BUILD:+isSet} == isSet ]] ; then
                        if [ $retval -eq 0 ] ; then
                            echo "$0 : exit success."
                        else
                            echo "$0 : exit failure."
                        fi
                        exit $retval
                    fi
                fi
    
                ;;
    
            *)
                echo "$0 : unknown action \"$1\""
                retval=1
                ;;
        esac
##    fi
       
    if [ $retval -eq 0 ]
    then
        if [ $SST_BUILD_TYPE = "documentation" ]
        then
            # dump list of sst-core undocumented files
            echo "============================== SST-CORE DOXYGEN UNDOCUMENTED FILES =============================="
            sed -e 's/^/#doxygen /' ./sst-core/doc/undoc.txt
            echo "============================== SST-CORE DOXYGEN UNDOCUMENTED FILES =============================="
            retval=0
        else
            # Build was successful, so run tests, providing command line args
            # as a convenience. SST binaries must be generated before testing.
    
            if [[ $buildtype == *_dist_* ]] ; then  
                 setUPforMakeDisttest $1 $2 $3 $4
                 exit 0                  #  Normal Exit for make dist
            else          #  not make dist
                #    ---  These are probably temporary, but let's line them up properly anyway
                pwd
                echo "            CHECK ENVIRONMENT VARIABLES "
                env | grep SST
                echo "            End of SST Environs"
                pwd
                ls
                #    ---
                if [ -d "test" ] ; then
                    echo " \"test\" is a directory"
                    echo " ################################################################"
                    echo " #"
                    echo " #         ENTERING dotests  "
                    echo " #"
                    echo " ################################################################"
                    dotests $1 $4
                fi
            fi               #   End of sstmainline_config_dist_test  conditional
        fi
    fi
    date
    
    if [ $retval -eq 0 ]
    then
        echo "$0 : exit success."
    else
        echo "$0 : exit failure."
    fi
    
    exit $retval
}    



#=========================================================================
# Script Entry
# $0 = <Name of this script>
# $1 = Build Scenario
#=========================================================================
# THIS CODE SHOULD ALWAYS BE AT THE BOTTOM OF THE SCRIPT
# Setup a handler to run when the script is finished and/or errors.
trap ScriptExitHandler EXIT
trap ScriptErrorHandler ERR
#set -e

# Check Parameters
if [ $# -lt 1 ] || [ $# -gt 1 ]
then
    echo "Usage : $0 <built/test scenario>"
    exit 0
fi

# Call the main routine with the Build Scenario
Main $0 $1

