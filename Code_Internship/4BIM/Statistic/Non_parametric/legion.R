############################################
#
#        Test de Population 
#
############################################

librabry(nortest)

# Cette distribution suit-elle une loi normale

setwd('/home/jchan/Documents/4BIM/Statistique')

# Lecture des donnees :
data = read.table('legion.txt',sep='\t',h=T,dec='.') 

# Traitement des données :

mesure =  data$mesures
freq = data$frequences
mes=rep(mesure,freq)

# Représentation :

qqnorm(mes)
qqplo(quantile(mesure),qnorm(....
abline(0.1) # première bissectrice

# Test de normalité

shapiro.test(mes) # la taille de l'échantillon est trop grande. 

# Fonction de répartition théorique :

ecdf(mes)

#Empirical CDF 
#Call: ecdf(mes)
#x[1:16] =     33,     34,     35,  ...,     47,     48

# Test non paramétrique de Smirnov :

m = mean(mes)
sd = sd(mes)
pnorm(33,m,sd) # préparation du test du chi²

ks.test("pnorm",m,sd)
lillie.test
