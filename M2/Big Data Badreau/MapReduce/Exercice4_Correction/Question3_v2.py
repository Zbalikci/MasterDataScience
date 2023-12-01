#! /usr/bin/env python3

from mrjob.job import MRJob
from mrjob.step import MRStep

class utilisateurs_plus_visites(MRJob):
    def mapper1(self, _, line):
        line_split = line.split(',')
        if line_split[0]=='C' :
            yield line_split[2], line_split.count('V')

    def reducer1(self, users, nbVisites):
        yield None, (sum(nbVisites),users)

    def reducer2(self, _, valeurs):
        ordered_val = sorted(valeurs, reverse=True)[:15]
        for nbVisites,users in ordered_val :
            yield users,f"{nbVisites} visites"

    def steps(self):
        return [
            MRStep(mapper=self.mapper1,
                    reducer=self.reducer1),
            MRStep(reducer=self.reducer2)
        ]
        
if __name__ == '__main__':
    utilisateurs_plus_visites.run()