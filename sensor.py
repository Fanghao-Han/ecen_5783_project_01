#!/bin/env python3
###############################################################################
#
#
#
#
#
#
###############################################################################

# add signal handler

import os
import project01
import signal
import subprocess
import sys
import time

MIN_DELAY = 1
MAX_DELAY = 15

def signal_handler(signum, frame):
    global EXT_b
    EXT_b = True
    
    print( "Signal hit; will exit gracefully" )
    project01.syslog_message( "Signal hit" )
    
def main():

    global EXT_b
    EXT_b = False
    
    signal.signal( signal.SIGINT, signal_handler )

    process1 = subprocess.Popen(['python3','project01.py','--sensor','--name','sensor_01','--count','1000','--delay','10'])
    time.sleep(MIN_DELAY)
    process2 = subprocess.Popen(['python3','project01.py','--sensor','--name','sensor_02','--count','2000','--delay','12'])
    time.sleep(MIN_DELAY)
    process3 = subprocess.Popen(['python3','project01.py','--sensor','--name','sensor_03','--count','3000','--delay','4'])

    while( not EXT_b ):
        time.sleep(MAX_DELAY)

    process1.terminate()
    process2.terminate()
    process3.terminate()

    time.sleep(MIN_DELAY*5)

    project01.syslog_message( "All processes should be terminated" )

    #project01.main(['-s','--name','sensor_05'])
    #project01.main(['-s','--name','sensor_03'])

if __name__ == "__main__": main()
