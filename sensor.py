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

MAX_SENSORS = 50

######################################################
# Helper line for how to run script
######################################################
def help_info():
    print( "Add help info here" )

######################################################
#
######################################################
def sensor( sleep_count, log_name, data ):
    while( not EXT_b ):
        time.sleep( sleep_count )
        
        data["update"] = True
        data["count"] = (data["count"] + 1)%10000
        data["temp"] += ( random.randrange(10) - 5 )
        
        write_json( "txt_logs/" + log_name, json.dumps( data ) )

        syslog_message( "Sensor " + data["name"] + " is alive with " + json.dumps( data ) )

######################################################
# Signal Handler: catch signal but don't exit
# Allows for graceful exit     
######################################################
def signal_handler(signum, frame):

    # reference to use the global variable; not redeclaration
    # set exit so script can exit while loop
    global EXT_b
    EXT_b = True
    syslog_message( "Signal hit; will exit gracefully" )

######################################################
# Wrapper for writing to syslog
######################################################
def syslog_message( message ):
    syslog.syslog( "[SENSOR] " + message )

######################################################
# Wrapper function to write json string to file
######################################################
def write_json( write_file, json_string ):

    # Open file for append/write, then write json string and new line
    # character, and then close file-pointer
    fp = open( write_file, "a" )
    fp.write( json_string + "\n" )
    fp.close


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
    DLY_v = 5
    # Filename variable: String
    FLN_v = "sensor_"
    # Output variable: Dictionary
    OUT_d = { "name": "generic", "temp": 72, "target_temp": 72, "alarm": 0, "error": 0, "count": 0, "update": False }

    # GETOPT command line option parsing    
    try:
        opts, args = getopt.getopt( argv, "hsn:c:d:t:", ["help", "suppress", "name=", "count=", "delay=", "target_temp=" ] )
    except getopt.GetoptError:
        print( "Invalid input; use --help or -h for requirements" )
        sys.exit(1)
        
    for opt, arg in opts:
        if opt in ( "-h", "--help" ):
            help_info()
            sys.exit(0)
        elif opt in ( "-d", "--delay" ):
            DLY_v = int(arg)
        elif opt in ( "-n", "--name" ):
            OUT_d["name"] = arg
        elif opt in ( "-c", "--count" ):
            OUT_d["count"] = int(arg)
        elif opt in ( "-s", "--suppress" ):
            SPP_b = True
        elif opt in ( "-t", "--target_temp" ):
            OUT_d["target_temp"] = int(arg)

    # Signal handler setup for SIGING (ctrl + C) and SIGTERM (kill ID)            
    signal.signal( signal.SIGINT, signal_handler )
    signal.signal( signal.SIGTERM, signal_handler )
       
    # Double checks that the txt_logs directory exists and if not creates it
    # it is possible that if this was a newly cloned workspace and this script
    # was run first, that it would not exist yet and the script would try
    # to write files from a directory that does not exists, causing an error 
    if( not os.path.isdir('txt_logs') ):
        os.mkdir('txt_logs')
        syslog_message( "txt_logs dir created" )

    # Checks that the name of the file associated with the sensor has not been
    # created/used yet.  For ease, the file name is generically "sensor_#" and
    # will just cycle checking for each value starting at 0 and going up to 
    # MAX_SENSORS.  When a filename is found to not exist, it is then passed on
    for ii in range( MAX_SENSORS ):
        # if file does not exists, update variable and break from for loop
        if not path.exists('txt_logs/' + FLN_v + str(ii) + '.txt' ):
            FLN_v = FLN_v + str(ii) + '.txt'
            break
        # if there is not an avaiable filename, then exit with error
        elif( ii == MAX_SENSORS ):
            print( "ERROR: Max number of sensors reached" )
            # FIXME - add syslog error message
            sys.exit(1)
            
    # Originally wrote setup json info to log right away but think this can
    # be removed now that the master script limits what it prints
#    write_json( "txt_logs/" + FLN_v, json.dumps( OUT_d ) )

    # Send sensor/filename to syslog for tracking; could be removed    
    syslog_message( "Sensor thread with name " + OUT_d["name"] + " setup with log file name " + FLN_v + " and with " + json.dumps( OUT_d ) )
    
    # Call the function that has the while loop that will randomize values and
    # write to log files
    sensor( DLY_v, FLN_v, OUT_d )

######################################################
# when run as script, ref where to start
######################################################
if __name__ == "__main__": main( sys.argv[1:] )



