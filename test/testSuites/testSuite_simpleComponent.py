#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Test:
#     test_simpleComponent
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
# Control order that tests are run    
# Run Tests in order of discovered in file    
# Handle the asserts cleanly
# Dump xml structure
# Clean up fail reports
# Exclude tests from run all
# allow for run specific tests
###############TO DOS:

# Import Python System Level Modules
import os
import sys
import unittest

# Set the Path to the Included SST Testing Modules
TEST_SUITE_ROOT = os.path.dirname(os.path.realpath(__file__))
SST_MODULES_PATH = TEST_SUITE_ROOT + "/../include"
sys.path.append(SST_MODULES_PATH)

# Import SST Testing Modules
import SST_TestCase 
import SST_TestSupport as Test

#. $TEST_SUITE_ROOT/../include/testDefinitions.sh
#. $TEST_SUITE_ROOT/../include/testSubroutines.sh

################################################################################
# DEFINES

L_SUITENAME="SST_simpleComponent_suite" # Name of this test suite; will be used to
                                        # identify this suite in XML file. This
                                        # should be a single string, no spaces
                                        # please.

#TODO: L_BUILDTYPE=$1                   # Build type, passed in from bamboo.sh as a convenience
                                        # value. If you run this script from the command line,
                                        # you will need to supply this value in the same way
                                        # that bamboo.sh defines it if you wish to use it.
                                        
L_TESTFILE=[]                           # Empty list, used to hold test file names

################################################################################

class testSuite_simpleComponent(SST_TestCase.SST_TestCase):
#class testSuite_simpleComponent(unittest.TestCase):
    """TEST Suite DOC
    
    Placeholder for a TestCase inside a result. As far as a TestResult
    is concerned, this looks exactly like a unit test. Used to insert
    arbitrary errors into a test suite run.
    """

################################################################################
# TEST Setup Functions

    @classmethod
    def setUpClass(self):
        print "top setUpClass"
        self.L_SUITENAME="SST_simpleComponent_suite" # Name of this test suite; will be used to
                                                     # identify this suite in XML file. This
                                                     # should be a single string, no spaces
                                                     # please.
        
        #TODO: self.L_BUILDTYPE=$1                   # Build type, passed in from bamboo.sh as a convenience
                                                     # value. If you run this script from the command line,
                                                     # you will need to supply this value in the same way
                                                     # that bamboo.sh defines it if you wish to use it.
                                                
        self.L_TESTFILE=[]                           # Empty list, used to hold test file names
        
        # Get all the Important Environment Variables
        self.SST_ROOT               = os.environ["SST_ROOT"]
        self.SST_TEST_OUTPUTS       = os.environ["SST_TEST_OUTPUTS"]
        self.SST_TEST_REFERENCE     = os.environ["SST_TEST_REFERENCE"]
        self.SST_TEST_INSTALL_BIN   = os.environ["SST_TEST_INSTALL_BIN"]
        self.SST_TEST_RESULTS       = os.environ["SST_TEST_RESULTS"]

        ## DEBUG output
        print "self.SST_ROOT = {0}".format(self.SST_ROOT)
        print "self.SST_TEST_OUTPUTS = {0}".format(self.SST_TEST_OUTPUTS)
        print "self.SST_TEST_REFERENCE = {0}".format(self.SST_TEST_REFERENCE)
        print "self.SST_TEST_INSTALL_BIN = {0}".format(self.SST_TEST_INSTALL_BIN)
        print "self.SST_TEST_RESULTS = {0}".format(self.SST_TEST_RESULTS)

        print "\n\n"

        print "Test.SST_ROOT = {0}".format(Test.SST_ROOT)
        print "Test.SST_TEST_OUTPUTS = {0}".format(Test.SST_TEST_OUTPUTS)
        print "Test.SST_TEST_REFERENCE = {0}".format(Test.SST_TEST_REFERENCE)
        print "Test.SST_TEST_INSTALL_BIN = {0}".format(Test.SST_TEST_INSTALL_BIN)
        print "Test.SST_TEST_RESULTS = {0}".format(Test.SST_TEST_RESULTS)



        # Display the details about assertion failures along with the message
#        self.longMessage = True

#        print "AARON - Desc = {0}".format(self.shortDescription())

