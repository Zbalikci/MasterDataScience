#!/bin/env python3

import json
import pprint
import pandas as pd
""" 
with open("stop_areas.json",'r') as file:
    data = json.load(file)
    print(data)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(data['stop_areas'])

nom_gare=[]
longitude=[]	
latitude=[]

for k in range(len(data['stop_areas'])):
    nom_gare.append(data['stop_areas'][k]['name'])
    longitude.append(data['stop_areas'][k]['coord']['lon'])
    latitude.append(data['stop_areas'][k]['coord']['lat'])

dict={'nom de la gare':nom_gare,'longitude':longitude,'latitude':latitude}

df=pd.DataFrame(dict)
print(df)
#df.to_csv('ex1.csv', encoding='utf-8',index=False)
"""
from sys import getsizeof
carre = lambda t:t*t

n = 15
x = map(carre,range(n))
l = [carre(i) for i in range(n)]
print(getsizeof(x))
print(getsizeof(l)) #la liste prend plus de place
print(x)
print(next(x))
print(next(x))
print(x)
for X in x :
    print(X)
print(x)

for X in x :
    print(X)
print(x)
print(l)


####################################
f1 = lambda t:t%2==0

x = map(carre,range(n))
y = filter(f1,x)
print(y)
for Y in y :
    print(Y)
print("il reste rien même pas les impaire dans l'itérateur : ")
for X in x :
    print(X)

####################################
print("==================================================================")
from functools import reduce
f2 = lambda t,u: t+u

x = map(carre,range(n))
y = filter(f1,x)
z = reduce(f2,y)
print(z)


####################################
print("==================================================================")
from random import uniform
from statistics import mean, variance

n = 1000
X = [uniform(2.5, 10.0) for i in range(n)]
print("Résultats attendus")
print(f"Moyenne : {mean(X):.3f}, Variance : {variance(X)*(n-1)/(n):.3f}")

def calcul_moy_var(X):
    n=len(X)
    somme = lambda t,u: t+u
    mu=reduce(somme,X)/n

    carre = lambda t:t*t
    x2 = map(carre,X)

    var= reduce(somme,x2)/n - mu**2
    return [mu,var]

def calcul_moy_var(X):

    func_map = lambda t:(t**2,t,1)
    mapper=map(func_map,X)
    somme = lambda t,u: [a+b for a,b in zip(t,u)]
    somme_carre,somme_simple,n=reduce(somme,mapper)
    var= somme_carre/n - (somme_simple/n)**2
    return [somme_simple/n,var]

print("\nRésultats obtenus")
res = calcul_moy_var(X)
print(f"Moyenne : {res[0]:.3f} - Variance : {res[1]:.3f}")