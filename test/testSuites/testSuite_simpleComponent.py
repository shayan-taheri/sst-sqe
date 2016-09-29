#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# TestSuite:
#     testSuite_simpleComponent
# Purpose:
#     Exercise the simpleComponent of the simpleElementExample
# Inputs:
#     None
# Outputs:
#     test_simpleComponent.out file
# Expected Results
#     Match of output file against reference file
# Caveats:
#     The output files must match the reference file *exactly*,
#     requiring that the command lines for creating both the output
#     file and the reference file be exactly the same.
#-------------------------------------------------------------------------------

###############TO DOS:
# print name of testsuite at top before running
# Handle the asserts cleanly
# Exclude tests from run all
# allow for run specific tests
# See if Jenkins will process xml file without cdata sections
# Add remaining env code for BUILD_TYPE_USER from testDefinitions.sh
# Handle timout flag in test
#
# Add code for:
#   multithread_multirank_patch_Suites() in testDefinitions.sh
#
#   in testSubroutines.sh rewrite...  
#   checkPerCent(), pc100(), squashXML(), main(), myWC(), preFail(),
#   RemoveComponentWarning() 
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

class testSuite_simpleComponent(SST_TestCase.SST_TestCase):
    """TEST Suite DOC
    
    Placeholder for a TestCase inside a result. As far as a TestResult
    is concerned, this looks exactly like a unit test. Used to insert
    arbitrary errors into a test suite run.
    """
    
################################################################################
# Support Routines Run At Startup and Before and After each Test
# Note: These do not have to be defined

    @classmethod
    def setUpClass(self):
        """ Top Level setUpClass, called BEFORE ANY tests are run a single time"""
        super(testSuite_simpleComponent, self).setUpClass()  # Call the Base Class Method
        #print "Top Level setUpClass()"
        pass
        
    @classmethod
    def tearDownClass(self):
        """ Top Level tearDownClass, called AFTER ALL tests are run a single time"""
        super(testSuite_simpleComponent, self).tearDownClass() # Call the Base Class Method
        #print "Top Level tearDownClass()"
        pass

    def setUp(self):
        """ Top Level setUp, called before every test is run"""
        super(testSuite_simpleComponent, self).setUp() # Call the Base Class Method
        #print "Top Level setUp()"
        pass
        
    def tearDown(self):
        """ Top Level tearDown, called after every test is run"""
        super(testSuite_simpleComponent, self).tearDown() # Call the Base Class Method
        #print "Top Level tearDown()"
        pass

################################################################################
# TESTS 

    def test_simpleComponent(self):
        """ test_simpleComponent
        
            Perform a test of the simpleComponent of simpleElement
        """
        print "RUNNING test_simpleComponent - SHOULD PASS"
        
        # Define a common basename for test output and reference
        # files. XML postprocessing requires this.
        testDataFileBase = "test_simpleComponent"
        outFile = "{0}/{1}.out".format(Env.SST_TEST_OUTPUTS, testDataFileBase)
        referenceFile = "{0}/{1}.out".format(Env.SST_TEST_REFERENCE, testDataFileBase)
        
        # Define Software Under Test (SUT) and its runtime arguments
        sut = "{0}/sst".format(Env.SST_TEST_INSTALL_BIN)
        sutArgs = "{0}/simpleElementExample/tests/test_simpleComponent.py".format(Env.SST_TEST_ELEMENTS_SRC)

        # Check that we can run the SUT
        if Test.is_exe(sut):
            # Run SUT
            RetVal = Test.run_shell_cmd_redirected("{0} {1}".format(sut, sutArgs), outFile)

#           TODO: HANDLE Timeout Situation
            TIME_FLAG=/tmp/TimeFlag_$$_${__timerChild}
#            if [ -e $TIME_FLAG ] ; then 
#                 echo " Time Limit detected at `cat $TIME_FLAG` seconds" 
#                 fail " Time Limit detected at `cat $TIME_FLAG` seconds" 
#                 rm $TIME_FLAG 
#                 return 
#            fi 

