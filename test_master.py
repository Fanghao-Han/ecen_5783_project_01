#!/bin/env python3

###############################################################################
#
#
#
#
#
#
###############################################################################

import os
import master
import signal
import subprocess
import sys
import time

MIN_DELAY = 1
MAX_DELAY = 20
MAX_COUNT = 10

######################################################
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

    # Create subprocess by calling created master.py script and command
    # line options
    process1 = subprocess.Popen(['python3','master.py','--delay','30'])

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
            
    # Send SIGTERM signal to subprocess
    process1.terminate()

    # Just added clean-up time; could be removed
    time.sleep(MIN_DELAY*5)

    # Syslog update info
    master.syslog_message( "All processes should be terminated" )
    
######################################################
# when run as script, ref where to start
######################################################
if __name__ == "__main__": main()

