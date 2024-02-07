#install.packages("tseries")
library(tseries)
library(datasets)
data=AirPassengers
plot(data,ylab="Airpassengers")
grid()
frequency(data)

#si on regarde le graphe ce n'ai pas compatible avec le modèle additif
#car l'amplitude augmente (c'est peut-être un modèle multiplicatif ?)
#donc on le change pour pouvoir utiliser un modèle additif

Ldata=log(data)
plot(Ldata, ylab='Airpassengers')
grid()
frequency(Ldata)

decomp=decompose(Ldata,type="additive",)
plot(decomp$seasonal)
plot(decomp$trend)
plot(decomp$random)
plot(decomp$figure)
plot(decomp$figure,type="l")
sum(decomp$figure) #environ zéro car c'est la contrainte voir 1.3 page 

plot(decomp)

n=length(decomp$trend)
time=1:n
mod=lm(decomp$trend ~ time)
summary(mod)

estimateur_a0=mod$coefficients[1]
estimateur_a1=mod$coefficients[2]

# on a maintenant un modèle prédictif car la tendance m_t=a0+a1*t
# et pour n'importe quel moment dans le temps on peut prédire car on a estimé a0 et a1

plot(time, decomp$trend,type="l",ylab='trend') #la tendance
lines(time,estimateur_a0+time*estimateur_a1,col='red',lty=2) #fontion linéaire a0+t*a1
#lty=2 signifie en pointillé


time2=(n+1):(n+24)
pred=estimateur_a0+time2*estimateur_a1+decomp$figure
#figure = un motif et seasonal c'est le tout !

plot(c(Ldata,pred),type="l") #on a rajouté les 2 périodes prédit (24 mois = 2 ans car 1 an = 1 période = 12 mois)

#meilleur plot:
plot(ts(c(Ldata,pred),frequency = 12,start = 1949),ylab='Log(AirPassengers)',type='l')
lines(ts(pred,frequency = 12,start = 1961),col='red',lwd=2)
grid()
#en rouge gras(lwd=2) sont les valeurs prédites


#Là on a fait log(airpassengers) mais on veut airpassengers ! :
plot(ts(c(data,exp(pred)),frequency = 12,start = 1949),ylab='AirPassengers',type='l')
lines(ts(exp(pred),frequency = 12,start = 1961),col='red',lwd=2)
grid()

#à faire pour les tp prochains :
#install.packages("Rcpp")
#install.packages("RcppArmadillo")
#install.packages("forecast")
library("Rcpp")
library("RcppArmadillo")
library("forecast")