# Support functions

#-------------------------------------------------------------------------
# Function: ModuleEx
# Description:
#   Purpose:
#       This funciton is a wrapper Around the moduleex.sh command which wraps the module 
#       command used to load/unload  external dependancies.  All calls to module should be 
#       redirected to this function.  If a failure is detected in the module command, it will be
#       noted and this function will cause the bamboo script to exit with the error code.
#   Input:
#       $@: Variable number of parameters depending upon module command operation
#   Output: Any output from the module command.
#   Return value: 0 on success, On error, bamboo.sh will exit with the moduleex.sh error code.
ModuleEx() {
    # Call (via "source") the moduleex.sh script with the passed in parameters  
    . $SST_ROOT/../utilities/moduleex.sh $@
    # Get the return value from the moduleex.sh
    retval=$?
    if [ $retval -ne 0 ] ; then
        echo "ERROR: 'module' failed via script $SST_ROOT/test/utilities/moduleex.sh with retval= $retval; script exiting"
        exit $retval
    fi
    return $retval  
}

#-------------------------------------------------------------------------
# Function: TimeoutEx
# Description:
#   Purpose:
#       This function is a wrapper Around the TimeoutEx.sh which will execute 
#       a command with a timeout 
#   Input:
#       $@: Variable number of parameters depending upon module command operation
#   Output: Any output from the command being run.
#   Return value: The return value of the command being run or !=0 to indicate 
#   a timeout or error.
TimeoutEx() {
    # Call (via "source") the moduleex.sh script with the passed in parameters  
    $SST_ROOT/../utilities/TimeoutEx.sh $@
    # Get the return value from the TimeoutEx.sh
    return $retval  
}

