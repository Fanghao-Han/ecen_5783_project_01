#!/bin/env python3

# add signal handler

import project01
import subprocess
import time

process1 = subprocess.Popen(['python3','project01.py','-s','--name','sensor_01','-c','2'])
time.sleep(1)
process2 = subprocess.Popen(['python3','project01.py','-s','--name','sensor_02','-c','3'])
time.sleep(1)
process3 = subprocess.Popen(['python3','project01.py','-s','--name','sensor_03','-c','4'])
time.sleep(20)

process1.terminate()
process2.terminate()
process3.terminate()

time.sleep(5)

project01.syslog_message( "All processes should be terminated" )

#project01.main(['-s','--name','sensor_05'])
#project01.main(['-s','--name','sensor_03'])

