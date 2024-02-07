# Récupération du dataset Rain
Rain = scan("http://robjhyndman.com/tsdldata/hurst/precip1.dat", skip=1)
Rain = ts(Rain, start=c(1813))
plot(Rain, main="Dataset Rain")

library("tseries")
adf.test(Rain)
kpss.test(Rain)
# La série semble stationnaire

acf(Rain)
pacf(Rain)
# Serait-ce simplement un bruit blanc décentré ?
Box.test(Rain, type="Ljung-Box", lag=5)

library("forecast")
auto.arima(Rain) # ARMA(0,0) avec intercept ?

ARMA = arima(Rain, order=c(1, 0, 1), include.mean = TRUE)
summary(ARMA) # Intercept très significatif mais AR1 et MA1 non-significatifs

ARMA = arima(Rain, order=c(0, 0, 0), include.mean = TRUE)
summary(ARMA) # Intercept très significatif

# On conserve le modèle bruit blanc décentré...

plot(Rain)
RainInf = fitted(ARMA) - sqrt(ARMA$sigma2)*1.96
RainSup = fitted(ARMA) + sqrt(ARMA$sigma2)*1.96
polygon(c(1813:1912, 1912:1813), c(RainInf, rev(RainSup)), col="gray", border="red")
lines(fitted(ARMA), col="red")
lines(Rain)
legend("topleft", legend=c("Rain", "One-Step ARMA(0,0)"), col=c("black", "red"), lty=1)
# Est-ce normal... ? Oui car un modèle avec seulement un intercept ne modélise qu'une valeur moyenne !

source("TP4_CheckupRes.R")
checkupRes(ARMA$residuals)
# Rien de choquant dans la normalité et la blancheur des résidus
Box.test(ARMA$residuals, lag=5)
shapiro.test(ARMA$residuals) # P-val douteuse... Visuellement c'est OK


dev.off()
# Récupération du dataset Volcano
Volcano = scan("http://robjhyndman.com/tsdldata/annual/dvi.dat", skip=1)
Volcano = ts(Volcano, start=c(1500))
plot(Volcano, main="Dataset Volcano")

# On va passer au log pour atténuer l'échelle en ordonnées
# Attention : certaines données étant nulles, il faut translater auparavant

LVolcano = log(Volcano+1)
plot(LVolcano, main="Dataset log-Volcano")

library("tseries")
adf.test(LVolcano)
kpss.test(LVolcano)
# La série semble stationnaire

acf(LVolcano)
pacf(LVolcano)
# Comportement ARMA (décroissance rapide)
# Peut-être AR(5) ? Ou "petit" ARMA ?

# Tentative AR(5)
ARMA = arima(LVolcano, order=c(5, 0, 0), include.mean = TRUE)
summary(ARMA) # L'ensemble est significatif
BIC(ARMA)

# Tentative ARMA(1,1)
ARMA = arima(LVolcano, order=c(1, 0, 1), include.mean = TRUE)
summary(ARMA) # Doute sur le MA(1)
BIC(ARMA) # BIC moins bon que l'AR(5)

auto.arima(LVolcano, max.d=0, ic="bic")
# AR(1) décentré sur la base du BIC dans la classe des ARMA

auto.arima(LVolcano, max.d=0, ic="aic")
# ARMA(5,1) décentré sur la base de l'AIC dans la classe des ARMA
# On semble retrouver un mix de nos deux modèles avec l'AIC...

# Tentative AR(1)
ARMA = arima(LVolcano, order=c(1, 0, 0), include.mean = TRUE)
summary(ARMA) # Tout est significatif
BIC(ARMA)
checkupRes(ARMA$residuals)
Box.test(ARMA$residuals, lag=5)
# Modèle beaucoup trop petit, trop de corrélation résiduelle encore présente

# Tentative ARMA(5,1)
ARMA = arima(LVolcano, order=c(5, 0, 1), include.mean = TRUE)
summary(ARMA) # Tout est significatif
BIC(ARMA)

# Modélisation
plot(LVolcano)
lines(fitted(ARMA), col="red")
legend("topleft", legend=c("LVolcano", "One-Step"), col=c("black", "red"), lty=1)

checkupRes(ARMA$residuals)
Box.test(ARMA$residuals, lag=5)
shapiro.test(ARMA$residuals)
# Bruit blanc mais pas de normalité
# C'était attendu : la série contient beaucoup de 0

dev.off()
# Transformation inverse
ModVolcano = exp(fitted(ARMA))-1
plot(Volcano)
lines(ModVolcano, col="red")
legend("topleft", legend=c("Volcano", "One-Step ARMA(5,1)"), col=c("black", "red"), lty=1)
# La hauteur des pics est mal modélisée...

# Conclusion : dataset qui gagnerait probablement à être modélisé par une autre approche !!
