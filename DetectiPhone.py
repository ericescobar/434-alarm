#!/usr/bin/python
from awake import wol
import time
import socket
import os
import sqlite3
import datetime

def WOL(mac,ip,name):
    	#Send Magic packet to wakeup iPhone
	for iteration in range(10):
		wol.send_magic_packet(mac, dest=ip , port=9)
		time.sleep(.1)	
	#Check to see if iPhone is online	
    	time.sleep(2)
	response=1
	attempts=0
	#Try 3 times to ping it
	while response != 0 and attempts<3:
		response = os.system("ping -c 1 " + ip + " > /dev/null" )
		attempts=attempts+1
	if response == 0:
		#print "Online"
		pingstatus = "Online"
	else:
		#print "Offline"
		pingstatus = "Offline"
	return pingstatus

def SQL_Lookup():
	db = sqlite3.connect('alarm.db')
	cursor = db.cursor()
	data=cursor.execute('''SELECT mac,ip,name FROM phonelist'''
				)
	DeviceList=[];
	for row in data:
		mac=row[0]
		ip=row[1]
		name=row[2]
		DeviceList.append([mac,ip,name])
		#print mac
	return DeviceList
def WriteLog(mac,ip,name,status):
	#Define Time
	tUTC=time.time()
	timedate = datetime.datetime.now()
	tdate = timedate.strftime('%Y-%m-%d_%H:%M:%S')
	tday = timedate.day
	tmonth = timedate.month
	tyear = timedate.year
	thour =  timedate.hour
	tminute = timedate.minute
	tsecond = timedate.second
	#Start SQL stuff
	db = sqlite3.connect('alarm.db')
	cursor = db.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS phonelog(id INTEGER PRIMARY KEY, 
		mac TEXT, 
		ip TEXT, 
		name TEXT, 
		status TEXT, 
		date_utc INTEGER, 
		date_time TEXT,
		year INTEGER,
		month INTEGER,
		day INTEGER,
		hour INTEGER,
		minute INTEGER,
		second INTEGER)'''
		)
	cursor.execute('''INSERT INTO phonelog(mac, 
		ip,
		name, 
		status, 
		date_utc, 
		date_time,
		year,
		month,
		day,
		hour,
		minute,
		second)VALUES(?,?,?,?,?,?,?,?,?,?,?,?)''',(mac,ip,name,status,tUTC,tdate,tyear,tmonth,tday,thour,tminute,tsecond)
		)
	db.commit()
	if status == "Online":
		cursor.execute('''UPDATE phonelist SET last_seen=? WHERE mac=?''',(tUTC,mac)
		)
		print "Updated Last Seen"  
		db.commit()
	db.close()

DeviceList=SQL_Lookup()
for device in DeviceList:
	ip=device[1]
	mac=device[0]
	name=device[2]
	status=WOL(mac,ip,name)
	print name + ': ' + status
	WriteLog(mac,ip,name,status)
