############################################
#
#             Exercice 9 :  Kruskal-Wallis
#
############################################

setwd("~/4BiM/Statistique/Test_Non_parametrique")

# Lecture des donnees :
data = read.table('Ex9_rats.txt',sep='\t',h=T,dec='.') 

# Traitement des données :
poids =  data$�..poids
milieu = data$milieu

# Test de K-moyenne :

kruskal.test(poids,milieu)

#	 Kruskal-Wallis rank sum test

#data:  poids and milieu
#Kruskal-Wallis chi-squared = 3.8498, df = 3, p-value = 0.2782


####################################################
#
#     Exercice 8 :  Multi-géométrique (Spearman)
#
####################################################

# Lecture des donnees :
data2 = read.table('Ex8_cafe.txt',sep='\t',h=T,dec='.') 

# Traitement des données :
gouteur =  data2$Gouteur
essence = data2$Essence
note = data2$Note

# Représentation :

plot(essence,note)

# Test de K-moyenne :

kruskal.test(note,essence)

#	Kruskal-Wallis rank sum test

#data:  note and essence
#Kruskal-Wallis chi-squared = 11.6194, df = 3, p-value = 0.008807

# On a un effet café selon le test (p-value = 0.009)

# Mais pourtant ce n'est pas tout a fait ça puisque l'on a pas inclu l'interaction gouteur. Or il n'y a pas de répétition on ne peut donc pas tester la répétition.
# mais on sait que c'est le même gouteur tout le long, les données ne sont donc pas indépendantes !!

# Nous sommes donc dans un cas de répartition multi-géométrique : 
# -> test de permutation :  test de Spearman (cf page 74)




