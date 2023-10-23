data_btc = read.csv("/users/2024/ds2/122003362/Depots/MasterDataScience/Semestre 3/Séries Chronologiques/Datasets/BTC-USD.csv",sep=',')
data_btc$Date = as.Date(data_btc$Date , format = "%Y-%m-%d")
plot(data_btc$Date,data_btc$Close,type="l",ylab="Close",xlab='Date',main='Action BTC')
plot(data_btc$Date,log(data_btc$Close),type="l",ylab="log(Close)",xlab='Date',main='Action BTC')
grid()


#tendance constante : Arima(...,include.mean=True)  donne l'intercept : la valeur moyenne de la série
#          linéaire : Arima(...,include.drift=True) donne l'intercept et le drift

library(forecast)

#moi : pour annuler la tendance : 
"""
model_arima = Arima(log_btc, include.drift=TRUE)
summary(model_arima)
k = length(model_arima$coef) #le drift c'est le dernier élément
drift = model_arima$coef[k]
print(drift)
Res=model_arima$residuals
"""

#Le prof :
# A la main

log_btc = log(data_btc$Close)
plot(log_btc,type='l')
n = length(log_btc)

Tps = 1:n
RegLin=lm(log_btc~Tps)
lines(fitted(RegLin),col='red',lty=2)
Res = RegLin$residuals


checkupRes(Res) #du TP4
#Ce n'est pas un bruit blanc car y'a un pique au PACF

library(tseries)
adf.test(Res) #On ne rejette pas l'hypothèse de non-stationnarité
kpss.test(Res) #On ne rejette pas l'hypothèse de stationnarité
#Les deux test se contredise


#La décroissance ne sont pas assez rapides
#La Pacf a un pique avant de s'annuler donc on propose un AR(1)

ARMA = Arima(Res,order=c(1,0,0), include.drift=FALSE,include.mean=FALSE)
summary(ARMA)

Res = ARMA$residuals
checkupRes(Res)
dev.off()

model_final = fitted(RegLin)+fitted(ARMA)
plot(log_btc,type='l')
#lines(model_final,col='red',lty=2)
# Intervalle de confiance :
BS = model_final + 1.96*sqrt(ARMA$sigma2) # Borne inf
BI = model_final - 1.96*sqrt(ARMA$sigma2) # Borne sup

lines(BI,col='red',lty=2)
lines(BS,col='blue',lty=2)

## On enlève la tendance avec le drift :

model_arima = Arima(log_btc, order = c(1,0,0), include.drift=TRUE)
summary(model_arima) # elles sont tous significatifs
k = length(model_arima$coef) #le drift c'est le dernier élément
drift = model_arima$coef[k]
print(drift)
Res=model_arima$residuals

checkupRes(Res) 
dev.off()

# On applique l'exp sur les données qui sont en log :

plot(data_btc$Close,type='l')
#lines(model_final,col='red',lty=2)
# Intervalle de confiance :
BS =  exp( model_final + 1.96*sqrt(ARMA$sigma2)) # Borne inf
BI =  exp( model_final - 1.96*sqrt(ARMA$sigma2)) # Borne sup

lines(BI,col='red',lty=2)
lines(BS,col='blue',lty=2)
grid()
