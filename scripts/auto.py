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
import sys

# Pfad zum Logfile
logfile = "logfiles/sensorstation.txt"
# Paramter: 1.Sensor - 2.Intervall - 3.Gpio-Nummer1 - 4.Gpio-Nummer2
try:
	sensor = sys.argv[1]
except:
	sensor = "NULL"
try:
	inp1 = sys.argv[2]
except:
	inp1 = 10
try:
	gp1 = sys.argv[3]
except:
	gp1 = -1
try:
	gp2 = sys.argv[4]
except:
	gp2 = -1

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
# Crontab einlesen und anzeigen
def readTasks():
	try:
		crontab = subprocess.check_output(["crontab", "-l"])
		crontab = crontab.split("\n")
		textboxL.configure(state="normal")
		textboxL.delete("1.0", "end-1c")
		i=0
		for t in crontab:
			if (t != ""):
				i=i+1
				textboxL.insert("end", "Job "+str(i)+": "+readTaskLine(t)+"\n" )
		textboxL.configure(state="disabled")
	except:
		pass
# Crontab Format einlesen und darstellen in der Liste
def readTaskLine(line):
	t = line.split(" ")
	l = len(t)
	# Wochentag einem Namen vergeben
	items_week = ["So.","Mo.","Di.","Mi.","Do.","Fr.","Sa.","So."]
	if (t[4] != "*"):
		t[4] = items_week[int(t[4])]
	# Laenge des Eintrags pruefen
	if (l == 9):
		s = "\tMonat: %s, Wochentag: %s, Tag: %s, Stunde: %s, Minute: %s,\n\tSensor: %s, Laufzeit[Min]: %s, Intervall[Sek]: %s" %(t[3],t[4],t[2],t[1],t[0],t[6],t[7],t[8])
	elif (l == 10):
		s = "\tMonat: %s, Wochentag: %s, Tag: %s, Stunde: %s, Minute: %s,\n\tSensor: %s, Laufzeit[Min]: %s, Intervall[Sek]: %s,\n\tGPIO1: %s"  %(t[3],t[4],t[2],t[1],t[0],t[6],t[7],t[8],t[9])
	elif (l == 11):
		s = "\tMonat: %s, Wochentag: %s, Tag: %s, Stunde: %s, Minute: %s,\n\tSensor: %s, Laufzeit[Min]: %s, Intervall[Sek]: %s,\n\tGPIO1: %s, GPIO2: %s"  %(t[3],t[4],t[2],t[1],t[0],t[6],t[7],t[8],t[9],t[10])
	return s

# In die Crontab schreiben
def newTask():
	global minute_i, hour_i, day_i, month_i, week_i, sensor, inp1, gp1, gp2
	# Textbox einlesen und pruefen
	end1 = textbox_end.get("1.0", "end-1c")
	if (testEnd(end1) ):
		# Shellscript starten zum Eintragen in die Crontab
		l = 9
		if (gp2 != -1):
			l = l + 1
		if (gp1 != -1):
			l = l + 1
		if (l == 9):
			writeToLogfile("LOG: %s - Create new cronjob with sensor %s." % (getTimestamp(), sensor) )
			subprocess.call(["./scripts/write_crontab.sh",str(minute_i),str(hour_i),str(day_i),str(month_i),str(week_i),sensor,end1,inp1])
		elif (l == 10):
			writeToLogfile("LOG: %s - Create new cronjob with sensor %s at the GPIO number %s." % (getTimestamp(), sensor, gp1) )
			subprocess.call(["./scripts/write_crontab.sh",str(minute_i),str(hour_i),str(day_i),str(month_i),str(week_i),sensor,end1,inp1,gp1])
		elif (l == 11):
			writeToLogfile("LOG: %s - Create new cronjob with sensor %s at the GPIO number %s, %s." % (getTimestamp(), sensor, gp1, gp2) )
			subprocess.call(["./scripts/write_crontab.sh",str(minute_i),str(hour_i),str(day_i),str(month_i),str(week_i),sensor,end1,inp1,gp1,gp2])

		readTasks()

# In die Crontab schreiben
def deleteAllTasks():
	writeToLogfile("LOG: %s - Delete all cronjobs." % getTimestamp() )
	subprocess.call("./scripts/delete_crontab.sh")
	readTasks()
# Pruefen, ob die Laufzeit eine gueltige Zahl ist
def testEnd(end1):
	try:
		end1 = int(end1)
		if (end1 >= 1 and end1 <= 86400):
			return 1
		else:
			writeToLogfile("ERR: %s - The runtime must be 1-86400!" % getTimestamp() )
			showerror("Ausserhalb der Laufzeit", "Die Laufzeit muss zwischen 1 und 86400 liegen!")
	except ValueError:
		writeToLogfile("ERR: %s - Entering the runtime must contain only numbers!" % getTimestamp() )
		showerror("Keine Zahl", "Die Eingabe der Laufzeit darf nur Zahlen enthalten!")
	return 0
