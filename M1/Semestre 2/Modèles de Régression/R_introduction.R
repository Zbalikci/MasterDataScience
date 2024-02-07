#library("expm")
#help("for")

#Pour affecter une valeur à une variable
#a = 5
#a <- 5

for (i in 1:5) {
  print(1:i)
}

for (n in c(2,5,10,20,50)) {
  x <- stats::rnorm(n)
  cat(n, ": ", sum(x^2), "\n", sep = "")
}

#c=pour définir une liste (abréviation de colonne)
#rnorm génère aléatoirement des variables alétoires qui suivent la loi normale
#r pour random et norm pour loi normale
#help("rnorm) -----> rnorm(n, mean = 0, sd = 1) (sd c'est l'écart-type en anglais)
#hist(x) pour aficher l'histogramme

#stats::rnorm (...) -------> package::fonction (...)
#quand le package est déjà installé, on a pas besoin de l'appeler et on peut l'utiliser direct
#(sauf s'il y a une autre fonction de même nom dans un autre package, là il faut préciser le package d'origine)

#cat c'est le print "joli"
#\n pour aller à la ligne et sep c'est pour mettre un truc/symbole entre chaque ligne
#x^2 est une abréviation de R , il met au carré chaque élèment de x (qui est une colonne/vecteur) !!on ne calcule pas le carré d'un vecteur!!

f <- factor(sample(letters[1:5], 10, replace = TRUE))
for(i in unique(f)) print(i)

s = "bonjour"
typeof(s)
is.numeric(2)
is.numeric(4.5)
is.numeric(s)
is.character(2)
is.character(s)

#et : &
#ou : |
#non : ! (il faut le mettre au début des affirmations)
#ou exclusif : xor

a=3

if (a==1) {
  b=10*a
} else if (a==2) {
  b= a*3 
} else {
  b = a + 1
}
cat (b)


n=0
while (n<=50){
  n=n+1
  cat(n,sep='\n')
  if (n%%20 ==0){
    break
  }
}
# n modulo 20 : n%%20

################################################################################

#création de fonction

estPair = function(x){
  if (is.numeric(x)){
    return (x%%2==0)
  }else {
    cat("Argument non numérique!")
  }
 
}

estPair(201)
estPair(s)
estPair(154)


################################################################################

operation = function(a,b,symbol='+'){
  if (symbol=='+'){
    return(a+b)
  } else if (symbol== '-'){
    return(a-b)
  } else if (symbol== '*'){
    return(a*b)
  }
}

operation(15,9)
operation(15,9,'*')

################################################################################

#Courbe gaussien

U = seq(-6, 5, by= 0.01 )
print(U)

#ça en une ligne

V=1/sqrt(2*pi) * exp(-U^2/2)


#ou bien en 4 lignes 


#N=length(U)
#V=rep(0,N)
#for (i in 1:N){
  #V[i]=1/sqrt(2*pi) * exp(-U[i]^2/2)
#}

#plot(U,V) -----> nuage de points

W =1/sqrt(4*pi) * exp(-(U+2)^2/4)

plot(U,V,type='l',col='blue',lwd=3,main='Densité des lois normale', xlab="x",ylab = "y=f(x)",xlim = c(-5.5,4),lty=6)
lines(U,W,type='l',col='red',lwd=3 ,lty=1)
grid(col = 'black')
legend("topright", legend = c("N(0,1)", "N(-2,2)"), col=c("blue" , "red"), lty = c(6,1))

#lty =0, 1 , 2 , 3 ,4 5 ou 6
#lwd : épaisseur du trait
#lines pour superposer les courbes qui vient après l'initialisation de la première courbe

