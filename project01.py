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
import sys
import getopt
import time
import syslog
import json
import random
import signal
import os

# Signal Handler: catch signal but don't exit
# let calling script handle and 
def signal_handler_suppress(signum, frame):
    syslog_message( "Signal hit" )
    
def signal_handler_exit(signum, frame):
    global EXT_b
    EXT_b = True
    syslog_message( "Signal hit; will exit gracefully" )

def syslog_message( message ):
    syslog.syslog( "[PROJECT01] " + message )

def help_info():
    #print( "Add help info here" )
    syslog_message( "Add help info here" )
    
def sensor( sleep_count, data ):
    while( not EXT_b ):
        time.sleep( sleep_count )
        
        data["temp"] += ( random.randrange(10) - 5 )
        JSN_v = json.dumps( data )

        #print( "Sensor " + sensor_name + " is alive" )
        syslog_message( "Sensor " + data["name"] + " is alive with " + JSN_v )

        data["count"] = (data["count"] + 1)%10000
        
def master( sleep_count ):
    while( not EXT_b ):
        time.sleep( sleep_count )
        syslog_message( "Master process is alive" )
        

def main( argv ):

    global EXT_b

    # Exit variable: Bool
    EXT_b = False
    # Sensor variable: Bool
    SNR_b = False
    # Master variable: Bool
    MST_b = False
    # Suppress variable: Bool
    SPP_b = False
    # Delay variable: Value
    DLY_v = 5
    # Output variable: Dictionary
    OUT_d = { "name": "generic", "temp": 72, "alarm": 0, "error": 0, "count": 0 }
    
    try:
        opts, args = getopt.getopt( argv, "hsmd:n:c:", ["help", "sensor", "master", "suppress", "name=", "count=", "delay=" ] )
    except getopt.GetoptError:
        print( "Invalid input; use --help or -h for requirements" )
        sys.exit(1)
        
    for opt, arg in opts:
        if opt in ( "-h", "--help" ):
            help_info()
            sys.exit(0)
        elif opt in ( "-s", "--sensor" ):
            SNR_b = True
        elif opt in ( "-m", "--master" ):
            MST_b = True
        elif opt in ( "-d", "--delay" ):
            DLY_v = int(arg)
        elif opt in ( "-n", "--name" ):
            OUT_d["name"] = arg
        elif opt in ( "-c", "--count" ):
            OUT_d["count"] = int(arg)
        elif opt in ( "--suppress" ):
            SPP_b = True
            
            
    if( SPP_b == True ):
        signal.signal( signal.SIGINT, signal_handler_suppress )
    else:
        signal.signal( signal.SIGINT, signal_handler_exit )

    if( (SNR_b == True) and (MST_b == True) ):
        print( "Cannot be defined as master and as sensor; try again" )
        sys.exit(1)
    else:
        if( SNR_b == True ):
            syslog_message( "Sensor thread with name " + OUT_d["name"] + " setup" )
            sensor( DLY_v, OUT_d )
            
        elif( MST_b == True ):
            syslog_message( "Master thread setup" )
            master( DLY_v )


if __name__ == "__main__": main( sys.argv[1:] )



