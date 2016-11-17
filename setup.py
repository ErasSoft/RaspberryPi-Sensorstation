#!/usr/bin/python
# Hochschule Neubrandenburg
# VMGG33 - Informatik-Projekt
# Verfasser: Tino Schuldt
# Datum: 16.12.2015


# Bibliotheken einbinden
try:
	# for Python2
	from Tkinter import *
except ImportError:
	# for Python3
	from tkinter import *
from tkMessageBox import *
from time import *
from thread import start_new_thread
import os.path
import subprocess

# Pfad zum Logfile
logfile = "logfiles/sensorstation.txt"


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
	f = open(logfile, "a")
	f.write(message+"\n")
	f.close()
# Die Config-Datei auslesen
def readSensorsFile():
	f = open("config/sensors.txt", "r")
	sensorList = f.read()
	f.close()
	return sensorList.strip().split('\n')
# Aus einer Liste den ersten Wert zurueckgeben
def readAvailableSensors(sensorList):
	newSensorList = []
	for t in sensorList:
		pos = t.find(',')
		newSensorList.append(t[:pos])
	return newSensorList
# Aus einer Liste die anderen Werte zurueckgeben
def readAvailableSensorsMeta(sensorList):
	newSensorList = []
	for t in sensorList:
		pos = t.find(',')
		newSensorList.append(t[pos+1:])
	return newSensorList
# Optionbox Eintrag auswaehlen
def select(value):
	global selectSensor
	selectSensor = value
	
	# Index Nummer herrausfinden und dem Array zuordnen
	global items
	i = 0
	k = 0
	for t in items:
		if (value == t):
			k=i
		i=i+1
	global meta
	selectSensorMeta.set(meta[k])
# Config Button gedrueckt
def config(sensor):
	global selectButton
	# Aktion im Logfile protokollieren
	writeToLogfile("LOG: %s - Configure the sensor: %s" % (getTimestamp(),sensor))
	# Das Fenster mit dem Sensor starten in einem eigenen Thread
	start_new_thread(newWindow, (sensor,) )
# Eigener Thread zum Starten der neuen Fenster
def newWindow(sensor):
	try:
		# Neues Fenster starten
		#subprocess.call("python ./"+sensor+".py", shell=True)
		subprocess.call("./scripts/"+sensor+".py")
		writeToLogfile("LOG: %s - Close window: %s.py" % (getTimestamp(),sensor) )
	except:
		writeToLogfile("ERR: %s - Failed to start the window: %s.py" % (getTimestamp(),sensor) )
		showerror("Fenster nicht gefunden", "Fehler beim Starten des Fensters: "+sensor+".py")


### MAIN ###
# Fenster erzeugen
main = Tk()
main.title("Konfiguration der Sensorstation")
main.configure(height=400,width=600)

# Datei config/sensors.txt einlesen
sensorList = readSensorsFile()
items = readAvailableSensors(sensorList)
meta = readAvailableSensorsMeta(sensorList)

# Ersten Eintrag nutzen (Standardwerte bestimmen)
fruit = StringVar()
fruit.set(items[0])
selectSensor = items[0]
selectSensorMeta = StringVar()
selectButton = StringVar()
selectSensorMeta.set(meta[0])

# Elemente anzeigen
frame_sensor = Frame(main)
frame_sensor.pack(padx=15, pady=20, side=LEFT)
label = Label(frame_sensor, text="Nutze Sensor:")
label.pack(side=TOP)
menu_sensor = OptionMenu(frame_sensor, fruit, *items, command=select)
menu_sensor.pack(side=LEFT)

frame_description = Frame(main)
frame_description.pack(padx=15, pady=20, side=LEFT)
label = Label(frame_description, text="Messart:")
label.pack(side=TOP)
labelText = Label(frame_description, textvariable=selectSensorMeta)
labelText.pack(pady=5, side=LEFT)

frame_button = Frame(main)
frame_button.pack(padx=15, pady=20, side=LEFT)
label = Label(frame_button, text="Aktion:")
label.pack(side=TOP)
button_conf = Button(frame_button,text="Konfigurieren",command=lambda: config(selectSensor))
button_conf.pack(side=LEFT)

# Loop
main.mainloop()
