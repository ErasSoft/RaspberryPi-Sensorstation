# Hochschule Neubrandenburg
# VMGG33 - Informatik-Projekt
# Verfasser: Tino Schuldt
# Datum: 16.12.2015


class DHT22:
        def __init__(self, gpio_pin):
                self.gpio_pin = int(gpio_pin)
        def read(self):
                import Adafruit_DHT        
                sensor = Adafruit_DHT.DHT22
                humidity, temperature = Adafruit_DHT.read_retry(sensor, self.gpio_pin)
		return humidity, temperature         
	def __str__(self):
		humidity, temperature = self.read()
		return "Temperatur: %5.3f C Luftfeuchtigkeit: %5.3f %%" % (temperature, humidity)

class DS18B20:
        def __init__(self):
                try:
                        # Liste der Sensoren auslesen
                        file = open("/sys/devices/w1_bus_master1/w1_master_slaves")
                        # Datei einlesen
                        self.w1_slaves = file.readlines()
                        # File schliessen
                        file.close()
                except IOError:
                        print("Bad configuration!")
        def read(self):
                try:
                        # Liste der Sensoren auslesen
                        for line in self.w1_slaves:
                                # Auslsen aus Resultat
                                w1_slave = line.split("\n")[0]
                                # Sensor Datei oeffnen
                                file = open("/sys/bus/w1/devices/" + w1_slave + "/w1_slave")
                                # Inhalt des File auslesen
                                t_raw = file.read()
                                # File schliessen
                                file.close()

                                # Temperatur und Datei auslesen
                                stringvalue = t_raw.split("\n")[1].split(" ")[9]
                                # Temperatur konvertieren
                                temperature = float(stringvalue[2:]) / 1000
                                # Temperatur ausgeben
                                return temperature
                except IOError:
                        print("No Sensor found!")
                        return 0
        def __str__(self):
                return "Temperatur: %5.3f C" % self.read()

class HCSR04:
        def __init__(self, gpio_trigger, gpio_echo):
                self.gpio_trigger = int(gpio_trigger)
                self.gpio_echo = int(gpio_echo)
        def __del__(self):
                import RPi.GPIO as GPIO
                GPIO.cleanup()                
        def read(self):
                import RPi.GPIO as GPIO
                import time
                GPIO.setmode(GPIO.BCM)
                # Richtung der GPIO-Pins festlegen (IN / OUT)
                GPIO.setup(self.gpio_trigger, GPIO.OUT)
                GPIO.setup(self.gpio_echo, GPIO.IN)
                # setze Trigger auf HIGH
                GPIO.output(self.gpio_trigger, True)
                # setze Trigger nach 0.01ms aus LOW
                time.sleep(0.00001)
                GPIO.output(self.gpio_trigger, False)
                StartZeit = time.time()
                StopZeit = time.time()
                # speichere Startzeit
                while GPIO.input(self.gpio_echo) == 0:
                        StartZeit = time.time()
                # speichere Ankunftszeit
                while GPIO.input(self.gpio_echo) == 1:
                        StopZeit = time.time()
                # Zeit Differenz zwischen Start und Ankunft
                TimeElapsed = StopZeit - StartZeit
                # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
                # und durch 2 teilen, da hin und zurueck
                distanz = (TimeElapsed * 34300) / 2
                return distanz
        def __str__(self):
                return "Entfernung: %5.3f cm" % self.read()

