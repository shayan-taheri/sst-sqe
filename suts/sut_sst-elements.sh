###################################################
## sst-sqe Build/Test Software Under Test (SUT)
###################################################
# This SUT file provides description on how
# to build/install the sst-elements software on the test 
# machine.
###################################################

SUT_NAME="sst-elements"

echo "DEBUG: INSIDE FILE $SUT_NAME"

# Identify the Loading Subroutine for this dependancy
# This is the name of a subroutine in this file with a unique name
# that will be called to build/install the dependancy.
SUT_LOAD_FCN="Load_sut_sst-elements"
