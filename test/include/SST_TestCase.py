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

# Element Tree Method
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

## Import SST Testing Modules
import SST_TestLoader
import SST_TestRunner 
import SST_TestEnvironment as Env

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
        #print "Base setUpClass"
        # If directory for SUT outputs does not exist, create it
        if os.path.exists(Env.SST_TEST_OUTPUTS) == False:
            os.makedirs(Env.SST_TEST_OUTPUTS)

    @classmethod
    def tearDownClass(self):
        """ Base tearDownClass, called AFTER ALL tests are run a single time"""
        #print "Base tearDownClass"
        pass

    def setUp(self):
        """ Base setUp, called before every test is run"""
        #print "Base setUp"
        pass
        
    def tearDown(self):
        """ Base tearDown, called after every test is run"""
        #print "Base tearDown"
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

def SST_RunTestSuite(testclass, testlist = None, verbosity = 0):
# testclass = The class to be run as part of this testing
# testlist = A list of tests names (strings) of tests to be run, If = None all tests are run
# verbosity = 0 - No Result Output
#             1 - Minimal Output
#             2 - Full Output

    # Launch script with discovery using our TestRunner
#    testrunner = SST_TestRunner.SST_TestRunner(verbosity=verbosity, descriptions=True)
#    unittest.main(verbosity=verbosity, exit=False, testRunner=testrunner)

#    # More Direct way of running (with a bit more control)
    testloader = SST_TestLoader.SST_TestLoader()
    casenames = testloader.getTestCaseNames(testclass)
    testloader.sortTestMethodsUsing = None
#    casenames = testloader.getTestCaseNames(testclass)
#    print "casenames2 = {0}".format(casenames)
    
    
#    suite = unittest.TestLoader().loadTestsFromTestCase(testclass)
    testsuite = testloader.loadTestsFromTestCase(testclass)
    testrunner = SST_TestRunner.SST_TestRunner(verbosity=verbosity, descriptions=True)
    testrunner.run(testsuite)




## #    # More Direct way of running (with a bit more control)
##     testloader = unittest.TestLoader()
##     testloader.sortTestMethodsUsing = None
## #    suite = unittest.TestLoader().loadTestsFromTestCase(testclass)
##     testsuite = testloader.loadTestsFromTestCase(testclass)
##     testrunner = SST_TestRunner.SST_TestRunner(verbosity=verbosity, descriptions=True)
##     testrunner.run(testsuite)


#    # More Direct way of running (with a bit more control)
#    suite = unittest.TestSuite()
#    suite.addTest(testSuite_simpleComponent('test_simpleComponent'))
#    suite.addTest(testSuite_simpleComponent('test_vvvothertest'))
#    suite.addTest(testSuite_simpleComponent('test_wwwothertest'))
#    suite.addTest(testSuite_simpleComponent('test_xxxothertest'))
#    suite.addTest(testSuite_simpleComponent('test_yyyothertest'))
#    suite.addTest(testSuite_simpleComponent('test_zzzothertest'))
#    testrunner = SST_TestRunner.SST_TestRunner(verbosity=verbosity, descriptions=True)
#    testrunner.run(suite)

    # Get the results
    results = testrunner.getFinalResults()
    
    # Store the testresults into a Jenkins formatted XML file
    generate_jenkins_xml_results(results)

####

################################################################################
# Support Code to allow CDATA to be used with the xml.etree.cElementTree module
# NOTE: These functions may not be needed if Jenkins will process the system-out 
#       structures without CDATA 
################################################################################

# Add CDATA FUNCTION
def CDATA(text=None):
    element = ET.Element('![CDATA[')
    element.text = text
    return element

# Point to the original _serialize_xml code in xml.etree.cElementTree
ET._original_serialize_xml = ET._serialize_xml

# Create a new _serialize_xml that can process CDATA
def _serialize_xml(write, elem, encoding, qnames, namespaces):
#    print "_serialize_xml tag = {0}; tail = {1}".format(elem.tag, elem.tail)
    if elem.tag == '![CDATA[':
