
library("tseries")
source("TP4_checkupRes.R")

plot(EuStockMarkets)
Y = EuStockMarkets[,1]
X = diff(log(Y))
plot(X, type="l")
grid()
checkupRes(X)
Box.test(X, lag=10, type="Ljung-Box")
## Bruit blanc assez crédible
adf.test(X)
kpss.test(X) # Léger doute mais la stationnarité semble confirmée également

checkupRes(X^2)
## Le comportement de X^2 peut correspondre à un ARMA
adf.test(X^2)
kpss.test(X^2) # Tests en contradiction

### Mise en évidence (empiriquement) des changements de variance conditionnelle
fen = 100
n = length(X)
Var = rep(0, n-fen+1)
for (i in 1:(n-fen+1)){
  Var[i] = var(X[i:(i+fen-1)]) # Variance empirique
}
dev.off()
plot(Var, type="l", col="red")
grid()

### Tentative GARCH
X = X-mean(X)
acf(X^2)
pacf(X^2)
# La série (Xt^2) suit un ARMA(max(p,q), p)
# Avec : p l'ordre de la partie GARCH et q l'ordre de la partie ARCH
# q=2, p=0 : ARMA(2,0) = AR(2)
# q=1, p=1 : ARMA(1,1)

GARCH11 = garch(X, order=c(1,1))
summary(GARCH11)
BIC11 = AIC(GARCH11, k=log(n))

GARCH02 = garch(X, order=c(0,2))
summary(GARCH02)
BIC02 = AIC(GARCH02, k=log(n))
# Modèle GARCH(1,1) meilleur au sens du BIC
### Attention ! GARCH(p,q), p étant l'ordre de la partie GARCH

### Aspect graphique
plot(X, type="l")
lines(GARCH11$fitted.values[,1], type="l", col="red")
lines(GARCH11$fitted.values[,2], type="l", col="red")
# Attention : fitted.values renvoie la volatilité estimée (non pas les valeurs reconstruites de la série comme pour les ARMA)
# Variance : gamma(0) = omega/(1-alpha(1)-beta(1))
Coef = GARCH11$coef
s = sqrt(Coef[1]/(1-Coef[2]-Coef[3])) # Ecart-type en régime stationnaire
abline(h=c(-s,s), col="orange")
grid()

plot(X, type="l")
lines(GARCH02$fitted.values[,1], type="l", col="blue")
lines(GARCH02$fitted.values[,2], type="l", col="blue")
# Attention : fitted.values renvoie la volatilité estimée (non pas les valeurs reconstruites de la série comme pour les ARMA)
# Variance : gamma(0) = omega/(1-alpha(1)-beta(1))
Coef = GARCH02$coef
s = sqrt(Coef[1]/(1-Coef[2]-Coef[3])) # Ecart-type en régime stationnaire
abline(h=c(-s,s), col="magenta")
grid()

### Pour aller plus loin : ARMA-GARCH, package fGarch (plus de possibilités que garch dans tseries)
