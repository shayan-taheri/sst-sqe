"""Test result object"""

# NOTE: This fis is a modified version of the Python 2.7.12 Source file 
#       "unittest/result.py" with minor modifications to class 
#       TestResult() in order to provide additional data needed for 
#       Jenkins. 

import os
import sys
import traceback
import datetime
import socket

from StringIO import StringIO

from unittest import util
from functools import wraps

__unittest = True

def failfast(method):
    @wraps(method)
    def inner(self, *args, **kw):
        if getattr(self, 'failfast', False):
            self.stop()
        return method(self, *args, **kw)
    return inner

STDOUT_LINE = '\nStdout:\n%s'
STDERR_LINE = '\nStderr:\n%s'


class SST_TestResult(object):
    """Holder for test result information.

    Test results are automatically managed by the TestCase and TestSuite
    classes, and do not need to be explicitly manipulated by writers of tests.

    Each instance holds the total number of tests run, and collections of
    failures and errors that occurred among those test runs. The collections
    contain tuples of (testcase, exceptioninfo), where exceptioninfo is the
    formatted traceback of the error that occurred.
    """
    _previousTestClass = None
    _testRunEntered = False
    _moduleSetUpFailed = False
    def __init__(self, stream=None, descriptions=None, verbosity=None):
        self.failfast = False
        self.failures = []
        self.errors = []
        self.testsRun = 0
        self.skipped = []
        self.expectedFailures = []
        self.unexpectedSuccesses = []
        self.shouldStop = False
        self.buffer = False
        self._stdout_buffer = None
        self._stderr_buffer = None
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        self._mirrorOutput = False
        self.successes = []
        self.allTestsProcessed = []
        self.allTestsStartDateTime = None
        self.allTestsStopDateTime = None
        self.allTestsTimeTaken = None
        self.testStartTime = None
        self.testStopTime = None
        self.testTimeTaken = None
        self.testHostName = None
        self.testSuiteName = None
        self.testName = None

    def printErrors(self):
        "Called by TestRunner after test run"

    def startTest(self, test):
        "Called when the given test is about to be run"
        self.testsRun += 1
        self._mirrorOutput = False
        self._setupStdout()
        #print "DEBUG - startTest"
        self.testName = test._testMethodName
        self.testSuiteName = test.__class__.__name__
        self.testStartTime = datetime.datetime.now()

    def _setupStdout(self):
        if self.buffer:
            if self._stderr_buffer is None:
                self._stderr_buffer = StringIO()
                self._stdout_buffer = StringIO()
            sys.stdout = self._stdout_buffer
            sys.stderr = self._stderr_buffer

    def startTestRun(self):
        """Called once before any tests are executed.

        See startTest for a method called before each test.
        """
        #print "DEBUG - startTestRun"
        self.allTestsStartDateTime = datetime.datetime.now()
        self.testHostName = socket.gethostname()

    def stopTest(self, test):
        """Called when the given test has been run"""
        self._restoreStdout()
        self._mirrorOutput = False
        #print "DEBUG - stopTest"
        self.testStopTime = datetime.datetime.now()
        self.testTimeTaken = self.testStopTime - self.testStartTime
        # Add a tuple for the testname and runtimes for each test processed
        self.allTestsProcessed.append((test, self.testTimeTaken.total_seconds()))

    def _restoreStdout(self):
        if self.buffer:
            if self._mirrorOutput:
                output = sys.stdout.getvalue()
                error = sys.stderr.getvalue()
                if output:
                    if not output.endswith('\n'):
                        output += '\n'
                    self._original_stdout.write(STDOUT_LINE % output)
                if error:
                    if not error.endswith('\n'):
                        error += '\n'
                    self._original_stderr.write(STDERR_LINE % error)

            sys.stdout = self._original_stdout
            sys.stderr = self._original_stderr
            self._stdout_buffer.seek(0)
            self._stdout_buffer.truncate()
            self._stderr_buffer.seek(0)
            self._stderr_buffer.truncate()

    def stopTestRun(self):
        """Called once after all tests are executed.

        See stopTest for a method called after each test.
        """
        #print "DEBUG - stopTestRun"
        self.allTestsStopDateTime = datetime.datetime.now()
        self.allTestsTimeTaken = self.allTestsStopDateTime - self.allTestsStartDateTime

    @failfast
    def addError(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info().
        """
        self.errors.append((test, self._exc_info_to_string(err, test)))
        self._mirrorOutput = True

    @failfast
    def addFailure(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info()."""
        self.failures.append((test, self._exc_info_to_string(err, test)))
        self._mirrorOutput = True

    def addSuccess(self, test):
        "Called when a test has completed successfully"
        self.successes.append(test)

    def addSkip(self, test, reason):
        """Called when a test is skipped."""
        self.skipped.append((test, reason))

    def addExpectedFailure(self, test, err):
        """Called when an expected failure/error occurred."""
        self.expectedFailures.append(
            (test, self._exc_info_to_string(err, test)))

    @failfast
    def addUnexpectedSuccess(self, test):
        """Called when a test was expected to fail, but succeed."""
        self.unexpectedSuccesses.append(test)

    def wasSuccessful(self):
        "Tells whether or not this result was a success"
        return len(self.failures) == len(self.errors) == 0

    def stop(self):
        "Indicates that the tests should be aborted"
        self.shouldStop = True

    def _exc_info_to_string(self, err, test):
        """Converts a sys.exc_info()-style tuple of values into a string."""
        exctype, value, tb = err
        # Skip test runner traceback levels
        while tb and self._is_relevant_tb_level(tb):
            tb = tb.tb_next

        if exctype is test.failureException:
            # Skip assert*() traceback levels
            length = self._count_relevant_tb_levels(tb)
            msgLines = traceback.format_exception(exctype, value, tb, length)
        else:
            msgLines = traceback.format_exception(exctype, value, tb)
        #print "DEBUG - _exc_info_to_string(): orig msgLines = {0}".format(msgLines)

        # Create a different (less verbose) string to return 
        sstmsgLines = "{0} ({1}); File: {2}, line {3}".format(exctype.__name__, value, tb.tb_frame.f_code.co_filename, tb.tb_lineno)
        #print "DEBUG - _exc_info_to_string(): sstmsgLines = {0}".format(sstmsgLines)
        msgLines = sstmsgLines

        if self.buffer:
            output = sys.stdout.getvalue()
            error = sys.stderr.getvalue()
            if output:
                if not output.endswith('\n'):
                    output += '\n'
                msgLines.append(STDOUT_LINE % output)
            if error:
                if not error.endswith('\n'):
                    error += '\n'
                msgLines.append(STDERR_LINE % error)
                
        return ''.join(msgLines)


    def _is_relevant_tb_level(self, tb):
        return '__unittest' in tb.tb_frame.f_globals

    def _count_relevant_tb_levels(self, tb):
        length = 0
        while tb and not self._is_relevant_tb_level(tb):
            length += 1
            tb = tb.tb_next
        return length

    def __repr__(self):
        return ("<%s run=%i successes=%i errors=%i failures=%i skipped=%i>" %
               (util.strclass(self.__class__), self.testsRun, len(self.successes), 
                len(self.errors), len(self.failures), len(self.skipped)))
