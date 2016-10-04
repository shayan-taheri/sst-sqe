#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# TestSuite:
#     testSuite_merlin
# Purpose:
#     Exercise merlin code in SST
# Inputs:
#     None
# Outputs:
#     test_merlin_xxx.out file
# Expected Results
#     Match of output file against reference file
# Caveats:
#     For shunit2, the output files must match the reference file *exactly*,
#     requiring that the command lines for creating both the output
#     file and the reference file be exactly the same.
# Exception for merlin tests:
#     A fuzzy compare has been inserted here.   The only thing that varies is
#     the value of the total Ticks simulated.  With binaries shared from SVN, 
#     there should be no need for fuzziness.  When the static binary is build
#     using compiler and libraries on the host, the exact number of Ticks in the 
#     program may vary from that reported in the reference file checked into SVN.
#
#    Does not use subroutine because it invokes the build of all test binaries.
#-------------------------------------------------------------------------------

###############TO DOS:
# Print name of testsuite at top before running
# Handle the asserts cleanly
# Exclude tests from run all
# allow for run specific tests
# See if Jenkins will process xml file without cdata sections
# Add remaining env code for BUILD_TYPE_USER from testDefinitions.sh
# Handle timout flag in test
#
# ADD Env variable SST_TEST_ONE_TEST_TIMEOUT to test (related to timout monitor code)
# Handle Multi-rank flag
#
###############TO DOS:

# Import Python System Level Modules
import os
import sys
import unittest

# Set the Path to the Included SST Testing Modules
TEST_SUITE_ROOT = os.path.dirname(os.path.realpath(__file__))
SST_TEST_MODULES_PATH = os.path.normpath(TEST_SUITE_ROOT + "/../include")
sys.path.append(SST_TEST_MODULES_PATH)

# Import SST Testing Modules
import SST_TestCase 
import SST_TestEnvironment as Env
import SST_TestSupport as Test

################################################################################
# Test Suite Class
# Note: Tests are run in alphabetical order

class testSuite_merlin(SST_TestCase.SST_TestCase):
    """TEST Merlin"""
    
################################################################################
# Support Routines Run At Startup and Before and After each Test
# Note: These do not have to be defined

    @classmethod
    def setUpClass(self):
        """Top Level setUpClass, called BEFORE ANY tests are run a single time"""
        super(testSuite_merlin, self).setUpClass()  # Call the Base Class Method
        pass
        
    @classmethod
    def tearDownClass(self):
        """Top Level tearDownClass, called AFTER ALL tests are run a single time"""
        super(testSuite_merlin, self).tearDownClass() # Call the Base Class Method
        pass

    def setUp(self):
        """Top Level setUp, called before every test is run"""
        super(testSuite_merlin, self).setUp() # Call the Base Class Method
        pass
        
    def tearDown(self):
        """Top Level tearDown, called after every test is run"""
        super(testSuite_merlin, self).tearDown() # Call the Base Class Method
        pass


################################################################################
# GENERIC TEST TEMPLATE 

#===============================================================================
#                       TEMPLATE
#     Subroutine to run many similiar tests without reproducing the script.
#     First parameter is the name of the test, must match test_merlin_<name>()
#     Second parameter is the execution cycle tolerance in hundredths of a
#     percent.   (5% therefore is 500.)

    def merlin_Template(self, merlin_case, Tol):

        # Define a common basename for test output and reference files
        # XML postprocessing requires this.
