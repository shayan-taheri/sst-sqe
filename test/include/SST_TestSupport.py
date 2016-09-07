#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import Python System Level Modules
import os
import subprocess
import xml.etree.cElementTree as ET
import xml.dom.minidom as minidom


print "initialize_test_system"
SST_ROOT               = os.environ["SST_ROOT"]
SST_TEST_OUTPUTS       = os.environ["SST_TEST_OUTPUTS"]
SST_TEST_REFERENCE     = os.environ["SST_TEST_REFERENCE"]
SST_TEST_INSTALL_BIN   = os.environ["SST_TEST_INSTALL_BIN"]
SST_TEST_RESULTS       = os.environ["SST_TEST_RESULTS"]




################################################################################
# SUPPORT CODE

def file_exists(fpath):
    return os.path.isfile(fpath)

####

def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

####

def run_quick_shell_cmd(cmdline):
    # turn the command line into a list
    cmd_param_list = cmdline.split()
    shelloutput = subprocess.Popen(cmd_param_list, stdout=subprocess.PIPE).communicate()[0]    
    return shelloutput

####

def run_shell_cmd_redirected(cmdline, stdoutfile, stderrfile=None):
    # turn the command line into a list
    cmd_param_list = cmdline.split()
    
    # Open the stdout file
    out = open(stdoutfile,"wb")

    # Open the stderr file
    if stderrfile == None:
        err = None
    else:
        err = open(stderrfile,"wb")
    
    # Run the command
    p = subprocess.Popen(cmd_param_list, stdout=out, stderr=err)  
    
    # wait for app to finish
    ret_code = p.wait()
    out.flush()
    if err != None:
        err.flush()
    return ret_code

####

def compare_sorted(file1, file2):
    print(run_quick_shell_cmd("sort -o xo {0}".format(file1)))
    print(run_quick_shell_cmd("sort -o xr {0}".format(file1)))
    RtnVal = run_shell_cmd_redirected("diff -b xo xr", "diff_sorted")
    if RtnVal == 0:
        os.remove(xo)
        os.remove(xr)
        return 0
    print(run_quick_shell_cmd("wc {0}".format("diff_sorted")))
    return 1

################################################################################

def generate_jenkins_xml_results(testResults, outputDir = None):
    
    # Figure out where to suff the output
    SST_TEST_RESULTS       = os.environ["SST_TEST_RESULTS"]
    if outputDir == None:
        finaloutputdir = SST_TEST_RESULTS
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

    # Second level "testsuite" element
    testsuite = ET.SubElement(testsuites, "testsuite", name=testResults.testSuiteName, 
                              tests=str(testResults.testsRun), 
                              failures=str(len(testResults.failures)), 
                              skipped=str(len(testResults.skipped)), 
                              errors=str(len(testResults.errors)), 
                              hostname=testResults.testHostName, 
                              time=str(int(testResults.allTestsTimeTaken.total_seconds())),
                              timestamp=testResults.allTestsStartDateTime.strftime('%Y-%m-%dT%H:%M:%S'))

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


    # Fix the xml formatting with indentions (make pretty the xml file)
    testsuites = minidom.parseString(ET.tostring(testsuites)).toprettyxml(indent="    ", encoding='utf-8')
    
    # Print out the xml as part of the results
    print "TestSuite Results:\n{0}".format(testsuites)
    
    # Write the output
    with open("xmlreport.xml", "w") as f:
        f.write(testsuites)

