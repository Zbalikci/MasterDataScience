#! /usr/bin/env python3

from mrjob.job import MRJob
import re
from mrjob.step import MRStep

WORD_RE = re.compile(r"^V,[\d]+,[\d]+")

class MRWordFreqCount(MRJob):
    def mapper(self, _, line):
        for id in WORD_RE.findall(line):
            id=id[2:-2]
            n=id[-1]
            yield id, 1

    def reducer(self, id, counts):
        if sum(counts)>600:
            yield None, (sum(counts),id)

if __name__ == '__main__':
    MRWordFreqCount.run()