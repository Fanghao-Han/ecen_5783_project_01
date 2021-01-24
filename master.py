#!/bin/env python3

###############################################################################
#
#
#
#
#
#
###############################################################################

# packages
import getopt
import glob
import json
import os
import random
import signal
import sys
import syslog
import time

from os import path

######################################################
# Signal Handler: catch signal but don't exit
# Allows for graceful exit   
######################################################
def signal_handler(signum, frame):
    global EXT_b
    EXT_b = True
    syslog_message( "Signal hit; will exit gracefully" )

######################################################
# Wrapper for writing to syslog
######################################################
def syslog_message( message ):
    syslog.syslog( "[MASTER] " + message )

######################################################
# Helper line for how to run script
######################################################
def help_info():
    print( "Add help info here" )
        
######################################################
# Master function that is the bulk of the 
# functionality of the script
######################################################
def master( sleep_count ):

    # Main while look that should only exit if changed signal handler
    while( not EXT_b ):
        
        # just proof of life message to syslog; FIXME remove after development
        syslog_message( "Master process is alive" )
        
#        DAT_a = []
#        cnt_1 = 0
        
        # find/store all logs in txt_logs directory and the for each file (f)
        # open the file and read each json line and append to the cleared 
        # data array; after reading through a file, check for the number of 
        # lines that were read and print up to the last 10 (less if there are 
        # not 10)
        log_files = glob.glob('txt_logs/*.txt')
        for f in log_files:
        
            # clear input array and reset counter
            INP_a = []
            cnt_2 = 0
        
            # open current file and append read line to array
            with open(f) as fp:
                for line in fp:
                    INP_a.append( json.loads(line) )
                    cnt_2 += 1

            # check number of lines read and add appropriate number to data 
            # array
            if( cnt_2 > 0 ):
                print( "------------------------------" )
                print( " " + INP_a[0]["name"] )
                # less than 10
                if( (cnt_2 > 0) and (cnt_2<10) ):
                    for ii in range(0,cnt_2):
                        print( " - " + str(INP_a[ii]["count"]) + " : " + str(INP_a[ii]["temp"]) )
#                        DAT_a.append( INP_a[ii]["name"] + " : " + str(INP_a[ii]["temp"]) )
#                        cnt_1 += 1
                # 10 or more
                elif( cnt_2 >= 10 ):
                    for ii in range(cnt_2-10,cnt_2):
                        print( " - " + str(INP_a[ii]["count"]) + " : " + str(INP_a[ii]["temp"]) )
#                        DAT_a.append( INP_a[ii]["name"] + " : " + str(INP_a[ii]["temp"]) )
#                        cnt_1 += 1
                    
            # do nothing if count is 0
        
        # print out data array
#        if( cnt_1 > 0 ):
#            for ii in range(0,cnt_1-1):
#                print( DAT_a[ii] )            
        # loop to next file or complete
        
        
        print( "==============================" )
    
        # sleep for the delay count provided on the command line or the
        # default value of 30 seconds
        time.sleep( sleep_count )
    # loop back if EXT_b is still False

######################################################
#
######################################################
def main( argv ):

    # EXT_b is used as a global variable to indicate to exit while loop in 
    # the master() function and is set to True by the signal handler
    global EXT_b

    # Exit variable: Bool
    EXT_b = False
    # Delay variable: Value
    DLY_v = 30
    
    # GETOPT command line option parsing
    try:
        opts, args = getopt.getopt( argv, "hd:", ["help", "delay=" ] )
    except getopt.GetoptError:
        print( "Invalid input; use --help or -h for requirements" )
        # FIXME - look to add syslog error information
        sys.exit(1)
        
    for opt, arg in opts:
        if opt in ( "-h", "--help" ):
            help_info()
            sys.exit(0)
        elif opt in ( "-d", "--delay" ):
            DLY_v = int(arg)
            
    # Signal handler setup for SIGING (ctrl + C) and SIGTERM (kill ID)
    signal.signal( signal.SIGINT, signal_handler )
    signal.signal( signal.SIGTERM, signal_handler )
        
    # Double checks that the txt_logs directory exists and if not creates it
    # it is possible that if this was a newly cloned workspace and this script
    # was run first, that it would not exist yet and the script would try
    # to read files from a directory that does not exists, causing an error
    if( not os.path.isdir('txt_logs') ):
        os.mkdir('txt_logs')
        syslog_message( "txt_logs dir created" )

    # During developement, each time this command was run, it would erase all
    # sensor logs so old logs from previous runs would pop up.  This should be
    # handled by the sensor test script but it is possible that if the sensor
    # scripts are run manually, this script might show old logs but should be
    # able to tell the difference since they will include time/date
#    old_txt_logs = glob.glob('txt_logs/*.txt')
#    for f in old_txt_logs:
#        os.remove(f)

    # Just time stamped message that can be found in syslogs (rasp pi should
    # be found in /var/log/syslog; just grep for any info)
    syslog_message( "Master thread setup" )
    
    # Call the function that has a while loop and delay (either default or
    # input from the command line), will stay in loop until EXT_b is set to
    # True via the signal handler
    master( DLY_v )

######################################################
# when run as script, ref where to start
######################################################
if __name__ == "__main__": main( sys.argv[1:] )



