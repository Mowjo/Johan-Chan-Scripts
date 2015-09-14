####################################################
#
#             TEST DE POPULATION
#
####################################################

# Voir exercice 1 :
setwd('/home/jchan/Documents/4BIM/Statistique/Test-Non-paramétrique')

# Lecture des donnees :
data = read.table('Post-Opératoire.txt',sep='\t',h=T,dec='.') 

# Traitement des données :
A =  data$A
B = data$B
boxplot(data)

# Test de Normalité :

shapiro.test(A) # pas assez d'échanitillon pour tester la normalité

# On fait donc un test de Smirnov pour savoir si les deux echanitllon suivent la même loi (cf poly page 58)

ks.test(A,B)

#  Two-sample Kolmogorov-Smirnov test

#data:  A and B
#D = 0.625, p-value = 0.08702
#alternative hypothesis: two-sided

# On a 8/100 chance d'observé cette distribution on accepte H0 :  même loi de distribution. 


# Etant donné que l'on ne connait pas la distribution nous devons choisir un test qui non paramétrique qui permet de savoir si il y a oui on non une différence entre ces 2 drogues.

### Test des Signes :

# On considère que le même individu a pris les même drogues successivement. Test décris dans le poly !!
# On utilise la loi binomiale !

### Test des Rangs Signés : de Wilcoxon (voir poly)

wilcox.test(A,B,paired = T)

### Test de dispersion :

# mood.test
# ansari.test
# fligner.test

### Test de variance :

# bartlett.test
# hartley.test
# var.test







####################################################
#
#       Comparaison des tendances centrales
#            
####################################################

med = median(A,B) # = 4.6

table(B<med)

FALSE  TRUE 
2     6 

table(A<med)

FALSE  TRUE 
4     4

# Test EXACT de fisher :

fisher.test(matrix(c(4,4,2,6),2,2)) 

#p-value = 0.6084
#alternative hypothesis: true odds ratio is not equal to 1
#95 percent confidence interval:
#  0.2485664 45.7630284
#sample estimates:
#odds ratio 
#   2.79346 

# P-value = 0.6 :  imposssible de dire si la distribution est différentes pour chacune des drogues.


# Test de la somme des Rangs : SR

wilcox.test(A,B)

#	Wilcoxon rank sum test

#data:  A and B
#W = 49, p-value = 0.08298
#alternative hypothesis: true location shift is not equal to 0

# IMPORTANT : plus performant que celui du test de la médiane puisque il écrase la distribution. 
# Dans le cas de K-moyenne on n'utilise pas l'ANOVA dans le cas non-paramétrique mais le test de Kruskal-Wallis. 