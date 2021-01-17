#!/usr/bin/python3.4


# sudo pip3 install suntime

import datetime
from suntime import Sun, SunTimeException
from parameters import *
from time import sleep
from datetime import datetime, timedelta
import pytz

print("""
                  ,.
                 (\(\)
 ,_              ;  o >
  {`-.          /  (_)
  `={\`-._____/`   |
   `-{ /    -=`\   |
    `={  -= = _/   /
       `\  .-'   /`
        {`-,__.'===,_
        //`        `\\
       //
      `\=
""")


print("Script de gestion de la porte du Poulallier")
print("===========================================")
# On 
# longitude et latitude sont presents dans le fichier parameters.py
print("le poulailler se situe ici (lat:{}, long:{})".format(latitude, longitude))

sun = Sun(latitude, longitude)


def monter():
	print("On monte()")
	with open("position.txt","r") as mon_fichier :
		if mon_fichier.readlines()[0]!="bas":
			raise Exception("On me demande de descendre alors que je ne suis pas en bas !")
	with open("position.txt","w") as mon_fichier :
		mon_fichier.write("monte")
	sleep(1.0)
	with open("position.txt","w") as mon_fichier :
		mon_fichier.write("haut")
	return


def descendre():
	print("On descend()")
	print("on verifie que la position n'est pas aberante")
	with open("position.txt","r") as mon_fichier :
		if mon_fichier.readlines()[0]!="haut":
			raise Exception("On me demande de descendre alors que je ne suis pas en haut !")
		else:
			print("position ok")
		mon_fichier.close()

	with open("position.txt","w") as mon_fichier :
		print("on indique dans le fichier que la porte est en train de descendre")
		mon_fichier.write("descend")
	sleep(1.0)
	with open("position.txt","w") as mon_fichier :
		print("on indique dans le fichier que la porte est en bas")
		mon_fichier.write("bas")
	return
	








# Cette boucle est parcourue toute les minutes
# l'heure de leve/couche de soleil est recalculee
# si l'heure actuelle est comprise entre les deux la porte doit etre levee
# sinon elle doit etre baissee
while 1:

	# Get today's sunrise and sunset in UTC
	# Le time zone est importee dans parameters.py
	today_sr = sun.get_sunrise_time().replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))
	today_ss = sun.get_sunset_time().replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))
	print("Aujourd'hui le soleil se leve a {} et se couche a {}".format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))

	# Les heures d'ouvertures sont trop restrictives
	# on elargie la plage horaire
	# l elargissement est importe de parameters.py
	print("On elargie la plage horaire de {} heures et {} minutes".format(elarg_heures,elarg_minutes))
	today_sr -= timedelta(hours=elarg_heures,minutes=elarg_minutes)
	today_ss += timedelta(hours=elarg_heures,minutes=elarg_minutes)

	# line de code de test pour modifier la plage horaire
	#today_ss -= timedelta(hours=3,minutes=0)

	print("On leve la porte a {} et on ferme a {}".format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))
	# Attention ici dattime.now() suppose que l'heure du system est UTC alors que c'est deja Europe/Paris
	# La librairie suntime quant a elle ne s'occupe pas de l'heure system
	# Je corrige donc cette disymetrie en retirant une heure pour qu'il ne compte pas deux fois le decalage horaire du a la TZ !
	now = datetime.now().replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone)) - timedelta(hours=1)
	current_time = now.strftime("%H:%M")
	print("Actuellement il est : ", current_time)

	position = open("position.txt", "r").readlines()[0]
	if position == "haut" :
		pass
	elif position == "bas" :
		pass
	else:
		print("erreur de lecture du fichier, on ne sait pas si la porte est en haut ou en bas")
		raise Exception("Le fichier position.txt n'est pas conforme. Position de la porte inconnue.")
	# On a passe le test sans lever d'exception on peut afficher la position
	print("La porte est actuellement en {}".format(position))

	if ((today_sr < now) and (now < today_ss)):
		print("On est dans la plage horaire, la porte doit etre en haut")
		if position != "haut":
			monter()
			print("on monte la porte")
		else :
			print("la porte est deja dans la bonne position")
	if ((now <= today_sr) or (today_ss <= now)):
		print("On n'est pas dans la plage horaire, la porte doit etre en bas")
		if position != "bas":
			descendre()
			print("on descend la porte")
		else :
			print("la porte est deja dans la bonne position")



#	sleep(6.0)
	break


