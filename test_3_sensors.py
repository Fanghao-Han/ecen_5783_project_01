#!/bin/env python3

###############################################################################
#
#
#
#
#
#
###############################################################################

import glob
import os
import sensor
import signal
import subprocess
import sys
import time

MIN_DELAY = 1
MAX_DELAY = 20
MAX_COUNT = 10

######################################################.
# Signal Handler: catch signal but don't exit
# Allows for graceful exit 
######################################################
def signal_handler(signum, frame):   

    global EXT_b
    EXT_b = True
     
    print( "Signal hit; will exit gracefully" )
    master.syslog_message( "Signal hit" )
    
######################################################
######################################################
def main():

    global EXT_b
    EXT_b = False
    
    CNT_v = 0
    
    # Setup signal handler for wrapper script
    signal.signal( signal.SIGINT, signal_handler )
    signal.signal( signal.SIGTERM, signal_handler )
    
    old_txt_logs = glob.glob('txt_logs/*.txt')
    for f in old_txt_logs:
        os.remove(f)
    
    process1 = subprocess.Popen(['python3','sensor.py','--name','sensor_01','--count','1000','--delay','10'])
    time.sleep(MIN_DELAY)
    process2 = subprocess.Popen(['python3','sensor.py','--name','sensor_02','--count','2000','--delay','10'])
    time.sleep(MIN_DELAY)
    process3 = subprocess.Popen(['python3','sensor.py','--name','sensor_03','--count','3000','--delay','10'])

    # loop that will sleep and then check for all exit conditions
    while( not EXT_b ):
    
        # sleep to limit processing
        time.sleep(MAX_DELAY)
        
        # check for return value from the subprocesses
        poll_p1 = process1.poll()
        poll_p2 = process2.poll()
        poll_p3 = process3.poll()

        # if all the subprocesses had a return value, can exit the loop
        if (poll_p1 is not None) and (poll_p2 is not None) and (poll_p3 is not None):
            EXT_b = True
            
        # back-up counter to run for defined number of loops
        if( CNT_v >= MAX_COUNT ):
            EXT_b = True
        else:
            CNT_v += 1

    sensor.syslog_message( "term p1" )
    process1.terminate()
    sensor.syslog_message( "term p2" )
    process2.terminate()
    sensor.syslog_message( "term p3" )
    process3.terminate()

    time.sleep(MIN_DELAY*5)

    sensor.syslog_message( "All processes should be terminated" )
    
######################################################
# when run as script, ref where to start
######################################################
if __name__ == "__main__": main()

