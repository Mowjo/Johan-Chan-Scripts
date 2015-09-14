####   Station2 : CORRIGER SUR MOODLE

setwd('/home/jchan/Documents/Mathematiques/Statistique/Qualitatif/Exercice_2')



# Chargement des donnees

# entrer le separateur + header + separateur decimal
data = read.table('station2.txt',sep='\t',h=T,dec='.') 

# Traitement
pollution = data$pollution
station = data$station


# Representation :
par(mfrow = c(1,3))
boxplot(pollution~station)
plot(as.numeric(station),pollution) # les donnees sont rangées en fonction de l'ordre alphabetique des station
levels(station) # donne l'ordre alphabetique des station .
coplot(pollution~station|rep(1,30))

	
###### Verification des hypothèses

# Homogénéité des variances

bartlett.test(pollution,station) # bartlett utilisé pour différents échantillons

# Résultat :  Test proche de 1 -> homogénéité des variances . 

# Test de normalité 

shapiro.test(pollution)

# Resultat :  Le test montre que les donnee sont gaussienne -> les residus le sont aussi !

# On considère que les variables sont controlés et indépendante . (a priori )

###### Regression lineaire qualitative ######

fstat = as.factor(station) # indique que cette variable est qualitative. 

# Creation du modele 

lm1 = lm(pollution~fstat) 

summary(lm1) # La station s4 est différente de la station s1 du fait que la différence de pollution entraine une p-value < 5% 

model.matrix(lm1) # affiche les matrices du modele 

contrasts(fstat) # 

#### Anova :

anova(lm1) # On obtient une p-value inférieur à 5% il y a donc différence entre les moyennes de pollution des stations. 

# Calcul manuel de la valeur de F :

(anova(lm1)[1,2]/3)/(anova(lm1)[2,2]/6)

# Calcul de la p-value :

1-pf((anova(lm1)[1,2]/3)/(anova(lm1)[2,2]/6),3,6)

#### Vérification des hypothèses (suite)

par(mfrow=c(2,2))

plot(lm1)

# Résidus perpendiculaire aux variables explicatrices : les résidus ne dépendent pas des variables (Residuals vs Fitted) 
# On a bien normalité ( Q-Q plot) et homogénéité des variances (Scale location).
# On a pas de valeurs abérrantes !

##### Changement de contraste : plus complexe

# On veut comparer la pollution des station 1 & 2 avec celle des stations 3-4 :



# première colonne séparer les groupes [1,1,-1,-1]
# identifier de manières unique les composants des groupe : [1,-1,0,0] et [0,0,1,-1]
# Attention : le produit scalaires des colonnes doit être null & la somme des valeurs d'une même colonne doit être nul !
# on obtient :

# 1 1 0      y1: b0 + b1 + b2
# 1 -1 0     y2: b0 + b1 - b2
# -1 0 1     y3: b0 - b1 + b3
# -1 0 -1    y4: b0 - b1 - b3

# On obtient alors : b0 = (y1+y2+y3+y4)/4
#					 b1	= (y1+y2-(y3+y4))/4
#                    b2 = (y1-y2)/2
#					 b3 = (y3-y4)/2

# Donc b1 nous permet de comparer ce qui nous intéresse !!



a =  contrasts(fstat)

a[1,1] = 1
a[2,1] = 1
a[3,1] = -1
a[4,1] = -1

a[1,2] = 1
a[2,2] = -1
a[3,2] = 0
a[4,2] = 0

a[1,3] = 0
a[2,3] = 0
a[3,3] = 1
a[4,3] = -1

fstat2 = fstat

contrasts(fstat2) = a

lm2 = lm(pollution~fstat2) 

summary(lm2) # le deuxième coefficient b1 est de 1.0893 qui n'est pas considérer comme étant différent de 0 par la p-value 
		     # Par contre le dernir coefficient b3 est considérer comme étant différent de 0 -> la station 3 et 4 sont différente !
		     
## Anova :

anova(lm2) # l'anova quelque soit le contraste ne change pas !


## Deuxième jeu de contraste :

# 1/3  1/2  1
# 1/3  1/2  -1
# 1/3  -1   0
# 1    0    0


# On regarde b1 = (3y4 - (y1+y2+y3))/4


