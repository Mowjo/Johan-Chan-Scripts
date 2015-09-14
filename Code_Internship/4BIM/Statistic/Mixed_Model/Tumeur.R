############################################
#
#     Exercice 2 : modèle mixte
#
############################################

# On veut étudier comparativement l'infuence de 3 traitements sur le developpement d'une tumeur greffee et de ses metastases.
# On dispose pour cela de 15 animaux. Le critere de jugement choisi est le poids de la tumeur et des metastases apres 2 mois de traitement.

# Remarque : - Les resultats (en g) sont dans le fichier tumeur.dat
#			 - l'effet bloc est un effet ALEATOIRE corrollaire. 



setwd('/home/jchan/Documents/4BIM/Statistique')

# Lecture des donnees :
data = read.table('tumeur.txt',sep='\t',h=T,dec='.') 

# Traitement des données :

traitement = data$traitement
bloc = data$bloc
poids = data$poids

# Représentation

stripchart(poids~traitement)

plot(poids~traitement)

coplot(poids~traitement|bloc,rows=1)

	### Etude de l'interacion : 

xtabs(~traitement+bloc)

#			bloc
#traitement 1 2 3 4 5
#        t1 1 1 1 1 1
#        t2 1 1 1 1 1
#        t3 1 1 1 1 1

# On n'a pas de répétition, il est donc impossible d'étudier l'interaction par un modele linéaire !

# On va donc essayer de représenter les données pour essayer d'observer une interaction traitement-bloc :

require(lattice)
print(stripplot(poids~traitement,col=as.numeric(bloc),pch=as.numeric(bloc)))

# On remarque qu'il y a un bloc qui donne des mesure plus grandes !
# Autre solution :

interaction.plot(traitement,bloc,poids)

# On suppose une interaction bien qu'on ne puisse pas la quantifier !
	
	#### Création du modèle :
	

ftraitement = as.factor(traitement)
fbloc = as.factor(bloc)

lm1 = lm(poids~ftraitement+fbloc)

# Analyse du modèle 

anova(lm1)

#	Analysis of Variance Table

#Response: poids
#            Df  Sum Sq  Mean Sq F value  Pr(>F)  
#ftraitement  2 0.31996 0.159980  4.6817 0.04506 *
#fbloc        4 0.42843 0.107107  3.1344 0.07924 .
#Residuals    8 0.27337 0.034172      

# Effet fixe : on a une p-value de 0.04 donc il y a un effet traitement significatif.
# Effet aléatoire : 0.08 non significatif. Pas d'effet bloc.  


		#### Hypothèses :

bartlett.test(poids,traitement)

#Bartlett test of homogeneity of variances

#data:  poids and traitement
#Bartlett's K-squared = 1.2876, df = 2, p-value = 0.5253