################################################################################
A=matrix(c(-1,2,0,3,1,4,1,2,-3,2,0,1), 3, 4 ,byrow = TRUE)
print(A)
print(t(A))
print(A[2,]) #affiche la 2e ligne
print(A[,2]) #affiche la 2e colonne
print(A[2,3]) #affiche l'élément à la 2e ligne et 3e colonne
print(A*A) #: multiplie élèment par élément en R (aucun sens en maths car pb de taille)
print(A %*% t(A)) # multiplication matricielle (pour les tailles : (3,4)*(4,3) c'est bon )
print(sqrt(A)) # affiche les racines de chaque élèments de A

B = rbind(A,c(2,7,-1,4))
print(B)
#rbind: empiler en ligne (bind : lier et row : ligne, donc cbind pour empiler en colonne)

print(det(B))

print(solve(B)) #l'inverse de B : solve(B)

print(B%*%solve(B))

E=eigen(B)
E$values

sum(E$vectors[,1]^2)

D=diag(c(1,5,6,9))
print(D)
C=matrix(0,6,3)
F=matrix(1,6,3)
print(C)
print(F)
print(diag(B))
print(sum(diag(B)))#trace

################################################################################

employe = data.frame(
  emp_id=1:5,
  emp_name=c('Zeynep','Mariamma','Clément','Ivan','Clara'),
  salary=c(623.5,750.9,680.0,820.0,742.8),
  start_date=as.Date(c("2012-03-25","2014-04-24","2014-03-07","2015-07-15","2013-06-13")),
  stringsAsFactors = FALSE
)
print(employe)
employe[2:3,]
colnames(employe)
colnames(employe)=c("Id","Nom","Salaire","Date")
rownames(employe)
rownames(employe)=c("E1","E2","E3","E4","E5")
employe["E3","Nom"]="Quentin"
employe=cbind(employe,c("a","b","c","d","e"))
print(employe)
colnames(employe)[5]="new"

################################################################################

X=rnorm(1000)

f=function(u){
  return(1/sqrt(2*pi) * exp(-u^2/2))
}
hist(X,freq = FALSE,col = 'lightgreen',border='purple')

help("hist")

curve(f,from=-5,to=5,n=1000,add=TRUE,type='l',col="red")
#n'oublie pas add=TRUE pour qu'il l'ajoute sur l'histogramme

################################################################################

ages=data.frame(
  val=c(40,45,15)
)
print(ages)
pie(ages$val,labels = c("<15",">=15 et <=60",">60"),col = c("forestgreen","lightblue","yellow"))

################################################################################

boxplot(X) #boît à moustache de X
boxplot(X,notch = TRUE,col = 'orange')


################################################################################

illustrerTCL=function(n,N){
  TCL=rep(0,N)
  for (i in 1:N){
    X=rbinom(n,50,0.3)
    TCL[i]=sqrt(n)*(mean(X)-15)/(sqrt(10.5))
  }
  hist(TCL,freq = FALSE,col = 'lightgreen',border='purple')
  curve(1/sqrt(2*pi) * exp(-x^2/2),add=TRUE,lwd=2,lty="dotted",col="red")
}
illustrerTCL(100000,10000)

################################################################################

illustrerTCL=function(n,N){
  TCL=rep(0,N)
  for (i in 1:N){
    X=rpois(n,4)
    TCL[i]=sqrt(n)*(mean(X)-4)/2
  }
  hist(TCL,freq = FALSE,col = 'lightgreen',border='purple')
  curve(1/sqrt(2*pi) * exp(-x^2/2),add=TRUE,lwd=2,lty="dotted",col="red")
}
illustrerTCL(10000,1000)

################################################################################

sort(c(8,45,21,40,12)) #trier

#équivalent de append en R :

L=c()
L=c(L,5)
L=c(L,-10)
L=c(L[1],4,L[2])
L[-3] #affiche tout les élèments sauf le 3e avant la fin
L=L[-3] #enlève le 3e élèment avant la fin

Liste=seq(0,100,by=2)


which(Liste>50) #envoie les indices
Liste[which(Liste>50)]
Liste>50
sum(Liste>50)
Liste[-c(25:30)]
