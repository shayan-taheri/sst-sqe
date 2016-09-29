"""Running tests"""

   
# NOTE: This fis is a modified version of the Python 2.7.12 Source file 
#       "unittest/runner.py" with minor modifications and rename of class 
#       TextTestRunner() in order to provide better control of the output, and
#       support of our custom report information. 

import sys
import time
import unittest

#from unittest import result
import SST_TestResult
from unittest import registerResult

__unittest = True


class _WritelnDecorator(object):
    """Used to decorate file-like objects with a handy 'writeln' method"""
    def __init__(self,stream):
        self.stream = stream

    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            raise AttributeError(attr)
        return getattr(self.stream,attr)

    def writeln(self, arg=None):
        if arg:
            self.write(arg)
        self.write('\n') # text-mode streams translate to \r\n if needed


class SST_TextTestResult(SST_TestResult.SST_TestResult):
    """A test result class that can print formatted text results to a stream.

    Used by SST_TestRunner.
    
    NOTE: This is a modified version of the Python 2.7.12 Source file runner.py
          with minor modifications and rename to SST_TextTestResult() 
    """
    separator1 = '=' * 70
    separator2 = '-' * 70
    separatorshort = '-' * 10

    def __init__(self, stream, descriptions, verbosity):
        super(SST_TextTestResult, self).__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return '\n'.join((str(test), doc_first_line))
        else:
            return str(test)

    def startTest(self, test):
        super(SST_TextTestResult, self).startTest(test)
        if self.showAll:
            self.stream.write(self.getDescription(test))
            self.stream.write(" ... ")
            self.stream.flush()

    def addSuccess(self, test):
        super(SST_TextTestResult, self).addSuccess(test)
        if self.showAll:
            self.stream.writeln("ok")
        elif self.dots:
            self.stream.write('.')
            self.stream.flush()

    def addError(self, test, err):
        super(SST_TextTestResult, self).addError(test, err)
        if self.showAll:
            self.stream.writeln("ERROR")
        elif self.dots:
            self.stream.write('E')
            self.stream.flush()

    def addFailure(self, test, err):
        super(SST_TextTestResult, self).addFailure(test, err)
        if self.showAll:
            self.stream.writeln("FAIL")
        elif self.dots:
            self.stream.write('F')
            self.stream.flush()

    def addSkip(self, test, reason):
        super(SST_TextTestResult, self).addSkip(test, reason)
        if self.showAll:
            self.stream.writeln("skipped {0!r}".format(reason))
        elif self.dots:
            self.stream.write("s")
            self.stream.flush()

    def addExpectedFailure(self, test, err):
        super(SST_TextTestResult, self).addExpectedFailure(test, err)
        if self.showAll:
            self.stream.writeln("expected failure")
        elif self.dots:
            self.stream.write("x")
            self.stream.flush()

    def addUnexpectedSuccess(self, test):
        super(SST_TextTestResult, self).addUnexpectedSuccess(test)
        if self.showAll:
            self.stream.writeln("unexpected success")
        elif self.dots:
            self.stream.write("u")
            self.stream.flush()

    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printSuccessList('SUCCESS', self.successes)
        self.printSkipList('SKIPPED', self.skipped)
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printSuccessList(self, flavour, successlist):
        for test in successlist:
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s: %s" % (flavour,self.getDescription(test)))

    def printSkipList(self, flavour, skiplist):
        for test, err in skiplist:
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s: %s" % (flavour,self.getDescription(test)))
            #self.stream.writeln(self.separatorshort)
            self.stream.writeln("%s" % err)

    def printErrorList(self, flavour, errorlist):
        for test, err in errorlist:
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s: %s" % (flavour,self.getDescription(test)))
            #self.stream.writeln(self.separatorshort)
            self.stream.writeln("%s" % err)

class SST_TestRunner(object):
    """A test runner class that displays results in textual form.

    It prints out the names of tests as they are run, errors as they
    occur, and a summary of the results at the end of the test run.
    
    NOTE: This is a modified version of the Python 2.7.12 Source file runner.py
          with minor modifications and rename to SST_TestRunner() 
    """
    resultclass = SST_TextTestResult

    def __init__(self, stream=sys.stderr, descriptions=True, verbosity=1,
                 failfast=False, buffer=False, resultclass=None):
        self.stream = _WritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.failfast = failfast
        self.buffer = buffer
        if resultclass is not None:
            self.resultclass = resultclass
        # A place to store the Final Results
        self.finalResult = None
            
    def _makeResult(self):
        return self.resultclass(self.stream, self.descriptions, self.verbosity)

    def getFinalResults(self):
        return self.finalResult
    
    def run(self, test):
        "Run the given test case or test suite."
        result = self._makeResult()
        registerResult(result)
        result.failfast = self.failfast
        result.buffer = self.buffer
        startTime = time.time()
        startTestRun = getattr(result, 'startTestRun', None)
        if startTestRun is not None:
            startTestRun()
        try:
            test(result)
        finally:
            stopTestRun = getattr(result, 'stopTestRun', None)
            if stopTestRun is not None:
                stopTestRun()
        stopTime = time.time()
        timeTaken = stopTime - startTime
#        if hasattr(result, 'separator2'):
#            self.stream.writeln(result.separator2)
        run = result.testsRun
        self.stream.writeln()
        #self.stream.writeln("TESTSUITE %s: Ran %d test%s in %.3fs" % (result.testSuiteName, run, run != 1 and "s" or "", timeTaken))
        self.stream.writeln("Final Report from unittest:")
        result.printErrors()
        self.stream.writeln(result.separator1)

        expectedFails = unexpectedSuccesses = skipped = 0
        try:
            results = map(len, (result.expectedFailures,
                                result.unexpectedSuccesses,
                                result.skipped))
        except AttributeError:
            pass
        else:
            expectedFails, unexpectedSuccesses, skipped = results

        self.stream.writeln("TESTSUITE %s: Processed %d test%s, Passed %d; Skipped %d and found %d Failures in %.3fs" % (result.testSuiteName, run, run != 1 and "s" or "", len(result.successes), len(result.skipped), len(result.failures) + len(result.errors), timeTaken))
        self.stream.writeln(result.separator2)

#        infos = []
#        if not result.wasSuccessful():
#            self.stream.write("FAILED")
#            failed, errored = map(len, (result.failures, result.errors))
#            if failed:
#                infos.append("failures=%d" % failed)
#            if errored:
#                infos.append("errors=%d" % errored)
#        else:
#            self.stream.write("OK")
#        if skipped:
#            infos.append("skipped=%d" % skipped)
#        if expectedFails:
#            infos.append("expected failures=%d" % expectedFails)
#        if unexpectedSuccesses:
#            infos.append("unexpected successes=%d" % unexpectedSuccesses)
#        if infos:
#            self.stream.writeln(" (%s)" % (", ".join(infos),))
#        else:
#            self.stream.write("\n")
            
        # Save off the Final Results
        self.finalResult = result
        return result
