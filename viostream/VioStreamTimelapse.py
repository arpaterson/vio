#!/usr/bin/python

# VioStream.py
# Anthony Paterson
# May 2015

import os, sys, time
import VioStream

if __name__ == "__main__":
 
 os.chdir('/var/www/logs')
 
 cam = VioStream.VioStream('172.16.197.197')
 
 #reset to defaults
 cam.command('resettodefaults')
 time.sleep(10)  #seems to need a lot of time to recover form this one.

 #set time
 t = time.time() # get current time, seconds since epoch
 ti = int(t)     #round down to integer
 tstr = str(ti)  #convert to string
 cam.command('settime', tstr)
 time.sleep(1)
 
 #set options
 cam.command('setvideomode','1080p30-high-record1080p-streamNO')
 cam.command('recordfiletype','mp4')
 cam.command('recordtype','loop')
 cam.command('recordlooptime','30')

 #start
 #cam.command('recordstart')
 #cam.command('recordtag') #tag at 20 seconds into the second loop.
 #cam.command('recordstop')
 while(True):
  cam.command('stillsave') #also save a jpeg to the sdcard.
  time.sleep(1.0)
 
