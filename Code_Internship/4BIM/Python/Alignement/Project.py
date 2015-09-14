#-*- coding:utf8-*-

import random
import math
import copy
aa =('A','T','C','G')

#####################################################################################
#
#						 CLASSE GENE 
#
#####################################################################################
class Gene:

	def __init__(self,mu,sigma,nom): 
		self.nom = nom
		self.mu = mu
		self.sigma = sigma
		self.sens = 1 #si il est dans le mauvais sens alors -1 
		self.taille = int(round(random.gauss(self.mu,self.sigma))+1) #arrondi a l'unite, essayer d'arrondir a l'unite d'au dessus aussi
# ATTENTION EXCLURE 0
		self.seq_gene = []
		for i in range(self.taille):   #n = range(self.taille)
			self.seq_gene.append(random.choice(aa))
		

		
	def __repr__(self):
		affiche = ""
		for i in range(len(self.seq_gene)):
			affiche += str(self.seq_gene[i])+ " "
		return affiche
	
	def substitution(self): # modèle de kimura
		alpha = 4
		beta = 1
		pos = random.randint(0,self.taille-1)
		proba = random.randint(0,alpha)
		if proba in range(alpha):
			if self.seq_gene[pos] == "A":
				self.seq_gene[pos] = "G"
				
			elif self.seq_gene[pos] == "G":
				self.seq_gene[pos] = "A"
				
			elif self.seq_gene[pos] == "T":
				self.seq_gene[pos] = "C"
				
			else:
				self.seq_gene[pos] = "T"
		if proba in range(alpha,alpha + beta):
			if self.seq_gene[pos] == "A":
				self.seq_gene[pos] = random.choice(("C","T"))
				
			elif self.seq_gene[pos] == "T":
				self.seq_gene[pos] = random.choice(("A","G"))
				
			elif self.seq_gene[pos] == "C":
				self.seq_gene[pos] = random.choice(("A","G"))
				
			else:
				self.seq_gene[pos] = random.choice(("T","C"))

	def evolution_gene(self,pas,tmax):
		nb_subst = 0
		fichier = open('resultat_substitution','w')
		temp_seq_1 = ""
		temp_seq_1 = ''.join(self.seq_gene)
		iter = tmax/pas
		for i in range(iter):
			for j in range(pas):
				self.substitution()
				nb_subst += 1
			nb_subst_theo =  0
			temp_seq_2 = ""
			temp_seq_2 = ''.join(self.seq_gene)
			for index in range(self.taille):
				if temp_seq_1[index] != temp_seq_2[index]:
					nb_subst_theo += 1
			fichier.write(str(nb_subst)+" "+str(nb_subst_theo)+"\n")
		fichier.close()
          

	def saturation_gene(self):
		nb_subst = 0
		fichier = open('resultat_saturation','w')
		temp_seq_1 = ""
		temp_seq_1 = ''.join(self.seq_gene)
		p = 2000000/75 # traduit qu'il y a 75 chance sur 100 000 d'avoir une substitution dans un gène de 1500 nucléotide par génération
		for i in range(0,45*pow(10,7),25): # on opère tout les 25ans = une génération
			prob = random.randint(0,p)
			if prob == 0:
				self.substitution()
				nb_subst += 1
			if i%10000 == 0:
				nb_subst_theo =  0
				temp_seq_2 = ""
				temp_seq_2 = ''.join(self.seq_gene)
				for index in range(self.taille):
					if temp_seq_1[index] != temp_seq_2[index]:
						nb_subst_theo += 1
				fichier.write(str(i)+" "+str(nb_subst)+" "+str(nb_subst_theo)+"\n")
		fichier.close()
		
