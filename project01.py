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

def signal_handler(signum, frame):
    syslog_message( "Signal hit" )

def syslog_message( message ):
    syslog.syslog( "[PROJECT01] " + message )

def help_info():
    #print( "Add help info here" )
    syslog_message( "Add help info here" )
    
def sensor( sleep_count, data ):
    while True:
        time.sleep(sleep_count)
        
        data["temp"] += (random.randrange(10) - 5)
        JSN_v = json.dumps( data )

        #print( "Sensor " + sensor_name + " is alive" )
        syslog_message( "Sensor " + data["name"] + " is alive with " + JSN_v )

        data["count"] = (data["count"] + 1)%10000

def main( argv ):

    SNR_b = False
    MST_b = False
    CNT_v = 5
    
    OUT_d = { "name": "generic", "temp": 72, "alarm": 0, "error": 0, "count": 0 }
    
    signal.signal( signal.SIGINT, signal_handler )
    
    try:
        opts, args = getopt.getopt( argv, "hsmd:n:c:", ["help", "sensor", "master", "name=", "count=", "delay=" ] )
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
            CNT_v = int(arg)
        elif opt in ( "-n", "--name" ):
            OUT_d["name"] = arg
        elif opt in ( "-c", "--count" ):
            OUT_d["count"] = int(arg)

    if( (SNR_b == True) and (MST_b == True) ):
        print( "Cannot be defined as master and as sensor; try again" )
        sys.exit(1)
    else:
        if( SNR_b == True ):
            #print( "Sensor thread with name " + NME_s + " setup" )
            syslog_message( "Sensor thread with name " + OUT_d["name"] + " setup" )
            sensor( CNT_v, OUT_d )
            
        elif( MST_b == True ):
            print( "Master thread with name " + OUT_d["name"] + " setup" )


if __name__ == "__main__": main( sys.argv[1:] )



