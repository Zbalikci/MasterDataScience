
# Fonction permettant de simuler et renvoyer un processus ARMA gaussien de taille n avec :
# - la partie AR dans Phi
# - la partie MA dans Theta
# - la moyenne m
# - un bruit gaussien N(0, s2)
simulerARMA = function(n, m, Phi, Theta, s2){
  
  # Bruit N(0, s2)
  E = rnorm(n, 0, sqrt(s2))
  
  # Ordres  du processus
  p = length(Phi)
  q = length(Theta)
  r = max(p, q)

  # S?rie recentr?e
  Y = rep(0, n)
  
  # Construction pas ? pas de la structure ARMA
  for (i in (r+1):n){
    ar = ifelse(p > 0, sum(Phi*Y[(i-1):(i-p)]), 0)
    ma = ifelse(q > 0, sum(Theta*E[(i-1):(i-q)]), 0)
    Y[i] = ar + ma + E[i]
  }
  
  # La s?rie est centr?e sur m avant renvoi
  Y = Y+m
  
  # Repr?sentation graphique
  plot(1:n, Y, type="l", xlab="Temps", ylab=paste("S?rie ARMA(", substitute(p), ",", substitute(q), ")", sep=""))
                                                  
  return(Y)
}

# Quelques exemples stationnaires
X = simulerARMA(100, 5, c(0.1), c(0.2, 0.3), 2)
X = simulerARMA(1000, -2, c(-0.5, 0.3), c(), 1)
X = simulerARMA(200, 0, c(), c(0.3, -1, 0.5), 1.5)

# Quelques exemples non stationnaires
X = simulerARMA(500, 0, c(1), c(), 1)
X = simulerARMA(500, 0, c(-1), c(), 1)

# La diff?rence est claire, non ?

library(tseries)

# Exemple de 'arima.sim' donn? dans la documentation
X = arima.sim(n = 63, list(ar = c(0.8897, -0.4858), ma = c(-0.2279, 0.2488)), sd = sqrt(0.1796))
plot(X)

# Notre ?quivalent
X = simulerARMA(63, 0, c(0.8897, -0.4858), c(-0.2279, 0.2488), 0.1796)

# ACF et PACF d'un MA(5)
X = simulerARMA(100000, 0, c(), c(0.2, 0.3, 0.8, -0.5, 0.3), 1)
acf(X, lag.max = 50)
pacf(X, lag.max = 50)

# PACF et PACF d'un AR(2)
X = simulerARMA(100000, 0, c(0.5, 0.4), c(), 1)
acf(X, lag.max = 50)
pacf(X, lag.max = 50)

# PACF et PACF d'un ARMA(2, 2)
X = simulerARMA(100000, 0, c(0.3, 0.6), c(-0.3, 0.8), 1)
acf(X, lag.max = 50)
pacf(X, lag.max = 50)

# Tests de bruit blanc
Box.test(X, type="Ljung-Box", lag=1) # Corr?lation d'ordre 1 seulement
Box.test(X, type="Ljung-Box", lag=5) # Corr?lations d'ordre 1 ? 5 (mieux !)
Box.test(rnorm(100), type="Ljung-Box", lag=5)

# Tests de stationnarit? et de non stationnarit?
# Exemples stationnaires
X = simulerARMA(1000, -2, c(-0.5, 0.3), c(), 1)
adf.test(X)
kpss.test(X)
X = simulerARMA(200, 0, c(), c(0.3, -1, 0.5), 1.5)
adf.test(X)
kpss.test(X)
# attention kpss(X,null='Trend') élémine la tendance et regardes les residus donc ça peut fausser les conclusions

X = (1:1000) + rnorm(1000)
plot(X, trend ='l') # ce n'est clairement pas stationaire
kpss.test(X,null="Trend") # pourtant le test nous dit que c'est stationnaire.

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
# A?e, la cata ici ! Mais pourquoi... ??

# On reprend l'exemple du cours... et on d?couvre la fonction Arima...
library(forecast)
X = simulerARMA(200, 0, c(0.6, 0.2), c(0.7), 1)
ARMA = Arima(X, order = c(2, 0, 1), include.mean = FALSE)
summary(ARMA)

# ... ainsi que la fonction auto.arima calibr?e sur le BIC
auto.arima(X, max.p = 5, max.q = 5, max.d = 0, ic = "bic")
# On voit que ?a ne co?ncide pas toujours avec le bon mod?le, car n n'est pas tr?s grand
# Mais ?a fournit des mod?les tr?s coh?rents malgr? tout

library(TSA)

# Donn?es r?elles de conso ?lectrique
data(electricity)
plot(electricity)
Y = log(electricity)
plot(Y)

# D?composition additive sur le log puis mod?lisation ARMA sur la fluctuation
Decomp = decompose(Y)
plot(Decomp)
Res = Decomp$random
# Subtilit? : Decomp$random contient des NA en d?but et fin (dus ? la moyenne mobile arithm?tique utilis?e pour ?liminer la saisonnalit?)
# On les supprime pour ?tudier la structure de corr?lation
Res = Res[!is.na(Res)]

adf.test(Res)
kpss.test(Res)
Box.test(Res)
# Stationnaire mais pas bruit blanc !

acf(Res, lag.max = 50)
pacf(Res, lag.max = 50)
# Ni AR ni MA

auto.arima(Res)
# Un ARMA(1,1) non centr? est sugg?r?
ARMA = Arima(Res, order = c(1, 0, 1), include.mean = TRUE)
plot(Res, type="l")
lines(fitted(ARMA), type="l", col="red")

ACF=acf(ARMA$residuals,lag=50)
plot(ACF,ylim=c(-1,1))
PACF=pacf(ARMA$residuals,lag=50)
plot(PACF,ylim=c(-1,1))
Box.test(ARMA$residuals,lag=12,type="Ljung-Box")
Box.test(ARMA$residuals,lag=3,type="Ljung-Box")
# Le résidus : celui qu'on a pas réussi à expliquer avec notre modèle c'est juste du bruit comme on peut l'obeserver avec le ACF et PACF