#! /usr/bin/python
# -*- coding: utf-8 -*-

# 3 FEVRIER

import socket, sys, threading, time, select
from targui_gui import *
#from PyQt4 import QtCore, QtGui
from targui_jeu_gui import * 

HOST= "127.0.0.1" # ou "localhost"
PORT_J = 8045 # Pour le jeu
PORT_T = 8055  # Pour le tchat

#################################################           
class ThreadJeu(QtCore.QThread):  #threading.Thread
    def __init__(self, conn, ui):
        QtCore.QThread.__init__(self)
        #threading.Thread.__init__(self)
        self.connexion = conn  # réf. du socket de connexion
        self.ui = ui
        
    def run(self):
        global PSEUDO
        self.send(PSEUDO)

        jeu = True
        while True : # Attente d'un message démarrant le jeu
            
            message_recu = self.rec()
            
            if message_recu == "creation_table":
                print "*** Création d'une table : Attente d'un second joueur… ***"
            
            elif message_recu == "choix_table":
                self.choix_table()
            elif  message_recu == "start" : 
                # print "(C) cas deb"
                break
                
            elif not message_recu or message_recu.upper() == "STOP" : 
                print "(C) cas stop"
                jeu = False
                break
                    
        if jeu :
            print "(C) la partie commence"
            pseudo_adv = self.rec()
            self.emit(QtCore.SIGNAL("update_pseudo_adv"),pseudo_adv)
            couleur = self.rec()
            self.emit(QtCore.SIGNAL("update_couleur"),couleur)
            
            while True:
                partie = self.rec()
                if partie == "break": break
                else:
                    self.update_plateau()
                    self.phase1()
                    self.phase2()
                    self.phase3()
                    self.fin_manche()
            print "Fin"
    
        self.connexion.close()
        
    """
    ##################################################
    #           Fonctions phasesX                    #
    ##################################################
    """
    
    def choix_table(self) :
        print "***********************\nChoix d'une table de jeu\n***********************"
                
        print "Choissisez le numéro d'une table déjà créée pour la rejoindre ou saisisez N pour créer une nouvelle table :\n"
        
        tables = self.rec()
        print "Tables :" 
        for t in eval(tables) : print "-%s" % t
        print "-(N) Nouvelle table"
        
        tables_dispo = self.rec()
        parties_en_cours  = eval(self.rec())
        print "partie en cours = ", parties_en_cours
        
        print "Parties en cours :"
        if len(parties_en_cours) < 1 : print "Aucune partie en cours"
        else : 
            for p in parties_en_cours :
                 print "- %s" % p
        
        
        while True :
            choix = raw_input("Choix : ")
            if (choix in eval(tables_dispo) or choix.upper() == "N") : 
                print "choix acceptable"
                break
        
        print "Choix = ", choix
        self.send(choix)
        
    def update_plateau(self) :
        ### Mise à jour du plateau : cartes, position voleur, ressources, emplacement cliquable...
        print """
        #--------------------------#
               Update Plateau
        #--------------------------#
        """
                
        cartes = self.rec()
        cartes = eval(cartes)
        plateau_hi = self.rec()
        voleur = self.rec()
        
        ## Signaux pour l'interface graphique :
        self.emit(QtCore.SIGNAL("voleur"),eval(voleur))
        self.emit(QtCore.SIGNAL("plateau_hi"),[eval(plateau_hi)])
        
        for carte in cartes :
            self.emit(QtCore.SIGNAL("cartes"),carte)
            
        self.update_ressources()
        self.update_pourcentage()
                
    def phase1(self):
        ### Phase I : Placement des targuis
        
        print """
        #--------------------------#
                  Phase I
        #--------------------------#
        """
        
        for j in range(6) : 
            print "(C) tour %i" % j
            lab = self.rec()
            print "lab =", lab
            consigne = self.rec()
            print "consigne =", consigne
        
            if consigne == "go" :
                print "joueur en cours"
                self.emit(QtCore.SIGNAL("allow_clic"))
                self.emit(QtCore.SIGNAL("setCAW"),lab)
                while self.ui.case == 0: pass
                print "go - case = ", self.ui.case
                self.send(str(self.ui.case))
                self.ui.case = 0    
                
            elif consigne == "wait" : 
                print "joueur en attente"
                self.emit(QtCore.SIGNAL("setC"),lab)
            
            plateau_hi = self.rec()
            self.emit(QtCore.SIGNAL("plateau_hi"),[eval(plateau_hi)])
            case = self.rec()
            targui = self.rec()
            self.emit(QtCore.SIGNAL("targui"),(targui,int(case)))
        self.update_pourcentage()
            
            
    def phase2(self):
        ### Phase II : Placement des marqueurs 
        
        print """
        #--------------------------#
                 Phase II
        #--------------------------#
        """
        
        marqueurs = self.rec()
        # "type marqu = ", type(marqueurs)
        marqueurs = eval(marqueurs) 
        # print "marqueurs = ", marqueurs
        for marqueur in marqueurs :
            self.emit(QtCore.SIGNAL("affichage_marqueur"),marqueur)
        
        
            
                        
    def phase3(self):
        ### Phase III : Récupération des pions
        
        print """
        #--------------------------#
                 Phase III
        #--------------------------#
        """
        self.update_pourcentage()
        
        self.emit(QtCore.SIGNAL("supprimer_tout_hilight"))

        for i in range(2):
            lab = self.rec()
            self.emit(QtCore.SIGNAL("setC"),ui.formateMessage(lab))
            
            consigne = self.rec()
            print "consigne =", consigne
            
            while True:
                info = self.rec()
                if info == "break": break
                
                couleur = self.rec()
                cliquable = self.rec()
                
                if consigne == "joueur" :
                    self.emit(QtCore.SIGNAL("plateau_hi"),[eval(cliquable)])
                    self.emit(QtCore.SIGNAL("allow_clic"))
                    while self.ui.case == 0: pass
                    print "go - case = ", self.ui.case
                    self.send(str(self.ui.case))
                    self.ui.case = 0
                    
                elif consigne == "adversaire" : 
                    self.emit(QtCore.SIGNAL("plateau_hi"),[eval(cliquable),couleur])


                case = int(self.rec())
                
                action = self.rec()


                # 
                
                if action == "marchandise_targui":
                    lab = self.rec()
                    self.emit(QtCore.SIGNAL("setC"),lab)
                    
                elif action == "action_targui":
                    lab = self.rec()
                    self.emit(QtCore.SIGNAL("setC"),lab)
                    
                elif action == "marchandise_marqueur":
                    lab = self.rec()
                    self.emit(QtCore.SIGNAL("setC"),lab)
                    self.emit(QtCore.SIGNAL("nettoyer_cache"))
                    self.emit(QtCore.SIGNAL("change_carte_to_tribu"),case)
                elif action == "tribus_marqueur":
                    self.gestion_tribus(case, consigne)

                self.emit(QtCore.SIGNAL("supprimer_pion"),case)
                self.update_ressources()
            self.update_pourcentage()

    def fin_manche(self):
        self.emit(QtCore.SIGNAL("supprimer_tout_hilight"))
        
    """ 
    ########################################
    # Methodes d'échange avec le serveur   #
    ########################################
    """     
    def rec(self,rep="ok"):
        m  = self.connexion.recv(1024)
        self.send(rep)
        return m
        
    def send(self,message) : 
        # print "(C) Envoi :", message
        self.connexion.send(message)
    
    def decode(self,messages):
        
        return map(lambda x : x[4:], messages.split(";")[:-1])
    
    def update_ressources(self):
        perso = self.rec()
        adv = self.rec()
        self.emit(QtCore.SIGNAL("update_ressources"),[eval(perso), eval(adv)])

    def update_pourcentage(self):
        pourcentage = self.rec()
        self.emit(QtCore.SIGNAL("update_pourcentage"),int(round(float(pourcentage))))

    def fin_partie(self):
        print "on quitte tout"

    def gestion_tribus(self, case, consigne):
        lab = self.rec()
        self.emit(QtCore.SIGNAL("setC"),lab)
        if not lab[0]=="!":
            if consigne == "joueur":
                while self.ui.option == "": pass
                option = str(self.ui.option)
                self.ui.option = ""
                self.send(option)
                option = self.rec()
                if option == "oui":
                    
                    emplacements_possible = self.rec()
                    print "emplacements_possible = ", emplacements_possible
                    
                    lab = self.rec()
                    self.emit(QtCore.SIGNAL("setC"),lab)

                    self.emit(QtCore.SIGNAL("plateau_decliquable"))
                    self.emit(QtCore.SIGNAL("plateau_hi_tab"),eval(emplacements_possible))
                    self.emit(QtCore.SIGNAL("allow_clic_tab"))
                    while self.ui.case_tab == -1: pass
                    print "go - case = ", self.ui.case_tab
                    self.send(str(self.ui.case_tab))
                    self.ui.case_tab = -1
                    self.emit(QtCore.SIGNAL("plateau_decliquable_tab"))
                    case_tab = int(self.rec())
                    self.emit(QtCore.SIGNAL("trans_achat"),[case,case_tab,consigne])
                    self.emit(QtCore.SIGNAL("change_carte_to_marchandise"),case)

                else:
                    lab = self.rec()
                    self.emit(QtCore.SIGNAL("setC"),lab)

                    
            elif consigne == "adversaire":
                option = self.rec()
                if option == "oui":
                    lab = self.rec()
                    self.emit(QtCore.SIGNAL("setC"),lab)
                    case_tab = int(self.rec())
                    self.emit(QtCore.SIGNAL("trans_achat"),[case,case_tab,consigne])
                    self.emit(QtCore.SIGNAL("change_carte_to_marchandise"),case)
                else :
                    lab = self.rec()
                    self.emit(QtCore.SIGNAL("setC"),lab)

