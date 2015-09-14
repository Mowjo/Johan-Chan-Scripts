# -*- coding: utf-8 -*-

import select
import socket
import sys
import threading
import time
import random

from targui_gui import *
from targui_jeu_gui import * 

## Variables globales ##
NOMBREJOUEUR = 2
PSEUDOS = []
TABLES = {}
PARTIES = []

HOST = '' # on écoute tout
PORT_J = 8045 # Pour le jeu
PORT_T = 8055 # Pour le tchat
BACKLOG= 5
SIZE= 1024
THREADS = []
LISTEN = 2
RAPPORT_AV = 100/60.
#self.sock_serveur = None

################################################################
class Thread_Client(threading.Thread) :
    
    def __init__(self, (sock_client, address) ):
    
        print "*****************************************"
        print "(C) Connected from", address
        print "*****************************************"
        
        ### Phase 0 - Initialisation des clients :
        
        threading.Thread.__init__(self)
        self.sock_client = sock_client
        self.address = address
        self.size = 1024
        self.pseudo = ""
        
    def run(self):
    
        global TABLES
        global PARTIES
        
        print "(C) TABLES : ", TABLES
        print "(C) PARTIES : ", PARTIES
            
        ### Phase 0 - Choix pseudos :
        
        pseudo = self.sock_client.recv(1024)
        print "(S) pseudo =", pseudo
        self.pseudo = pseudo
            
        ### Phase 0 - Choix d'une table :
        
        # Aucune table de libre sur le serveur :
        if len(TABLES) == 0 : 
            TABLES[1] = [self]
            self.sock_client.send("creation_table")
            ack = self.sock_client.recv(1024)
            
        # Au moins une table en attente sur le serveur :
        else :
            tables_dispo = []
            choix = []
            for table in TABLES.keys():
                if len(TABLES[table])<2 :
                    choix.append("(%i) Table créée par %s" % (table,TABLES[table][0].pseudo))
                    tables_dispo.append(str(table))
            
            # Déclenche la phase de choix de table pour le client
            self.sock_client.send("choix_table")    
            ack = self.sock_client.recv(1024)
            
            # On envoi la liste des choix possible
            self.sock_client.send("%s" % choix)
            ack = self.sock_client.recv(1024)
            
            # Et la liste des numéros de tables associés aux choix possible
            self.sock_client.send("%s" % tables_dispo)
            ack = self.sock_client.recv(1024)
            
            # Envoi des parties en cours pour suivre la progression :
            l = map(lambda x : "Partie entre %s & %s (Progression )" % (x.t[0].pseudo,x.t[1].pseudo),PARTIES )
            print "l = ", l
            self.sock_client.send(str(l))
            ack = self.sock_client.recv(1024)
            
            # On attend la réponse du client    
            choix = self.sock_client.recv(1024)
            
            if choix.upper() == "N" :
                print "Création nouvelle table"
                TABLES[len(TABLES)+1] = [self]
                # On prévient le client de l'ouverture d'une table
                self.sock_client.send("creation_table")
                ack = self.sock_client.recv(1024)
            
            elif choix in tables_dispo :
                global PARTIE
                # On ajoute le client à une table existate
                TABLES[int(choix)].append(self)
                
                # On lance une partie sur cette table
                partie = ThreadPartie(self.sock_client,TABLES[int(choix)])
                partie.start()
                PARTIES.append(partie)
                del TABLES[int(choix)]
                
        print "CHOIX TABLE FINI"

################################################################

class ThreadServeur(threading.Thread):

    #--------------------------------------------------------
    def __init__(self, conn):
        
        threading.Thread.__init__(self)
        self.connexion = conn   # réf. du socket de connexion
        
    #--------------------------------------------------------   
    def run(self):
                
        while True :
        
            print "(S) Attente client"
            c = Thread_Client(self.connexion.accept())
            c.start()

#################################################

