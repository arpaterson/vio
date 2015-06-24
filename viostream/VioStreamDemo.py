#!/usr/bin/python

# VioStream.py
# Anthony Paterson
# May 2015

import os, sys, time
import VioStream

if __name__ == "__main__":
 
 os.chdir('/var/ww/logs')
 
 cam = VioStream.VioStream('172.16.197.197')
 
 #
 print "\n Testing URL assembly:\n"
 url = cam._commandURL('system?resolution=','1080p30-high-record1080p-streamNO')
 print url

 print "\n Testing command transmission:\n"
 cam.command('setvideomode','1080p30-high-record1080p-streamN') #test an incorrect one
 time.sleep(1)

 cam.command('setvideomode','1080p30-high-record1080p-streamNO') #test a correct one
 time.sleep(1)
 print "\n Doing a Test run of expected usage: \n"
 
 cam.command('resettodefaults')
 time.sleep(10)  #seems to need a lot of time to recover form this one.

 t = time.time() # get current time, seconds since epoch
 ti = int(t)     #round down to integer
 tstr = str(ti)  #convert to string
 cam.command('settime', tstr)
 time.sleep(1)

 cam.command('setvideomode','1080p30-high-record1080p-streamNO')
 cam.command('recordfiletype','mp4')
 cam.command('recordtype','loop')
 cam.command('recordlooptime','30')
 cam.command('recordstart')
 time.sleep(50) #Leave recording for 50 seconds so that at least one loop is discarded
 cam.command('recordtag') #tag at 20 seconds into the second loop.
 cam.command('stillsave') #also save a jpeg to the sdcard.
 time.sleep(0.5)
 cam.command('recordtag') #tag again in close succession
 time.sleep(9.5)	  #this brings us tothe end of the second loop.
 time.sleep(40)		  # a loop should be discarded.
 cam.command('recordtag') #tag 10 seconds into 4th loop.
 time.sleep(60)		  # a loop should be discarded
 cam.command('recordtag') #tag 10 seconds into 6th loop.
 time.sleep(60)
 cam.command('recordstop')
