#! /usr/bin/env python3
import re
import sys
from pyspark import SparkContext

motif = re.compile("\w+")
sc = SparkContext()
lines = sc.textFile(sys.argv[1])
word_count= lines.flatMap(lambda line: line.split())
word_count2 = word_count.filter(lambda word:len(word)>5)
word_count3 = word_count2.map(lambda  word: ( word.lower(),1))
word_count4 = word_count3.reduceByKey(lambda a,b: a+b)
word_count5 = word_count4.map(lambda  t: ( t[1],t[0]))
word_count6 = word_count5.sortByKey(ascending=False)
res = word_count6.first()

print(res)