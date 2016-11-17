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

# Sensor
sensor = "DHT22"
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
# Installationsscript des Sensors starten
def install():
	errorlevel = 9
	try:
		errorlevel = subprocess.call("install/dht22.sh")
	except:
		writeToLogfile("ERR: %s - Error during installation of the sensor: %s" % (getTimestamp(),sensor) )
		showerror("Fehler", "Fehler bei der Installation!")
	if (errorlevel == 0):
		writeToLogfile("LOG: %s - The installation of the sensor %s was successful!" % (getTimestamp(),sensor) )
		showinfo("Installation erfolgreich", "Die Installation war erfolgreich!")
	if (errorlevel == 1):
		writeToLogfile("ERR: %s - To install the sensor %s root privileges are required!" % (getTimestamp(),sensor) )
		showerror("Fehlende Rechte", "Zum Installieren werden root-Rechte benoetigt!")
	checkButtons()
# Messwerte abfragen
def test():
	gp1 = textbox_gpio1.get("1.0", "end-1c")
	if (testGPIO(gp1) ):
		from sensor import DHT22
		sensor_dht22 = DHT22(gp1)
		writeToLogfile("LOG: %s - Test measurement of the sensor %s to GPIO number %s: %s" % (getTimestamp(), sensor, gp1, sensor_dht22) )
		showinfo('Test-Messung', sensor_dht22)
# Pruefen, ob die GPIO-Nummer stimmt
def testGPIO(gp1):
	try:
		gp1 = int(gp1)
		if (gp1 >= 0 and gp1 <= 40):
			return 1
		else:
			writeToLogfile("ERR: %s - The GPIO number must be between 0 and 40!" % getTimestamp() )
			showerror("Keine GPIO-Nummer", "Die GPIO-Nummer muss zwischen 0 und 40 liegen!")
	except ValueError:
		writeToLogfile("ERR: %s - Entering the GPIO number may only contain numbers!" % getTimestamp() )
		showerror("Keine Zahl", "Die Eingabe der GPIO-Nummer darf nur Zahlen enthalten!")
	return 0
# Pruefen, ob das Intervall zur Speicherung eine gueltige Zahl ist
def testIntervall(inp1):
	try:
		inp1 = int(inp1)
		if (inp1 >= 1 and inp1 <= 86400):
			return 1
		else:
			writeToLogfile("ERR: %s - The interval must be 1-86400!" % getTimestamp() )
			showerror("Ausserhalb des Intervalls", "Der Intervall muss zwischen 1 und 86400 liegen!")
	except ValueError:
		writeToLogfile("ERR: %s - Entering the interval must contain only numbers!" % getTimestamp() )
		showerror("Keine Zahl", "Die Eingabe des Intervall darf nur Zahlen enthalten!")
	return 0
# In Datenbank schreiben
def save():
	global startSave
	if (startSave == False):
		# Textbox einlesen und pruefen
		gp1 = textbox_gpio1.get("1.0", "end-1c")
		if (testGPIO(gp1) ):
			inp1 = textbox_inp1.get("1.0", "end-1c")
			if (testIntervall(inp1) ):
				startSave = True
				selectAufzeichnung.set("Aufzeichnung stoppen")
				writeToLogfile("LOG: %s - Recording the sensor %s at the GPIO number %s started." % (getTimestamp(), sensor, gp1) )
				start_new_thread(saveIntervall, (gp1, inp1) )
	else:
		startSave = False
		selectAufzeichnung.set("Aufzeichnung starten")
# Eigener Thread zur Aufzeichnung
def saveIntervall(gp1, inp1):
	# Sensor initialisieren
	from sensor import DHT22
	sensor_dht22 = DHT22(gp1)
	# Datenbank und Bibliotheken einbinden
	import sqlite3
        import time
	# Verbindung aufbauen
	connection = sqlite3.connect("data/database.db")
	cursor = connection.cursor()		
	# Einmalig die Tabelle erstellen
	sql_command = """
	CREATE TABLE IF NOT EXISTS dht22 (
		timestamp TIMESTAMP PRIMARY KEY,
		temperature FLOAT,
		humidity FLOAT

	) ;"""
	cursor.execute(sql_command)
	global startSave
	while(startSave):
		# Sensor auslesen
		humidity, temperature = sensor_dht22.read()
		timestamp = getTimestamp()
		# Oben in der Textbox anzeigen
		textboxL.configure(state="normal")
		textboxL.insert("1.0", "%s,%5.3f,%5.3f\n" % (timestamp, temperature, 	humidity))
		textboxL.configure(state="disabled")
		# Werte speichern
		cursor.execute("INSERT INTO dht22 (timestamp, temperature, humidity) VALUES (?,?,?)", (timestamp, temperature, humidity))
		connection.commit()
		# Warten wie im Intervall angegeben
		inp1 = int(inp1)
		for i in range(inp1):
			time.sleep(1)
			if (startSave == False):
				break

	writeToLogfile("LOG: %s - Recording the sensor %s at the GPIO number %s stopped." % (getTimestamp(), sensor, gp1) )
	connection.close()

