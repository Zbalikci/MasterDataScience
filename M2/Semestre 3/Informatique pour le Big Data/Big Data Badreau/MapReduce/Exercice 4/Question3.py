#! /usr/bin/env python3

from mrjob.job import MRJob
import re
from mrjob.step import MRStep
import operator
WORD_RE = re.compile(r'^C,"[\d]+",[\d]+\n(^V,[\d]+,[\d]+)+')

class MRWordFreqCount(MRJob):
    
    def mapper(self, _, line):
        for id in WORD_RE.findall(line):
            id=id[2:-2]
            yield id, 1

    def reducer1(self, id, counts):
        yield None,(sum(counts),id)

    def reducer2(self,_,paire):
        sorted_pairs = sorted(paire, key=lambda x: x[0], reverse=True)
        yield from sorted_pairs[:5]

    def steps(self):
        return [
           MRStep(mapper=self.mapper,
                  reducer=self.reducer1),
           MRStep(reducer=self.reducer2)
        ]

if __name__ == '__main__':
    MRWordFreqCount.run()