#        startSeconds=`date +%s`
        testDataFileBase = "{0}_{1}".format("test_merlin", merlin_case)
        outFile ="{0}/{1}.out".format(Env.SST_TEST_OUTPUTS, testDataFileBase)
        newOut ="{0}/{1}.newout".format(Env.SST_TEST_OUTPUTS, testDataFileBase)
        newRef ="{0}/{1}.newref".format(Env.SST_TEST_OUTPUTS, testDataFileBase)
        testOutFiles ="{0}/{1}.testFile".format(Env.SST_TEST_OUTPUTS, testDataFileBase)
        referenceFile = "{0}/{1}.out".format(Env.SST_TEST_REFERENCE, testDataFileBase)

        # Define Software Under Test (SUT) and its runtime arguments
        sut = "{0}/sst".format(Env.SST_TEST_INSTALL_BIN)
        sutArgs = "{0}/merlinSdls/{1}.py".format(Env.SST_TEST_SDL_FILES, merlin_case)
        
        # Check that the merlin python file exists
        if not Test.does_file_exist(sutArgs):  # Must check first as assert 
            Test.list_file_directory(sutArgs)
        self.assertTrue(Test.does_file_exist(sutArgs), "Error: Cannot find file {0}".format(sutArgs))
        
#        echo " Running from `pwd`"

        # Look to see if the SST_MULTI_RANK_COUNT Env variable is set
        if Env.is_env_var_set("SST_MULTI_RANK_COUNT") == False:
            runcmdline = "{0} {1}".format(sut, sutArgs)
            RetVal = Test.run_shell_cmd_redirected(runcmdline, outFile)
        else:
            multirankcount = Env.get_env_var_value("SST_MULTI_RANK_COUNT")
            runcmdline = "mpirun -np {0} -output-filename {1} {2} {3}".format(multirankcount, testOutFiles, sut, sutArgs)
            RetVal = Test.run_shell_cmd_redirected(runcmdline, outFile)
            runcmdline = "cat {0}*".format(testOutFiles)
            Test.run_shell_cmd_redirected(, outFile)

#        TODO: HANDLE Timeout Situation
#        TIME_FLAG=/tmp/TimeFlag_$$_${__timerChild} 
#        if [ -e $TIME_FLAG ] ; then 
#             echo " Time Limit detected at `cat $TIME_FLAG` seconds" 
#             fail " Time Limit detected at `cat $TIME_FLAG` seconds" 
#             rm $TIME_FLAG 
#             return 
#        fi

#        if [ $RetVal != 0 ]  
#        then
#             echo ' '; echo WARNING: sst did not finish normally ; echo ' '
#             ls -l ${sut}
#             fail "WARNING: sst did not finish normally, RetVal=$RetVal"
#             wc $outFile
#             echo " 20 line tail of \$outFile"
#             tail -20 $outfile
#             echo "    --------------------"
#             return
#        fi
#        wc ${outFile} ${referenceFile} | awk -F/ '{print $1, $(NF-1) "/" $NF}'
    
    
#            diff ${referenceFile} ${outFile} > /dev/null;
#            if [ $? -ne 0 ]
#            then
#    ##  Follows some bailing wire to allow serialization branch to work
#    ##          with same reference files
#         sed s/' (.*)'// $referenceFile > $newRef
#         ref=`wc ${newRef} | awk '{print $1, $2}'`; 
#         ##        ref=`wc ${referenceFile} | awk '{print $1, $2}'`; 
#         sed s/' (.*)'// $outFile > $newOut
#         new=`wc ${newOut} | awk '{print $1, $2}'`; 
#         ##          new=`wc ${outFile}       | awk '{print $1, $2}'`;
#            wc $newOut       
#                   if [ "$ref" == "$new" ];
#                   then
#                       echo "outFile word/line count matches Reference"
#                   else
#                       echo "$merlin_case test Fails"
#                       tail $outFile
#                       fail "outFile word/line count does NOT matches Reference"
#                   fi
#            else
#                    echo ReferenceFile is an exact match of outFile
#            fi
#    
#            endSeconds=`date +%s`
#            echo " "
#            elapsedSeconds=$(($endSeconds -$startSeconds))
#            echo "${merlin_case}: Wall Clock Time  $elapsedSeconds seconds"



################################################################################
# TESTS 

