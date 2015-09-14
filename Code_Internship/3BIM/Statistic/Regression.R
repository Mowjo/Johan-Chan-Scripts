
#### Modele de Baranyi :


setwd('/home/jchan/Documents/Mathematiques/Regression')
library(nlstools)



###### Chargement des donnees #######
    
    # entrer le separateur + header + separateur decimal

data = read.table('lm76t8.txt',sep='\t',h = T,dec='.') 


# Traitement
t = data$t
y = data$ylog10
donnee = rbind(t,y)

# Définitions des paramètres :

ymax = 9 # a peu près
y0 = 6
lag = 50 # a peu près
mu = 0.1

# Representation graphique 

par(mfrow=c(1,3))
plot(t,y,xlab='Temps',ylab='y=log(N)') 
boxplot(y)
hist(y)

### Modele de Baranyi : #####


modele1 = ylog10~ymax+log10((-1+exp(mu*lag)+exp(mu*t))/(exp(mu*t)-1+exp(mu*lag)*10^(ymax-y0))) # on entre le modèle


nls1 = nls(modele1,data=data,start=list(ymax=9,mu=0.1,lag=50,y0=6)) # va créer le modele entré auparavant
 
par(mfrow=c(1,2))
preview(modele1,data,list(ymax=9,mu=0.1,lag=50,y0=6)) # donne un aperçu
plotfit(nls1,smooth=T) # plot le modele . 

# Etude du modele

summary(nls1) # permet d'obtenir la valeur des paramètres de la modélisation

overview(nls1) # donne le résumé de l'ensemble de la modélisation

# Etude des parametres , intervalle de confiance

region1=nlsConfRegions(nls1)
par(mfrow=c(1,2))
plot(region1,bounds = TRUE) # trace les région de confiances de nos paramètres pris 2 à 2 -> vérifier qu'elles sont élliptiques
plot(fitted(nls1),residuals(nls1),ylim=c(-0.5,0.5))

# test la normalité des résidus

shapiro.test(residuals(nls1)) # facultatif voir la suite


res1 = nlsResiduals(nls1) # on définit les résidus ( écart prédiction-observation)
plot(res1) # plot différent graphe pour étudier les résidus

test.nlsResiduals(res1) # permet de vérifier la normalité des résidus en fonction des paramètre estimé par la modélisation , Run test vérifie si il y a corrélation ou non entre les résidus . 

##### Modele de Kono ######

modele2 = ylog10~(t<=lag)*y0+(t>lag)*(ymax-log10(1+(10^(ymax-y0)-1)*exp(-mu*(t-lag)))) # on entre le modèle

nls2 = nls(modele2,data=data,start=list(ymax=9,mu=0.1,lag=50,y0=6)) # va créer le modele entré auparavant
 
par(mfrow=c(1,2))
preview(modele2,data,list(ymax=9,mu=0.1,lag=50,y0=6)) # donne un aperçu
plotfit(nls2,smooth=T) # plot le modele . 

# Etude du modele

summary(nls2) # permet d'obtenir la valeur des paramètres de la modélisation

overview(nls2) # donne le résumé de l'ensemble de la modélisation

# Etude des parametres , intervalle de confiance

region1=nlsConfRegions(nls2)
par(mfrow=c(1,2))
plot(region1,bounds = TRUE) # trace les région de confiances de nos paramètres pris 2 à 2 -> vérifier qu'elles sont élliptiques
plot(fitted(nls2),residuals(nls2),ylim=c(-0.5,0.5))


# test la normalité des résidus

shapiro.test(residuals(nls2)) # facultatif voir la suite


res2 = nlsResiduals(nls2) # on définit les résidus ( écart prédiction-observation)
plot(res2) # plot différent graphe pour étudier les résidus

test.nlsResiduals(res2) # permet de vérifier la normalité des résidus en fonction des paramètre estimé par la modélisation , Run test vérifie si il y a corrélation ou non entre les résidus . 

##### Test des modeles emboités


anova(nls1,nls2) # il nous sort que les 2 modèles ne sont pas ajustable . 

# on choisit donc le modèle le plus parcimonieux  , ici le modele 1 

# Critère AIC

AIC(nls1) # -39
AIC(nls2) # -24 -> on choisist le modele 1 .

# on choisit le modele avec un critère AIC le plus bas . Basé sur le log de la vraisemblance . 