#################################################       
class ThreadTchatEm(QtCore.QThread):
	"""objet thread gérant l'émission des messages"""
	def __init__(self, conn):
		QtCore.QThread.__init__(self)
		self.connexion = conn   # réf. du socket de connexion
		if len(sys.argv) == 2 :
			self.name = str(sys.argv[1])
		else :
			self.name = 'Client :' 
		
	def envoyer(self,message):
		message = self.name + ' : ' + message
		self.connexion.send(message)
            
           
#################################################

#################################################       
class ThreadTchatRe(QtCore.QThread):
	"""objet thread gérant la reception des messages"""
	def __init__(self, conn):
		QtCore.QThread.__init__(self)
		self.connexion = conn   # réf. du socket de connexion
		
	def run(self):
		while 1:
			Message = self.connexion.recv(4096)
			self.emit(QtCore.SIGNAL("reception_message"),Message)

                        
            
#################################################




# Programme principal - Établissement de la connexion
# protocoles IPv4 et TCP
sock_jeu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_jeu.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock_tchat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_tchat.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

# mySocket.setblocking(0) # Empêche de bloquer sur recv indéfiniement

try:
    sock_jeu.connect((HOST, PORT_J))
    sock_tchat.connect((HOST,PORT_T))
    
except socket.error :
    print "La connexion a échoué."
    sys.exit()
 
