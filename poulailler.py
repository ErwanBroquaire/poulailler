#!/usr/bin/python3.4


# sudo pip3 install suntime

import datetime
from suntime import Sun, SunTimeException
from time import sleep
from datetime import datetime, timedelta
import pytz
import logging

# import du module de gestion des entrees sorties
import RPi.GPIO as GPIO
# import de la gestion du temps
import time


# On importe les parametres 
from parameters import *



# On identifie les pins par rapport a leur emplacement physique
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

#On utilise les pins 18 et 22 pour piloter le moteur
GPIO.setup(pin1, GPIO.OUT)                   # broche 18 est une sortie numerique
GPIO.setup(pin2, GPIO.OUT)                   # broche 22 est une sortie numerique






# Pour faire des tests, il vaut mieux ecraser les logs a chaque test, on mettra "w". En prod on mettra "a"
logging.basicConfig(filename="log_poulailler.log", filemode="a", format='%(asctime)s_%(levelname)s_%(message)s', encoding='utf-8', level=log_level)
logging.debug("debug")
logging.info("info")
logging.warning("arning")
logging.error("error")

logging.info("""
      ,~.
   ,-'__ `-,
  {,-'  `. }              ,')
 ,( a )   `-.__         ,',')~,
<=.) (         `-.__,==' ' ' '}
  (   )                      /)
   `-'\   ,                    )
       |  \        `~.        /
       \   `._        \      /
        \     `._____,'    ,'
         `-.             ,'
            `-._     _,-'
                77jj'
               //_||
            __//--'/`          
          ,--'/`  '

""")


logging.info("Lancement du script de gestion de la porte du Poulallier")
logging.info("========================================================")
# On 
# longitude et latitude sont presents dans le fichier parameters.py
logging.info("le poulailler se situe ici (lat:{}, long:{})".format(latitude, longitude))

sun = Sun(latitude, longitude)





def monter():
	logging.info("On monte()")
	logging.debug("on verifie que la position n'est pas aberante")
	with open("position.txt","r") as mon_fichier :
		if mon_fichier.readlines()[0]!="bas":
			raise Exception("On me demande de monter alors que je ne suis pas en bas !")
		else:
			logging.debug("position ok")
		mon_fichier.close()

	with open("position.txt","w") as mon_fichier :
		logging.info("on indique dans le fichier que la porte est en train de monter")
		mon_fichier.write("monte")

	# On fait tourner le moteur dans un sens
	GPIO.setup(pin1, GPIO.OUT, initial=GPIO.HIGH)# broche 18 est a l'etat haut
	GPIO.setup(pin2, GPIO.OUT, initial=GPIO.LOW)# broche 22 est a l'etat bas

	time.sleep(16.6)
	#time.sleep(0.53)

	# On arrete le moteur
	GPIO.setup(pin1, GPIO.OUT, initial=GPIO.LOW)# broche 18 est a l'etat bas
	GPIO.setup(pin2, GPIO.OUT, initial=GPIO.LOW)# broche 22 est a l'etat bas


	with open("position.txt","w") as mon_fichier :
		logging.info("on indique dans le fichier que la porte est en haut")
		mon_fichier.write("haut")
	return
	

def descendre():
	logging.info("On descend()")
	logging.debug("on verifie que la position n'est pas aberante")
	with open("position.txt","r") as mon_fichier :
		if mon_fichier.readlines()[0]!="haut":
			raise Exception("On me demande de descendre alors que je ne suis pas en haut !")
		else:
			logging.debug("position ok")
		mon_fichier.close()

	with open("position.txt","w") as mon_fichier :
		logging.info("on indique dans le fichier que la porte est en train de descendre")
		mon_fichier.write("descend")


	# On fait tourner le moteur dans un sens
	GPIO.setup(pin1, GPIO.OUT, initial=GPIO.LOW)# broche 18 est a l'etat bas
	GPIO.setup(pin2, GPIO.OUT, initial=GPIO.HIGH)# broche 22 est a l'etat haut

	# On attend la duree qui va bien
	time.sleep(14.4)
	#time.sleep(0.25)

	# On arrete le moteur
	GPIO.setup(pin1, GPIO.OUT, initial=GPIO.LOW)# broche 18 est a l'etat bas
	GPIO.setup(pin2, GPIO.OUT, initial=GPIO.LOW)# broche 22 est a l'etat bas


	with open("position.txt","w") as mon_fichier :
		logging.info("on indique dans le fichier que la porte est en bas")
		mon_fichier.write("bas")
	return





	

