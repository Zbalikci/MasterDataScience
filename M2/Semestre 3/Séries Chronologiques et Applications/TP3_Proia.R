library(tseries)

simulerARMA <- function(n, m, Phi, Theta, s2) {
  E=rnorm(n,0,sqrt(s2))
  p=length(Phi)
  q=length(Theta)
  r=max(p,q)
  Y=rep(0,n)
  Y[1:r] = E[1:r]
  for ( i in ((r+1):n) ) {
    ar=ifelse(p>0,t(Phi)%*%Y[(i-1):(i-p)],0)
    ma=ifelse(q>0,t(Theta)%*%E[(i-1):(i-q)],0)
    Y[i] = E[i] + ar +  ma 
  }
  X=Y+m
  plot(X,type="l", main="Simulation ARMA",col='red',xlab="t")
  #return (Y+m)
}

