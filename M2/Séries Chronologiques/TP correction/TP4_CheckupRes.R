# Fonction permettant une analyse visuelle des résidus d'une modélisation par quelques graphiques adaptés
checkupRes = function(Res, l,lagmax=40, lblag=5){
  
  # Partitionnement de la fenêtre graphique 
  layout(matrix(c(1,1,1,2:7), nrow=3, ncol=3, byrow=TRUE))
  par(oma=c(0, 0, 0, 0))
  #par(mgp=c(0, 0, 0))
  par(mar=c(2.5, 2, 1.5, 2))
  
  m = mean(Res)
  s = sd(Res)
    
  # Série des résidus
  plot(Res, type="l", col="black", main="Série", xlab="", ylab="", cex=0.6)
  
  # ACF/PACF
  ACF = acf(Res, lag.max=lagmax, plot=FALSE)
  plot(ACF, ylim=c(-1, 1), xlab="", ylab="")
  title("ACF")
  PACF = pacf(Res, lag.max=lagmax, plot=FALSE)
  plot(PACF, ylim=c(-1, 1), xlab="", ylab="")
  title("PACF")
  
  # Nuage de points avec décalage de 1 dans le temps
  n = length(Res)
  plot(Res[1:(n-1)], Res[2:n], type="p", col="blue", main=substitute(bold("t / t-1")), xlab="", ylab="")
  
  # Test de Ljung-Box
  lbpv = Box.test(Res, lag=lblag, type="Ljung-Box")$p.value
  cat("Test de Ljung-Box : p-val=", lbpv, sep="")
  
  # Histogramme
  hist(Res, breaks=sqrt(n), freq=FALSE, col="skyblue", main="Densité", xlab="", ylab="")
  curve(dnorm(x, m=m, sd=s), col="red", lty=2, add=TRUE)
  
  # Test de Shapiro-Wilk
  swpv = shapiro.test(Res)$p.value
  cat("\nTest de Shapiro : p-val=", swpv, sep="")
  
  # QQ plots
  qqnorm(Res, main="Quantiles", xlab="", ylab="")
  qqline(Res, distribution=qnorm, lty=2)
  
  # Nuage de points standardisé
  plot((Res-m)/s, type="p", main=substitute(bold("Série standardisée")), xlab="", ylab="")
  abline(h=c(-1.96, 1.96), lty=2, col="red")
}
