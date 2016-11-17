#!/bin/bash
# Hochschule Neubrandenburg
# VMGG33 - Informatik-Projekt
# Verfasser: Tino Schuldt
# Datum: 16.12.2015


# Installations Routine
if [ `dpkg --get-selections | grep -c python-webpy` -eq 1 ]; then
	exit 0
else
	# Skript als root starten!
	if [ $(id -u) -ne 0 ]; then
	  echo "ERR: This script webservice.sh must be run as root!"
	  exit 1
	fi

	(
	  date +"LOG: %Y-%m-%d %H:%M:%S - Install Package <python-webpy>"
	  apt-get -y install python-webpy
	  date +"LOG: %Y-%m-%d %H:%M:%S - Run on failure: apt-get update"
	) 2>&1 | tee -a "logfiles/install_webservice.log" # logfile erstellen
fi
