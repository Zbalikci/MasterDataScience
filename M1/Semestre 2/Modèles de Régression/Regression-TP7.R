Effectif<-c(59,60,62,56,63,59,62,60)
Morts<-c(6,13,18,28,52,53,61,60)
Log_dose<-c(1.6907,1.7242,1.7552,1.7842,1.8113,1.8369,1.8610,1.8839)

data <-cbind(Log_dose,Effectif,Morts)

Survivants<- Effectif - Morts

Y<-cbind(Morts,Survivants)
X<-Log_dose

modele1<-glm(formula = Y ~ X, family = binomial(link = probit))
summary(modele1)

### Question 3

z<-qnorm(1-0.05/2)
IC<-c(19.728-1.487*z,19.728+1.487*z)

LD<- -(-34.935/19.723)

VAR<-vcov(glm(formula = Y ~ X, family = binomial(link = probit)))

FI<-c(-1/19.728,-34.935/(19.728^2))


ICLD<-c(LD-sqrt(t(FI)%*%VAR%*%FI)*z,LD+sqrt(t(FI)%*%VAR%*%FI)*z)
ICLD


### Question 5

modele1$null.deviance - modele1$deviance

