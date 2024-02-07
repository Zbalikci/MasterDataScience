library(car)
library(readr)
library(ggplot2)
library(tidyverse)

# Activité 4 :

company<-read_csv("company.csv")

y=company$production
x1=company$capital
x2=company$labor

# Question 2:
model=lm(log(y)~log(x1)+log(x2))
summary(model)

# Question 3:

# On rejette H0 au seuil de 5% car p-value: 2.716e-14
# Donc le modèle est significative

# Question 4:

n<-25
d<-3

t<-qt(0.975,n-d)

I1<-model$coefficients[2]-t*sqrt(0.03473)
I2<-model$coefficients[2]+t*sqrt(0.03473)
I<-c(I1,I2)


T1<-model$coefficients[3]-t*sqrt(0.02696)
T2<-model$coefficients[3]+t*sqrt(0.02696)
T<-c(T1,T2)

# Question 5:
Y<-log(company$production) - log(company$capital)
X1<-log(company$capital)
X2<-log(company$labor) - log(company$capital) 

model2=lm(Y~ X1 + X2)
summary(model2)

#------------------------------------------------------------------------

# Activité 5:

# Question 3:
library(carData)
aov(conformity ~ fcategory+partner.status, data=Moore)
summary(aov(conformity ~ fcategory+partner.status, data=Moore))

aov(conformity ~ partner.status+fcategory, data=Moore)
summary(aov(conformity ~ partner.status+fcategory, data=Moore))
