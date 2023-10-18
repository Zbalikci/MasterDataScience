#! /usr/bin/env python3

import sys
from pyspark import SparkContext
import re
from pyspark.sql import SparkSession, Row
spark = SparkSession.builder.master("local").getOrCreate()
df = spark.read.load("isd-history.csv",format="csv", sep=",", inferSchema="true", header="true")

print(df.count())