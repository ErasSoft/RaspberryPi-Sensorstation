#!/bin/bash
# Hochschule Neubrandenburg
# VMGG33 - Informatik-Projekt
# Verfasser: Tino Schuldt
# Datum: 16.12.2015


# In Benutzer-Crontab schreiben
(
# Parameter: 1.Minute (0-59) - 2.Stunde (0-23) - 3.Tag (1-31) - 4.Monat (1-12) - 5.Wochentag (0-7, Sonntag ist 0 oder 7) - 6. Sensor - 7. Dauer in Min. - 8. Intervall - 9. GPIO1 - 10. GPIO2

date +"LOG: %Y-%m-%d %H:%M:%S - Write crontab file to config/crontab.txt"
crontab -l > ./config/crontab.txt
date +"LOG: %Y-%m-%d %H:%M:%S - Add new job in the crontab file to config/crontab.txt"
if [ "$#" -eq 8 ]; then
	echo "$1 $2 $3 $4 $5 "`pwd`"/scripts/cronjob.py $6 $7 $8" >> ./config/crontab.txt
elif [ "$#" -eq 9 ]; then
	echo "$1 $2 $3 $4 $5 "`pwd`"/scripts/cronjob.py $6 $7 $8 $9" >> ./config/crontab.txt
elif [ "$#" -eq 10 ]; then
	echo "$1 $2 $3 $4 $5 "`pwd`"/scripts/cronjob.py $6 $7 $8 $9 ${10}" >> ./config/crontab.txt
fi
date +"LOG: %Y-%m-%d %H:%M:%S - Write from /config/crontab.txt in crontab"
crontab < ./config/crontab.txt

) 2>&1 | tee -a "logfiles/crontab.log" # logfile erstellen
