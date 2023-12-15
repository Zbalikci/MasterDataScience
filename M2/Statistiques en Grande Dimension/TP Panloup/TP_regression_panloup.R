library('glmnet')

# Exercice 1 : 

# Question 1 

simu_Y <- function(n, p, theta, sigma) {
  epsilon <- rnorm(n, mean = 0, sd = sigma)
  Y <- X %*% theta + epsilon
  return(Y)
}

###############################################################################

# Question 2

n = 100
p = 200
s = 10
theta = c(rep(1,s/2), rep(-1,s/2), rep(0,(p-s)))
sigma = 0.5

X = matrix(rnorm(n * p), nrow = n, ncol = p)
Y = simu_Y(n, p, theta, sigma)

LASSO_ex1 = glmnet(X, Y, alpha = 1)

print(LASSO_ex1)
plot(LASSO_ex1)

predict(LASSO_ex1, newx = X[1:10, ], s = c(0.01, 0.005))

print(coef(LASSO_ex1 )) # les coefficients estimés

# Plot des coefficients en fonction de l'intensité de la pénalisation
plot(LASSO_ex1, xvar = "lambda", label = TRUE)

###############################################################################

# Question 7

cv_Ex1 <- cv.glmnet(X, Y, alpha = 1)
print(cv_Ex1)
plot(cv_Ex1)

# Afficher les valeurs de λ.min et λ.1se
print(cv_Ex1$lambda.min)
print(cv_Ex1$lambda.1se)
print(coef(LASSO_ex1, s = cv_Ex1$lambda.min)) # les coefficients estimés

###############################################################################

# Question 8

n_test = 50  
X_test = matrix(rnorm(n_test * p), nrow = n_test, ncol = p)
epsilon_test = rnorm(n_test, mean = 0, sd = sigma)
Y_test = X_test %*% theta + epsilon_test

predictions_lasso <- predict(cv_Ex1, newx = X_test, s = "lambda.min")

mse_lasso = mean((Y_test - predictions_lasso)^2)/n_test

###############################################################################

# Question 10

cv_Ex1_ridge <- cv.glmnet(X, Y, alpha = 0)
predictions_ridge <- predict(cv_Ex1_ridge, newx = X_test, s = "lambda.min")

mse_ridge <- mean((Y_test - predictions_ridge)^2)/n_test

##############################################################################

# Exercice 2 : 

data_leukemia_small <- read.csv("/users/2024/ds2/122003362/Téléchargements/leukemia_small.csv")
head(data_leukemia_small)

data_leukemia_big <- read.csv("/users/2024/ds2/122003362/Téléchargements/leukemia_big.csv")
head(data_leukemia_big)