#####################################################################################
#
#								CLASSE GENOME
#
#####################################################################################
class Genome:
	def __init__(self,nb_gene,mu,sigma): # ça ne me plait pas trop de passer mu et sigma dans genome avant d'aller à gene, faut trouver une alternative
		self.nb_gene = nb_gene
		n = range(1,self.nb_gene+1)
		self.genome = []
		for i in n:
			g = Gene(mu,sigma,i)
			self.genome.append(g)
		self.distance = []	# distance double coupé collé
		self.etat_sommet = {}
		self.genome_origine = copy.deepcopy(self.genome)
		
	def __repr__(self):
		
		affiche = ""
		for i in range(len(self.genome)):
			affiche += str(self.genome[i].nom) + " "
			affiche += str(self.genome[i]) + "\n"
		for i in range(len(self.genome)):
			affiche += str(self.genome[i].nom)
			if self.genome[i].sens == 1:
				affiche += "+ "
			else :
				affiche += "- "
		
		affiche += "\n"
		for i in range(len(self.genome_origine)):
			affiche += str(self.genome_origine[i].nom) + " "
			affiche += str(self.genome_origine[i]) + "\n"
		for i in range(len(self.genome_origine)):
			affiche += str(self.genome_origine[i].nom)
			if self.genome_origine[i].sens == 1:
				affiche += "+ "
			else :
				affiche += "- "
				
		return affiche		
		
	def inversion(self):          
		debut = random.randint(0,self.nb_gene-1)
		taille = random.randint(1,self.nb_gene-debut)
		temp = []
		for i in range(taille):
			temp.append(self.genome[debut+i])
			temp[i].sens = -1*temp[i].sens
			temp[i].seq_gene.reverse()
		temp.reverse()
		for i in range(taille):
			self.genome[debut+i] = temp[i]

	def liste_adjacence(self,temp_genome): 
		liste_adj =[]
		liste_adj.append([temp_genome[0].sens*temp_genome[0].nom])
		for i in range(len(temp_genome)-1):
			liste_adj.append([-1*temp_genome[i].sens*temp_genome[i].nom,temp_genome[i+1].sens*temp_genome[i+1].nom]) # <+> signifie le début du gene et <-> la fin du gene 
		liste_adj.append([temp_genome[len(temp_genome)-1].nom*-1*temp_genome[len(temp_genome)-1].sens])
		return liste_adj

	def chemin(self): # la méthhode inversion est faites à ce moment la 
		adjacence_init = self.liste_adjacence(self.genome_origine)
		self.inversion()
		adjacence_final = self.liste_adjacence(self.genome)[:]
		adjacence_final += adjacence_init[:]
		return adjacence_final
	
	
	def DFS(self):
		#initialisation
		nb_cycle=0
		impair = 0
		graphe = self.chemin() # inversion appliquée à ce moment là par la méthode chemin
		for element in range(1,self.nb_gene+1):
			self.etat_sommet[element] = "inconnu"
			self.etat_sommet[-element] = "inconnu"	
		for sommet in self.etat_sommet.keys():
			longueur_chemin = 0
			if self.etat_sommet[sommet] == "inconnu":
				nb_cycle += self.DFS_parcours(sommet,graphe)
				for i in self.etat_sommet.keys():
					if self.etat_sommet[i] == "explore":
						longueur_chemin += 1
						self.etat_sommet[i] = "connu"
				if longueur_chemin%2 == 1:
					impair += 1
				
		distance_double_coupe_colle = self.nb_gene - (nb_cycle + (impair/2))
		#print nb_cycle,impair
		#print "distance double coupe/colle :",distance_double_coupe_colle
		return distance_double_coupe_colle


	def DFS_parcours(self,sommet,graphe):
		nb_cycle = 0
		self.etat_sommet[sommet] = "explore"
		liste_sommet = []
		temp_graphe = []
		for j in graphe:
			temp_graphe.append(j)

		for i in temp_graphe:
			if sommet in i and len(i) != 1:
				temp_adj = []
				for k in i:
					temp_adj.append(k)
				temp_adj.remove(sommet)
				liste_sommet.append(temp_adj[0])
		for element in liste_sommet :
			if self.etat_sommet[element] == "inconnu":
				self.DFS_parcours(element,graphe)
				
			else :
				if element == liste_sommet[len(liste_sommet)-1]:
					nb_cycle = 1
		

		return nb_cycle
	
	def evolution_genome(self):

		bool_inversion = True
		nb_inversion_obs = 0
		while bool_inversion == True:
			nb_inversion_theo = self.DFS() # inversion ici
			nb_inversion_obs += 1
			if nb_inversion_obs != nb_inversion_theo:
				bool_inversion = False
		
		
		return (nb_inversion_obs,nb_inversion_theo)		
#####################################################################################
#
#								OUTPUT FONCTION 
#
#####################################################################################

### ***********  Alignement ****************************************:
	
def compare(seq1,seq2,corresp,miss,i,j):
	score = 0
	if seq1[i] == seq2[j]:
		score = corresp
	else:
		score = miss
	return score


def initialisation(seq1,seq2):
	nouv_seq1 = "0" + seq1
	nouv_seq2 = "0" + seq2
	
	matrice = [[]]
	for i in range(len(nouv_seq1)):
		matrice[0].append(-i)
	for j in range(1,len(nouv_seq2)):
		matrice.append([])
		matrice[j].append(-j)
	return matrice,nouv_seq1,nouv_seq2
	
	
def affichage(matrice):
	for j in range(len(matrice)):
		ligne = ""
		for i in range(len(matrice[j])):
			ligne += str(matrice[j][i])+ "\t"
		print ligne

def score(seq1,seq2,matrice,i,j):
	list_score = []
	temp = matrice[j-1][i-1] + compare(seq1,seq2,0,1,i,j)# on pose 0 pour match et 1 pour mismatch 
	list_score.append(temp)
	temp = matrice[j][i-1] - 100 # theoriquement le gap est fixe a -inf
	list_score.append(temp)
	temp = matrice[j-1][i] - 100 # theoriquement le gap est fixe a -inf
	list_score.append(temp)
	return max(list_score)

def complete(aa1,aa2):
	matrice = initialisation(aa1,aa2)[0]
	seq1 = initialisation(aa1,aa2)[1]
	seq2 =initialisation(aa1,aa2)[2]
	for j in range(1,len(seq2)):
		for i in range(1,len(seq1)):
			result = score(seq1,seq2,matrice,i,j)
			matrice[j].append(result)
	#affichage(matrice)
	return matrice[len(aa1)][len(aa2)] # retourne le nombre suppose de mutations
	


#####################################################################################
#
#														 MAIN 
#
#####################################################################################
def main():
#	nb_gene = input("Combien de gènes doit contenir votre génome ?\n")
#	print("Les gènes n'ont pas tous la même longueur. Leur taille suit une distribution gaussienne")
#	mu = input("moyenne de la distribution :")
#	sigma = input("ecart-type :")
	
	mu = 1500
	sigma = 2
	nb_gene = 10
	
	#*********************Etude du génome que niveau des bases
	g = Gene(mu,sigma,"Test")
	#g.evolution_gene(10,10000)
	g.saturation_gene()
	#*********************Etude du génome au niveau des inversions
	#fichier2 = open("resultats_inversions","w")
	
	#genome = Genome(nb_gene,mu,sigma)
	#genome.DFS()
	#nb_inversion_obs = 0
	#for i in range(1000):
	#	nb_inversion_theo = genome.DFS()
	#	nb_inversion_obs += 1
	#	fichier2.write(str(i+1)+" "+str(nb_inversion_obs)+" "+str(nb_inversion_theo)+"\n")
		
	#fichier2.close()


#Nanoarchaeum equitans : taille du genome : 0,49Mpb  avec 536 gènes.
main()
