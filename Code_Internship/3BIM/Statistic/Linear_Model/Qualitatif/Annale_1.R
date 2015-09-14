####  Plusieurs variables qualitatives :

setwd('/home/jchan/Documents/Mathematiques/Statistique')



# Chargement des donnees

# entrer le separateur + header + separateur decimal
data = read.table('qlqc30.txt',sep='\t',h=T,dec='.') 



# Traitement
patient = data$patient 
qol = data$qol # qualité de vie 
questionaire = data$questionnaire
traitement = data$traitement

# Representation :

boxplot(qol~questionaire,qt = c(1,4,2,3))
coplot(qol~questionaire|traitement)
interaction.plot(questionaire,traitement,qol) # il n'y aurait pas d'interaction entre les varaibles qualitatives questionaire et traitement.



####################################################
#
# Modèle le moins contraint  =  modele avec inter
#
####################################################

fquestionaire = as.factor(questionaire)
ftraitement = as.factor(traitement)

lm1 = lm(qol~ftraitement*fquestionaire)

summary(lm1)

#Coefficients:
#                                Estimate Std. Error t value Pr(>|t|)    
#(Intercept)                      82.3636     1.5391  53.514  < 2e-16 *** 
#ftraitementct-                  -21.7321     1.9340 -11.237  < 2e-16 ***
#fquestionaireQ12                  2.8182     2.1766   1.295  0.19807     # différence entre Q12 et Q0 avec chimio
#fquestionaireQ3                   5.2727     2.1766   2.422  0.01702 *  
#fquestionaireQ6                   5.8182     2.1766   2.673  0.00864 ** 
#ftraitementct-:fquestionaireQ12  -0.6603     2.7350  -0.241  0.80967      # différence entre chimio et pas chimio au temps Q12
#ftraitementct-:fquestionaireQ3   -0.7990     2.7350  -0.292  0.77071   
#ftraitementct-:fquestionaireQ6   -0.8708     2.7350  -0.318  0.75078    

####################################################
#
# Modèle le moins contraint  =  modele sans inter
#
####################################################


lm2 = lm(qol~ftraitement+fquestionaire)

summary(lm2)


#Coefficients:
#                 Estimate Std. Error t value Pr(>|t|)    
#(Intercept)       82.7326     1.1012  75.132  < 2e-16 *** # valeur prédite et non la moyenne.
#ftraitementct-   -22.3146     0.9548 -23.370  < 2e-16 *** # différence entre chimio et non.
#fquestionaireQ12   2.4000     1.3014   1.844 0.067739 .   # différence entre Q12 et Q0 à traitement comparable.
#fquestionaireQ3    4.7667     1.3014   3.663 0.000379 *** 
#fquestionaireQ6    5.2667     1.3014   4.047 9.44e-05 ***


anova(lm(residuals(lm2) ~ fquestionaire:ftraitement))


#Response: residuals(lm2)
#                           Df  Sum Sq Mean Sq F value Pr(>F)
#fquestionaire:ftraitement   7    3.31  0.4731  0.0182      1 # p-value de 1 donc il n'y a pas d'interaction significative.
#Residuals                 112 2918.36 26.0568        

# test si il y a une interaction sur les résidus du modèle 2 -> permet de savoir si il y a bien interaction.       


plot((residuals(lm2))) # les mesures pour un même patient ne sont pas indépendantes les unes des autres !!!! Le modèle n'est pas valide.
