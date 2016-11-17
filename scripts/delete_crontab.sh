#!/bin/bash
# Hochschule Neubrandenburg
# VMGG33 - Informatik-Projekt
# Verfasser: Tino Schuldt
# Datum: 16.12.2015


# In Benutzer-Crontab schreiben
(
date +"LOG: %Y-%m-%d %H:%M:%S - Write empty file to config/crontab.txt"
echo -n > ./config/crontab.txt
date +"LOG: %Y-%m-%d %H:%M:%S - Write from /config/crontab.txt in crontab"
crontab < ./config/crontab.txt

) 2>&1 | tee -a "logfiles/crontab.log" # logfile erstellen