##            # HANDLE Timeout Situation
##            if Test.check_timout_flag() == True:
##                self.fail("DDD FAILED")
##                return
###                 echo " Time Limit detected at `cat $TIME_FLAG` seconds" 
###                 fail " Time Limit detected at `cat $TIME_FLAG` seconds" 
###                 rm $TIME_FLAG 
###                 return 
###            fi 

            # Check the return code from SST 
            if RetVal != 0:
                errormsg = " - WARNING: sst did not finish normally, RetVal = {0}".format(RetVal)
                print errormsg
                print(Test.run_quick_shell_cmd("ls -l {0}".format(sut)))
                self.fail(errormsg)
                return

            # Quick dump of the Word Count and difference between files 
            # TODO: Make these a utility function 
            print(Test.run_quick_shell_cmd("wc {0} {1}".format(referenceFile, outFile)))
            RtnVal = Test.run_shell_cmd_redirected("diff -b {0} {1}".format(referenceFile, outFile), "_raw_diff")
            
            if RtnVal != 0:
                print(Test.run_quick_shell_cmd("wc {0}".format(_raw_diff)))
                rtn = Test.compare_sorted(referenceFile, outfile)
                if rtn == 0:
                    print " Sorted match with Reference File"
                    os.remove(_raw_diff)
                else:
                    errormsg = " - Reference does not Match Output"
                    print(errormsg)
                    print(Test.run_quick_shell_cmd("diff -b {0} {1}".format(referenceFile, outFile)))
                    self.fail(errormsg)
            else:
                print("Exact match with Reference File")
        else:
            # Problem encountered: can't find or can't run SUT 
            # (doesn't really do anything in Phase I)
            errormsg = " - Problem with SUT (Not Found): {0}".format(sut)
            print(errormsg)
            print(Test.run_quick_shell_cmd("ls -l"))
            self.fail(errormsg)
        
####

    def test_aaaothertest(self):
        """ test_aaothertest short description
        
            Placeholder for a test description
        """
        # Force an outside assert
        print "RUNNING test_aaaothertest - SHOULD FAIL : NOTE : This Test Comes After test_simpleComponent in Source Code"
        x = 5 / 0
        self.assertEquals(5, 5, "aaaothertest FAILED")
        
####

    def test_bbbothertest(self):
        """ test_bbbothertest short description
        
            Placeholder for a test description
        """
        # Force an outside assert
        print "RUNNING test_bbbothertest - SHOULD PASS"
        
####
        

    def test_cccothertest(self):
        """ test_cccothertest short description
        
            Placeholder for a test description
        """
        # Force an outside assert
        print "RUNNING test_cccothertest - SHOULD PASS"
        
####

    def test_dddothertest(self):
        """test_dddothertest short description
        
        Placeholder for a test description
        """
        print "RUNNING test_dddothertest - SHOULD FAIL"
        self.fail("DDD FAILED")

####
        
    def test_vvvothertest(self):
        """test_vvvothertest short description
        
        Placeholder for a test description
        """
        # Force an outside assert
        print "RUNNING test_vvvothertest - SHOULD FAIL"
        x = 5 / 0
        self.assertEquals(5, 5, "VVV FAILED")
        
####

    def test_wwwothertest(self):
        """test_wwwothertest short description
        
        Placeholder for a test description
        """
        print "RUNNING test_wwwothertest - SHOULD PASS"
        
        self.assertEquals(5, 5, "WWW FAILED")
        
####
        
    def test_xxxothertest(self):
        """test_xxxothertest short description
        
        Placeholder for a test description
        """
        print "RUNNING test_xxxothertest - SHOULD FAIL"
        self.assertEquals(5, 4, "XXX FAILED")
        
####

    def test_yyyothertest(self):
        """test_yyyothertest short description
        
        Placeholder for a test description
        """
        print "RUNNING test_yyyothertest - SHOULD PASS"

####

    @unittest.skip("demonstrating skipping")
    def test_zzzothertest(self):
        """test_zzzothertest short description
        
        Placeholder for a test description
        """
        print "RUNNING test_zzzothertest - SHOULD SKIP"
        self.fail("ZZZ FAILED")

################################################################################
# Tun this module as a Test Suite
if __name__ == '__main__':
    SST_TestCase.SST_RunTestSuite(testSuite_simpleComponent) 
    