# Affichage Fenetre

fen = Application(sys.argv)
PSEUDO = sys.argv[1] if len(sys.argv)>1 else "Joueur1" ### A modifier si personne ne rentre de pseudo
fen.MainWindow = MainWindowUi(fen, PSEUDO, "Attente d'un copinou")
ui = fen.MainWindow
    
# Création et lancement des threads :
th_J = ThreadJeu(sock_jeu,ui)
th_Em = ThreadTchatEm(sock_tchat)
th_Re = ThreadTchatRe(sock_tchat)


# Gestion signaux :
ui.connect(th_J,QtCore.SIGNAL("voleur"),ui.affichage_voleur)
ui.connect(th_J,QtCore.SIGNAL("plateau_hi"),ui.plateau_hi)
ui.connect(th_J,QtCore.SIGNAL("plateau_decliquable"),ui.plateau_decliquable)
ui.connect(th_J,QtCore.SIGNAL("allow_clic"),ui.allow_clic)
ui.connect(th_J,QtCore.SIGNAL("plateau_hi_tab"),ui.plateau_hi_tab)
ui.connect(th_J,QtCore.SIGNAL("allow_clic_tab"),ui.allow_clic_tab)
ui.connect(th_J,QtCore.SIGNAL("plateau_decliquable_tab"),ui.plateau_decliquable_tab)
ui.connect(th_J,QtCore.SIGNAL("cartes"),ui.modifier_carte)
ui.connect(th_J,QtCore.SIGNAL("setCAW"),ui.setConsignesAndWait)
ui.connect(th_J,QtCore.SIGNAL("setC"),ui.setConsignes)
ui.connect(th_J,QtCore.SIGNAL("targui"),ui.affichage_targui)
ui.connect(th_J,QtCore.SIGNAL("affichage_marqueur"),ui.affichage_marqueur)
ui.connect(th_J,QtCore.SIGNAL("supprimer_tout_hilight"),ui.supprimer_tout_hilight)
ui.connect(th_J,QtCore.SIGNAL("update_pseudo_adv"),ui.update_pseudo_adv)
ui.connect(th_J,QtCore.SIGNAL("update_couleur"),ui.update_couleur)
ui.connect(th_J,QtCore.SIGNAL("supprimer_pion"),ui.supprimer_pion)
ui.connect(th_J,QtCore.SIGNAL("update_ressources"),ui.update_ressources)
ui.connect(th_J,QtCore.SIGNAL("update_pourcentage"),ui.update_pourcentage)
ui.connect(th_J,QtCore.SIGNAL("nettoyer_cache"),ui.nettoyer_cache)
ui.connect(th_J,QtCore.SIGNAL("change_carte_to_tribu"),ui.change_carte_to_tribu)
ui.connect(th_J,QtCore.SIGNAL("change_carte_to_marchandise"),ui.change_carte_to_marchandise)
ui.connect(th_J,QtCore.SIGNAL("trans_achat"),ui.transferer_carte_achat)
th_J.connect(ui,QtCore.SIGNAL("fin_jeu"),th_J.fin_partie)
th_Em.connect(ui,QtCore.SIGNAL("envoyer_message"),th_Em.envoyer)
ui.connect(th_Re,QtCore.SIGNAL("reception_message"),ui.chat_reception) # L 279

# Lancement des threads
th_J.start()
th_Em.start()
th_Re.start()
# Main loop
sys.exit(fen.exec_())

