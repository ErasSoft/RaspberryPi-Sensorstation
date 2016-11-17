#!/usr/bin/python
# Hochschule Neubrandenburg
# VMGG33 - Informatik-Projekt
# Verfasser: Tino Schuldt
# Datum: 21.12.2015


# Bibliotheken einbinden
from time import *
import os.path
import sys


# Absoluten Pfad der Datei auslesen
pfad = os.path.dirname(os.path.abspath(sys.argv[0]))
# Eine Ebene hoeher gehen ins Hauptverzeichnis
pfad = pfad.rsplit('/', 1)[0]

# Paramter: 1.Sensor - 2.Laufzeit - 3.Intervall - (4.Gpio-Nummer1 - 5.Gpio-Nummer2)
try:
	sensor = sys.argv[1]
except:
	sensor = "NULL"
try:
	endtime = sys.argv[2]
except:
	endtime = 5
try:
	inp1 = sys.argv[3]
except:
	inp1 = 10
try:
	gp1 = sys.argv[4]
except:
	gp1 = 4
try:
	gp2 = sys.argv[5]
except:
	gp2 = 4


### FUNKTIONEN ###
# Aktuelles Datum und Uhrzeit im TIMESTAMP-Format liefern
def getTimestamp():
	# aktuelle, lokale Zeit als Tupel
	lt = localtime()
	# Entpacken des Tupels, Datum
	jahr, monat, tag, stunde, minute, sekunde = lt[0:6]
	timestamp = "%04i-%02i-%02i %02i:%02i:%02i" % (jahr,monat,tag,stunde,minute,sekunde)
	return timestamp
# Ins Logfile schreiben
def writeToLogfile(message):
	print(message)
	f = open(pfad+"/logfiles/sensorstation.txt", "a")
	f.write(message+"\n")
	f.close()
# Aktuelles Datum und Uhrzeit in Datetimeobjekt
def getDatetime():
	import datetime
	return datetime.datetime.strptime(getTimestamp(), '%Y-%m-%d %H:%M:%S')
def saveDHT22(gp1, inp1):
	# Sensor initialisieren
	from sensor import DHT22
	sensor_dht22 = DHT22(gp1)
	# Datenbank und Bibliotheken einbinden
	import sqlite3
        import time
	# Startzeit und startvariable setzen
	d1 = getDatetime()
	t1 = time.mktime(d1.timetuple() )
	startSave = True
	# Verbindung aufbauen
	connection = sqlite3.connect(pfad+"/data/database.db")
	cursor = connection.cursor()		
	# Einmalig die Tabelle erstellen
	sql_command = """
	CREATE TABLE IF NOT EXISTS dht22 (
		timestamp TIMESTAMP PRIMARY KEY,
		temperature FLOAT,
		humidity FLOAT
	) ;"""
	cursor.execute(sql_command)
	while(startSave):
		# Sensor auslesen
		humidity, temperature = sensor_dht22.read()
		timestamp = getTimestamp()
		# Werte speichern
		cursor.execute("INSERT INTO dht22 (timestamp, temperature, humidity) VALUES (?,?,?)", (timestamp, temperature, humidity))
		print("%s %s %s" %(timestamp, temperature, humidity) )
		connection.commit()
		# Warten wie im Intervall angegeben
		inp1 = int(inp1)
		for i in range(inp1):
			time.sleep(1)
			d2 = getDatetime()
			t2 = time.mktime(d2.timetuple() )
			# Pruefen, ob Timestamp von Anfang ueber der Minuten Zeit liegt
			mi = int(t2-t1)/60
			if (int(mi) >= int(endtime) ):
				startSave = False
				break
	connection.close()
