library(car)
data<-Moore
summary(data)
Y<-data$conformity
X<-data$partner.status
Z<-data$fcategory

#Question 2 :

summary(aov(lm(Y~X+Z)))
summary(aov(lm(Y~Z+X)))

#Question 3 :

summary(aov(Y~X+Z))
summary(aov(Y~Z+X))

#Question 4 :

model1 <- aov(Y~X*Z)
summary(model1)

#Question 5:

model2 <- Anova(lm(Y~X+Z),type=2)
summary(model2)
