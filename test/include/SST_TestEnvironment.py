#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import Python System Level Modules
import os
import sys
import subprocess

###############################################################################
# Support Routines
###############################################################################

def DEBUG_dump_sstenv(prefix):
    print "{0} os.environ =".format(prefix)
    envlistsorted = sorted(os.environ)
    for k in envlistsorted:
        if "SST" in k:
            print "   {0} = {1}".format(k, os.environ[k])

def run_quick_shell_cmd(cmdline):
    # turn the command line into a list
    cmd_param_list = cmdline.split()
    shelloutput = subprocess.Popen(cmd_param_list, stdout=subprocess.PIPE).communicate()[0]    
    return shelloutput

def is_env_var_set(envVar):
    try:
        envVar = os.environ["envVar"]
        return True
    except KeyError:
        return False

def get_env_var_value(envVar):
    try:
        envVar = os.environ["envVar"]
        return envVar
    except KeyError:
        return None

def set_env_var_value(envVar, newVal):
    os.environ["envVar"] = newVal


###############################################################################
###############################################################################
###############################################################################
# THE CODE BELOW IS RUN ON MODULE LOAD.  It Sets a number of variables related
# to the module that are environment variables used during the test run
###############################################################################
###############################################################################
###############################################################################

#print "DEBUG - Initialize Test System Environment"

#DEBUG_dump_sstenv("BEFORE")

###############################################################################
# Get and Check HOME Environment Variable

# Check to see HOME has been set.  If not found then exit
try:
    HOME = os.environ["HOME"]
except KeyError:
    print " ****** ERROR: Can not find environment variable $HOME ******"
    sys.exit(1)

# Validate the SST_ROOT path 
if os.path.exists(HOME) == False:
    print " ****** ERROR: Can not locate directory for $HOME ******"
    print " ******        Illegal Directory = {0}".format(HOME)
    sys.exit(1)

###############################################################################
# Get and Check PATH Environment Variable

# Check to see PATH has been set, if not exit
try:
    PATH = os.environ["PATH"]
except KeyError:
    print " ****** ERROR: Can not find environment variable $PATH ******"
    sys.exit(1)

###############################################################################
# Check and/or set SST_ROOT Environment Variable
# This is the root of all the SST FILES

# Check to see SST_ROOT has been set.  If not then assume that SST_ROOT is 
# 3 Levels up from this file (SST_TestEnvironment.py) and then down to trunk
try:
    SST_ROOT = os.environ["SST_ROOT"]
except KeyError:
    this_file_path = os.path.dirname(os.path.realpath(__file__))
    SST_ROOT = os.path.normpath(this_file_path + "/../../../trunk")
    os.environ["SST_ROOT"] = SST_ROOT

# Validate the SST_ROOT path 
if os.path.exists(SST_ROOT) == False:
    print " ****** ERROR: Can not locate directory for $SST_ROOT ******"
    print " ******        Illegal Directory = {0}".format(SST_ROOT)
    sys.exit(1)

###############################################################################
# Check and/or set SST_TEST_INSTALL_BIN Environment Variable
# This is the SST installation preferences

# First see if the environment variables are populated, if not set var to None
try:
    SST_INSTALL_BIN_USER = os.environ["SST_INSTALL_BIN_USER"]
except KeyError:
    SST_INSTALL_BIN_USER = None

try:
    SST_INSTALL_BIN = os.environ["SST_INSTALL_BIN"]
except KeyError:
    SST_INSTALL_BIN = None

#print "DEBUG SST_INSTALL_BIN_USER = {0}".format(SST_INSTALL_BIN_USER)
#print "DEBUG SST_INSTALL_BIN = {0}".format(SST_INSTALL_BIN)

# Check to see SST_INSTALL_BIN_USER has been set.  
if SST_INSTALL_BIN_USER != None:
    # Let user's environment determine value
    # Since SST_INSTALL_BIN_USER is populated, 
    # let it detirmine the value of SST_TEST_INSTALL_BIN
    SST_TEST_INSTALL_BIN = SST_INSTALL_BIN_USER
    os.environ["SST_TEST_INSTALL_BIN"] = SST_TEST_INSTALL_BIN
