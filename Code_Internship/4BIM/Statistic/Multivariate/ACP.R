############################################
#
#   Analyse des données : Situation A
#
############################################


setwd('/home/jchan/Documents/4BIM/Analyse_donnees')

# Chargement des données :

library(ade4)
data(doubs)

# Détermination de doubs : le doubs est une rivière qui se jette dans le Rhônes. 

class(doubs)

# [1] "list"


names(doubs)

# [1] "env"     "fish"    "xy"      "species"

head(doubs$env)

 dfs alt   slo flo pH har pho nit amm oxy bdo
1   3 934 6.176  84 79  45   1  20   0 122  27
2  22 932 3.434 100 80  40   2  20  10 103  19
3 102 914 3.638 180 83  52   5  22   5 105  35
4 185 854 3.497 253 80  72  10  21   0 110  13
5 215 849 3.178 264 81  84  38  52  20  80  62
6 324 846 3.497 286 79  60  20  15   0 102  53

head(doubs$fish)

Cogo Satr Phph Neba Thth Teso Chna Chto Lele Lece Baba Spbi Gogo Eslu Pefl
1    0    3    0    0    0    0    0    0    0    0    0    0    0    0    0
2    0    5    4    3    0    0    0    0    0    0    0    0    0    0    0
3    0    5    5    5    0    0    0    0    0    0    0    0    0    1    0
4    0    4    5    5    0    0    0    0    0    1    0    0    1    2    2
5    0    2    3    2    0    0    0    0    5    2    0    0    2    4    4
6    0    3    4    5    0    0    0    0    1    2    0    0    1    1    1
  Rham Legi Scer Cyca Titi Abbr Icme Acce Ruru Blbj Alal Anan
1    0    0    0    0    0    0    0    0    0    0    0    0
2    0    0    0    0    0    0    0    0    0    0    0    0
3    0    0    0    0    0    0    0    0    0    0    0    0
4    0    0    0    0    1    0    0    0    0    0    0    0
5    0    0    2    0    3    0    0    0    5    0    0    0
6    0    0    0    0    2    0    0    0    1    0    0    0

head(doubs$xy)

 x  y
1  88  7
2  94 14
3 102 18
4 100 28
5 106 39
6 112 51

head(doubs$species) 


                Scientific        French           English code
1             Cottus gobio        chabot european bullhead Cogo
2       Salmo trutta fario  truite fario       brown trout Satr
3        Phoxinus phoxinus        vairon            minnow Phph
4   Nemacheilus barbatulus loche franche       stone loach Neba
5      Thymallus thymallus         ombre          grayling Thth
6 Telestes soufia agassizi       blageon           blageon Teso

# Représentation des données :

plot(doubs$xy,type='l',col='blue',lwd=4) # affichage du trajet de la rivière

# Analyse univariée : on choisira la variable amoniac.

names(doubs$env) # amoniac est la 9è variable

[1] "dfs" "alt" "slo" "flo" "pH"  "har" "pho" "nit" "amm" "oxy" "bdo"

s.value(doubs$xy,doubs$env[,9],add.plot=T) # on place la variable brut sur la représentation  géographique de la rivière. 

s.value(doubs$xy,scale(doubs$env[,9],center=T,scale=F),add.plot=T) # même représentation mais en ayant centré les valeurs de l'amoniac. 


	### ACP :


acp1 = dudi.pca(doubs$env,center=T,scale=T)
# on ne réduit pas forcément mais on centre toujours. 
#  a nous de choisir le nombre d'axes concernés : mais de pas prendre tout les axes car sinon l'ACP est inutile. Ou sinon ne pas prendre les "petits" axes puisque suerment du résidus. 
# somme des variances = somme des valeurs propres (=11) car variables réduites donc variance de 1 pour chaque axes. 

# On choisit 2 axes uniquement :
s.label(acp1$li,xax=1,yax=2)
# Axe horizontale = axe de plus grande variances
# centre est le centre de gravité du nuage de points. 
# On ne sait pas pourquoi la station 25 génère de la variabilité 
# WARNING: les axes sont caractériser par les mêmes variables du cercle de corrélation selon leurs places dans le cercle ( attention au signe de la corrélation)
# On interprète jamais ce qui est au centre du gaphique. 

# Représentation des coordonnées des variables (corrélation) :

s.corcircle(acp1$co)
#axe1 : horizontale axe2 : verticale

	# AXE 1 :
