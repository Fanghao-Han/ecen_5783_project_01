#!/bin/env python3

# packages
import sys
import getopt

def sensor( sensor_number ):
    print( "This is sensor " + str( sensor_number ) )

def main( argv ):
    #print 'testing project'
    
    cnt = 4
    
    cnt = cnt + 4
    
    print( "stuff = " + str(cnt) )
    
    sensor( cnt )
    cnt+=1
    sensor( cnt )
    cnt+=1
    sensor( cnt )
    cnt+=1
    sensor( cnt )
    cnt+=1
    sensor( cnt )
    cnt+=1

if __name__ == "__main__": main( sys.argv[1:] )
