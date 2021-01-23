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

# Signal Handler: catch signal but don't exit
# let calling script handle and     
def signal_handler(signum, frame):
    global EXT_b
    EXT_b = True
    syslog_message( "Signal hit; will exit gracefully" )

def syslog_message( message ):
    syslog.syslog( "[PROJECT01] " + message )

def help_info():
    #print( "Add help info here" )
    syslog_message( "Add help info here" )
        
def master( sleep_count ):
    while( not EXT_b ):
        time.sleep( sleep_count )
        syslog_message( "Master process is alive" )
        
        log_files = glob.glob('txt_logs/*.txt')
        for f in log_files:
            fp = open( f, "r" )
            print(fp.read())
            fp.close
            #print( f )

def main( argv ):

    global EXT_b

    # Exit variable: Bool
    EXT_b = False
    # Delay variable: Value
    DLY_v = 5
    # Filename variable: String
    FLN_v = "sensor_"
    # Output variable: Dictionary
    #OUT_d = { "name": "generic", "temp": 72, "target_temp": 72, "alarm": 0, "error": 0, "count": 0, "update": False }
    
    try:
        opts, args = getopt.getopt( argv, "hd:", ["help", "delay=" ] )
    except getopt.GetoptError:
        print( "Invalid input; use --help or -h for requirements" )
        sys.exit(1)
        
    for opt, arg in opts:
        if opt in ( "-h", "--help" ):
            help_info()
            sys.exit(0)
        elif opt in ( "-d", "--delay" ):
            DLY_v = int(arg)
            
            
    signal.signal( signal.SIGINT, signal_handler )
    signal.signal( signal.SIGTERM, signal_handler )
        
    if( not os.path.isdir('txt_logs') ):
        os.mkdir('txt_logs')
        syslog_message( "txt_logs dir created" )

    old_txt_logs = glob.glob('txt_logs/*.txt')
    for f in old_txt_logs:
        os.remove(f)

    syslog_message( "Master thread setup" )
    master( DLY_v )


if __name__ == "__main__": main( sys.argv[1:] )



