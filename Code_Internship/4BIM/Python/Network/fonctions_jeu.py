# -*- coding: utf-8 -*-

##############################################################
#																									    #
# 						FONCTIONS D'INTERACTION AVEC LE JEU								    #
#																									    #
##############################################################	

# Librairies :
import select
import socket
import sys
import threading
import time
import random


##############################################################
def gestion_tribus(Partie, tribu, joueur, j ) :
	
	"""Gestion des actions associées à l'activation d'une carte tribue"""
				
	#( type, coût, pv, power, num)
	
	if Partie.jeu.verification_ressources(tribu[1], joueur)  :
	
		if joueur["cartes_tableau"] < 12 :
		
			Partie.send_dif(j,'Souhaitez-vous acheter la carte tribue "%s" sous votre marqueur (%s) pour %i pv  ? (*oui*/*non*) : ' % (tribu[0], tribu[1], tribu[2]),"%s doit choisir quoi faire de sa carte tribu"% Partie.t[j].pseudo)
			achat = Partie.rec(j)
			Partie.send_all(achat)
			
			if achat == "oui" :
				# Paiement du coût en ressources :
				for ressources in tribu[1] : Partie.jeu.gestion_marchandises((ressources[0],-ressources[1]), joueur)
	
				# Gain de points de victoire :
				Partie.jeu.gestion_pv(tribu[2],joueur)
		
				# Gestion des pouvoirs spéciales :
		
				# Placement dans le tableau :
		
				lignes_dispo , emplacement_label, emplacements_possible = Partie.jeu.gestion_tableau(joueur)
				
				Partie.send(j,str(emplacements_possible))
				Partie.send_dif(j,'Où souhaitez-vous placer cette tribue "%s" ? (%s) :' % (tribu[0], " - ".join(emplacement_label)),"%s achète la tribu et doit choisir ou la placer" % Partie.t[j].pseudo)
				emplacement = int(Partie.rec(j))
				Partie.send_all(str(emplacement))

				Partie.jeu.ajout_tableau(emplacement/4, joueur, tribu)

				return True

			else : Partie.send_dif(j,"Vous n'achetez pas cette tribu","%s n'achète pas cette tribu"%Partie.t[j].pseudo)

		else : Partie.send_dif(j,"! Vous n'avez plus de place","%s n'a plus de place pour acheter sa tribu"%Partie.t[j].pseudo)
	else :  Partie.send_dif(j,"! Vous n'avez pas les ressources nécessaires pour acheter cette tribue", "! %s n'a pas les ressources nécessaires pour acheter sa tribue" % Partie.t[j].pseudo)
	
	return False
		
##############################################################
		
def noble(self, joueur) :

	"""Action de la première tuile contour"""
	
	if len( joueur["carte"]) == 1 :
		
		actions_possibles = ["D","R"]
		print "(%s) Noble : Quelle action souhaitez-vous effectuer ?" % joueur["couleur"]
		
		
		if self.jeu.verification_ressources( joueur["carte"][0][1], joueur ) :
			print "(J) Jouer la carte tribue"
			actions_possibles.append("J")
			
		print "(D) Défausser la carte tribue"
		print "(R) Ne rien faire"
			
		while True :
			action = raw_input("Choix : ")
			if action in actions_possibles : break
		
		if action == "J" : self.gestion_tribus(joueur["carte"],joueur)
		elif action =="D" : self.jeu.cartes_tribus.append(joueur["carte"].pop())

##############################################################
	
def marchand(self, joueur) :
	
	"""Action de la cinquième tuile contour"""
	
	while True : 
	
		# Variables locales :
		
		actions_possibles  = ["R"]
		deux_marchandises = []
		trois_marchandises = []
	
		seuil = 0
		l  = []
	
		for marchandise in ["sel","dattes","poivre"] :
		
			if joueur["marchandises"][marchandise] > 1 :
				deux_marchandises.append(marchandise)
				if joueur["marchandises"][marchandise] > 2 : trois_marchandises.append(marchandise)
			
		# Choix du joueur :
		
		print "(%s) Marchand : Quelle action souhaitez-vous effectuer ?" % joueur["couleur"]
	
		if len(deux_marchandises) > 0 :
			actions_possibles.append("M")
			print "(M) Echanger deux marchandises identiques contre une autre marchandise"
		
			if len(trois_marchandises) >0 :
				actions_possibles.append("P")
				print "(P) Echanger trois marchandises identiques contre une pièce d'or"
	
		print "(R) Ne rien faire"
	
		# Analyse du choix :
		
		while True :
			action = raw_input("Choix : ")
			if action in actions_possibles : break
				
		if action == "R" : break	
		
		else : 
		
			if action == "M" : 
				seuil = 2
				l = deux_marchandises
		
			else :
				seuil = 3
				l = trois_marchandises
	
			if len(l) == 1 : self.jeu.gestion_marchandises((l[0],-seuil),joueur)
	
			else : 
	
				while True :		
					march = raw_input("(%s) Quelles marchandise souhaitez-vous défausser ?  (%s)" %( joueur["couleur"],"/".join(l) ))
					if march in l : break
				self.jeu.gestion_marchandises((march,-seuil),joueur)
	
			if action == "M" :
		
				while True :
					choix = raw_input("(%s) Quelle marchandise souhaitez-vous en échange ?  (sel/dattes/poivre) :" % joueur["couleur"])
					if choix in joueur["marchandises"].keys() : break
				self.jeu.gestion_marchandises((choix,1),joueur)
	
			else : self.jeu.gestion_marchandises(("or",1),joueur)

