#! /usr/bin/env python3

import sys
from pyspark import SparkContext
import re

motif = re.compile("\w+")

sc = SparkContext()
lines = sc.textFile(sys.argv[1])
word_count = lines.filter(lambda line: len(line)>1 and line[1].isdigit())
#word_count2 = word_count.filter(lambda word : len(word)>1 and int(word[1]) >0)


res = word_count.count()
print("Nombre d'enregistrement : " , res)

word_count2 = word_count.map(lambda  word: word[57:63])
word_countNord = word_count2.filter(lambda word : '+' in word)
word_countSud = word_count2.filter(lambda word : '-' in word)
word_countNa = word_count2.filter(lambda word : '-' not in word and '+' not in word)
print("Nombre de stations par hémisphère : \n")
print(" - NA \t", word_countNa.count()," stations")
print(" - Nord ", word_countNord.count()," stations")
print(" - Sud \t", word_countSud.count()," stations")

#ou bien
def lat(signe):
    if signe == "+":
        return ("Nord",1)
    elif signe == '-':
        return ("Sud",1)
    else:
        return ("NA",1)

word_count_lat = word_count.map(lambda l : lat(l[57]))
print(word_count_lat.reduceByKey( lambda a,b : a+b).collect())

from datetime import datetime
word_count4 = word_count.filter(lambda word : word[91:]!="").map(lambda  word: (int((datetime.strptime(word[91:99], '%Y%m%d') - datetime.strptime(word[82:90], '%Y%m%d')).days),word[13:41]))
word_count5 = word_count4.sortByKey(ascending=False)
for word in word_count5.take(10):
    print(word[1],word[0]/365," année")

rdd_pays= word_count.map(lambda  word: (word[43:46],1)).reduceByKey(lambda a,b :a+b)
rdd_pays2=rdd_pays.map(lambda t : (t[1],t[0]))

print(rdd_pays2.sortByKey(ascending=False).first())