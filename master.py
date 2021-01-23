#!/bin/env python3

# add signal handler

import os
import project01
import signal
import subprocess
import sys
import time

MIN_DELAY = 1
MAX_DELAY = 15
MAX_COUNT = 10

def signal_handler(signum, frame):

    global EXT_b
    EXT_b = True
    
    print( "Signal hit; will exit gracefully" )
    project01.syslog_message( "Signal hit" )

def main():

    global EXT_b
    EXT_b = False
    
    CNT_v = 0
    
    signal.signal( signal.SIGINT, signal_handler )

    # project01.main(['-m','--name','sensor_master'])
    
    process1 = subprocess.Popen(['python3','project01.py','--master','--delay','10','--suppress'])

    # loop that will sleep and then check for all exit conditions
    while( not EXT_b ):
    
        # sleep to limit processing
        time.sleep(MAX_DELAY)
        
        # check for return value from the subprocess
        poll_p1 = process1.poll()
        
        # if the subprocess had a return value, can exit the loop
        if (poll_p1 is not None):
            EXT_b = True
            
        # back-up counter to run for defined number of loops
        if( CNT_v >= MAX_COUNT ):
            EXT_b = True
        else:
            CNT_v += 1
            
    process1.terminate()

    time.sleep(MIN_DELAY*5)

    project01.syslog_message( "All processes should be terminated" )
    
if __name__ == "__main__": main()