##     def test_simpleComponent(self):
##         """ test_simpleComponent
##         
##             Perform a test of the simpleComponent of simpleElement
##         """
##         print "RUNNING test_simpleComponent - SHOULD PASS"
##         
##         # Define a common basename for test output and reference
##         # files. XML postprocessing requires this.
##         testDataFileBase = "test_simpleComponent"
##         outFile = "{0}/{1}.out".format(Env.SST_TEST_OUTPUTS, testDataFileBase)
##         referenceFile = "{0}/{1}.out".format(Env.SST_TEST_REFERENCE, testDataFileBase)
##         
##         # Define Software Under Test (SUT) and its runtime arguments
##         sut = "{0}/sst".format(Env.SST_TEST_INSTALL_BIN)
##         sutArgs = "{0}/simpleElementExample/tests/test_simpleComponent.py".format(Env.SST_TEST_ELEMENTS_SRC)
## 
##         # Check that we can run the SUT
##         if Test.is_exe(sut):
##             # Run SUT
##             RetVal = Test.run_shell_cmd_redirected("{0} {1}".format(sut, sutArgs), outFile)
## 
## #           TODO: HANDLE Timeout Situation
## #            TIME_FLAG=/tmp/TimeFlag_$$_${__timerChild}
## #            if [ -e $TIME_FLAG ] ; then 
## #                 echo " Time Limit detected at `cat $TIME_FLAG` seconds" 
## #                 fail " Time Limit detected at `cat $TIME_FLAG` seconds" 
## #                 rm $TIME_FLAG 
## #                 return 
## #            fi 
## 
##             # Check the return code from SST 
##             if RetVal != 0:
##                 errormsg = " - WARNING: sst did not finish normally, RetVal = {0}".format(RetVal)
##                 print errormsg
##                 print(Test.run_quick_shell_cmd("ls -l {0}".format(sut)))
##                 self.fail(errormsg)
##                 return
## 
##             # Quick dump of the Word Count and difference between files 
##             # TODO: Make these a utility function 
##             print(Test.run_quick_shell_cmd("wc {0} {1}".format(referenceFile, outFile)))
##             RtnVal = Test.run_shell_cmd_redirected("diff -b {0} {1}".format(referenceFile, outFile), "_raw_diff")
##             
##             if RtnVal != 0:
##                 print(Test.run_quick_shell_cmd("wc {0}".format(_raw_diff)))
##                 rtn = Test.compare_sorted(referenceFile, outfile)
##                 if rtn == 0:
##                     print " Sorted match with Reference File"
##                     os.remove(_raw_diff)
##                 else:
##                     errormsg = " - Reference does not Match Output"
##                     print(errormsg)
##                     print(Test.run_quick_shell_cmd("diff -b {0} {1}".format(referenceFile, outFile)))
##                     self.fail(errormsg)
##             else:
##                 print("Exact match with Reference File")
##         else:
##             # Problem encountered: can't find or can't run SUT 
##             # (doesn't really do anything in Phase I)
##             errormsg = " - Problem with SUT (Not Found): {0}".format(sut)
##             print(errormsg)
##             print(Test.run_quick_shell_cmd("ls -l"))
##             self.fail(errormsg)
        
####

    def test_merlin_dragon_12(self):          
        self.merlin_Template("dragon_12", 500)
    
    def test_merlin_dragon_72(self):          
        self.merlin_Template("dragon_72", 500)
    
    def test_merlin_ft_r16(self):          
        self.merlin_Template("ft_r16", 500)
    
    def test_merlin_ft_r8(self):          
        self.merlin_Template("ft_r8", 500)
    
    def test_merlin_torus_3x3x3(self):          
        self.merlin_Template("torus_3x3x3", 500)
    
    def test_merlin_trafficgen_trivial(self):
        self.merlin_Template("trivialTrafficGen", 500)


################################################################################
# Run this module as a Test Suite
if __name__ == '__main__':
    SST_TestCase.SST_RunTestSuite(testSuite_merlin) 
    