elif SST_INSTALL_BIN != None:
    # Since SST_INSTALL_BIN is populated and the user has not specified an 
    # override via SST_INSTALL_BIN_USER let SST_INSTALL_BIN detirmine the value
    # of SST_TEST_INSTALL_BIN
    SST_TEST_INSTALL_BIN = SST_INSTALL_BIN
    os.environ["SST_TEST_INSTALL_BIN"] = SST_TEST_INSTALL_BIN
else:
    # Neither SST_INSTALL_BIN or SST_INSTALL_BIN_USER has been set, try to 
    # set SST_TEST_INSTALL_BIN relative to SST_ROOT
    SST_TEST_INSTALL_BIN = os.path.normpath(SST_ROOT + "/../../local/bin")
    os.environ["SST_TEST_INSTALL_BIN"] = SST_TEST_INSTALL_BIN
    
# Validate the SST_TEST_INSTALL_BIN path 
if os.path.exists(SST_TEST_INSTALL_BIN) == False:
    print " ****** ERROR: Can not locate directory for SST_TEST_INSTALL_BIN ******"
    print " ******        Illegal Directory = {0}".format(SST_TEST_INSTALL_BIN)
    sys.exit(1)

###############################################################################
# Check and/or set SST_TEST_INSTALL_PACKAGES Environment Variable
# Find location of SST externals installation

# Check to see SST_TEST_INSTALL_PACKAGES has been set. If Not then set it to
# a reasonable location
try:
    SST_TEST_INSTALL_PACKAGES = os.environ["SST_TEST_INSTALL_PACKAGES"]
except KeyError:
    SST_TEST_INSTALL_PACKAGES = os.path.normpath(SST_TEST_INSTALL_BIN + "/../packages")
    os.environ["SST_TEST_INSTALL_PACKAGES"] = SST_TEST_INSTALL_PACKAGES

## Validate the SST_TEST_INSTALL_PACKAGES path 
#if os.path.exists(SST_TEST_INSTALL_PACKAGES) == False:
#    print " ****** ERROR: Can not locate directory for $SST_TEST_INSTALL_PACKAGES ******"
#    print " ******        Illegal Directory = {0}".format(SST_TEST_INSTALL_PACKAGES)
#    sys.exit(1)

###############################################################################
# Check and/or set SST_TEST_ROOT Environment Variable
# Location of test directory in SVN tree

# Check to see SST_TEST_ROOT has been set. If Not then set it to
# a reasonable location

try:
    SST_TEST_ROOT = os.environ["SST_TEST_ROOT"]
except KeyError:
    SST_TEST_ROOT = os.path.normpath(SST_ROOT + "/test")
    os.environ["SST_TEST_ROOT"] = SST_TEST_ROOT

# Validate the SST_TEST_ROOT path 
if os.path.exists(SST_TEST_ROOT) == False:
    print " ****** ERROR: Can not locate directory for $SST_TEST_ROOT ******"
    print " ******        Illegal Directory = {0}".format(SST_TEST_ROOT)
    sys.exit(1)

###############################################################################
# Set Many more SST_XXX Environment Variables based upon the above vars

# Location of Where elements live within sst-elements 
SST_TEST_ELEMENTS_SRC = os.path.normpath(SST_ROOT + "/sst-elements/src/sst/elements")
os.environ["SST_TEST_ELEMENTS_SRC"] = SST_TEST_ELEMENTS_SRC

# Location of various test driver include files
#export SST_TEST_INCLUDE=${SST_TEST_ROOT}/include
SST_TEST_INCLUDE = os.path.normpath(SST_TEST_ROOT + "/include")
os.environ["SST_TEST_INCLUDE"] = SST_TEST_INCLUDE

# Location of test suite scripts
#export SST_TEST_SUITES=${SST_TEST_ROOT}/testSuites
SST_TEST_SUITES = os.path.normpath(SST_TEST_ROOT + "/testSuites")
os.environ["SST_TEST_SUITES"] = SST_TEST_SUITES

# Location of reference files; SUT output files will be compared against 
# files in this directory
#export SST_TEST_REFERENCE=${SST_TEST_ROOT}/testReferenceFiles
SST_TEST_REFERENCE = os.path.normpath(SST_TEST_ROOT + "/testReferenceFiles")
os.environ["SST_TEST_REFERENCE"] = SST_TEST_REFERENCE

