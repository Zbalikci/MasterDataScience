#! /usr/bin/env python3

from mrjob.job import MRJob
import re
from mrjob.step import MRStep

WORD_RE = re.compile(r"^V,[\d]+,[\d]+")

class MRWordFreqCount(MRJob):
    def mapper(self, _, line):
        for id in WORD_RE.findall(line):
            id=id[2:-2]
            yield id, 1

    def reducer(self, id, counts):
        s=sum(counts)
        if s>600:
            yield s,id

if __name__ == '__main__':
    MRWordFreqCount.run()