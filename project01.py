#!/bin/env python3

# packages
import sys
import getopt
import time

def help_info():
    print( "Add help info here" )

def sensor( sensor_name, sleep_count ):
    while True:
        time.sleep(sleep_count)
        print( "Sensor " + sensor_name + " is alive" )

def main( argv ):

    SNR_b = False
    MST_b = False
    NME_s = ""
    CNT_v = 5
    
    try:
        opts, args = getopt.getopt( argv, "hsmn:c:", ["help", "sensor", "master", "name=", "count=" ] )
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
        elif opt in ( "-n", "--name" ):
            NME_s = arg
        elif opt in ( "-c", "--count" ):
            CNT_v = int(arg)

    if( (SNR_b == True) and (MST_b == True) ):
        print( "Cannot be defined as master and as sensor; try again" )
        sys.exit(1)
        
    elif( NME_s == "" ):
        if( SNR_b == True ):
            print( "Generic sensor thread setup" )
            sensor( "generic" , CNT_v )
            
        elif( MST_b == True ):
            print( "Generic master thread setup" )
    
    else:
        if( SNR_b == True ):
            print( "Sensor thread with name " + NME_s + " setup" )
            sensor( NME_s, CNT_v )
            
        elif( MST_b == True ):
            print( "Master thread with name " + NME_s + " setup" )


if __name__ == "__main__": main( sys.argv[1:] )