#    @classmethod
#    def tearDownClass(self):
#        SST_TestCase.SST_TestCase.tearDownClass()  # Call base class
#        print"top tearDownClass"
#        pass
# 
#    def setUp(self):
#        SST_TestCase.SST_TestCase.setUp(self)
#        print"top setUp"
#        pass
        
#    def tearDown(self):
#        pass

################################################################################
# TESTS Setup Functions

    def test_aaaothertest(self):
        """ test_aaothertest short description
        
            Placeholder for a test description
        """
        # Force an outside assert
        print "RUNNING FIRST TEST"
        x = 5 / 0
        self.assertEquals(5, 5, "VVV FAILED")
        
####
        
    def test_simpleComponent(self):
        """ test_simpleComponent
        
            Perform a test of the simpleComponent of simpleElement
        """
        
        # Define a common basename for test output and reference
        # files. XML postprocessing requires this.
        testDataFileBase = "test_simpleComponent"
        outFile = "{0}/{1}.out".format(self.SST_TEST_OUTPUTS, testDataFileBase)
        referenceFile = "{0}/{1}.out".format(self.SST_TEST_REFERENCE, testDataFileBase)
        # Add basename to list for XML processing later
        self.L_TESTFILE.append(testDataFileBase)
        
        # Define Software Under Test (SUT) and its runtime arguments
        sut = "{0}/sst".format(self.SST_TEST_INSTALL_BIN)
        sutArgs = "{0}/sst-elements/src/sst/elements/simpleElementExample/tests/test_simpleComponent.py".format(self.SST_ROOT)


        ## DEBUG output
        #print "testDataFileBase = {0}".format(testDataFileBase)
        #print "outFile = {0}".format(outFile)
        #print "referenceFile = {0}".format(referenceFile)
        #print "self.L_TESTFILE = {0}".format(self.L_TESTFILE)
        #print "sut = {0}".format(sut)
        #print "sutArgs = {0}".format(sutArgs)

        # Check that we can run the SUT
        if Test.is_exe(sut):
            # Run SUT
            RetVal = Test.run_shell_cmd_redirected("{0} {1}".format(sut, sutArgs), outFile)
            #print "RetVal = {0}".format(RetVal)
            #print run_shell_cmd("cat {0}".format(outFile))
            # force an error
            #RetVal = 1
            
#           TODO: HANDLE Timeout Situation
#            TIME_FLAG=/tmp/TimeFlag_$$_${__timerChild} 
#            if [ -e $TIME_FLAG ] ; then 
#                 echo " Time Limit detected at `cat $TIME_FLAG` seconds" 
#                 fail " Time Limit detected at `cat $TIME_FLAG` seconds" 
#                 rm $TIME_FLAG 
#                 return 
#            fi 

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
        
    def test_vvvothertest(self):
        """test_vvvothertest short description
        
        Placeholder for a test description
        """
        # Force an outside assert
        print "AARON DIVIDE BY ZERO"
        x = 5 / 0
        self.assertEquals(5, 5, "VVV FAILED")
        
####

    def test_wwwothertest(self):
        """test_wwwothertest short description
        
        Placeholder for a test description
        """
        #print "AARON ID = {0}".format(self.id())
        #print "AARON OTHER = %s.%s" % (self.__class__.__module__, self.__class__.__name__)
        #print "AARON TestScriptName = %s" % (self.__class__.__name__)
        #print "AARON TestName = %s" % (self._testMethodName)
        #print "AARON testMethodDoc = %s" % (self._testMethodDoc)
        
        self.assertEquals(5, 5, "WWW FAILED")
        
####
        
    def test_xxxothertest(self):
        """test_xxxothertest short description
        
        Placeholder for a test description
        """
        self.assertEquals(5, 4, "XXX FAILED")
        
####

    def test_yyyothertest(self):
        """test_yyyothertest short description
        
        Placeholder for a test description
        """
        self.fail("YYY FAILED")

####

    @unittest.skip("demonstrating skipping")
    def test_zzzothertest(self):
        """test_zzzothertest short description
        
        Placeholder for a test description
        """
        self.fail("ZZZ FAILED")

################################################################################
# Tun this module as a Test Suite
if __name__ == '__main__':
    SST_TestCase.SST_RunTestSuite() 
    




