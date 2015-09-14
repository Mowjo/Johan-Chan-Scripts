####  Plusieurs variables qualitatives :

setwd('/home/jchan/Documents/Mathematiques/Statistique/Qualitatif/Exercice_5')



# Chargement des donnees

# entrer le separateur + header + separateur decimal
data = read.table('dure.txt',sep='\t',h=T,dec='.') 

# etude la dureté de l'eau et le nombre de décès sur plusieurs années.

# Traitement
ville = data$ville 
mort = data$mort 
durete = data$durete
geo = data$geo

# Representation :

plot(mort~durete,type='n')
points(mort~durete,subset=geo=='N',col='blue')
points(mort~durete,subset=geo=='S',col='red')

# Il semble y avoir une décroissance de mort en fonction de la dureté de l'eau

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#-- Modele basique
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

lm0=lm(mort~1)

summary(lm0)


#Coefficients:
#            Estimate Std. Error t value Pr(>|t|)    
#(Intercept)  1523.29      24.09   63.23   <2e-16 *** -> nombre moyen de morts


abline(h=coefficients(lm0))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#-- Modele 1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

lm1 = lm(mort~durete)

summary(lm1)

#Coefficients:
#             Estimate Std. Error t value Pr(>|t|)    
#(Intercept) 1670.3613    29.6628  56.312  < 2e-16 *** -> mortalité pour une dureté nulle
#durete        -3.1146     0.4896  -6.362 3.65e-08 *** il y a effet de la durete sur la mortalite


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#-- Modele 2
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

fgeo = as.factor(geo)
lm2 = lm(mort~fgeo)

summary(lm2)

#Coefficients:
#            Estimate Std. Error t value Pr(>|t|)    
#(Intercept)  1628.71      23.77  68.530  < 2e-16 *** -> mortalité prédite pour le nord
#fgeoS        -248.79      36.51  -6.814 6.49e-09 *** -> différence de mortalité entre Sud et Nord (significatif !)

plot(mort~durete,type='n')
points(mort~durete,subset=geo=='N',col='blue')
points(mort~durete,subset=geo=='S',col='red')
abline(h = 1628,col='yellow')
abline(h=1380,col='pink')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#-- Modele 3
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

lm3 = lm(mort~fgeo+durete)
# mu = b0 + b1*I[S] + b2*durete

summary(lm3)

#Coefficients:
#             Estimate Std. Error t value Pr(>|t|)    
#(Intercept) 1690.1797    25.8496  65.385  < 2e-16 *** -> 
#fgeoS       -172.0338    37.3655  -4.604 2.43e-05 *** -> b1 : différence de mortalite entre S et N à durete comparable (significatif)
#durete        -1.9906     0.4864  -4.092 0.000138 *** -> b2 : pente entre mortalite et durete à localisation geo comparable

# A durete comparable, il y a plus de mortalite au nord qu'au sud.

### Comparaison : entre modele 1 et 3 : si la localisation a un effet sur la durete
#   Comparaison : entre modele 2 et 3 :si la durete a un effet  sur la localisation

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#-- Modele 4 : Interacion
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


lm4 = lm(mort~fgeo*durete)
# mu = b0 + b1*I[S] + b2*durete + gamma*I[S]*durete

summary(lm4)

#Coefficients:
#              Estimate Std. Error t value Pr(>|t|)    
#(Intercept)  1685.2890    32.9582  51.134  < 2e-16 ***
#fgeoS        -160.9365    59.2759  -2.715  0.00884 ** -> diférence mortalite entre S et N quand durete nulle
#durete         -1.8322     0.8167  -2.243  0.02891 *  -> pente durete pour N
#fgeoS:durete   -0.2477     1.0215  -0.243  0.80927    -> gamma différence de pente de durete entre S et N (non significatif)

# A localisation géographique différente l'effet de la durete est le même. il n'y a donc pas d'interaction, on garde le modele 3
# Si on pose gamma = 0 on retombe sur le modele 3, ils sont donc emboités ( 3 & 4 )

### Comparaison :

anova(lm3,lm4)










