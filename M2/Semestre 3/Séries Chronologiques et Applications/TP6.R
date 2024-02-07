Rain = scan("http://robjhyndman.com/tsdldata/hurst/precip1.dat", skip=1)
Rain = ts(Rain, start=c(1813))
library(forecast)
model_arima = Arima(log(Rain), include.drift=TRUE)
summary(model_arima) 
k = length(model_arima$coef) 
drift = model_arima$coef[k]
print(drift)
Res=model_arima$residuals

checkupRes(Res)
dev.off()

library(tseries)
adf.test(Res) 
kpss.test(Res)

#######################################################################

Volcano = scan("http://robjhyndman.com/tsdldata/annual/dvi.dat", skip=1)
Volcano = ts(Volcano, start=c(1813))

plot(log(Volcano+1)) #certain valeur valent 0 donc on rajoute 1 pour pouvoir appliquer le log

ARMA_volcano = Arima(log(Volcano+1), include.drift=TRUE)
summary(ARMA_volcano) 
k = length(ARMA_volcano$coef) 
drift = ARMA_volcano$coef[k]
print(drift)
Res=ARMA_volcano$residuals

checkupRes(Res) # si on regarde ACF PACF, c'est très autocorrélés 
dev.off()


adf.test(Res) 
kpss.test(Res)
# Les deux test ne se contredise pas : On peut supposer que c'est stattionaires donc on effectue un auto arima sur les residuals

auto.arima(Res,d=0,ic='bic')
ARMA_volcano2 = Arima(log(Volcano+1),order=c(5,0,1), include.drift=FALSE,include.mean = FALSE)
summary(ARMA_volcano2)


