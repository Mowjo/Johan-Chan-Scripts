############################################
#
#     Exercice 1 : modèle fixe
#
############################################

#Le tableau de donnees du fichier PDSSOURI.dat repertorie les poids a 6 semaines de souris femelles issues de differentes portees issues de 18 femelles qui ont ete croisees avec 6 males differents (a raison de 3 femelles par male).

# Deux souris femelles ont ensuite ete tirees au sort par portee et pesees. On voudrait savoir si dans ce groupe les poids des femelles a 6 mois different de facon signicative d'une mere a l'autre et d'un pere a l'autre

# Remarque : - Effet mâle : FIXE. pour le percevoir il faudrait que l'efffet mâle soit supérieur à celui des femelles !
#			 - Pour tester l'effet femelle on le teste par rapport à la résiduelle.  

setwd('/home/jchan/Documents/4BIM/Statistique')

# Lecture des donnees :
data = read.table('pdsouris.txt',sep='\t',h=T,dec='.') 

# Traitement des données :

pere = data$pere
mere = data$mere
poids = data$poids

# Représentation

coplot(poids~pere|mere,rows=1)

	#### Création du modèle :

# Modèle avec interaction.

fpere = as.factor(pere)
fmere = as.factor(mere)

# On veut tester l'effet de la mere :

lm1 = lm(poids~pere+mere)

#Analysis of Variance Table

#Response: poids
#          Df  Sum Sq Mean Sq F value  Pr(>F)  
#pere       5  53.141 10.6283  2.8684 0.03184 *
#mere       1  13.954 13.9537  3.7659 0.06209 .
#Residuals 29 107.455  3.7053       

# On veut tester l'effet du pere :

a1 = aov(poids~pere+Error(mere))

#Error: mere
#     Df Sum Sq Mean Sq
#pere  1  38.82   38.82

#Error: Within
#          Df Sum Sq Mean Sq F value Pr(>F)
#pere       5  28.28   5.655   1.526  0.213
#Residuals 29 107.45   3.705    
