#!/usr/bin/python
# Hochschule Neubrandenburg
# VMGG33 - Informatik-Projekt
# Verfasser: Tino Schuldt
# Datum: 07.01.2016

# Beschreibung:
# Startet den Webservice unter localhost:8080

import web
import os.path

# Klasse zum Aufrufen im Webservice bei neuen Sensoren muss diese bearbeitet werden!
def start(s):
	if(s == "ds18b20"):
		return ds18b20().GET()
	if(s == "dht22"):
		return dht22().GET()
	if(s == "hcsr04"):
		return hcsr04().GET()	

# URLs die mit dem Webbrowser erreicht werden koennen
urls = (
	'/',		'index',
	'/all',		'all',
	'/dht22',	'dht22',
	'/ds18b20',	'ds18b20',
	'/hcsr04',	'hcsr04'
)

# Main-Methode
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()



# Klassen mit GET-Methoden
# Parameter ?rows=2 zum Auslesen der letzten Eintraege
def rows():
	try:
		i = web.input().rows
		# Standardwert setzen bei ?rows
		if(not i):
			i = "1"
		return " ORDER BY timestamp DESC LIMIT "+i
	except:
		return ""
# Abfrage Modus mit Parametern ?pretty
def pretty(parks):
	import json
	try:
		t = web.input().pretty
		# Formatiertes JSON
		return json.dumps(parks, sort_keys=True, indent=2, separators=(',', ':')) 
	except:
		# Unformatiertes JSON
		return json.dumps(parks) 
# Startseite laden
class index:
	def GET(self):
		import sqlite3
		sensor = []
		connection = sqlite3.connect("data/database.db")
		cursor = connection.cursor()
		try:
			cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
			for row in cursor:
				sensor.append(row[0])
			connection.close()
			data = ""
			for s in sensor:
				data += '<a href="'+s+'?pretty">'+s+'</a><br>'
			# Wenn Daten veraendert wurden
			if (data != ""):
				data = '<html><head><title>Webservice der Sensorstation</title></head><body><h3>Sensor:</h3>'+data+'<br><a href="all?pretty">Alle Sensoren</a> - <a href="all?calc&pretty">Mittelwerte/Max/Min</a></body></html>'
				return data
			else:
				return "No data here!"
		except:
			connection.close()
			return "No data here!"
class dht22:
	def GET(self):
		import sqlite3
		connection = sqlite3.connect("data/database.db")
		cursor = connection.cursor()
		try:
			# Query String bauen
			s = "SELECT * FROM dht22"
			s += rows()
			cursor.execute(s)

			# Array nach folgender Struktur aufbauen (JSON-Format)
			parks = []
			try:
				# Parameter ?calc zum Berechnen der Mittelwerte, Max, Min
				a = web.input().calc
				temperature = 0
				humidity = 0
				i = 0
				z1 = ""
				z2 = ""
				for row in cursor:
					i = i + 1
					temperature += row[1]
					humidity += row[2]
					if(i==1):
						z1 = row[0]
						temperature_max = temperature
						temperature_min = temperature
						humidity_max = humidity
						humidity_min = humidity
					z2 = row[0]
					if(row[1] > temperature_max):
						temperature_max = row[1]
					if(row[1] < temperature_min):
						temperature_min = row[1]
					if(row[2] > humidity_max):
						humidity_max = row[2]
					if(row[2] < humidity_min):
						humidity_min = row[2]
				temperature = temperature / i
				humidity = humidity / i
				parks.append({
					'timestamp_start' : z1,
					'timestamp_stop' : z2,
					'values' : i,
					'temperature_average' : temperature,
					'temperature_max' : temperature_max,
					'temperature_min' : temperature_min,
					'humidity_average' : humidity,
					'humidity_max' : humidity_max,
					'humidity_min' : humidity_min
				})		
			except:
				for row in cursor:
					parks.append({
						'timestamp' : row[0],
						'temperature' : row[1],
						'humidity' : row[2]
					})
			connection.close()	
			json = pretty(parks)
			return json
		except:
			connection.close()
			return "No data here!"
class ds18b20:
	def GET(self):
		import json
		import sqlite3
		connection = sqlite3.connect("data/database.db")
		cursor = connection.cursor()
		try:
			# Query String bauen
			s = "SELECT * FROM ds18b20"
			s += rows()
			cursor.execute(s)

			# Array nach folgender Struktur aufbauen (JSON-Format)
			parks = []
			try:
				# Parameter ?calc zum Berechnen der Mittelwerte, Max, Min
				a = web.input().calc
				temperature = 0
				i = 0
				z1 = ""
				z2 = ""
				for row in cursor:
					i = i + 1
					temperature += row[1]
					if(i==1):
						z1 = row[0]
						temperature_max = temperature
						temperature_min = temperature
					z2 = row[0]
					if(row[1] > temperature_max):
						temperature_max = row[1]
					if(row[1] < temperature_min):
						temperature_min = row[1]
				temperature = temperature / i
				parks.append({
					'timestamp_start' : z1,
					'timestamp_stop' : z2,
					'values' : i,
					'temperature_average' : temperature,
					'temperature_max' : temperature_max,
					'temperature_min' : temperature_min
				})		
			except:
				for row in cursor:
					parks.append({
						'timestamp' : row[0],
						'temperature' : row[1]
					})

			connection.close()	
			json = pretty(parks)
			return json
		except:
			connection.close()
			return "No data here!"
class hcsr04:
	def GET(self):
		import json
		import sqlite3
		connection = sqlite3.connect("data/database.db")
		cursor = connection.cursor()
		try:
			# Query String bauen
			s = "SELECT * FROM hcsr04"
			s += rows()
			cursor.execute(s)

			# Array nach folgender Struktur aufbauen (JSON-Format)
			parks = []
			try:
				# Parameter ?calc zum Berechnen der Mittelwerte, Max, Min
				a = web.input().calc
				distance = 0
				i = 0
				z1 = ""
				z2 = ""
				for row in cursor:
					i = i + 1
					distance += row[1]
					if(i==1):
						z1 = row[0]
						distance_max = distance
						distance_min = distance
					z2 = row[0]
					if(row[1] > distance_max):
						distance_max = row[1]
					if(row[1] < distance_min):
						distance_min = row[1]
				distance = distance / i
				parks.append({
					'timestamp_start' : z1,
					'timestamp_stop' : z2,
					'values' : i,
					'distance_average' : distance,
					'distance_max' : distance_max,
					'distance_min' : distance_min
				})		
			except:
				for row in cursor:
					parks.append({
						'timestamp' : row[0],
						'distance' : row[1]
					})

			connection.close()	
			json = pretty(parks)
			return json
		except:
			connection.close()
			return "No data here!"
class all:
	def GET(self):
		import sqlite3
		sensor = []
		connection = sqlite3.connect("data/database.db")
		cursor = connection.cursor()
		try:
			cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
			for row in cursor:
				sensor.append(row[0])
		
			data = "{\n"
			for s in sensor:
				jsondata = start(s)
				if(jsondata != "No data here!"):
	 				# Komma nach dem veraendern immer ranhaengen
					if (data != "{\n"):
						data+=",\n"
					data += '"'+s+'": '+jsondata
			# Wenn Daten veraendert wurden
			if (data != "{\n"):
				data += "\n}"
				return data
			else:
				return "No data here!"
		except:
			connection.close()
			return "No data here!"

