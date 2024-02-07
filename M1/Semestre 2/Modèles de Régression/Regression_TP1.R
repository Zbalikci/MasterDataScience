library(MASS)
data(Boston)
View(Boston)
library(ggplot2)
ggplot(Boston,aes(x=medv,y=lstat)) + geom_point()
#ou plot(Boston$medv,Boston$lstat)
#Question 1 : polynome de degré 2 (le plus simple), exp(-x) ou 1/

#Question 2 : Regarder F-statistic

reg<-lm(formula = Boston$lstat ~ Boston$medv + I(Boston$medv^2))
summary(reg)
#names(reg)
#reg$coefficients

#qf(0.95,2,503)
#qf(c(0.95,0.99),2,503)

#On remarque que F-statistic>3.01 et 4.64 donc on peut rejeter H0:"Coeffs nuls"

#Question 3:
X<-15
Y<-reg$coefficients[3]*X^2+reg$coefficients[2]*X+reg$coefficients[1]

n<-506
d<-3
t<-qt(0.975,n-d)
#Intervalle de confiance
var<-1/(n-d)*sum(reg$residuals^2)
X<-cbind(rep(1,506),Boston$medv,Boston$medv^2)
matr<-t(X)%*%X
invers<-solve(matr)
x<-c(1,15,15^2)
prod<-t(x)%*%invers%*%x

I1<-Y+t*sqrt(var*(1+prod))
I2<-Y-t*sqrt(var*(1+prod))
I<-c(I2,I1)
#On a bien Y qui appartient à l'intervalle
