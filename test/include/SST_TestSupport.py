#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import Python System Level Modules
import os
import sys
import subprocess


################################################################################
# SUPPORT CODE

def does_file_exist(fpath):
    """ Returns true if file exists """
    return os.path.isfile(fpath)

####

def is_exe(fpath):
    """ Returns true if file exists and is a executable """
    return does_file_exist(fpath) and os.access(fpath, os.X_OK)

####

def list_file_directory(fpath):
    """ List the directory contents of a filepath.  File does not have to exist """   
    dir = os.path.dirname(fpath)
    dirlist = os.listdir(dir)
    print "Files in Directory: {0}".format(dir)
    for entry in dirlist:
        print entry
    
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

def check_timout_flag():
    pass
    #TODO: Look at timeLimitEnforcer code in shunit2 to see how this whole mess works
    
    # Check for Timeout Situation
#    TIME_FLAG="/tmp/TimeFlag_$$_${__timerChild}" 
#    if os.path.exists(TIME_FLAG) == True:
    
#           TODO: HANDLE Timeout Situation
#            TIME_FLAG=/tmp/TimeFlag_$$_${__timerChild} 
#            if [ -e $TIME_FLAG ] ; then 
#                 echo " Time Limit detected at `cat $TIME_FLAG` seconds" 
#                 fail " Time Limit detected at `cat $TIME_FLAG` seconds" 
#                 rm $TIME_FLAG 
#                 return 
#            fi 
    

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

