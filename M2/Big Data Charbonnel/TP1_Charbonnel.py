#!/bin/env python3

def producteur():
    result = []
    for i in range(10000):
        result.append(gros_calcul_couteux(i))
    return result

def consommateur():
  for e in producteur():
    traiter(e)

def semaine():
    print("début_de_semaine", end=" ")
    for j in ("lu","ma","me","je","ve"):
        yield j
    print("fin_de_semaine")

s=semaine()
print(next(s))
print(next(s))
print(next(s))
print(next(s))
print(next(s))
"print(next(s))"

for jour in semaine():
  print(jour, end=" ")

def fibonnacci():
    f_0=0
    f_1=1
    while True:
        f=f_0+f_1
        f_0,f_1=f_1,f
        yield f

for k in fibonnacci():
    if k<100:
        print("terme suivant", k, end=" ")
    else:
        break

#les 20 premiers termes :

for k,i in enumerate(fibonnacci()):
    print(i)
    if k > 20:
        break

from datetime import datetime
import time

def chrono():
    debut=datetime.now()
    while True:
        s=datetime.now()- debut
        yield s


# mon_chrono = chrono()
# next(mon_chrono)       # déclenche le chrono
# time.sleep(5)
# print("\n5 sec après:")
# print(next(mon_chrono))  # affiche le temps écoulé depuis le déclenchement
# time.sleep(2)
# print("2 sec après:")
# print(next(mon_chrono))  # affiche le temps écoulé depuis le déclenchement


f=open("/usr/share/dict/words", "r")
print(f.readline())
print(f.readline())
print(f.readline())
print(f.readline())
lines = f.readlines() # readlines lit tout donc peut pas faie readline après un readlines
print(lines[:9])
print(type(lines))
print(lines[200].replace("\n",""))
inverse=lines[200].replace("\n","")[::-1]
print(inverse)
f.close()


def chercher():
    with open("/usr/share/dict/words", "r") as f:
        for line in f:
            if line != "" and len(line)>3:
                mot=line.replace("\n","")
                inverse=mot[::-1]
                if mot == inverse:
                    yield mot

for i,c in enumerate(chercher()):
    print(c)
    if i > 41:
        break





from random import randrange

def _palin(n):
  with open('/usr/share/dict/words', 'r') as f:
    for word in f:
      word = word.strip()
      if len(word)==n:
        if word==word[::-1]: 
          yield word

def palin(n):
  try:
    return next(palin.h[n])
  except KeyError:
    palin.h[n] = _palin(n)
    return next(palin.h[n])

if __name__ == "__main__":
  palin.h = {}
  for i in range(30):
    for j in [5,6,7]:
      if randrange(10)<7:
        try:
          print(j,palin(j))
        except StopIteration:
          print(f"plus de palindrome de {j} lettres")








def termes(n, liste_actuelle=None):
    if liste_actuelle is None:
        liste_actuelle = []

    # Cas de base : somme des termes égale à n
    if sum(liste_actuelle) == n:
        print(liste_actuelle)
        return

    # Cas récursif : ajouter un terme à la liste actuelle
    for terme in range(1, n - sum(liste_actuelle) +1):
        termes(n, liste_actuelle + [terme])

n=5
termes(n)




def termes(n,min, max, liste_actuelle=None):
    if liste_actuelle is None:
        liste_actuelle = []

    # Cas de base : somme des termes égale à n
    if sum(liste_actuelle) == n and min<=len(liste_actuelle)<=max:
        print(liste_actuelle)
        return

    # Cas récursif : ajouter un terme à la liste actuelle
    for terme in range(1, n - sum(liste_actuelle) +1):
        termes(n, min, max, liste_actuelle + [terme])

n=5
min=3
max=4
termes(n,min, max)




def termes(n,l):
    if sum(l)==n:
        print(l)
    for i in range(1,n-sum(l)+1):
        termes(n,l+[i])

 
if __name__=="__main__":
    l = []
    termes(5,l)

print( " VERSION 2  ")

