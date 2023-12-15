
# Fonction permettant de simuler et renvoyer un processus ARMA gaussien de taille n avec :
# - la partie AR dans Phi
# - la partie MA dans Theta
# - la moyenne m
# - un bruit gaussien N(0, s2)
simulerARMA = function(n, m, Phi, Theta, s2){
  
  # Bruit N(0, s2)
  E = rnorm(n, 0, sqrt(s2))
  
  # Ordresdu processus
  p = length(Phi)
  q = length(Theta)
  r = max(p, q)

  # Série recentrée
  Y = rep(0, n)
  
  # Construction pas à pas de la structure ARMA
  for (i in (r+1):n){
    ar = ifelse(p > 0, sum(Phi*Y[(i-1):(i-p)]), 0)
    ma = ifelse(q > 0, sum(Theta*E[(i-1):(i-q)]), 0)
    Y[i] = ar + ma + E[i]
  }
  
  # La série est centrée sur m avant renvoi
  Y = Y+m
  
  # Représentation graphique
  plot(1:n, Y, type="l", xlab="Temps", ylab=paste("Série ARMA(", substitute(p), ", ", substitute(q), ")", sep=""))
                                                  
  return(Y)
}

# Quelques exemples stationnaires
X = simulerARMA(100, 5, c(0.1), c(0.2, 0.3), 2)
X = simulerARMA(1000, -2, c(-0.5, 0.3), c(), 1)
X = simulerARMA(200, 0, c(), c(0.3, -1, 0.5), 1.5)

# Quelques exemples non stationnaires
X = simulerARMA(500, 0, c(1), c(), 1)
X = simulerARMA(500, 0, c(-1), c(), 1)

# La différence est claire, non ?

library(tseries)

# Exemple de 'arima.sim' donné dans la documentation
X = arima.sim(n = 63, list(ar = c(0.8897, -0.4858), ma = c(-0.2279, 0.2488)), sd = sqrt(0.1796))
plot(X)

# Notre équivalent
X = simulerARMA(63, 0, c(0.8897, -0.4858), c(-0.2279, 0.2488), 0.1796)

# ACF et PACF d'un MA(5)
X = simulerARMA(1000, 0, c(), c(0.2, 0.3, 0.8, -0.5, 0.3), 1)
acf(X, lag.max = 50)
pacf(X, lag.max = 50)

# PACF et PACF d'un AR(2)
X = simulerARMA(1000, 0, c(0.5, 0.4), c(), 1)
acf(X, lag.max = 50)
pacf(X, lag.max = 50)

# PACF et PACF d'un ARMA(2, 2)
X = simulerARMA(1000, 0, c(0.3, 0.6), c(-0.3, 0.8), 1)
acf(X, lag.max = 50)
pacf(X, lag.max = 50)

# Tests de bruit blanc
Box.test(X, type="Ljung-Box", lag=1) # Corrélation d'ordre 1 seulement
Box.test(X, type="Ljung-Box", lag=5) # Corrélations d'ordre 1 à 5 (mieux !)
Box.test(rnorm(100), type="Ljung-Box", lag=5)

# Tests de stationnarité et de non stationnarité
# Exemples stationnaires
X = simulerARMA(1000, -2, c(-0.5, 0.3), c(), 1)
adf.test(X)
kpss.test(X)
X = simulerARMA(200, 0, c(), c(0.3, -1, 0.5), 1.5)
adf.test(X)
kpss.test(X)
X = rnorm(1000)
adf.test(X)
kpss.test(X)

# Exemples non stationnaires
X = simulerARMA(500, 0, c(1), c(), 1)
adf.test(X)
kpss.test(X)
X = simulerARMA(500, 0, c(-1), c(), 1)
adf.test(X)
kpss.test(X)
# Aîe, la cata ici ! Mais pourquoi... ??

# On reprend l'exemple du cours... et on découvre la fonction Arima...
library(forecast)
X = simulerARMA(200, 0, c(0.6, 0.2), c(0.7), 1)
ARMA = Arima(X, order = c(2, 0, 1), include.mean = FALSE)
summary(ARMA)

# ... ainsi que la fonction auto.arima calibrée sur le BIC
auto.arima(X, max.p = 5, max.q = 5, max.d = 0, ic = "bic")
# On voit que ça ne coïncide pas toujours avec le bon modèle, car n n'est pas très grand
# Mais ça fournit des modèles très cohérents malgré tout

library(TSA)

# Données réelles de conso électrique
data(electricity)
plot(electricity)
Y = log(electricity)
plot(Y)

# Décomposition additive sur le log puis modélisation ARMA sur la fluctuation
Decomp = decompose(Y)
plot(Decomp)
Res = Decomp$random
# Subtilité : Decomp$random contient des NA en début et fin
# (dus à la moyenne mobile arithmétique utilisée pour éliminer la saisonnalité)
# On les supprime pour étudier la structure de corrélation
Res = Res[!is.na(Res)]

adf.test(Res)
kpss.test(Res)
Box.test(Res)
# Stationnaire mais pas bruit blanc !

acf(Res, lag.max = 50)
pacf(Res, lag.max = 50)
# Ni AR ni MA

auto.arima(Res)
# Un ARMA(1,1) non centré est suggéré
ARMA = Arima(Res, order = c(1, 0, 1), include.mean = TRUE)
plot(Res, type="l")
lines(fitted(ARMA), type="l", col="red")