# Location of miscellaneous SUT input files, if needed
#export SST_TEST_INPUTS=${SST_TEST_ROOT}/testInputFiles
SST_TEST_INPUTS = os.path.normpath(SST_TEST_ROOT + "/testInputFiles")
os.environ["SST_TEST_INPUTS"] = SST_TEST_INPUTS

# Location of SDL input files, if needed
#export SST_TEST_SDL_FILES=${SST_TEST_INPUTS}/testSdlFiles
SST_TEST_SDL_FILES = os.path.normpath(SST_TEST_INPUTS + "/testSdlFiles")
os.environ["SST_TEST_SDL_FILES"] = SST_TEST_SDL_FILES

# Location of various temporary SUT input files
#export SST_TEST_INPUTS_TEMP=${SST_TEST_INPUTS}/testInputsTemporary
SST_TEST_INPUTS_TEMP = os.path.normpath(SST_TEST_INPUTS + "/testInputsTemporary")
os.environ["SST_TEST_INPUTS_TEMP"] = SST_TEST_INPUTS_TEMP

# Location where SUT output files will be placed
#export SST_TEST_OUTPUTS=${SST_TEST_ROOT}/testOutputs
SST_TEST_OUTPUTS = os.path.normpath(SST_TEST_ROOT + "/testOutputs")
os.environ["SST_TEST_OUTPUTS"] = SST_TEST_OUTPUTS

# Location where XML test reports will be placed for Bamboo
#export SST_TEST_RESULTS=${SST_TEST_ROOT}/test-reports
SST_TEST_RESULTS = os.path.normpath(SST_TEST_ROOT + "/test-reports")
os.environ["SST_TEST_RESULTS"] = SST_TEST_RESULTS

# Location of test utility scripts
#export SST_TEST_UTILITIES=${SST_TEST_ROOT}/utilities
SST_TEST_UTILITIES = os.path.normpath(SST_TEST_ROOT + "/utilities")
os.environ["SST_TEST_UTILITIES"] = SST_TEST_UTILITIES

###  # Location of shunit2 root
###  #export SHUNIT2_ROOT=${SST_TEST_UTILITIES}/shunit2 #link to actual shunit2 dir
###  SHUNIT2_ROOT = os.path.normpath(SST_TEST_UTILITIES + "/shunit2")
###  os.environ["SHUNIT2_ROOT"] = SHUNIT2_ROOT
###  
###  # Location of shunit2 source files
###  #export SHUNIT2_SRC=${SHUNIT2_ROOT}/src
###  SHUNIT2_SRC = os.path.normpath(SHUNIT2_ROOT + "/src")
###  os.environ["SHUNIT2_SRC"] = SHUNIT2_SRC

# Adjust path for Bamboo install preferences
#export PATH=${PATH}:/usr/local/bin
PATH = PATH + ":/usr/local/bin"
os.environ["PATH"] = PATH

# Location of external test files
#export SST_TEST_EXTERNAL_INPUT_FILES=${HOME}/sstDeps/test/inputFiles
SST_TEST_EXTERNAL_INPUT_FILES = os.path.normpath(HOME + "/sstDeps/test/inputFiles")
os.environ["SST_TEST_EXTERNAL_INPUT_FILES"] = SST_TEST_EXTERNAL_INPUT_FILES

# Location of external test input files for prospero
#export SST_TEST_EXTERNAL_INPUT_FILES_PROSPERO=${SST_TEST_EXTERNAL_INPUT_FILES}/prospero
SST_TEST_EXTERNAL_INPUT_FILES_PROSPERO = os.path.normpath(SST_TEST_EXTERNAL_INPUT_FILES + "/prospero")
os.environ["SST_TEST_EXTERNAL_INPUT_FILES_PROSPERO"] = SST_TEST_EXTERNAL_INPUT_FILES_PROSPERO

