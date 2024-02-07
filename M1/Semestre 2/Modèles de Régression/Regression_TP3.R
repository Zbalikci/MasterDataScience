library(car)
library(tidyverse)
data<-read.csv("C:/Users/zbalikci/Downloads/water.csv")

head(data,4)

library(ggplot2)
ggplot(data,aes(x=fluoride,y=sodium)) + geom_point()

#Question 1:
reg<-lm(formula = data$sodium ~ data$fluoride )
summary(reg)

#Question 2: (Residual standard error: 195.9)^2
sig2<-195.9^2
sig2
#ou
var<-1/(n-d)*sum(reg$residuals^2) 

#Question 3:
#Intervalle de confiance
n<-20
d<-2
t<-qt(0.975,n-d)

I1<-reg$coefficients[2]-t*sqrt(21.38)
I2<-reg$coefficients[2]+t*sqrt(21.38)
I<-c(I1,I2)

#Question 4:
# Multiple R-squared:  0.8049
# On rejette H0 au seuil de 1%

#Question 5:
#Effacer donner 16 et 19
