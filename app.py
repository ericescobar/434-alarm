from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import sqlite3
import sendSMS
import subprocess
import datetime
import time
import SendNewSensorCode

app = Flask(__name__)
Bootstrap(app)

def test():
	sendSMS.sms("+15599772611","nice")

@app.route('/')
def index():
	return render_template("index.html")
@app.route('/list')
def list():
	con = sqlite3.connect("alarm.db")
   	con.row_factory = sqlite3.Row
   	cur = con.cursor()
   	cur.execute("select * from phonelist")
      	rows = cur.fetchall(); 
	CurrentTime=time.time()
	#test()
	for i in rows:
		print CurrentTime - int(i[5])
	print rows
   	return render_template("list.html",rows = rows, CurrentTime=CurrentTime)
    	#return render_template('index.html')

@app.route('/sensorlist')
def sensorlist():
	con = sqlite3.connect("alarm.db")
   	con.row_factory = sqlite3.Row
   	cur = con.cursor()
   	cur.execute("select * from sensorlist")
      	rows = cur.fetchall(); 
   	return render_template("sensorlist.html",rows = rows)
@app.route('/sensorlog')
def sensorlog():
	con = sqlite3.connect("alarm.db")
   	con.row_factory = sqlite3.Row
   	cur = con.cursor()
	beforeTime=int(time.time()-86400)
	cur.execute("select * from sensorlog WHERE last_seen_unix > ? ORDER BY last_seen_unix DESC", (beforeTime,))
      	rows = cur.fetchall(); 
   	return render_template("sensorlog.html",rows = rows)

@app.route("/sensor_config")
def sensor_config():
	SendNewSensorCode.ListenForCode()		
	return render_template("/sensor_config.html")

@app.route('/addsensor', methods=['GET','POST'])
def addsensor():
    	return render_template("addsensor.html")

@app.route('/findcode')
def findcode():
	return redirect('/findcode')
	SendNewSensorCode.ListenForCode()	
@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
	if request.method == 'POST':
		SensorName = request.form['Sname']
		SensorCode = request.form['Scode']
		SensorType = request.form['Stype']
		SensorLocation = request.form['Slocation']
         	with sqlite3.connect("alarm.db") as con:
            		cur = con.cursor()
            		cur.execute("""INSERT INTO sensorlist (name,code,type,location) VALUES (?,?,?,?)""",(SensorName,SensorCode,SensorType,SensorLocation) )            
            		con.commit()
            		msg = "Record successfully added"
	     	return render_template("result.html",msg = 'msg')
         	con.close()

@app.route('/dropdown')
def dropdown():
	return render_template('dropdown.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

