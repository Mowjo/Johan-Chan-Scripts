##### Pression artérielle systolique 

setwd('/home/jchan/Documents/Mathématiques/Statistique/Exercice_4')

# Objectif  : déterminer l'impact de chacun des facteurs sur le modele ! 


# Chargement des donnees

# entrer le separateur + header + separateur decimal

data = read.table('pas.txt',sep='\t',h=T,dec='.') 


# Traitement
pas = data$pas
age = data$age
ttaille = data$ttaille
bmi = data$bmi



# Representation graphique 

par(mfrow = c(1,3))
boxplot(age)
boxplot(ttaille)
boxplot(bmi)

pairs(cbind.data.frame(pas,age,ttaille,bmi)) # on ne peut rien en conclure


### Construction des modele univariés

# Construction du modèle age :


modele_age = lm(pas~age)

age_p = predict(modele_age)

age_res = residuals(modele_age)

summary(modele_age)

cor.test(pas,age)

# on a une p_value de 0.007 < alpha , le facteur age a un effet : augmente la pression systolique

# Construction du modèle age :


modele_ttaille = lm(pas~ttaille)

ttaille_p = predict(modele_ttaille)

ttaille_res = residuals(modele_ttaille)

summary(modele_ttaille)

cor.test(pas,ttaille)

# on a une p_value de 0.024 < alpha , le facteur tour de taille a un effet : augmente la pression arterielle systolique

# Construction du modèle age :


modele_bmi = lm(pas~bmi)

bmi_p = predict(modele_bmi)

bmi_res = residuals(modele_bmi)

summary(modele_bmi)

cor.test(pas,bmi)

# on a une p_value de 0.078 > alpha , le facteur bmi n'a apparement pas d'effet sur la presion systolique mais on est a la limite d'alpha donc on garde un droit de réserve !


### Construction du modele multivariée

modele_1 = lm(pas~age+ttaille+bmi)

summary(modele_1)

# on remarque que chacun des facteurs ont tendance à faire augementer la pressios systolique 

# Pour l'age, on constate qu'il y a effet sur la pression systolique :
# Exemple : à bmi et tour de taille constant , lorsque l'age augmente d'1 , la pression systolique augmente de 0.52

# On constate qu'il n'y a pas d'effet du tour de taille et de la bmi à niveau constant . 

# On constatait que le tour de taille avait un effet dans le modele univarié car le tour de taille augementait avec l'age ( qui lui a u effet)


# Analyse de la variance :

anova(modele_1)

# la Sum Sq montre la variabilité engendré par le facteur concerné 

### Construction du modele age+bmi+ttaille :

modele_2 = lm(pas~age+bmi+ttaille)

summary(modele_2) #aucune difference avec le modele_1

# ANOVA

anova(modele_2)

# Analyse de la variance est modifié : du a la correlation des variables explicatrices
# La variabilité exprimé par le deuxieme facteur est calculé avec celle restante 

### Modele simplifié

# d'apres les cardiologues , la bmi n'influerait pas sur la pression systolique

modele_s = lm(pas~age+ttaille)

summary(modele_s) 

# Augmentation de pas statistiquement significative de l'age lorsque le ttaille ne varie pas
# Augmentation de pas statistiquement significative du ttaille lorsque l'age ne varie pas

anova(modele_s)
# DDL des résidus N-3 !


### Conclusion : le modele simplifié est choisi :

# - d'un point de vue biologique plus logique

SCE_r1 = 118.97
SCE_r2 = 116.02

anova(modele_1,modele_s) # commande qui permet de comparer les modele

# On a F = 0.1588 et la p_value = 0.6928 > alpha , donc les deux modeles explique tout deux aussi bien la pas 
# d'apres le ppe de parcimonie on choisit donc le modele simplifié !