class ThreadPartie(threading.Thread):
    """ Thread jeu"""
    #----------------------------------------------
    def __init__(self, conn, threads):
        
        threading.Thread.__init__(self)
        self.connexion = conn   # réf. du socket de connexion
        
        ## Initialisation jeu :
        self.jeu = Jeu()
        self.t = threads # threads des joueurs
        print "self.t = ", self.t
        self.pourcentage = 0
        
    #---------------------------------------------- 
    def run(self):
        
        global PSEUDOS
        global THREADS
        
        ### Phase 0 - Initialisation des clients :
        print "Début fonction partie"
                
        try :
                    
            ### Phase 0 - Début du jeu :
        
            # Permet d'avertir les clients du début de la partie :
            self.send_all("start") 

            #Envoi le pseudo de l'adversaire
            for i in range(2) : 
                self.send(i,self.t[(i+1)%2].pseudo)
                self.send(i,self.jeu.joueurs[i]["couleur"])
            # Random ordre de jeu (Premier joueur en position 0)
            random.shuffle(self.t) 
        
            # Initialisation du plateau de départ :
            self.init_plateau()
            
            while True:
                if not self.jeu.fin_partie():
                    self.send_all("go on")
                    self.update_plateau()
                    self.phase1()
                    self.phase2()
                    self.phase3()
                    self.fin_manche()
                else : 
                    self.send_all("break")
                    break
                
            
        except KeyboardInterrupt, SystemExit :
            print "FIN SERVEUR"
            self.join()
            self.connexion.close()
            
    """         
    ##################################################
    #           Fonctions phasesX                    #
    ##################################################      
    """ 

    def init_plateau(self):
    
        self.jeu.initialisation_plateau()
    
        
    def update_plateau(self) :
        
        print """
        #--------------------------#
               Update Plateau
        #--------------------------#
        """
        
        cartes = []
        for i in [6,7,8,11,12,13,16,17,18] :
            if self.jeu.plateau[i][0] == 1 :
                cartes.append((i,self.jeu.plateau[i][1],"marchandise"))
                
            else :  
                cartes.append((i,self.jeu.plateau[i][1],self.jeu.cartes_tribus_dico[self.jeu.plateau[i][1]][0]))

        print cartes

        # Découverte des cartes initiales
        e = self.send_all(str(cartes)) 
        # Préparation des emplacements cliquables
        e = self.send_all(str(self.jeu.gestion_plateau())) 
        # Position initiale du voleur
        e = self.send_all(str(self.jeu.voleur)) 
        # Ressources initiales
        self.update_ressources()
        self.update_pourcentage()
        
    def phase1(self):
        ### Phase I : Placement des targuis
        
        print """
        #--------------------------#
                  Phase I
        #--------------------------#
        """
        
        for j in range(6) : # 0 1 2 3 4 5 
    
            print "(P) Tour %i" % j
    
            ## Messages différents à chaque joueurs :
            self.send_dif( j%2, "Placer un targui sur une carte du contour",
            "C'est au tour de %s" % self.t[j].pseudo )

            ## Consigne joueur/non joueurs :
            self.send_dif(j%2, "go", "wait")

            ## Reception de la case cliquée par le joueur actif :
            case = self.rec(j%2)

            # Envoie des nouvelles données à tous les joueurs
            self.send_all(str(self.jeu.placement_targuis(int(case),j%2)))
            self.send_all( str(case))
            self.send_all(str(self.jeu.joueurs[j%2]["couleur"].lower()))
        self.update_pourcentage()
    
    def phase2(self):
        ### Phase II : Placement des marqueurs 
    
        print """
        #--------------------------#
                  Phase II
        #--------------------------#
        """
    
        l_marqueurs = []
        for joueur in self.jeu.joueurs : 
            for marqueur in self.jeu.placement_marqueur(joueur) : 
                l_marqueurs.append([joueur["couleur"].lower(), marqueur])

        self.send_all(str(l_marqueurs))
    
    def phase3(self):
        ### Phase III : Récupération des pions
    
        print """
        #--------------------------#
                  Phase III
        #--------------------------#
        """
        self.update_pourcentage()

        for j in range(2) :
            joueur = self.jeu.joueurs[j]
            self.send_dif( j, "Retirez vos pions.",
                           "C'est au tour de %s." % self.t[j].pseudo)
            self.send_dif(j, "joueur", "adversaire")

            while True :
                if len(self.jeu.phase_marqueur(joueur)) == 0 :
                    self.send_all("break")              
                    break
                else : self.send_all("go on")
                self.send_all(joueur["couleur"].lower())
                self.send_all(str(self.jeu.phase_marqueur(joueur)))
                case = self.rec(j)
                print "case = ", case
                self.send_all(case)
                case = int(case)

                
                # Action targuis :
                
                if case in joueur["targuis"] :
                    # Marchandises :
                    if len(self.jeu.plateau[case]) > 1 : 
                        self.jeu.plateau[case][0](self.jeu.plateau[case][1], joueur) 
                        self.send_all("marchandise_targui")
                        self.send_dif(j,"Vous gagnez +1 %s"%self.jeu.plateau[case][1][0],"%s gagne +1 %s"%(PSEUDOS[j],self.jeu.plateau[case][1][0]))
                    # Actions spéciales :
                    else :
                        self.send_all("action_targui")
                        self.send_dif(j,"Vous faites une action spéciale","%s fait une action spéciale"%PSEUDOS[j])
                        #self.jeu.plateau[case][0](joueur)
                
                    joueur["targuis"].remove(case)

                
                # Action marqueurs :
            
                elif case in joueur["marqueurs"]  : 
        
                    if self.jeu.plateau[case][0] == 1 : # marchandise
                        lab = ""
                        for i in self.jeu.cartes_marchandises_dico[self.jeu.plateau[case][1]] : 
                            self.jeu.gestion_marchandises(i, joueur) 
                            lab += " +%i %s"%(int(i[1]),i[0])
                            
                        labj = "Vous gagnez %s"%lab
                        labdif = "%s gagne %s"%(self.t[j].pseudo,lab)
                        
                        self.send_all("marchandise_marqueur")
                        self.send_dif(j,labj,labdif)
                        
                        self.jeu.mise_a_jour(case)
                        
                
                    else :
                        self.send_all("tribus_marqueur")
                        if self.gestion_tribus(self.jeu.cartes_tribus_dico[self.jeu.plateau[case][1]], joueur,j) : self.jeu.mise_a_jour(case)
            
                    joueur["marqueurs"].remove(case)    

                self.update_ressources()
            self.update_pourcentage()
            
    def fin_manche(self):
        PSEUDOS.reverse()
        THREADS.reverse()
        self.jeu.fin_manche()
        
