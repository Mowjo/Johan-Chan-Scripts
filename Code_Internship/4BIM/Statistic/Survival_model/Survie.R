##############################################################
#
#             Modele de Survie : Kaplan Meier
#
##############################################################


sexe = c(1,1,1,1,1,1,1,1,1,1)
suivi = c(19.7,25.8,45.6,37.4,34.4,33.7,17.8,12.9,14.1,12.5)
etat = c(1,1,1,0,0,0,0,1,0,0)

plot(survfit(Surv(suivi,etat)~1))
# pointillés = intervalle de confiance


##############################################################
#
#                    Modele de Cox 
#
##############################################################


setwd('/home/jchan/Documents/4BIM/GLM')



#Lecture des donnees :
data = read.table('Freireich.txt',h=T) 

#LOGWBC : logarythme du taux de globule blanc
# 6-MP :  colonne de traitement 
# delta : variable d évènement 



# Durée de survie : 

tab = survfit(Surv(T,delta)~1,data=data)
summary(tab)

     Call: survfit(formula = Surv(T, delta) ~ 1, data = data)

time n.risk n.event survival std.err lower 95% CI upper 95% CI
1     42       2    0.952  0.0329       0.8901        1.000
2     40       2    0.905  0.0453       0.8202        0.998
3     38       1    0.881  0.0500       0.7883        0.985
4     37       2    0.833  0.0575       0.7279        0.954
5     35       2    0.786  0.0633       0.6709        0.920
6     33       3    0.714  0.0697       0.5899        0.865
7     29       1    0.690  0.0715       0.5628        0.845
8     28       4    0.591  0.0764       0.4588        0.762
10     23       1    0.565  0.0773       0.4325        0.739
11     21       2    0.512  0.0788       0.3783        0.692
12     18       2    0.455  0.0796       0.3227        0.641
13     16       1    0.426  0.0795       0.2958        0.615
15     15       1    0.398  0.0791       0.2694        0.588
16     14       1    0.369  0.0784       0.2437        0.560
17     13       1    0.341  0.0774       0.2186        0.532
22      9       2    0.265  0.0765       0.1507        0.467
23      7       2    0.189  0.0710       0.0909        0.395

plot(tab)


# Ajout de la variable 6-MP

tab2 = survfit(Surv(T,delta)~MP,data=data)
summary(tab2)
plot(tab2)


# Comparaison de distribution de la survie :

tab3 = survdiff(Surv(T,delta)~MP,data=data)


Call:
  survdiff(formula = Surv(T, delta) ~ MP, data = data)

N Observed Expected (O-E)^2/E (O-E)^2/V
MP=0 21       21     10.7      9.77      16.8
MP=1 21        9     19.3      5.46      16.8

Chisq= 16.8  on 1 degrees of freedom, p= 4.17e-05 

# p-value < 0.05 donc le traitement a un effet sur la survie en l'améliorant !

# Modele de Cox :

cox1 = coxph(Surv(T,delta)~MP,data=data)
summary(cox1)

Call:
  coxph(formula = Surv(T, delta) ~ MP, data = data)

n= 42, number of events= 30 

coef exp(coef) se(coef)      z Pr(>|z|)    
MP -1.5721    0.2076   0.4124 -3.812 0.000138 ***
  ---
  Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

exp(coef) exp(-coef) lower .95 upper .95
MP    0.2076      4.817   0.09251    0.4659

Concordance= 0.69  (se = 0.053 )
Rsquare= 0.322   (max possible= 0.988 )
Likelihood ratio test= 16.35  on 1 df,   p=5.261e-05
Wald test            = 14.53  on 1 df,   p=0.0001378
Score (logrank) test = 17.25  on 1 df,   p=3.283e-05


##############################################################
#
#                   Survie et Cancer du sein
#
##############################################################

#Lecture des donnees :
data = read.table('breast.txt',h=T) 

# Modele : 

tab = survfit(Surv(T,delta)~nbGanglion,data=data)
summary(tab)
plot(tab)

cox1 = coxph(Surv(T,delta)~nbGanglion,data=data)
summary(cox1)


