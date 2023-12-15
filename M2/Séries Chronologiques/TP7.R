library(forecast)
n = length(gold)
plot(gold,type = "l")

###################################################################

Y = gold[(n-364):n]
n = length(Y)
plot(Y,type="l")

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
plot(X,type="l")
lines(LocNA,X[LocNA],col='red',type='p',pch=3)
###################################################################

library(tseries)
kpss.test(X)
adf.test(X)

###################################################################

DX = diff(X)
plot(DX,type="l")

###################################################################

acf(DX)  #q=1 donc MA(1)
pacf(DX) # décroissance exponentielle (donc c'est pas un AR ?)

###################################################################

arima = Arima(X,order=c(0,1,1),include.drift=TRUE)

Res = arima$residuals
library(car)
checkupRes(Res)
dev.off()

forecast_result <- forecast(arima, h = 30, level = 80)
plot(forecast_result, main = "Prévisions ARIMA(0,1,1)")

###################################################################

arima2 = Arima(X,order=c(0,1,1),include.drift=FALSE)
forecast_result2 <- forecast(arima2, h = 30, level = 80)
plot(forecast_result2, main = "Prévisions ARIMA(0,1,1)")