#------------------------------------------------------------------------------------------------------
                
    def gestion_tribus(self, tribu, joueur, j ) :
        
        """Gestion des actions associées à l'activation d'une carte tribue"""
                    
        #( type, coût, pv, power, num)
        
        if self.jeu.verification_ressources(tribu[1], joueur)  :
        
            if joueur["cartes_tableau"] < 12 :
            
                self.send_dif(j,'Souhaitez-vous acheter la carte tribue "%s" sous votre marqueur (%s) pour %i pv  ? (*oui*/*non*) : ' % (tribu[0], tribu[1], tribu[2]),"%s doit choisir que faire de sa carte tribu"% self.t[j].pseudo)
                achat = self.rec(j)
                self.send_all(achat)
                if achat == "oui" :
                    # Paiement du coût en ressources :
                    for ressources in tribu[1] : self.jeu.gestion_marchandises((ressources[0],-ressources[1]), joueur)
        
                    # Gain de points de victoire :
            
                    self.jeu.gestion_pv(tribu[2],joueur)
            
                    # Gestion des pouvoirs spéciales :
            
                    # Placement dans le tableau :
            
                    lignes_dispo , emplacement_label, emplacements_possible = self.jeu.gestion_tableau(joueur)
                    
                    self.send(j,str(emplacements_possible))
                    self.send_dif(j,'Où souhaitez-vous placer cette tribue "%s" ? (%s) :' % (tribu[0], " - ".join(emplacement_label)),"%s achète la tribu et doit choisir ou la placer" % self.t[j].pseudo)
                    emplacement = int(self.rec(j))
                    self.send_all(str(emplacement))

                    self.jeu.ajout_tableau(emplacement/4, joueur, tribu)

                    return True

                else : self.send_dif(j,"Vous n'achetez pas cette tribu","%s n'achète pas cette tribu"%self.t[j].pseudo)

            else : self.send_dif(j,"! Vous n'avez plus de place","%s n'a plus de place pour acheter sa tribu"%self.t[j].pseudo)
        else :  self.send_dif(j,"! Vous n'avez pas les ressources nécessaires pour acheter cette tribue", "! %s n'a pas les ressources nécessaires pour acheter sa tribue" % self.t[j].pseudo)
        
        return False


#-----------------------------------------------------------------------------------------------------
        
        
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

#*****************************************************************************************************************************************************************
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

#*****************************************************************************************************************************************************************
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
                
#*****************************************************************************************************************************************************************
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
        
                    
#*****************************************************************************************************************************************************************
    def caravane(self, joueur) :
        
        """Action de la treisième tuile contour"""              
        
        carte = self.jeu.cartes_marchandises.pop(0)
        for marchandise in self.jeu.cartes_marchandises_dico[carte] :
            self.jeu.gestion_marchandises(marchandise, joueur)
        
        self.jeu.cartes_marchandises.append(carte)
        print "(Caravane) Mise à jour carte %i (%s) " % (carte, self.jeu.cartes_marchandises)
