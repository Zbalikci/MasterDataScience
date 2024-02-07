# Le jeu de données 'gold' se trouve dans le package 'forecast'
library(forecast)
ng = length(gold)
plot(gold, type="l", ylab="Gold", xlab="Jours")
grid()
Y = gold[(ng-364):ng]
n = length(Y)

# Il y a des valeurs manquantes...
# On va les reconstruire à l'aide de la méthode (simpliste) de l'interpolation linéaire

LocNA = which(is.na(Y))
X = Y
# On remarque que les NA vont soit par 1 soit par 2 et ne sont pas en début ni en fin de série
# D'où l'algorithme simplifié suivant
for (i in LocNA){
  if ( is.na(Y[i]) ){
    
    # NA isolé
    if ( !is.na(X[i+1]) ){
      X[i] = (X[i-1] + X[i+1])/2
    }
    
    # Double NA
    else{
      c = (X[i+2] - X[i-1])/3
      X[i] = X[i-1] + c
      X[i+1] = X[i-1] + 2*c
    }
  }
}

# Mise en évidence des points reconstruits
plot(Y, type="l", ylab="Gold", xlab="Jours")
lines(LocNA, X[LocNA], col="red", type="p", pch=3)
# On voit se dessiner une tendance linéaire décroissante
Tps = 1:n
lines(Tps, fitted(lm(X ~ Tps)), col="blue", lty=2)
grid()

# La série est non stationnaire
library(tseries)
kpss.test(X)
adf.test(X)

# Avec une différenciation, on récupère la stationnarité
DX = diff(X)
plot(DX, type="l", ylab="Diff Gold", xlab="Jours")
grid()
kpss.test(DX)
adf.test(DX)

# Pas un bruit blanc, 1 pic très significatif dans l'ACF et PACF décroissante...
Box.test(DX, lag=5)
acf(DX)
pacf(DX)

# Partons par exemple sur un MA(1) avec une tendance linéaire
# Coefficient MA(1) très significatif... mais celui de la tendance linéaire est douteux
Mod = Arima(X, order=c(0,1,1), include.drift=TRUE)
summary(Mod)

# Résidus bruit blanc (non)
source("TP4_CheckupRes.R")
checkupRes(Mod$residuals)

# Superposition signal/modèle
dev.off()
plot(X, type="l", ylab="Gold", xlab="Jours")
lines(fitted(Mod), type="l", col="red")
grid()

# Prédiction de 30 jours supplémentaires (IC à 80% et 95% par défaut)
# Avec drift
h = 30
Pred = forecast(Mod, h=h)
plot(Pred, xlab="Jours (01/04/88 to 31/03/89 + Prédictions pour 04/89)", ylab="Gold")
grid()

# Prédiction de 30 jours supplémentaires (IC à 80% et 95% par défaut)
# Sans drift
Mod = Arima(X, order=c(0,1,1), include.drift=FALSE)
h = 30
Pred = forecast(Mod, h=h)
plot(Pred, xlab="Jours (01/04/88 to 31/03/89 + Prédictions pour 04/89)", ylab="Gold")
grid()

# On voit que même si le drift n'est pas significatif, il semble essentiel à la prédiction
# Modélisation et prédiction sont deux notions différentes...
