#!/usr/bin/python3.4

print("lancement du moteur")

# import du module de gestion des entrees sorties
import RPi.GPIO as GPIO
# import de la gestion du temps
import time

# on identifie les pins par rapport a leur emplacement physique
# les pins 2 et 4 fournissent du 5V par exemple 
GPIO.setmode(GPIO.BOARD)

# On desactive les warnings
GPIO.setwarnings(False)

# on identifie les pins qui serviront au pilotage du moteur, 18 et 22 par exemple
# attention il y a deux numerotation ici les pins sont identifiees de 1 a 40
pin1=18
pin2=22


# On arrete le moteur
GPIO.setup(pin1, GPIO.OUT, initial=GPIO.LOW)# broche 18 est a l'etat bas
GPIO.setup(pin2, GPIO.OUT, initial=GPIO.LOW)# broche 22 est a l'etat bas

#On demande a l'utilisateur s'il est pret
#input('pret pour DESCENDRE?')

#On utilise les pins 18 et 22 pour piloter le moteur
GPIO.setup(pin1, GPIO.OUT)                   # broche 18 est une sortie numerique
GPIO.setup(pin2, GPIO.OUT)                   # broche 22 est une sortie numerique


# On fait tourner le moteur dans un sens
GPIO.setup(pin1, GPIO.OUT, initial=GPIO.LOW)# broche 18 est a l'etat bas
GPIO.setup(pin2, GPIO.OUT, initial=GPIO.HIGH)# broche 22 est a l'etat haut

# On attend la duree qui va bien
time.sleep(14.4)
#time.sleep(0.25)

# On arrete le moteur
GPIO.setup(pin1, GPIO.OUT, initial=GPIO.LOW)# broche 18 est a l'etat bas
GPIO.setup(pin2, GPIO.OUT, initial=GPIO.LOW)# broche 22 est a l'etat bas




exit()
