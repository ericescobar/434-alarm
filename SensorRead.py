#!/usr/bin/python
import time
import os
import sqlite3
import datetime
import serial
import sendSMS

def SQL_Lookup(code):
	print code
	db = sqlite3.connect('alarm.db')
	cursor = db.cursor()
	data=cursor.execute('''SELECT name,type,location FROM sensorlist WHERE code=?''', (str(code),))
        SensorList=[];
        for row in data:
                name=row[0]
                type=row[1]
                location=row[2]
                SensorList.append(name)
                SensorList.append(type)
                SensorList.append(location)
	if not SensorList:
		SensorList.append("Unknown")
		SensorList.append("Unknown")
		SensorList.append("Unknown")
	print SensorList
	return SensorList
	
def WriteLog(SensorList,RadioID):
	#Define Time
	tUTC=time.time()
	name=SensorList[0]
	type=SensorList[1]
	code=RadioID
	location=SensorList[2]
	timedate = datetime.datetime.now()
	tdate = timedate.strftime('%Y-%m-%d_%H:%M:%S')
	#Start SQL stuff
	db = sqlite3.connect('alarm.db')
	cursor = db.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS sensorlog(id INTEGER PRIMARY KEY, 
		name TEXT, 
		code INTEGER, 
		type TEXT, 
		last_seen_unix INTEGER,
		last_seen_human TEXT, 
		location TEXT)'''
		)
	cursor.execute('''INSERT INTO sensorlog(name, 
		code,
		type, 
		last_seen_unix, 
		last_seen_human, 
		location
		)VALUES(?,?,?,?,?,?)''',(name,code,type,tUTC,tdate,location)
		)
	db.commit()
	db.close()
ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS)
#Initial values for first run of the loop
LastSensor=0
loggedTime=5
#

while 1:
        RadioID=ser.readline()
        RadtioID=int(RadioID)
	currentTime = time.time()
        if RadioID>100 and (RadioID != LastSensor or currentTime-loggedTime>1):
		#The and/or business 'debounces' the button
		#This makes sure one log per action instead of 5 logs 1ms apart
		#print RadioID
		SensorList=SQL_Lookup(int(RadioID))	
		WriteLog(SensorList,RadioID)
                LastSensor = RadioID
		loggedTime= time.time()