#print "DEBUG - HOME                      = {0}".format(HOME)
#print "DEBUG - PATH                      = {0}".format(PATH)
#print "DEBUG - SST_ROOT                  = {0}".format(SST_ROOT)
#print "DEBUG - SST_INSTALL_BIN_USER      = {0}".format(SST_INSTALL_BIN_USER)
#print "DEBUG - SST_TEST_INSTALL_PACKAGES = {0}".format(SST_TEST_INSTALL_PACKAGES)
#print "DEBUG - SST_TEST_ROOT             = {0}".format(SST_TEST_ROOT)
#print "DEBUG - SST_TEST_INSTALL_BIN      = {0}".format(SST_TEST_INSTALL_BIN)
#print "DEBUG - SST_TEST_OUTPUTS          = {0}".format(SST_TEST_OUTPUTS)
#print "DEBUG - SST_TEST_REFERENCE        = {0}".format(SST_TEST_REFERENCE)
#print "DEBUG - SST_TEST_RESULTS          = {0}".format(SST_TEST_RESULTS)

###############################################################################
###############################################################################
###############################################################################

# Get the information on the HOST OS
SST_TEST_HOST_OS_KERNEL = run_quick_shell_cmd("uname -s").strip('\n')
SST_TEST_HOST_OS_KERNEL_VERSION = run_quick_shell_cmd("uname -r").strip('\n')
SST_TEST_HOST_OS_KERNEL_ARCH = run_quick_shell_cmd("uname -p").strip('\n')

# Init the Distrib Variables
SST_TEST_HOST_OS_DISTRIB_MACOS = 0
SST_TEST_HOST_OS_DISTRIB_CENTOS = 0
SST_TEST_HOST_OS_DISTRIB_TOSS = 0
SST_TEST_HOST_OS_DISTRIB_UBUNTU = 0
SST_TEST_HOST_OS_UNKNOWN = 0

# Get distrib and version
if SST_TEST_HOST_OS_KERNEL == "Darwin":
    # This is Darwin. Always check for Darwin first, since the checks
    # for Linux platform information contin GNU-isms that may not be
    # supported on MacOS
    SST_TEST_HOST_OS_DISTRIB = "MacOS"
    SST_TEST_HOST_OS_DISTRIB_VERSION = run_quick_shell_cmd("sw_vers -productVersion").strip('\n')
    SST_TEST_HOST_OS_DISTRIB_MACOS = 1

elif os.path.exists("/etc/centos-release") == True:
    # The presence of this file means this is CentOS, a Red Hat derivative
    SST_TEST_HOST_OS_DISTRIB = run_quick_shell_cmd('cut -d " " -f1 /etc/centos-release').strip('\n')
    SST_TEST_HOST_OS_DISTRIB_VERSION = run_quick_shell_cmd('cut -d " " -f3 /etc/centos-release').strip('\n')
    SST_TEST_HOST_OS_DISTRIB_CENTOS = 1

elif os.path.exists("/etc/toss-release") == True:
    # The presence of this file means this is TOSS, a Red Hat derivative
    SST_TEST_HOST_OS_DISTRIB = run_quick_shell_cmd("cat /etc/toss-release | sed 's|\([^-]\+\)\(-release.*\)|\1|'").strip('\n')
    SST_TEST_HOST_OS_DISTRIB_VERSION = run_quick_shell_cmd("cat /etc/toss-release | sed 's|toss-release-\(.\+\)|\1|'").strip('\n')
    SST_TEST_HOST_OS_DISTRIB_TOSS = 1

elif os.path.exists("/etc/lsb-release") == True:
    # The presence of this file (after checking for
    # distribution-specific platform information files) indicates an
    # attempt at Linux Standards Base (LSB) compliance.

    # Always check for distribution-specific platform information
    # files before checking for /etc/lsb-release, as a distribution
    # may contain both, and distribution-specific platform files
    # typically contain more detailed information.

    # !!! It seems there is no agreement on the content and format of
    # !!! the "lsb-release" file! The following logic is only known to
    # !!! work on Ubuntu's "lsb-release" file.

    SST_TEST_HOST_OS_DISTRIB = run_quick_shell_cmd("cat /etc/lsb-release | egrep DISTRIB_ID | sed 's|\(^DISTRIB_ID=\)\(.\+\)|\2|'").strip('\n')
    SST_TEST_HOST_OS_DISTRIB_VERSION = run_quick_shell_cmd("cat /etc/lsb-release | egrep DISTRIB_RELEASE | sed 's|\(^DISTRIB_RELEASE=\)\(.\+\)|\2|'").strip('\n')
    if SST_TEST_HOST_OS_DISTRIB == "Ubuntu":
        # Set this if this is Ubuntu, a Debian derivative
        SST_TEST_HOST_OS_DISTRIB_UBUNTU = 1

        # Of course, add other LSB-compliant Linuxes here...
    else:
        SST_TEST_HOST_OS_UNKNOWN = 1