##############################################################

def fata_morgana(self, joueur, positions) :
	
	"""Action de la neuvième tuile contour"""
	
	if len(joueur["marqueurs"]) == 0 :
		print "(%s) Fata Morgana : Vous avez déjà utilisé vos marqueurs" % joueur["couleur"]
	
	else :
	
		while True :
			action = raw_input( "(%s) Fata Morgana : Quel marqueur souhaitez-vous déplacer ? (%s/aucun)  : " % (joueur["couleur"], "/".join( map (str, joueur["marqueurs"]) ) ) )
			if action in map(str,joueur["marqueurs"]) or action == "aucun" : break
			
		if not action == "aucun" :
		
			while True :
				choix = raw_input("Où souhaitez-vous déplacer le marqueur %s ? (%s) : " % (action, "/".join(map(str,positions))))
				if choix in map(str,positions) : break
				
			joueur["marqueurs"].remove(int(action))
			joueur["marqueurs"].append(int(choix))
				
##############################################################

def orfevre(self, joueur) :		
	
	"""Action de la dixième tuile contour"""
	
	# Variables locales :
		
	actions_possibles  = ["R"]
	deux_marchandises = []
	quatre_marchandises = []

	nombre = 0
	action = 0
	l  = []

	for marchandise in  ["sel","dattes","poivre"]  :
	
		if joueur["marchandises"][marchandise] > 1 :
			deux_marchandises.append(marchandise)
			if joueur["marchandises"][marchandise] > 3 : quatre_marchandises.append(marchandise)
	
	# Choix du joueur :	
			
	print "(%s) Orfèvre : Que souhaitez-vous faire ?" % joueur["couleur"]
	
	if len(deux_marchandises) > 0 :
		print "(2M) Echanger deux marchandises identiques contre 1 PV"
		actions_possibles.append("2M")
		
		if len(quatre_marchandises) > 0 :
			print "(4M) Echanger quatre marchandises identiques contre 3 PV"
			actions_possibles.append("4M")
			
	if joueur["marchandises"]["or"] > 0 :
		print "(P) Echanger une pièce d'or contre 2 PV"
		actions_possibles.append("P")
		
		if joueur["marchandises"]["or"] > 1 :
			print "(2P) Echanger deux pièces d'or contre 4 PV"
			actions_possibles.append("2P")
	
	print "(R) Ne rien faire"
	
	while True :
	
		choix = raw_input("Choix : ")
		if choix in actions_possibles : break
		
	# Analyse du choix :
	
	if choix == "2M" : 
		action = 1
		nombre = (-2,1)
		l = deux_marchandises
		
	elif choix == "4M" :
		action = 1
		nombre = (-4,3)
		l = quatre_marchandises
	
	elif choix == "P" :
		action = 2
		nombre = (-1,2)
		
	elif choix == "2P" :
		action = 2
		nombre = (-2,4)
	
	if action == 1 :
		
		while True :
		
			march = raw_input("(%s) Quelles marchandise souhaitez-vous défausser ?  (%s) : " %( joueur["couleur"],"/".join(l) ))
			if march in l : break

		self.jeu.gestion_marchandises((march,nombre[0]),joueur)
		self.jeu.gestion_marchandises(("pv",nombre[1]),joueur)
		
	elif action == 2 : 
		self.jeu.gestion_marchandises(("or",nombre[0]),joueur)
		self.jeu.gestion_marchandises(("pv",nombre[1]),joueur)
				
##############################################################
	
def caravane(self, joueur) :
	
	"""Action de la treisième tuile contour"""				
	
	carte = self.jeu.cartes_marchandises.pop(0)
	for marchandise in self.jeu.cartes_marchandises_dico[carte] :
		self.jeu.gestion_marchandises(marchandise, joueur)
	
	self.jeu.cartes_marchandises.append(carte)
	print "(Caravane) Mise à jour carte %i (%s) " % (carte, self.jeu.cartes_marchandises)

##############################################################

def expansion_tribale(self, joueur) :
	
	"""Action de la quatorsième tuile contour"""	
			
	carte = self.jeu.cartes_tribus.pop(0)
	carte_info = self.jeu.cartes_tribus_dico[carte]
	print "Carte : (%s) de coût (%s) rapportant %i PV" % (carte_info[0], carte_info[1], carte_info[2])
	print "(%s) Expansion tribale : Quelle action souhaitez-vous faire ?" % joueur["couleur"]
	
	actions_possibles = ["D"]
	
	if len(joueur["carte"]) == 0 :
		actions_possibles.append("C")
		print "(C) Conserver la carte en main"
		
	if self.jeu.verification_ressources(self.jeu.cartes_tribus_dico[carte][1], joueur) :
		actions_possibles.append("A")
		print "(A) Acheter la tribue"
		
	print "(D) Défausser la carte"
	
	while True :
		
		choix = raw_input("Choix : ")
		if choix in actions_possibles : break
	
	print " test = ", self.jeu.cartes_tribus_dico[carte]
	if choix == "C" : joueur["carte"].append(self.jeu.cartes_tribus_dico[carte])
	elif choix == "A" : self.gestion_tribus(self.jeu.cartes_tribus_dico[carte], joueur)
	else : self.jeu.cartes_tribus.append(carte)
