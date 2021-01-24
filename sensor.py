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

# Signal Handler    
def signal_handler(signum, frame):
    global EXT_b
    EXT_b = True
    syslog_message( "Signal hit; will exit gracefully" )

def syslog_message( message ):
    syslog.syslog( "[PROJECT01] " + message )

def help_info():
    #print( "Add help info here" )
    syslog_message( "Add help info here" )
    
def sensor( sleep_count, log_name, data ):
    while( not EXT_b ):
        time.sleep( sleep_count )
        
        data["update"] = True
        data["count"] = (data["count"] + 1)%10000
        data["temp"] += ( random.randrange(10) - 5 )
        
        write_json( "txt_logs/" + log_name, json.dumps( data ), True )

        syslog_message( "Sensor " + data["name"] + " is alive with " + json.dumps( data ) )
        
def write_json( write_file, json_string, append ):
    if( append ):
        fp = open( write_file, "a" )
    else:
        fp = open( write_file, "w" )
        
    fp.write( json_string + "\n" )
    fp.close

def main( argv ):

    global EXT_b

    # Exit variable: Bool
    EXT_b = False
    # Delay variable: Value
    DLY_v = 5
    # Filename variable: String
    FLN_v = "sensor_"
    # Output variable: Dictionary
    OUT_d = { "name": "generic", "temp": 72, "target_temp": 72, "alarm": 0, "error": 0, "count": 0, "update": False }
    
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
            
    signal.signal( signal.SIGINT, signal_handler )
    signal.signal( signal.SIGTERM, signal_handler )
        
    if( not os.path.isdir('txt_logs') ):
        os.mkdir('txt_logs')
        syslog_message( "txt_logs dir created" )

    for ii in range( MAX_SENSORS ):
        if not path.exists('txt_logs/' + FLN_v + str(ii) + '.txt' ):
            FLN_v = FLN_v + str(ii) + '.txt'
            break
        elif( ii == MAX_SENSORS ):
            print( "ERROR: Max number of sensors reached" )
            sys.exit(1)
            
    write_json( "txt_logs/" + FLN_v, json.dumps( OUT_d ), False )
    
    syslog_message( "Sensor thread with name " + OUT_d["name"] + " setup with log file name " + FLN_v + " and with " + json.dumps( OUT_d ) )
    
    sensor( DLY_v, FLN_v, OUT_d )
            


if __name__ == "__main__": main( sys.argv[1:] )



