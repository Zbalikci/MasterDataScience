# Question 1:

x=c(0.088,0.99,0.54,0.062,0.14,0.51,0.81,0.39,0.56,0.90,
    0.99,0.63,0.95,0.0057,0.055,0.30,0.91,0.28,0.16,0.53)

y=c(0,1,0,0,1,0,1,1,1,1,
    1,1,1,0,0,1,1,0,1,1)
data<-data.frame(Y=as.factor(y),X=x)


# Question 2:
"Car Y est une variables qualitative à 2 modalités (binaire)"

# Question 3:
"cf. page 48"

# Question 4:
plot(x,y)
"L’estimateur de maximum de vraisemblance n’existe pas lorsque les données sont (quasi) séparables"
"donc on ne peut pas calculer l'estimateur de maximum de vraisemblance associé au coefficient de X analytiquement"

# Question 5:
model<-glm(formula = data$Y ~ data$X, family = binomial)
summary(model)
"On regarde la colonne des estimate : beta = (-1.4826,5.1865)"
beta<-c(-1.4826,5.1865)

# Question 6:
"cf page 53"

n<-20
sigma1<-0.9851^2*n
sigma2<-2.3542^2*n
V<-diag(c(sigma1,sigma2))

# Question 7:



# Question 8:

z<-qnorm(1-0.05/2)
ICup<-5.1865+2.3542*z
IClow<-5.1865-2.3542*z
IC<-c(IClow,ICup)

# Question 9:

"0 n'apartient pas à l'intervalle de confiance"
" "

# Question 10:



# Question 11:



# Question 12:



# Question 13:




