#############################################################
#
#                 TD 2 :
#
############################################################

setwd('/home/jchan/Documents/4BIM/GLM/Regression_Logistique')

#Traitement des données
data= read.table("ILLE.txt",h=T)

data$malade[data$malade==2]=0
data$malade=as.factor(data$malade)
levels(data$malade) = c("Temoin","Cas")
data$alcbin<-ifelse(data$alcool<3,0,1)
table(data$alcbin)


	#modele lié à l'alcool

modele = glm(malade~alcbin,data=data,family=binomial())
summary(modele)

#beta1 = 1.73 (cf summary)
OR1 = exp(1.73)#OR = 5.64

# intervalle de  confiance
IC_OR1 = exp(1.7299+1.96*0.1752)#7.95
IC2_OR1 =exp(1.7299-1.96*0.1752)#4.00

# 1 exclu de l'IC effet significatif, effet deletere car OR>1
#une personne qui consomme plus de 80g alcool par jour à 5.64 fois 
#plus de risque de developper cancer qu'une personne qui consomme moins 
#de 80g d'alcool par jour

table(data$alcbin,data$malade)

	#modele lié au tabac

data$tabacbin<-ifelse(data$tabac<3,0,1)
table(data$tabacbin)
modele2 = glm(malade~tabacbin,data=data,family=binomial())
summary(modele2)

exp(0.67)
exp(0.67334+1.96*0.17676)#2.77
exp(0.67334-1.96*0.17676)#1.38

	#modele relation dose/effet conso d'alcool

modele3 = glm(malade~alcool,data=data,family=binomial())
summary(modele3)

OR = exp(1.0468)
IC_1OR =exp(1.0468+1.96*0.0935)#3.42
IC2_1OR = exp(1.0468-1.96*0.0935)#2.37

#OR 3/1
OR1.2 = exp(2*1.0468)
IC_OR1.2=exp(2*1.0468+1.96*2*0.0935)
IC2_OR1.2=exp(2*1.0468-1.96*2*0.0935)

#OR 4/1
OR1.3 = exp(3*1.0468)#23.11311
IC_OR1.3=exp(3*1.0468+1.96*3*0.0935)#40.05206
IC2_OR1.3=exp(3*1.0468-1.96*3*0.0935)#13.34

	#modele effet alcool sur consommation

modele4 = glm(malade~as.factor(alcool),data=data,family=binomial())
summ = summary(modele4)
#Alcool 2
OR2 = exp(summ$coefficients[2])#3.56
IC_OR2=exp(summ$coefficients[2]-1.96*summ$coefficients[6])#2.26
IC2_OR2=exp(summ$coefficients[2]+1.96*summ$coefficients[6])#5.62

#Alcool 3
OR3 = exp(summ$coefficients[3])#7.80
IC_OR3 = exp(summ$coefficients[3]-1.96*summ$coefficients[7])#4.677
IC2_OR3 = exp(summ$coefficients[3]+1.96*summ$coefficients[7])#13.01

#Alcool 4
OR4= exp(summ$coefficients[4])#27.22
IC_OR4=exp(summ$coefficients[4]-1.96*summ$coefficients[8])#14.437
IC2_OR4=exp(summ$coefficients[4]+1.96*summ$coefficients[8])#51.34

summary(modele4)$cov.unscaled

#OR 4/3
a =summ$coefficients[4]-summ$coefficients[3]
#FAUX var43 = 0.01
var43=summary(modele4)$cov.unscaled[3,3]+summary(modele4)$cov.unscaled[4,4]-2*summary(modele4)$cov.unscaled[4,3]
exp(a-1.96*sqrt(var43)) #1.88
exp(a+1.96*sqrt(var43))#6.46

OR1.2 = exp(2*1.73)
OR1.3 = exp(3*1.73)

#2.4 PLOT 
plot(1,1,xlim=c(0,5),ylim=c(0,80),xlabel="alcool",ylabel="Odds ratio",col="red")
points(2,OR2,col="red")
points(3,OR3,col="red")
points(4,OR4,col="red")

segments(x0=2,y0=IC2_OR2,y1=IC_OR2,col="red")
segments(x0=3,y0=IC2_OR3,y1=IC_OR3,col="red")
segments(x0=4,y0=IC2_OR4,y1=IC_OR4,col="red")

points(1.9,OR,col="blue")
points(2.9,OR1.2,col="blue")
points(3.9,OR1.3,col="blue")

segments(1.9,y0=IC_1OR,y1=IC2_1OR)cd 
segments(2.9,y0=IC_OR1.2,y1=IC2_OR1.2)
segments(3.9,y0=IC_OR1.3,y1=IC2_OR1.3)

	# Question 3 :

data$alcbin_1<-ifelse(data$alcool<3,0,2)
table(data$alcbin_1)
data$alcbin_2<-ifelse(data$alcool<3,1,2)
table(data$alcbin_2)

modele_1 = glm(malade~alcbin_1,data=data,family=binomial())
summary(modele_1) # b0 = -1,86 b1 = 0,86
modele_1 = glm(malade~alcbin_2,data=data,family=binomial())
summary(modele_1) # b0 = -3,59 b1 = 1,73

# On remarque que b(alcbin_2) = b(alcbin_1) * 2 ET b1(alcbin) = b1(alcbin_1) 

	# Question 4 :

data$agebin <-ifelse(data$age<3,0,1)
table(data$agebin)

modele_glob = glm(malade~alcbin + tabacbin + agebin,data=data,family=binomial())
summ = summary(modele_glob)	#2.472719
OR = exp(summ$coefficients[4]) #11.85463

 # OR1
IC_OR = exp(summ$coefficients[4]-1.96*summ$coefficients[8])# 6.077881
IC2_OR = exp(summ$coefficients[3]+1.96*summ$coefficients[8])# 4.25038


	# Question 5 :
	
# en utilisant le .dat on obtient les même résultats pour un groupe de 8pers uniquement mais pas la même déviance :)


