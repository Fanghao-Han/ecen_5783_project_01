#!/bin/env python3

# add signal handler

import project01
import subprocess
import time

process1 = subprocess.Popen(['python3','project01.py','--sensor','--name','sensor_01','--count','1000','--delay','10'])
time.sleep(1)
process2 = subprocess.Popen(['python3','project01.py','--sensor','--name','sensor_02','--count','2000','--delay','12'])
time.sleep(1)
process3 = subprocess.Popen(['python3','project01.py','--sensor','--name','sensor_03','--count','3000','--delay','4'])
time.sleep(60)

process1.terminate()
process2.terminate()
process3.terminate()

time.sleep(5)

project01.syslog_message( "All processes should be terminated" )

#project01.main(['-s','--name','sensor_05'])
#project01.main(['-s','--name','sensor_03'])