#        write("<%s%s]]>%s" % (elem.tag, elem.text, elem.tail))
        write("<%s%s]]>\n" % (elem.tag, elem.text))
        return
    return ET._original_serialize_xml(
         write, elem, encoding, qnames, namespaces)
ET._serialize_xml = ET._serialize['xml'] = _serialize_xml

################################################################################

def generate_jenkins_xml_results(testResults, outputDir = None):
    
    # Figure out where to write the output xml file
    if outputDir == None:
        finaloutputdir = os.environ["SST_TEST_RESULTS"]
    else:
        finaloutputdir = outputDir

    # Debug Output
#    print " DEBUG ---- Results = {0}".format(testResults)
#    print " DEBUG ---- Test Suite Name = {0}".format(testResults.testSuiteName)
#    print " DEBUG ---- Suite Start Time = {0}".format(testResults.allTestsStartDateTime.strftime('%Y/%m/%d %H:%M:%S'))
#    print " DEBUG ---- Suite Stop Time = {0}".format(testResults.allTestsStopDateTime.strftime('%Y/%m/%d %H:%M:%S'))
#    print " DEBUG ---- Suite Total Run Time = {0} Seconds".format(testResults.allTestsTimeTaken.total_seconds())
#    print " DEBUG ---- HostName = {0}".format(testResults.testHostName)
#    print " DEBUG ---- # Successes = \n{0}".format(testResults.successes)
#    print " DEBUG ---- # Failed = \n{0}".format(testResults.failures)
#    print " DEBUG ---- # Skipped = \n{0}".format(testResults.skipped)
#    print " DEBUG ---- # Errors = \n{0}".format(testResults.errors)
#    print " DEBUG ---- # Total Tests Run = {0}".format(testResults.testsRun)
#    print " DEBUG ---- # List of Tests Processed = \n{0}".format(testResults.allTestsProcessed)

    # Build the XML infrastructure
    # Top level "testsuites" element
    testsuites = ET.Element("testsuites", name="NonJenkinsRun")

    # Second level "testsuite" element under "testsuites" element
    testsuite = ET.SubElement(testsuites, "testsuite", name=testResults.testSuiteName, 
                              tests=str(testResults.testsRun), 
                              failures=str(len(testResults.failures)), 
                              skipped=str(len(testResults.skipped)), 
                              errors=str(len(testResults.errors)), 
                              hostname=testResults.testHostName, 
                              time=str(int(testResults.allTestsTimeTaken.total_seconds())),
                              timestamp=testResults.allTestsStartDateTime.strftime('%Y-%m-%dT%H:%M:%S'))

    # Third level "testcase" element under "testsuite" element
    # Now create an "testcase" entry for each test that was processed 
    for processedtest, runtime in testResults.allTestsProcessed:
        #print "\n\nDebug - Processed Test = {0}; RunTime = {1}".format(processedtest, runtime)
        failflag = 0
        skipflag = 0
        errorflag = 0
        successflag = 0
        runstatus = ""
        
        # Get the name of the testcase from the test object
        testcasename="{0}".format(processedtest._testMethodName)

        #print "!!! STARTING LOOKING FOR {0}".format(processedtest)

        # Is this a failed test?
        for failedtest, err in testResults.failures:
            #print " --- in fails, Looking for {0}, testing against {1}".format(processedtest, failedtest)
            if failedtest == processedtest:
                #print " --- {0}, found in fails".format(processedtest)
                runstatus = "run"
                failflag = 1
                errmsg = err
                break

        # Is this an errored test?
        if failflag == 0 :
            for errtest, err in testResults.errors:
                #print " --- in errors, Looking for {0}, testing against {1}".format(processedtest, errtest)
                if errtest == processedtest:
                    #print " --- {0}, found in errors".format(processedtest)
                    runstatus = "run"
                    errorflag = 1    
                    errmsg = err
                    break

        # Is this a skipped test?
        if failflag == 0 and errorflag == 0:
            for skippedtest, err in testResults.skipped:
                #print " --- in skips, Looking for {0}, testing against {1}".format(processedtest, skippedtest)
                if skippedtest == processedtest:
                    #print " --- {0}, found in skipped".format(processedtest)
                    runstatus = "skipped"
                    skipflag = 1    
                    errmsg = err
                    break

        # Is this an successful test?
        if failflag == 0 and skipflag == 0 and errorflag == 0:
            for successtest in testResults.successes:
                #print " --- in successes, Looking for {0}, testing against {1}".format(processedtest, successtest)
                if successtest == processedtest:
                    #print " --- {0}, found in successes".format(processedtest)
                    runstatus = "run"
                    successflag = 1    
                    errmsg = ""
                    break
                
        # Error Case, Did we not find the test in the previous lists? 
        if failflag == 0 and skipflag == 0 and errorflag == 0 and successflag == 0:
            #print " --- SYSTEM ERROR DETECTED"
            runstatus = "error"
            errflag = 1    
            errtype = "Python SST_TestSupport.py System Error"
            errmsg = "generate_jenkins_xml_results() - unable to find test in succes, failure, errors or skipped lists"

        # Build the test case element under the testsuite element
        testcase = ET.SubElement(testsuite, "testcase", name=testcasename,
                                 classname="NonJenkinsRun.{0}".format(testResults.testSuiteName),
                                 status=runstatus, time=str(int(runtime)))

        # Get the error type if errmsg is populated necessary
        errtype = ""
        if len(errmsg) > 0:
            index = errmsg.find("(")
            if index > 0:
                errtype = errmsg[0:index-1]

        # Add any skipped, failure or error elements messages under the testcase element
        if skipflag == 1:
            skip_elem = ET.SubElement(testcase, "skipped", message=errmsg)
    
        if errorflag == 1:
            error_elem = ET.SubElement(testcase, "failure", type=errtype, message=errmsg)

        if failflag == 1:
            fail_elem = ET.SubElement(testcase, "failure", type=errtype, message=errmsg)


    # Third level "properties" element under "testsuite" - This element is not populated
    properties = ET.SubElement(testsuite, "properties")

    # Third level "system-out" & "system-err" elements under "testsuite"
    cdata = "TESTSUITE {0}.py: Total Suite Wall Clock Time {1} seconds".format(testResults.testSuiteName, str(int(testResults.allTestsTimeTaken.total_seconds())))
    system_out = ET.SubElement(testsuite, "system-out")
    system_out.text = cdata    
    
    system_err = ET.SubElement(testsuite, "system-err")
  
#    # USING CDATA (NOT SURE IF JENKINS WILL PROCESS REGULAR TEXT)     
#    cdata = CDATA("TESTSUITE {0}.py: Total Suite Wall Clock Time {1} seconds".format(testResults.testSuiteName, str(int(testResults.allTestsTimeTaken.total_seconds()))))
#    system_out = ET.SubElement(testsuite, "system-out")
#    system_out.append(cdata)    
#    
#    cdata = CDATA(" ")
#    system_err = ET.SubElement(testsuite, "system-err")
#    system_err.append(cdata)    

    # Fix the xml formatting with indentions (make pretty the xml file)
    testsuites = minidom.parseString(ET.tostring(testsuites)).toprettyxml(indent="    ", encoding='utf-8')
    
    # Print out the xml as part of the results (uncomment out to see the results
    #print "POST PARSING - TestSuite Results:\n{0}".format(testsuites)
    
    # Figure out the Name of the file
    finalfilename = "TEST-{0}.xml".format(testResults.testSuiteName)
    finaloutputfilepath = "{0}/{1}".format(finaloutputdir, finalfilename) 
    
    # Write the output
    with open(finaloutputfilepath, "w") as f:
        f.write(testsuites)










