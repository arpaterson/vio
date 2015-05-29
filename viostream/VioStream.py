#!/usr/bin/python

# VioStream.py
# Anthony Paterson
# May 2015

import os, sys, time
import logging
import socket
import unicodedata

# urllib support for Python 2 and Python 3
try:
    from urllib.request import urlopen, HTTPError, URLError
except ImportError:
    from urllib2 import urlopen, HTTPError, URLError

#

class VioStream:
	def __init__(self,ip):
	 self.ip = ip
	 self.timeout = 5.0
	 
	
	#statusMatrix = {
	#TEMPLATE:
	# http:/<ip>/api returns all properties in xml format not hex like gopro.

	commandMatrix = {
	 #System
	 'setsubnet':{	#takes effect after the ipaddress is changed.
	  'cmd':'system/subnet=',
	  'value':'255.255.255.252'
	 },
	 'setipaddress':{
	  'cmd':'system/ipadress',
	  'value':'172.16.197.197'
	 },
	 'settime':{
	  'cmd':'system?time=',
	  'value':'0' #default to utc Epoch
	 },
	 'setutctimezone':{
	  'cmd':'system?utc=',
	  'value':'0' #default to gmt
	 },
	 #'user':{
	 # 'cmd':'system?user=',
	 # 'value':''
	 #}
	 #'password':{
	 # 'cmd':'system?password=',
	 # 'value':''
	 #}
	 'resettodefaults':{
	  'cmd':'system/defaults'
	 },
	 'savesettings':{
	  'cmd':'system/settingssave'
	 },
	 'mountmsd':{ #Note this will disconnect the camera, and requires a power cycle to get RNDIS interface back.
	  'cmd':'system/msd'
	 },

	 #Sensor = quality/record res/sensor res/
	 'setvideomode':{
	  'cmd':'system?resolution=',
	  'value':'1080p30-high-record1080p-streamNO' #default to first setting listed in Stream Manual V1_14
	 },

	 #Power
	 'powertimeout':{
	  'cmd':'power/timeout',
	  'value':'0' #default to zero, inactivity power off timeout disabled.
	 },
	 'poweroff':{
	  'cmd':'power/stop'
	 },
	 'poweron':{
	  'cmd':'power/start'
	 },
	 
	 #Sensor
	 'sharpener':{
	  'cmd':'sensor?sharpener=',
	  'value':'1' #default on
	 },
	 'noisefilter':{
	  'cmd':'sensor?noisefilter=',
	  'value':'1' #default on
	 },
	 'exposuretime':{
	  'cmd':'sensor?exposuretime=',
	  'value':'70' #default 70, range 10-255 (40-90 rocommended)
	 },
	 'exposurezone':{
	  'cmd':'sensor?exposurezone=',
	  'value':'fullframe' #default fullframe, can be spot
	 },

	 #Record
	 'recordstart':{
	  'cmd':'record/start'
	 },
	 'recordstop':{
	  'cmd':'record/stop'
	 },
	 'recordtype':{
	  'cmd':'record?type=',
	  'value':'loop' #clip, loop, loopforward
	 },
	 'recordfiletype':{
	  'cmd':'record/filetype=',
	  'value':'mp4' #mp4, mov
	 },
	 'recordlooptime':{
	  'cmd':'record?looptime=',
	  'value':'30' #seconds, only kept if tagged when in loop mode.
	 },
	 'recordloopforwardtime':{
	  'cmd':'record?loopforwardtime=',
	  'value':'30' #seconds,
	 },
	 'recordtag':{
	  'cmd':'tagging/tag'
	 },
	 'downloadvideo':{
	  'cmd':'record/file/',
	  'value':''
	 },
	 #'deletevideo':{
	 # 'cmd':'record/file/{}/delete', #How to do this?? Add 'append' field and modify command()?
	 # 'value':'' 
	 #}
	 
	 #Stream
	 'startstream':{
	  'cmd':'stream/start'
	 },
	 'stopstream':{
	  'cmd':'stream/stop'
	 },

	 #MJpeg
	 'mjpegcapture':{
	  'cmd':'mjpeg/capture.jpg' #how to handle this?? it returns an html page/the jpg file?
	 },
	 'mjpegstart':{
	  'cmd':'mjpeg/start'	  
	 },
	 'mjpegstop':{
	  'cmd':'mjpeg/stop'
	 },
	 'mjpegquality':{
	  'cmd':'mjpeg?quality=',
	  'value':'75'	  
	 },

	 #Still
	 'stillcapture':{
	  'cmd':'still/capture.jpg'
	 },
	 'stillsave':{
	  'cmd':'still/save'
	 },
	 'stillquality':{
	  'cmd':'still?quality=',
	  'value':'75' 
	 },

	 #Overlay
	 'overlaystart':{
	  
	 },
	 'overlaystop':{
	  
	 },
	 'overlayxpos':{
	  
	 },
	 'overlayypos':{
	  
	 },
	 'overlayheight':{
	  
	 },
	 'overlaycolor':{
	  
	 },
	 
	 #Wifi Access Point
	 #NOT USED

	 #Wifi Client
	 #NOTUSED

	 #Microphone
	 #NOTUSED

	 #Beeper
	 'beeperstart':{
	  'cmd':'beeper/start'
	 },
	 'beeperstop':{
	  'cmd':'beeper/stop'
	 },
	 'beepervolume':{
	  'cmd':'beeper?volume=',
	  'value':'5'
	 },
	 
	 #SDCard
	 'sdcardformat':{
	  'cmd':'sdcard/format/yes'
	 },
	 'sdcardeject':{
	  'cmd':'sdcard/eject'
	 }
	}


	def command(self, command, value=None):
         func_str = 'VioStream.command({}, {})'.format(command, value)

         if command in self.commandMatrix:
          args = self.commandMatrix[command]
          # accept both None and '' for commands without a value
          if value == '':
              value = None
          # build the final url
          url = self._commandURL(args['cmd'], value)

          # attempt to contact the camera
          try:
              urlopen(url, timeout=self.timeout).read()
	      sys.stderr.write('{} - http success!\n'.format(func_str))
              return True
          except (HTTPError, URLError, socket.timeout) as e:
              sys.stderr.write('{} - error opening {}: {}\n'.format(
                  func_str, url, e))
	
         # catchall return statement
         return False
	
	def _commandURL(self,command, value):
	 if value is not None:
	  return 'http://{}/api/{}{}'.format(self.ip,command,value)
	 else:
	  return 'http://{}/api/{}'.format(self.ip,command)
	 
if __name__ == "__main__":

 cam = VioStream('172.16.197.197')
 
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
