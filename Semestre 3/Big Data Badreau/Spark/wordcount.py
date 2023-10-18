#! /usr/bin/env python3

import sys
from pyspark import SparkContext

sc = SparkContext()
lines = sc.textFile(sys.argv[1])
word_count= lines.flatMap(lambda line: line.split())
word_count2 = word_count.map(lambda  word: ( word,1))
word_count3 = word_count2.reduceByKey(lambda a,b: a+b)
res = word_count3.collect()

for word,cpt in res:
    print(word,cpt)

    