else:
    # worst case
    SST_TEST_HOST_OS_DISTRIB = "unknown"
    SST_TEST_HOST_OS_DISTRIB_VERSION = "unknown"
    SST_TEST_HOST_OS_DISTRIB_UNKNOWN = 1

# Add them to the environment
os.environ["SST_TEST_HOST_OS_KERNEL"]          = SST_TEST_HOST_OS_KERNEL
os.environ["SST_TEST_HOST_OS_KERNEL_VERSION"]  = SST_TEST_HOST_OS_KERNEL_VERSION
os.environ["SST_TEST_HOST_OS_KERNEL_ARCH"]     = SST_TEST_HOST_OS_KERNEL_ARCH
os.environ["SST_TEST_HOST_OS_DISTRIB"]         = SST_TEST_HOST_OS_DISTRIB
os.environ["SST_TEST_HOST_OS_DISTRIB_VERSION"] = SST_TEST_HOST_OS_DISTRIB_VERSION
os.environ["SST_TEST_HOST_OS_DISTRIB_MACOS"]   = str(SST_TEST_HOST_OS_DISTRIB_MACOS   )
os.environ["SST_TEST_HOST_OS_DISTRIB_CENTOS"]  = str(SST_TEST_HOST_OS_DISTRIB_CENTOS  )
os.environ["SST_TEST_HOST_OS_DISTRIB_TOSS"]    = str(SST_TEST_HOST_OS_DISTRIB_TOSS    )
os.environ["SST_TEST_HOST_OS_DISTRIB_UBUNTU"]  = str(SST_TEST_HOST_OS_DISTRIB_UBUNTU  )
os.environ["SST_TEST_HOST_OS_UNKNOWN"]         = str(SST_TEST_HOST_OS_UNKNOWN         )
 
#print "DEBUG - SST_TEST_HOST_OS_KERNEL          = {0}".format(SST_TEST_HOST_OS_KERNEL)
#print "DEBUG - SST_TEST_HOST_OS_KERNEL_VERSION  = {0}".format(SST_TEST_HOST_OS_KERNEL_VERSION)
#print "DEBUG - SST_TEST_HOST_OS_KERNEL_ARCH     = {0}".format(SST_TEST_HOST_OS_KERNEL_ARCH)
#print "DEBUG - SST_TEST_HOST_OS_DISTRIB         = {0}".format(SST_TEST_HOST_OS_DISTRIB)
#print "DEBUG - SST_TEST_HOST_OS_DISTRIB_VERSION = {0}".format(SST_TEST_HOST_OS_DISTRIB_VERSION)
#print "DEBUG - SST_TEST_HOST_OS_DISTRIB_MACOS   = {0}".format(SST_TEST_HOST_OS_DISTRIB_MACOS)
#print "DEBUG - SST_TEST_HOST_OS_DISTRIB_CENTOS  = {0}".format(SST_TEST_HOST_OS_DISTRIB_CENTOS)
#print "DEBUG - SST_TEST_HOST_OS_DISTRIB_TOSS    = {0}".format(SST_TEST_HOST_OS_DISTRIB_TOSS)
#print "DEBUG - SST_TEST_HOST_OS_DISTRIB_UBUNTU  = {0}".format(SST_TEST_HOST_OS_DISTRIB_UBUNTU)
#print "DEBUG - SST_TEST_HOST_OS_UNKNOWN         = {0}".format(SST_TEST_HOST_OS_UNKNOWN)

#DEBUG_dump_sstenv("AFTER")

###############################################################################
###############################################################################
###############################################################################

