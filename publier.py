#!/usr/bin/python3
import sys

with open("/var/www/html/index.html","w") as fichier:
	fichier.write("ouverture a {}\n<BR>".format(sys.argv[1]))
	fichier.write("fermeture a {}".format(sys.argv[2]))

