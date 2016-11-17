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
while read line; do
	if [[ $line = "dtoverlay=w1-gpio-pullup" ]] ; then
		installation=true
	fi
done < /boot/config.txt

if [ $installation ] ; then
	date +"LOG: %Y-%m-%d %H:%M:%S - Already installed Sensor DS18B20"
	exit 2
else
	date +"LOG: %Y-%m-%d %H:%M:%S - Install Sensor DS18B20"
	echo "dtoverlay=w1-gpio-pullup" >> /boot/config.txt
fi

) 2>&1 | tee -a "logfiles/install_ds18b20.log" # logfile erstellen
