############################################
#
#     Exercice 2 : modèle aléatoire
#
############################################

# On souhaite tester l'homogénéité des mesures établie par différent technicien utilisant plusieurs appareil. Le but est de savoir si il existe un effet technicien et/ou appareil. 


# On est dans un modèle de type aléatoire puisque c'est 3 technicien testé parmi beaucoup. 

setwd('/home/jchan/Documents/4BIM/Statistique')

# Lecture des donnees :
data = read.table('TECHAPPA.txt',sep='\t',h=T,dec='.') 

# Traitement des données :

technicien = data$Technicien
appareil = data$Appareil
mesure = data$mesure

# Représentation

coplot(mesure~technicien|appareil,rows=1)

# On a l'impression qu'il n'y a pas vraiment d'effet de variance. 

		#### Création du modèle :

	# Modèle avec interaction.

ftechnicien = as.factor(technicien)
fappareil = as.factor(appareil)

lm1 = lm(mesure~ftechnicien*fappareil)

# Analyse du modèle 

summary(lm1)

#Coefficients:
                                 Estimate Std. Error t value Pr(>|t|)    
#(Intercept)                       4.67333    0.31919  14.641 1.93e-11 ***
#ftechnicienEvelyne               -0.44000    0.45141  -0.975    0.343    
#ftechnicienFrancoise             -0.63000    0.45141  -1.396    0.180    
#fappareilA2                      -0.10333    0.45141  -0.229    0.822    
#fappareilA3                       0.05333    0.45141   0.118    0.907    
#ftechnicienEvelyne:fappareilA2    0.03000    0.63839   0.047    0.963    
#ftechnicienFrancoise:fappareilA2  0.60000    0.63839   0.940    0.360    
#ftechnicienEvelyne:fappareilA3    0.18667    0.63839   0.292    0.773    
#ftechnicienFrancoise:fappareilA3 -0.16667    0.63839  -0.261    0.797 


anova(lm1)

#						Df Sum Sq Mean Sq F value Pr(>F)
#ftechnicien            2 1.1547 0.57734  1.8889 0.1800
#fappareil              2 0.0515 0.02573  0.0842 0.9196
#ftechnicien:fappareil  4 0.7794 0.19484  0.6375 0.6424
#Residuals             18 5.5017 0.30565  

# On une p-value de 0.6424 > 0.05 on a donc pas d'interaction.

# WARNING ! : on ne regarde pas les p-values principales parce qu'elles sont fausses dans le modèle aléatoires avec interaction ! Il faut créer  un modèle SANS INTERACTION !

# Modèle sansd interaction :

ana1 = aov(mesure~appareil+technicien+Error(appareil:technicien))
# On créé le modèle non pas par rapport au résiduel mais par rapport à l'interaction.

summary(ana1)

#           Df Sum Sq Mean Sq F value Pr(>F)
#appareil    2 0.0515  0.0257   0.132  0.880
#technicien  2 1.1547  0.5773   2.963  0.162
#Residuals   4 0.7794  0.1948  

# On observe pas d'effet significatif des facteurs techniciens et appareils. 

	### Estimation de sigma technicien et appareil :
	


	### Hypothèse :
	
bartlett.test(mesure,technicien:appareil)

#	Bartlett test of homogeneity of variances

#data:  mesure and technicien:appareil
#Bartlett's K-squared = 3.9881, df = 8, p-value = 0.8582

interaction.plot(technicien,appareil,mesure,col=1.2) 
# Il semble y avoir 
