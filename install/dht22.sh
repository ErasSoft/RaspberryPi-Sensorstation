#!/bin/bash
# Hochschule Neubrandenburg
# VMGG33 - Informatik-Projekt
# Verfasser: Tino Schuldt
# Datum: 16.12.2015


# Skript als root starten!
if [ $(id -u) -ne 0 ]; then
  echo "ERR: This script must be run as root."
  exit 1
fi

# Installations Routine
(
if [ -d "downloads/Adafruit_Python_DHT/build" ]; then
	date +"LOG: %Y-%m-%d %H:%M:%S - Already installed Sensor DHT22"
	exit 2
else
	date +"LOG: %Y-%m-%d %H:%M:%S - Install Packages <build-essential> <python-dev> <pythin-openssl>"
	apt-get -y install build-essential python-dev python-openssl
	date +"LOG: %Y-%m-%d %H:%M:%S - Install Sensor DHT22"
	cd downloads/Adafruit_Python_DHT/
	python setup.py install
fi

) 2>&1 | tee -a "logfiles/install_dht22.log" # logfile erstellen