# Zeitgesteuert als cronjob in die Datenbank schreiben
def autosave():
	global sensor
	gp1 = textbox_gpio1.get("1.0", "end-1c")
	if (testGPIO(gp1) ):
		inp1 = textbox_inp1.get("1.0", "end-1c")
		if (testIntervall(inp1) ):
			try:
				writeToLogfile("LOG: %s - Open window for %s with 	automatic recording: auto.py" % (getTimestamp(),sensor) )
				# Neues Fenster starten
				subprocess.call(["./scripts/auto.py",sensor,inp1,gp1])
				writeToLogfile("LOG: %s - Close window: auto.py" % getTimestamp() )
			except:
				writeToLogfile("ERR: %s - Failed to start the window: auto.py" % getTimestamp() )
				showerror("Fenster nicht gefunden", "Fehler beim Starten des Fensters: auto.py")

# Daten als CSV bereitstellen
def csv():
	# Datenbank
	import sqlite3
	# Verbindung aufbauen
	connection = sqlite3.connect("data/database.db")
	cursor = connection.cursor()
	try:
		cursor.execute("SELECT * FROM dht22")
		csvdata = "data/dht22.csv"
		# Datei neu erstellen
		f = open(csvdata, "w")
		f.close()
		# Datensaetze anhaengen
		f = open(csvdata, "a")
		f.write("timestamp,temperature,humidity\n")
		for row in cursor:
			f.write(str(row[0])+","+str(row[1])+","+str(row[2])+"\n")
		f.close()
		connection.close()
		writeToLogfile("LOG: %s - Data successfully exported in the directory: %s" % (getTimestamp(),csvdata) )
		showinfo("Exportieren erfolgreich", "Die Werte wurden erfolgreich exportiert und befinden sich im Verzeichnis: "+csvdata)
	except:
		writeToLogfile("ERR: %s - No data available for export!" % getTimestamp() )
		showerror("Exportieren fehlgeschlagen", "Keine Daten zum exportieren vorhanden!")
# Pruefen, ob schon Installiert wurde (Buttons blockieren oder normal setzen)
def checkButtons():
	if (os.path.isdir("downloads/Adafruit_Python_DHT/build/")):
		textbox_gpio1.configure(state="normal")
		textbox_inp1.configure(state="normal")
		button_install.configure(state="disabled")
		button_test.configure(state="normal")
		button_db.configure(state="normal")
		button_autodb.configure(state="normal")
		button_csv.configure(state="normal")
	else:
		textbox_gpio1.configure(state="disabled")
		textbox_inp1.configure(state="disabled")
		button_install.configure(state="normal")
		button_test.configure(state="disabled")
		button_db.configure(state="disabled")
		button_autodb.configure(state="disabled")
		button_csv.configure(state="disabled")

### MAIN ###
# Fenster erzeugen
main = Tk()
main.title(sensor+" Sensor konfigurieren")
main.configure(height=400,width=600)

# Ersten Eintrag nutzen (Standardwerte bestimmen)
selectAufzeichnung = StringVar()
selectAufzeichnung.set("Aufzeichnung starten")
# Variable die den Thread Aufzeichnung regelt (True = aktiv / False = inaktiv)
startSave = False

# Eingabe anzeigen
frame_input = Frame(main)
frame_input.pack(padx=5, pady=15, side=LEFT)
label = Label(frame_input, text="Eingaben:")
label.pack(pady=15, side=TOP)
label = Label(frame_input, text="GPIO-Nummer:")
label.pack(pady=10, side=TOP)
textbox_gpio1 = Text(frame_input, height=1, width=10)
textbox_gpio1.pack(pady=10, side=TOP)
textbox_gpio1.insert(END, "17")
label = Label(frame_input, text="Intervall in Sekunden:")
label.pack(side=TOP)
textbox_inp1 = Text(frame_input, height=1, width=10)
textbox_inp1.pack(pady=15, side=TOP)
textbox_inp1.insert(END, "5")
label = Label(frame_input, text="Messliste:")
label.pack(side=TOP)
textboxL = Text(frame_input, height=15, width=40)
textboxL.pack(pady=10, side=TOP)
textboxL.configure(state="disabled")

# Buttons anzeigen
frame_button = Frame(main)
frame_button.pack(padx=5, pady=20, side=LEFT)
label = Label(frame_button, text="Aktion:")
label.pack(side=TOP)
button_install = Button(frame_button,text="Sensor installieren",command=install)
button_install.pack(pady=20, side=TOP)
button_test = Button(frame_button,text="Sensor testen",command=test)
button_test.pack(pady=20, side=TOP)
button_db = Button(frame_button,textvariable=selectAufzeichnung,command=save)
button_db.pack(pady=20, side=TOP)
button_autodb = Button(frame_button,text="Zeitgesteuerte Aufzeichnung",command=autosave)
button_autodb.pack(pady=20, side=TOP)
button_csv = Button(frame_button,text="Export als CSV-Datei",command=csv)
button_csv.pack(pady=20, side=TOP)
button_del = Button(frame_button,text="Beenden",command=main.destroy)
button_del.pack(pady=20, side=TOP)

# Aufbau mit GPIO-Schnittstelle anzeigen
frame_photo = Frame(main)
frame_photo.pack(padx=5, pady=20, side=LEFT)
label = Label(frame_photo, text="Aufbau mit der GPIO-Schnittstelle:")
label.pack(side=TOP)

try:
	photo = PhotoImage(file="./gui/"+sensor+".png")
	label_photo = Label(frame_photo, image=photo)
	label_photo.photo = photo
	label_photo.pack(side=TOP)
except:
	pass

# Pruefen, ob schon Installiert wurde
checkButtons()

# Loop
main.mainloop()