def saveDS18B20(gp1, inp1):
	# Sensor initialisieren
	from sensor import DS18B20
	sensor_ds18b20 = DS18B20()
	# Datenbank und Bibliotheken einbinden
	import sqlite3
        import time
	# Startzeit und startvariable setzen
	d1 = getDatetime()
	t1 = time.mktime(d1.timetuple() )
	startSave = True
	# Verbindung aufbauen
	connection = sqlite3.connect(pfad+"/data/database.db")
	cursor = connection.cursor()		
	# Einmalig die Tabelle erstellen
	sql_command = """
	CREATE TABLE IF NOT EXISTS ds18b20 (
		timestamp TIMESTAMP PRIMARY KEY,
		temperature FLOAT
	) ;"""
	cursor.execute(sql_command)
	while(startSave):
		# Sensor auslesen
		temperature = sensor_ds18b20.read()
		timestamp = getTimestamp()
		# Werte speichern
		cursor.execute("INSERT INTO ds18b20 (timestamp, temperature) VALUES (?,?)", (timestamp, temperature))
		print("%s %s" %(timestamp, temperature) )
		connection.commit()
		# Warten wie im Intervall angegeben
		inp1 = int(inp1)
		for i in range(inp1):
			time.sleep(1)
			d2 = getDatetime()
			t2 = time.mktime(d2.timetuple() )
			# Pruefen, ob Timestamp von Anfang ueber der Minuten Zeit liegt
			mi = int(t2-t1)/60
			if (int(mi) >= int(endtime) ):
				startSave = False
				break
	connection.close()
def saveHCSR04(gp1, gp2, inp1):
	# Sensor initialisieren
	from sensor import HCSR04
	sensor_hcsr04 = HCSR04(gp1,gp2)
	# Datenbank und Bibliotheken einbinden
	import sqlite3
        import time
	# Startzeit und startvariable setzen
	d1 = getDatetime()
	t1 = time.mktime(d1.timetuple() )
	startSave = True
	# Verbindung aufbauen
	connection = sqlite3.connect(pfad+"/data/database.db")
	cursor = connection.cursor()		
	# Einmalig die Tabelle erstellen
	sql_command = """
	CREATE TABLE IF NOT EXISTS hcsr04 (
		timestamp TIMESTAMP PRIMARY KEY,
		distance FLOAT
	) ;"""
	cursor.execute(sql_command)
	while(startSave):
		# Sensor auslesen
		distance = sensor_hcsr04.read()
		timestamp = getTimestamp()
		# Werte speichern
		cursor.execute("INSERT INTO hcsr04 (timestamp, distance) VALUES (?,?)", (timestamp, distance))
		print("%s %s" %(timestamp, distance) )
		connection.commit()
		# Warten wie im Intervall angegeben
		inp1 = int(inp1)
		for i in range(inp1):
			time.sleep(1)
			d2 = getDatetime()
			t2 = time.mktime(d2.timetuple() )
			# Pruefen, ob Timestamp von Anfang ueber der Minuten Zeit liegt
			mi = int(t2-t1)/60
			if (int(mi) >= int(endtime) ):
				startSave = False
				break
	connection.close()

### MAIN ###
if (sensor.upper() == "DHT22"):
	writeToLogfile("LOG: %s - Automatic recording of the sensor %s at the GPIO number %s started." % (getTimestamp(), sensor, gp1) )
	saveDHT22(gp1, inp1)
	writeToLogfile("LOG: %s - Automatic recording of the sensor %s at the GPIO number %s stopped." % (getTimestamp(), sensor, gp1) )
elif (sensor.upper() == "DS18B20"):
	writeToLogfile("LOG: %s - Automatic recording of the sensor %s at the GPIO number %s started." % (getTimestamp(), sensor, gp1) )
	saveDS18B20(gp1, inp1)
	writeToLogfile("LOG: %s - Automatic recording of the sensor %s at the GPIO number %s stopped." % (getTimestamp(), sensor, gp1) )
elif (sensor.upper() == "HCSR04"):
	writeToLogfile("LOG: %s - Automatic recording of the sensor %s at the GPIO number %s, %s started." % (getTimestamp(), sensor, gp1, gp2) )
	saveHCSR04(gp1, gp2, inp1)
	writeToLogfile("LOG: %s - Automatic recording of the sensor %s at the GPIO number %s, %s stopped." % (getTimestamp(), sensor, gp1, gp2) )
else:
	writeToLogfile("ERR: %s - Automatic recording without sensor!" % getTimestamp()  )
