# chronique 
library(deSolve)
rm(list=ls())
   Eq1 = function(t,x,parms)
   {
     dx1 = ((2*parms[2]*(parms[5]-parms[1])*x[2])/(parms[2]*parms[2]+x[2]*x[2]))*x[1]*(2-x[1])-x[1]
     dx2 = parms[3]*((x[1]*(1+parms[4]*parms[4])/(x[1]*x[1]+parms[4]*parms[4]))-x[2])
     list(c(dx1,dx2))
   }
   temps= seq(0,50,by=0.1)
   init1 = c(1,1)
   init2 = c(20,10)
   
   beta = 0.526627219
   cm = 40
   lambda = 30
   alpha = 0.1
   h = 10
   
   
   solution = lsoda(y=init1,times=temps,func= Eq1 ,parms = c(beta,cm,lambda,alpha,h))
   solution_bis = lsoda(y=init2,times=temps,func= Eq1 ,parms = c(beta,cm,lambda,alpha,h))
   par(mfrow=c(1,2))
   plot(temps,solution[,2],ylim=c(0,5),type="l",main="Densité de cellule",col='blue')
   lines(temps,solution[,3],type="l",col='red',lty=2)
   #lines(temps,solution_bis[,2],type='l',col='blue')
   #lines(temps,solution_bis[,3],type='l',col='blue',lty=2)

# Portrait de phase

plot (solution[,2],solution[,3],ylim=c(0,5),xlim=c(0,100),main='Portrait de phase',xlab='Population N',ylab='Population P',type='l',col='red')
lines(solution_bis[,2],solution_bis[,3],ylim=c(0,5),xlim=c(0,100),type='l',col='blue')
abline(h=r/a,col='green')
abline(v=m/(e*a),col='green')

# vitesse

xval=seq(0,100,by=15)
yval=seq(0,30,by=5)
for(x in xval){
  for(y in yval){
    dx=r*x-a*x*y
    dy = e*a*x*y-m*y
    arrows(x-0.1*dx,y-0.1*dy,x+0.1*dx,y+0.1*dy,length=0.05)}}
  }
}