# On projette chacun des points orthogonalement sur l'axe 1 et plus les variables sont proche de 1 ou -1 et plus elle contribuent à définir l'axe 1.
# Pas de 0.2 par case. 
# En projettant toute les variables sur l'axe 1 on observe un "paquet" au niveau de 0.8. Toute ces variables sont corrélé positivement , càd dans le cas de (dfs,nit) le nuage de point suivra la forme : nit  = b0 + b1*dfs. 
# L'axe 1 es donc l'axe de Pollution : plus on s'éloigne de la source (dfs) plus on aura de pollution.
	# AXE 2 :
# Les corrélation sur le second axe sont plus faibles

scatter(acp1)
# on obtient un biplot. Affiche le graphe des valeurs propres.
# code couleur : noir (axe représenté) gris (axes retenus mais non représenté) blancs (axes non représenté)

scatter(acp1,posieig="none") # pour retirer le biplot.

	### Avec 3 axes :

acp1 = dudi.pca(doubs$env,center=T,scale=T) # 3 axes choisis

scatter(acp1,xax=1,yax=2) # on choisit les axes représenté
s.corcircle(acp1$co,xax=1,yax=3) # l'axe 3 est en position verticale
# l'axe 3 ne fait que représenté le pH.

s.label(acp1$li,xax=1,yax=3) 
# on remarque que la station 15 a un pH élevé et la station 10 et 29 qui ont un pH faible. 


	# Représentation spatial des axe :
	

# Axe de plus grande variance, l'axe (1) Pollution :
s.value(doubs$xy,acp1$li[,1]) 
# On sait qu'il y a une fabrique de papier au niveau de forte pollution. 

# On va maintenant representer spatiallement le pH et l'axe 3 qui représente globalement le pH :

par(mfrow=c(1,2))

s.value(doubs$xy,scale(doubs$env[,5]))
s.value(doubs$xy,acp1$li[,3])
# On observe bien la corrélation négative du pH sur l'axe 3. 

names(acp1)
[1] "tab"  "cw"   "lw"   "eig"  "rank" "nf"   "c1"   "li"   "co"   "l1"  
[11] "call" "cent" "norm"

sapply(acp1$tab,mean)
 dfs           alt           slo           flo            pH 
 1.768695e-17 -3.397167e-19 -4.054916e-18  4.815303e-17 -1.853986e-18 
          har           pho           nit           amm           oxy 
 3.518091e-16  1.022493e-17 -4.040325e-17 -5.505940e-18  3.977811e-16 
          bdo 
 6.893267e-17
 
sapply(acp1$tab,var)*29/30 

dfs alt slo flo  pH har pho nit amm oxy bdo 
  1   1   1   1   1   1   1   1   1   1   1

acp1$cw # pondération des colonnes (Q = Ip)
[1] 1 1 1 1 1 1 1 1 1 1 1


acp1$lw # pondération des individus ( 1/30 = 1/n )
[1] 0.03333333 0.03333333 0.03333333 0.03333333 0.03333333 0.03333333
 [7] 0.03333333 0.03333333 0.03333333 0.03333333 0.03333333 0.03333333
[13] 0.03333333 0.03333333 0.03333333 0.03333333 0.03333333 0.03333333
[19] 0.03333333 0.03333333 0.03333333 0.03333333 0.03333333 0.03333333
[25] 0.03333333 0.03333333 0.03333333 0.03333333 0.03333333 0.03333333

acp1$co
 		Comp1      Comp2        Comp3
dfs  0.87335029 -0.3963445  0.163535199
alt -0.83905354  0.4537709 -0.129918288
slo -0.76020468  0.4145874  0.213039798
flo  0.77776175 -0.5037445  0.191181947
pH  -0.02457895 -0.3756069 -0.913313669 # forte corrélation avec 3
har  0.71229727 -0.4011204  0.033804286
pho  0.81110560  0.5033806 -0.136962677
nit  0.90154907  0.1066847 -0.011284133
amm  0.76710859  0.5785809 -0.127177507
oxy -0.74899491 -0.4280275 -0.001215206
bdo  0.73752596  0.5985336 -0.091096305

acp1$c1

		CS1         CS2         CS3
dfs  0.347355464 -0.26531698  0.16319254
alt -0.333714700  0.30375881 -0.12964607
slo -0.302354337  0.27752900  0.21259341
flo  0.309337268 -0.33721162  0.19078136
pH  -0.009775726 -0.25143506 -0.91139999
har  0.283300241 -0.26851403  0.03373345
pho  0.322599037  0.33696800 -0.13667570
nit  0.358570895  0.07141578 -0.01126049
amm  0.305100215  0.38730786 -0.12691103
oxy -0.297895906 -0.28652591 -0.00121266
bdo  0.293334385  0.40066440 -0.09090543

acp1$li[1,1] # <X_etoile/U>
[1] -4.400946

