#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A Python test script.
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


# Import Python System Level Modules
import os
import unittest

## Import SST Testing Modules
import SST_TestSupport
import SST_TestRunner 

################################################################################

class SST_TestCase(unittest.TestCase):
    """Base class for SST Test Cases 
    
    Placeholder for a TestCase inside a result. As far as a TestResult
    is concerned, this looks exactly like a unit test. Used to insert
    arbitrary errors into a test suite run.
    """

    @classmethod
    def setUpClass(self):
        """ Base setUpClass, called BEFORE ANY tests are run a single time"""
        pass

    @classmethod
    def tearDownClass(self):
        """ Base tearDownClass, called AFTER ALL tests are run a single time"""
        pass
 
    def setUp(self):
        """ Base setUp, called before every test is run"""
        pass
        
    def tearDown(self):
        """ Base tearDown, called after every test is run"""
        pass

####

    def strclass(self, cls):
        """ Return the class name"""
        #return "%s.%s" % (cls.__module__, cls.__name__)
        return "%s" % (cls.__name__)

    def __str__(self):
        """ Return a string of the class info """  
        #return "%s (%s)" % (self._testMethodName, self.strclass(self.__class__))
        return "%s (%s)" % (self._testMethodName, self.strclass(self.__class__))

    def __repr__(self):
        """ Return a string representation of the class """
        #return "<%s testMethod=%s>" % (self.strclass(self.__class__), self._testMethodName)
        return "<%s.%s>" % (self.strclass(self.__class__), self._testMethodName)

################################################################################

def SST_RunTestSuite():
#    verbosity = 0 - No Result Output
#                1 - Minimal Output
#                2 - Full Output


    # Launch script with discovery using our TestRunner
    testrunner = SST_TestRunner.SST_TestRunner(verbosity=0, descriptions=True)
    unittest.main(verbosity=0, exit=False, testRunner=testrunner)

#    # More Direct way of running (with a bit more control)
#    suite = unittest.TestLoader().loadTestsFromTestCase(testSuite_simpleComponent)
#    testrunner = SST_TestRunner.SST_TestRunner(verbosity=0, descriptions=True)
#    testrunner.run(suite)

#    # More Direct way of running (with a bit more control)
#    suite = unittest.TestSuite()
#    suite.addTest(testSuite_simpleComponent('test_simpleComponent'))
#    suite.addTest(testSuite_simpleComponent('test_vvvothertest'))
#    suite.addTest(testSuite_simpleComponent('test_wwwothertest'))
#    suite.addTest(testSuite_simpleComponent('test_xxxothertest'))
#    suite.addTest(testSuite_simpleComponent('test_yyyothertest'))
#    suite.addTest(testSuite_simpleComponent('test_zzzothertest'))
#    testrunner = SST_TestRunner.SST_TestRunner(verbosity=0, descriptions=True)
#    testrunner.run(suite)

    # Get the results
    results = testrunner.getFinalResults()
    
    # Figure out where to stuff them
    SST_TestSupport.generate_jenkins_xml_results(results)






