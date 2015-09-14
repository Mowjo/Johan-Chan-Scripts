library(ade4)
library(xtable)
library(meaudret)
data(meaudret)


# Représentation des données :

names(meaudret$env)


summary(meaudret$plan$sta)


# Création de l'ACP :

acp1 = dudi.pca(meaudret$env) # on en garde 3

summary(acp1)

#Total inertia: 9

#Eigenvalues:
#    Ax1     Ax2     Ax3     Ax4     Ax5 
# 5.1747  1.3204  1.0934  0.7321  0.4902 

#Projected inertia (%):
#    Ax1     Ax2     Ax3     Ax4     Ax5 
# 57.497  14.671  12.149   8.135   5.447 

#Cumulative projected inertia (%):
#    Ax1   Ax1:2   Ax1:3   Ax1:4   Ax1:5 
#  57.50   72.17   84.32   92.45   97.90 


#WARNING : AFC (=analyse des correspondances) met en évidences les évènements rares !


s.corcircle(acp1$co)
#axe1 : opposition au pH et au variables contaminante de l'eau
#ax2 : corrélé positivement au nitrate

s.label(acptot$li)
# station 2 en été et automne tire l'axe 1
# station  3 et 4 tire l'axe 2

	### Etude de la variabilité temporel : saison


# ACP intra :

acp_intra = wca(acp1,meaudret$design$season) # on en conserve 2

names(acp_intra)

[1] "tab"   "cw"    "lw"    "eig"   "rank"  "nf"    "c1"    "li"    "co"   
[10] "l1"    "call"  "ratio" "ls"    "as"    "tabw"  "fac"  

acp_intra$ratio # 63% de la strucutre total du tableau est contenu dans ce résidu (et donc pas dans saison) -> ce que nous allons analysé ici est donc 63% de la variabilité totale.

plot(acp_intra)
# dans le graphe "canonical weights" on remarque que la température  de l'eau n'intervient pas ce qui est normal puisque nous avons retiré l'effet des saisons. 
# "scores and classes" représentation de $ls
# "common centring" représentation de $library

par(mfrow=c(1,2))
s.class(acp1$li,meaudret$design$season)
s.class(acp_intra$ls,meaudret$design$season)

# En projection sur l'axe 1 on a les mêmes résultats. 
# Mais nous avons perdu la variabilité sur l'axe 2  en retirant l'effet saison (notament via l'automne)

par(mfrow=c(1,2))
s.label(acp1$li)
s.class(acp1$li,meaudret$design$season)

# ACP inter :

acp_inter = bca(acp1,meaudret$design$season)

acp_inter$ratio
[1] 0.3722686


plot(acp_inter)

		### Etude de la variabilité spatiale : sites
	
names(meaudret$env)

# ACP inter 

acpb_inter = bca(acp1,meaudret$design$site) # on conserve 2 axes

summary(acpb_inter)

Total inertia: 3.425

Eigenvalues:
     Ax1      Ax2      Ax3      Ax4 
2.681164 0.620768 0.113169 0.009503 

Projected inertia (%):
    Ax1     Ax2     Ax3     Ax4 
78.2912 18.1267  3.3046  0.2775 

Cumulative projected inertia (%):
    Ax1   Ax1:2   Ax1:3   Ax1:4 
  78.29   96.42   99.72  100.00 

acpb_inter$ratio
[1] 0.3805115

plot(acpb_inter) 
# on obsverve que le site 2 est celui qui possède le plus de variabilité
# la station 1 n'est pas sur le même affluent géographiquement.

acpb_intra = wca(acp1,meaudret$design$sites)

acpb_intra$ratio
[1] 0.6194885

plot(acpb_intra)