# Optionbox Eintrag auswaehlen
def selectMonth(value):
	global month, items_month, month_i
	month = value
	# Index Nummer herrausfinden und dem Array zuordnen
	i = 0
	k = 0
	for t in items_month:
		if (value == t):
			k=i
		i=i+1
	# Auswahl auf Variable speichern
	if (k == 0):
		month_i = '*'
	else:
		month_i = k
def selectWeek(value):
	global week, items_week, week_i
	week = value
	i = 0
	k = 0
	for t in items_week:
		if (value == t):
			k=i
		i=i+1
	if (k == 0):
		week_i = '*'
	else:
		week_i = k
def selectDay(value):
	global day, items_day, day_i
	day = value
	i = 0
	k = 0
	for t in items_day:
		if (value == t):
			k=i
		i=i+1
	if (k == 0):
		day_i = '*'
	else:
		day_i = k
def selectHour(value):
	global hour, items_hour, hour_i
	hour = value
	i = 0
	k = 0
	for t in items_hour:
		if (value == t):
			k=i
		i=i+1
	if (k == 0):
		hour_i = '*'
	else:
		hour_i = k-1
def selectMinute(value):
	global minute, items_minute, minute_i
	minute = value
	i = 0
	k = 0
	for t in items_minute:
		if (value == t):
			k=i
		i=i+1 
	if (k == 0):
		minute_i = '*'
	else:
		minute_i = (k-1)*5


### MAIN ###
# Fenster erzeugen
main = Tk()
main.title("Zeitgesteuerte Aufzeichnung mit dem Sensor "+sensor)
main.configure(height=400,width=600)

# Ersten Eintrag nutzen (Standardwerte bestimmen)
month = StringVar()
week = StringVar()
day = StringVar()
hour = StringVar()
minute = StringVar()
items_month = ["Jeden Monat","Januar","Februar","Maerz","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"]
items_week = ["Jeden Wochentag","Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]
items_day = ["Jeden Tag","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
items_hour = ["Jede Stunde","00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
items_minute = ["Jede Minute","00","05","10","15","20","25","30","35","40","45","50","55"]
month.set(items_month[0])
week.set(items_week[0])
day.set(items_day[0])
hour.set(items_hour[0])
minute.set(items_minute[0])
month_i = '*'
week_i = '*'
day_i = '*'
hour_i = '*'
minute_i = '*'

# Optionbox anzeigen
frame_start = Frame(main)
frame_start.pack(padx=15, pady=20, side=TOP)
label = Label(frame_start, text="Startzeit:")
label.pack(side=TOP)
frame_month = Frame(frame_start)
frame_month.pack(side=LEFT)
label = Label(frame_month, text="Monat:")
label.pack(side=TOP)
menu_month = OptionMenu(frame_month, month, *items_month, command=selectMonth)
menu_month.pack(padx=5, side=LEFT)
frame_week = Frame(frame_start)
frame_week.pack(side=LEFT)
label = Label(frame_week, text="Wochentag:")
label.pack(side=TOP)
menu_week = OptionMenu(frame_week, week, *items_week, command=selectWeek)
menu_week.pack(padx=5, side=LEFT)
frame_day = Frame(frame_start)
frame_day.pack(side=LEFT)
label = Label(frame_day, text="Tag:")
label.pack(side=TOP)
menu_day = OptionMenu(frame_day, day, *items_day, command=selectDay)
menu_day.pack(padx=5, side=LEFT)
frame_hour = Frame(frame_start)
frame_hour.pack(side=LEFT)
label = Label(frame_hour, text="Stunde:")
label.pack(side=TOP)
menu_hour = OptionMenu(frame_hour, hour, *items_hour, command=selectHour)
menu_hour.pack(padx=5, side=LEFT)
frame_minute = Frame(frame_start)
frame_minute.pack(side=LEFT)
label = Label(frame_minute, text="Minute:")
label.pack(side=TOP)
menu_minute = OptionMenu(frame_minute, minute, *items_minute, command=selectMinute)
menu_minute.pack(padx=5, side=LEFT)

# Eingabe anzeigen
frame_end = Frame(main)
frame_end.pack(side=TOP)
label = Label(frame_end, text="Laufzeit in Minuten:")
label.pack(side=TOP)
textbox_end = Text(frame_end, height=1, width=10)
textbox_end.pack(side=TOP)
textbox_end.insert(END, "5")

# Buttons anzeigen
frame_button = Frame(main)
frame_button.pack(padx=5, pady=20, side=RIGHT)
label = Label(frame_button, text="Aktion:")
label.pack(side=TOP)
button_new = Button(frame_button,text="Neuen Job",command=newTask)
button_new.pack(pady=20, side=TOP)
button_del = Button(frame_button,text="Alle Jobs entfernen",command=deleteAllTasks)
button_del.pack(pady=20, side=TOP)
button_exit = Button(frame_button,text="Fenster schliessen",command=main.destroy)
button_exit.pack(pady=20, side=TOP)

# Job Liste anzeigen
frame_list = Frame(main)
frame_list.pack(padx=5, pady=5, side=BOTTOM)
label = Label(frame_list, text="Alle aktiven Jobs:")
label.pack(side=TOP)
textboxL = Text(frame_list, height=15, width=75)
textboxL.pack(side=BOTTOM)
readTasks()

# Loop
main.mainloop()
