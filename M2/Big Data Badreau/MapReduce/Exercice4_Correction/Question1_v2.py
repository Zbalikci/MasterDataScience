#! /usr/bin/env python3

from mrjob.job import MRJob

class pages_plus_visitees(MRJob):
    def mapper(self, _, line):
        line_split = line.split(',')
        if line_split[0]=='V' :
            yield line_split[1], 1

    def reducer(self, id, visite):
        NbVisites = sum(visite)
        if NbVisites >= 1000 :
            yield id, f"{NbVisites} visites"
        
if __name__ == '__main__':
    pages_plus_visitees.run()