############################################

#         MAIN

############################################

# Cette boucle est parcourue toute les minutes
# l'heure de leve/couche de soleil est recalculee
# si l'heure actuelle est comprise entre les deux la porte doit etre levee
# sinon elle doit etre baissee
logging.debug("boucle while principale")
while 1:

	# Get today's sunrise and sunset in UTC
	# Le time zone est importee dans parameters.py
	#today_sr = sun.get_sunrise_time().replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))
	#today_ss = sun.get_sunset_time().replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))
	today_sr = sun.get_sunrise_time().replace(tzinfo=pytz.timezone(timezone))
	today_ss = sun.get_sunset_time().replace(tzinfo=pytz.timezone(timezone))
	logging.debug("Aujourd'hui le soleil se leve a {} et se couche a {}".format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))

	# Les heures d'ouvertures sont trop restrictives
	# on elargie la plage horaire
	# l elargissement est importe de parameters.py
	logging.debug("On decale la plage horaire de {} heures et {} minutes le matin".format(elarg_heures_matin,elarg_minutes_matin))
	today_sr += timedelta(hours=elarg_heures_matin,minutes=elarg_minutes_matin)
	logging.debug("On decale la plage horaire de {} heures et {} minutes le matin".format(elarg_heures_soir,elarg_minutes_soir))
	today_ss += timedelta(hours=elarg_heures_soir,minutes=elarg_minutes_soir)

	# line de code de test pour modifier la plage horaire
	#today_ss += timedelta(hours=5,minutes=0)

	logging.info("On leve la porte a {} et on ferme a {}".format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))
	logging.debug(today_sr)
	logging.debug(today_ss)


	now = datetime.now().replace(tzinfo=pytz.timezone(timezone))
	current_time = now.strftime("%H:%M")
	logging.debug("Actuellement il est : {}".format(current_time))
	logging.debug(now)

	position = open("position.txt", "r").readlines()[0]
	logging.debug("on ouvre le fichier position.txt")
	logging.debug("la position lue est : {}".format(position))
	if position == "haut" :
		pass
	elif position == "bas" :
		pass
	else:
		logging.error("erreur de lecture du fichier, on ne sait pas si la porte est en haut ou en bas")
		raise Exception("Le fichier position.txt n'est pas conforme. Position de la porte inconnue.")
	# On a passe le test sans lever d'exception on peut afficher la position
	logging.info("La porte est actuellement en {}".format(position))

	if ((today_sr < now) and (now < today_ss)):
		logging.info("On est dans la plage horaire, la porte doit etre en haut")
		if position != "haut":
			logging.debug("la position lue dans le fichier n'est pas 'haut'")
			logging.info("on monte la porte")
			monter()
		else :
			logging.info("la porte est deja dans la bonne position")

	if ((now <= today_sr) or (today_ss <= now)):
		logging.info("On n'est pas dans la plage horaire, la porte doit etre en bas")
		if position != "bas":
			logging.debug("la position lue dans le fichier n'est pas 'bas'")
			logging.info("on descend la porte")
			descendre()
		else :
			logging.info("la porte est deja dans la bonne position")

	attente = 60.0
	logging.debug("On attend {} secondes.".format(attente))
	logging.info("======================================")
	sleep(attente)
#	break


