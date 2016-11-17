#!/usr/bin/python
# Hochschule Neubrandenburg
# VMGG33 - Informatik-Projekt
# Verfasser: Tino Schuldt
# Datum: 16.12.2015


# Bibliotheken einbinden
from time import *
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
# Install Webservice
def install():
	return subprocess.call("./install/webservice.sh")

# Start Webservice
def start():
	import sys
	#import urllib2
	#myip = urllib2.urlopen("http://myip.dnsdynamic.org/").read()
	myip = "localhost"
	try:
		port = sys.argv[1]
	except:
		port = 8080
	writeToLogfile("LOG: %s - Start Webservice on http://%s:%s" % (getTimestamp(), myip, port) )
	subprocess.call(["python", "./scripts/webservice.py", str(port)])
	writeToLogfile("LOG: %s - Stop Webservice" % getTimestamp()  )


### MAIN ###
if (install() == 0):
	start()



















