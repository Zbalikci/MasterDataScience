#! /usr/bin/env python3

import sys
from pyspark import SparkContext
import re
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import col

spark = SparkSession.builder.master("local").getOrCreate()
df = spark.read.load("isd-history.csv",format="csv", sep=",", inferSchema="true", header="true")

print("Nombre d'enregistrement : ",df.count(),'\n')
print("Nombre de stations par hémisphère :",)
print("hémisphère NA:",df.filter(df.LAT.isNull()).count())
print("hémisphère Nord:",df.dropna(subset="LAT").filter(df.LAT>=0).count())
print("hémisphère Sud:",df.dropna(subset="LAT").filter(df.LAT<0).count(),'\n')

print("Stations ayant eu la plus longue période d'activité :",df.filter(df.BEGIN.isNotNull()).count(),'\n') 

print("Pays le plus représenté :",df.groupBy('CTRY').count().orderBy("count", ascending=False).first()[0],'\n')


print("Nombre de pays ayant des stations :",df.dropna(subset='CTRY').select('CTRY').distinct().count())
