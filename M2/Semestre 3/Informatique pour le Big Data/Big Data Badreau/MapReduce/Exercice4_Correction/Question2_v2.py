#! /usr/bin/env python3

from mrjob.job import MRJob
from mrjob.step import MRStep

class titres_pages_plus_visitees(MRJob):
    def mapper1(self, _, line):
        line_split = line.split(',')
        if line_split[0]=='V' :
            yield line_split[1], 1 # id_page, nb_visite
        elif line_split[0]=='A' :
            yield line_split[1], line_split[3] # id_page, title_page

    def reducer1(self, id, valeurs):
        cpt = 0
        for val in valeurs :
            if val==1 :
                cpt+=1
            else :
                title = val
        yield None, (cpt,title)

    def reducer2(self, _, valeurs):
        ordered_val = sorted(valeurs, reverse=True)[:5]
        for nbVisites,title in ordered_val :
            yield title,f"{nbVisites} visites"

    def steps(self):
        return [
            MRStep(mapper=self.mapper1,
                    reducer=self.reducer1),
            MRStep(reducer=self.reducer2)
        ]
        
if __name__ == '__main__':
    titres_pages_plus_visitees.run()