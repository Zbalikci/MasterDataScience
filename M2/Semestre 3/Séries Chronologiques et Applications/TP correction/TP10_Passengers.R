
source("TP4_CheckupRes.R")
library("forecast")
library("tseries")

### Chargement des données
data("AirPassengers")
plot(AirPassengers, type="l")
LAP = log(AirPassengers)
plot(LAP, type="l")
grid()
n = length(LAP)

### Première analyse graphique et différenciations
LAP_Diff = diff(LAP) # d=1 et D=0
LAP_Diff12 = diff(LAP, 12) # d=0 et D=1
LAP_Diff12D = diff(diff(LAP, 12)) # d=1 et D=1

adf.test(LAP_Diff)
kpss.test(LAP_Diff) # Semble stationnaire... malgré une périodicité évidente
plot(LAP_Diff, type="l")
acf(as.numeric(LAP_Diff), lag.max=40)
pacf(as.numeric(LAP_Diff), lag.max=40) # P=1 ? (PACF à l'échelle périodique)

adf.test(LAP_Diff12)
kpss.test(LAP_Diff12) # Pas très concluant...
plot(LAP_Diff12, type="l")
acf(as.numeric(LAP_Diff12), lag.max=40)
pacf(as.numeric(LAP_Diff12), lag.max=40)

adf.test(LAP_Diff12D)
kpss.test(LAP_Diff12D) # Semble stationnaire
plot(LAP_Diff12D, type="l")
acf(as.numeric(LAP_Diff12D), lag.max=40)
pacf(as.numeric(LAP_Diff12D), lag.max=40)

# On conserve (d,D)=(0,1) et (d,D)=(1,1) qui éliminent la périodicité

### Modélisation SARIMA(1,0,1)x(0,1,1)[12] avec tendance linéaire
Mod1 = Arima(LAP, order=c(1,0,1), seasonal=list(order=c(0,1,1), period=12), include.drift=TRUE)
summary(Mod1)
plot(LAP, type="l", lwd=2)
lines(fitted(Mod1), type="l", col="red")
lines(fitted(Mod1)-1.96*sqrt(Mod1$sigma2), type="l", lty=2, col="magenta")
lines(fitted(Mod1)+1.96*sqrt(Mod1$sigma2), type="l", lty=2, col="magenta")
grid()
checkupRes(Mod1$residuals)
Box.test(Mod1$residuals, lag=12, type="Ljung-Box") # Résidus globalement gaussiens (même si c'est douteux...) mais bruit blanc
# Très bonne modélisation dans l'ensemble

### Recherche du modèle minimisant le BIC par auto.arima
auto.arima(LAP, max.p=5, max.d=1, max.q=5, max.P=1, max.D=1, max.Q=1, ic="bic")
# SARIMA(0,1,1)x(0,1,1)[12]
Mod2 = Arima(LAP, order=c(0,1,1), seasonal=list(order=c(0,1,1), period=12))
summary(Mod2)
dev.off()
plot(LAP, type="l", lwd=2)
lines(fitted(Mod2), type="l", col="red")
lines(fitted(Mod2)-1.96*sqrt(Mod2$sigma2), type="l", lty=2, col="magenta")
lines(fitted(Mod2)+1.96*sqrt(Mod2$sigma2), type="l", lty=2, col="magenta")
grid()
checkupRes(Mod2$residuals)
Box.test(Mod2$residuals, lag=12, type="Ljung-Box") # Résidus globalement gaussiens, bruit blanc
# Très bonne modélisation dans l'ensemble (meilleure que la précédente ?)

### Comparaison sur un critère prédictif
LAP_Tronque = LAP[1:(n-12)]
LAP_DP = LAP[(n-11):n]
Mod1T = Arima(LAP_Tronque, order=c(1,0,1), seasonal=list(order=c(0,1,1), period=12), include.drift=TRUE)
Mod2T = Arima(LAP_Tronque, order=c(0,1,1), seasonal=list(order=c(0,1,1), period=12))
Pred1T = forecast(Mod1T, h=12)$mean
Pred2T = forecast(Mod2T, h=12)$mean
dev.off()
plot(LAP_DP, type="l", lwd=2)
lines(as.numeric(Pred1T), type="l", col="red", lwd=2)
lines(as.numeric(Pred2T), type="l", col="blue", lwd=2)
legend("topleft", legend=c("SARIMA(1,0,1)x(0,1,1)[12] + Trend", "SARIMA(0,1,1)x(0,1,1)[12]"), col=c("red", "blue"), lwd=2)
grid()
MSE1 = sum((LAP_DP-Pred1T)^2)/12
MSE2 = sum((LAP_DP-Pred2T)^2)/12 # Sur le critère prédictif de la dernière période, on retiendrait plutôt Mod2

### Prédictions et intervalles de prédiction
Pred = forecast(Mod2, h=24, level=95)
plot(Pred)
grid()

# Attention à la correction dans la prédiction exponentielle...
PredInit = exp(Pred$mean + Mod2$sigma2/2)
NTps = (n+1):(n+24)
plot(1:n, AirPassengers, type="l", lwd=2, xlab="Mois", xlim=c(1, n+24), ylim=c(0, 850))
polygon(c(NTps, rev(NTps)), c(exp(Pred$upper[,1]), rev(exp(Pred$lower[,1]))), col="orange", border=FALSE)
lines(NTps, PredInit, col="red", lwd=2)
lines((n+1):(n+24), exp(Pred$lower), col="red", lty=2)
lines((n+1):(n+24), exp(Pred$upper), col="red", lty=2)
grid()
legend("topleft", legend=c("Pred", "IP 95%"), col="red", lty=1:2, lwd=c(2,1))