def termes(n,l):
    for i in range(1,n):
        l2 = l + [i]
        if sum(l2)==n:
            print(l2)
            return
    
        elif sum(l2)<n:
            termes(n,l2)
        else:
            return
 
if __name__=="__main__":
  l = []
  termes(5,l)
  





"""

## exo ge1

```python
def Fibo():
    F=[0,1]
    print("Suite de Fibonacci:", end=" ")
    j=1
    while j>-1:
        F.append(F[j-1]+F[j])
        yield F[j-1]
        j+=1
```


```python
def fibo():
    x = 1
    y = 1
    yield x
    yield y
    while True:
        x,y = y, x+y
        yield y
        
suite = fibo()
for i in suite:
    print(i)
    if i > 20:
        break
```
ou bien : 

```python
# les termes <=20
for i in fibo():
    print(i)
    if i > 20:
        break
```

ou bien : 

```python
# les 20 premiers termes
for k,i in enumerate(fibo()):
    print(i)
    if k > 20:
        break
```

```python
def fib():
    u0 = 1
    u1 = 1
    while True: #True
        yield u0
        stock = u1
        u1 = u1+u0
        u0 =stock
        

f = fib()    

for i in range(5):   
    u0 = next(f)
    print('n=' , i,'u_n =',u0)

```


## exo ge2

```python
from datetime import datetime
import time

def chrono():
    debut=datetime.now()
    while True:
        s=datetime.now()- debut
        yield s
        
```

```python
import time

def chrono():
    t1=time.time()
    while True:
        t2=time.time()
        yield t2-t1
```
## exo ge3

```python
def chercher():
    with open("/usr/share/dict/words", "r") as f:
        for line in f:
            if line != "" and len(line)>3:
                mot=line.replace("\n","")
                inverse=mot[::-1]
                if mot == inverse:
                    yield mot
                    
for i,c in enumerate(chercher()):
    print(c)
    if i > 20:
        break
```



## exo ge3

```python
def palomino(n=None):
  with open("/usr/share/dict/words","r", encoding="utf-8") as texte:
    for l in texte:
      l=l.strip()
      if n:
        if len(l)==n:
          if l[(len(l)//2)-1::-1]==l[(len(l)-len(l)//2):]:
            yield l
    
### Programme

p=palomino(4)
print(4,next(p))
            

```

## exo ge3
```python

import os
import random as rd

path = '/usr/share/dict/words'

def P(path):
    palindrom = []
    
    with open(path,'r') as file:
        for line in file:
            word = line.strip() #.strip permet de tuer le '/n' 
            if (word == word[::-1]) & (len(word)>3): # word[::-1] lire le str à l'envers
                palindrom.append(word)
        palindrom = list(set(palindrom)) # set créer un obet du type set et fait le tri des doublons 
    #print(len(palindrom)) 
    while len(palindrom)>=1:
        w = rd.choice(palindrom) # find a random word in palindrom
        yield w
        palindrom.remove(w) #kill this word, the first find

pal = P(path)   

for i in range(22): 
    a = next(pal)
    print(a)
    
```
```python
#!/bin/env python3

from random import randrange

def _palin(n):
  with open('/usr/share/dict/words', 'r') as f:
    for word in f:
      word = word.strip()
      if len(word)==n:
        if word==word[::-1]: 
          yield word

def palin(n):
  try:
    return next(palin.h[n])
  except KeyError:
    palin.h[n] = _palin(n)
    return next(palin.h[n])

if __name__ == "__main__":
  palin.h = {}
  for i in range(30):
    for j in [5,6,7]:
      if randrange(10)<7:
        try:
          print(j,palin(j))
        except StopIteration:
          print(f"plus de palindrome de {j} lettres")

```

## exo ge4.1

```python
def termes(n,l):
  for i in range(1,n):
    l2 = l + [i]
    if sum(l2)==n:
      print(l2)
      return
    elif sum(l2)<n:
      termes(n,l2)
    else:
      return 
if __name__=="__main__":
  l = []
  termes(5,l)
   
```


"""