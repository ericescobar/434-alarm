#!/usr/bin/python
import time 
import serial 
import sendSMS
def ListenForCode():
	try:
		ser = serial.Serial(
			port='/dev/ttyUSB0',
        		baudrate = 9600,
        		parity=serial.PARITY_NONE,
        		stopbits=serial.STOPBITS_ONE,
        		bytesize=serial.EIGHTBITS,
			timeout=10) 
		x=ser.readline()
        	x=int(x)
		if x>100:
			print x
		#sendSMS.sms("+1xxxxxxxxxx","Your device's code is: "+str(x))
	except:
		print 'took to long!'
#ListenForCode()
