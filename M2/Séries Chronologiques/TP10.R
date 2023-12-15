library("forecast")
library("tseries")

data("AirPassengers")
plot(AirPassengers,type='l')
grid()

LAP = log(AirPassengers)
n = length(LAP)
plot(LAP,type='l')
grid()

# Test de stationnarité
kpss.test(LAP)
adf.test(LAP)

# Test de stationnarité sur dif I-B
DLAP = diff(LAP)
plot(DLAP, type="l", ylab="Diff Log(AirPassengers)", xlab="Jours")
grid()
kpss.test(DLAP)
adf.test(DLAP)

# Test de stationnarité sur dif I-B^12

DLAP2 = diff(LAP, lag=12)
plot(DLAP2, type="l", ylab="Diff Log(AirPassengers)", xlab="Jours")
grid()
kpss.test(DLAP2)
adf.test(DLAP2)

# Test de stationnarité sur dif (I-B)(I-B^12)

DLAP3 = diff(diff(LAP, lag=12))
plot(DLAP3, type="l", ylab="Diff Log(AirPassengers)", xlab="Jours")
grid()
kpss.test(DLAP3)
adf.test(DLAP3)


##############

acf(as.numeric(LAP),lag=100)
pacf(LAP,lag=100)

acf(as.numeric(DLAP),lag=100)
pacf(DLAP,lag=100)

acf(as.numeric(DLAP2),lag=100)
pacf(DLAP2,lag=100)

acf(as.numeric(DLAP3),lag=100)
pacf(DLAP3,lag=100)


##################

sarima = Arima(LAP, order = c(1,0,1),
               seasonal = list(order = c(0,1,1),period = 12), include.drift = TRUE)
plot(sarima)
summary(sarima) # on divise le premier par la 2e et elle doit être supérieure à 1,96 en module --> s'il est significative


##################

plot(LAP, type="l", lwd=2)
lines(fitted(sarima), type="l", col="red")
lines(fitted(sarima) - 1,96*sqrt(sarima$sigma2), type="l", lty=2,col="blue")
lines(fitted(sarima) + 1,96*sqrt(sarima$sigma2), type="l", lty=2,col="magenta")
grid()


auto.arima(LAP,max.p=5,max.d=1,max.q=5,max.P=1,max.D=1,max.Q=1,ic="bic")

sarima2 = Arima(LAP, order = c(0,1,1),
               seasonal = list(order = c(0,1,1),period = 12))
plot(sarima2)
summary(sarima2) 

Box.test(sarima2$residuals,lag=12,type='Ljung-Box')


############## On enlève la dernière période et on le prédit avec nos 2 modèles pour le comparer:

LAP_T = LAP[1:(n-12)]
LAP_DP = LAP[(n-11):n]

Mod1T = Arima(LAP_T, order = c(1,0,1),
                      seasonal = list(order = c(0,1,1),period = 12), include.drift = TRUE)
Mod2T = Arima(LAP_T, order = c(0,1,1),
                seasonal = list(order = c(0,1,1),period = 12))

Pred1T = forecast(Mod1T,h=12)
plot(Pred1T)
Pred2T = forecast(Mod2T,h=12)
plot(Pred2T)

#(Pred1T$mean[1:12] - LAP_DP) < (Pred2T$mean[1:12] - LAP_DP)

MSE1 = mean((Pred1T$mean[1:12] - LAP_DP)^2)
MSE2 = mean((Pred2T$mean[1:12] - LAP_DP)^2)
# MSE2 est plus petit donc on peut conclure que le 2e modèle est meilleur

################### Predictions des 2 années suivants (sur le modèle non tronquée:

Pred = forecast(sarima2,h=2*12,level=95)
plot(Pred)
grid()

################ Prediction sur les données initiales sans log

PredInit = exp(Pred$mean + sarima$sigma2/2) # on corige avec sigma^2/2
NTps =(n+1):(n+2*12)
plot(1:n,AirPassengers , type ='l', lwd = 2 , xlab = "Mois", xlim = c(1,n+24),ylim=c(0,850))
lines(NTps,PredInit,col='red',lwd=2)
lines(NTps,exp(Pred$lower),col='red',lty=2)
lines(NTps,exp(Pred$upper),col='red',lty=2)
grid()



