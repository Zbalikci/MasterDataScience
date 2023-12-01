library(tseries)
library(TSA)
library(forecast)
library(car)
X = arima.sim(n = 1000, list(ar = c(0.8897, -0.4858), ma = c(-0.2279, 0.2488)), sd = sqrt(0.1796))
ARMA = Arima(X, order = c(2, 0, 1), include.mean = FALSE)
summary(ARMA)
Res=ARMA$residuals

checkupRes = function(Res){
  layout(matrix(c(1,1,1,2:7), nrow=3, ncol=3, byrow=TRUE))
  ######## Graphe 1
  plot(Res,type='l',xlab='',ylab=expression(epsilon[t]),main='',col='black')
  ######## Graphe 2
  ACF=acf(Res,lag=50,plot=FALSE)
  plot(ACF,ylim=c(-1,1),main='')
  ######## Graphe 3
  PACF=pacf(Res,lag=50,plot=FALSE)
  plot(PACF,ylim=c(-1,1),main='',ylab='PACF')
  ######## Graphe 4
  n=length(Res)
  plot(Res[1:(n-1)],Res[2:n],type='p',col='purple',ylab=expression(epsilon[t]),xlab=expression(epsilon[t-1]))
  ######## Graphe 5
  moy=mean(Res)
  var=var(Res)
  hist(Res,main='',col='blue')
  "superposer la courbe de la loi normale(oy,var)"
  ######## Graphe 6
  qqPlot(Res)
  ######## Graphe 7
  ResCR = (Res-moy)/var
  plot(ResCR[1:(n-1)],ResCR[2:n])
  }

checkupRes(Res)

checkupRes(rnorm(1000))

dev.off()
