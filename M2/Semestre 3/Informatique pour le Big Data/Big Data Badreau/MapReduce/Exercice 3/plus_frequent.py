#! /usr/bin/env python3

from mrjob.job import MRJob
import re
from mrjob.step import MRStep
WORD_RE = re.compile(r"[\w]+")

class MRWordFreqCount(MRJob):
    def mapper(self, _, line):
        for word in WORD_RE.findall(line):
            if len(word)>5:
                yield word.lower(), 1

    def reducer1(self, word, counts):
        yield None , (sum(counts),word)

    def reducer2(self,_,paire):
        yield max(paire)

    def steps(self):
        return [
           MRStep(mapper=self.mapper,
                  reducer=self.reducer1),
           MRStep(reducer=self.reducer2)
        ]
if __name__ == '__main__':
    MRWordFreqCount.run()