#*****************************************************************************************************************************************************************
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
        

#*****************************************************************************************************************************************************************

    

        
    """ 
    ########################################
    # Methodes d'échange avec les clients  #
    ########################################
    """
    def adv(self, joueur) : return (joueur+1)%2
    
    def rec(self, joueur) :
        return self.t[joueur].sock_client.recv(4096)
        
    def send(self, joueur, message) :
        self.t[joueur].sock_client.send(message)
        a = self.t[joueur].sock_client.recv(4096)
        
    def send_all(self, message):
        print "threads =", self.t
        print "(S) Envoie tous : ", message
        
        for client in self.t :  
            print "send to : ", client
            client.sock_client.send(message)
            a = client.sock_client.recv(4096)
            
        return True
        
    def send_dif(self, joueur, message_joueur, message_adv):
    
        self.t[joueur].sock_client.send(message_joueur)
        a = self.t[joueur].sock_client.recv(4096)
        self.t[self.adv(joueur)].sock_client.send(message_adv)
        a = self.t[self.adv(joueur)].sock_client.recv(4096)
            
    def update_ressources(self):
        i = 0
        self.send_dif(i,str(self.jeu.joueurs[i]["marchandises"]),str(self.jeu.joueurs[(i+1)%2]["marchandises"]))
        self.send_dif(i,str(self.jeu.joueurs[(i+1)%2]["marchandises"]),str(self.jeu.joueurs[i]["marchandises"]))

    def update_pourcentage(self):
        self.pourcentage += 1
        self.send_all(str(self.pourcentage*RAPPORT_AV))

################################################################

class ThreadTchat(threading.Thread):

    #--------------------------------------------------------
	def __init__(self, conn):
		
		threading.Thread.__init__(self)
		self.connexion = conn   # réf. du socket de connexion
		self.CONNECTION_LIST = [] # liste des sockets
    #--------------------------------------------------------   

    #Fonction pour diffuser les messages a tout les clients :
	def diffuser_msg(self,message):
		for socket in self.CONNECTION_LIST:
			if socket != self.connexion  :
				try :
					socket.send(message)
				except :
					socket.close()
					self.CONNECTION_LIST.remove(socket)
					
					
	def run(self):
		
		# Initialisation :
		RECV_BUFFER = 4096 # Recommandable pour une bonne fluidite		
		# On ajoute la socket serveur a la liste :
		self.CONNECTION_LIST.append(self.connexion )
		
		print "Utilisation du port tchat : " + str(PORT_T)
		
		while 1:
			# Recuperation des sockets pretes a etre lue dans <read_sockets> par select :
			read_sockets,write_sockets,error_sockets = select.select(self.CONNECTION_LIST,[],[])
			
			for sock in read_sockets:
				# Nouvelle connection :
				if sock == self.connexion :
					# On ajoute la nouvelle connexion recue par serveur_socket :
					new_sock, addr = self.connexion .accept()
					self.CONNECTION_LIST.append(new_sock) # on oublie pas de l ajouter a la liste
					#self.THREADS.append(new_sock)
					self.diffuser_msg("Joueur [%s:%s] connecte\n" % addr)
										
				# Si nous recevons un message client :
				else:
	
					try:
						Message = sock.recv(RECV_BUFFER) # recuperation d un message eventuelle
						print Message
						if Message: # si message il y a
							self.diffuser_msg(Message)               
							
						
					except:
						self.diffuser_msg("Joueur (%s, %s) est hors ligne" % addr)
						print "Joeur (%s, %s) est hors ligne" % addr
						sock.close() # on ferme la socket inactive
						self.CONNECTION_LIST.remove(sock)
						continue
					
		self.connexion.close()
            
#################################################

## Ouverture Socket Jeu :
try :
    # Ouverture d'une socket pour le jeu
    sock_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_serveur.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock_serveur.bind( (HOST, PORT_J) )
    sock_serveur.listen(LISTEN)

    # Ouverture d'une socket pour le tchat
    sock_tchat =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock_tchat = setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock_tchat.bind( (HOST, PORT_T) )
    sock_tchat.listen(LISTEN)
    
except socket.error, (value, message):  
    if sock_serveur : sock_serveur.close()
    print "(S) Ouverture impossible de la socket :" + message
    sys.exit(1)         

## Création et lancement des threads :
th_tchat = ThreadTchat(sock_tchat)
th_serv = ThreadServeur(sock_serveur)

th_tchat.start()
th_serv.start()


