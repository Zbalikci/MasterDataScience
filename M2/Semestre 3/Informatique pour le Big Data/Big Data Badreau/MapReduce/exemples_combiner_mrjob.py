#! /usr/bin/env python3

from mrjob.job import MRJob

class moyenne_sansCombiner(MRJob):
    def mapper(self, _, x):
        yield _, float(x)

    def reducer(self, _, valeurs):
        L_valeurs = list(valeurs)
        yield "Moyenne (sans combiner) : ", f"{sum(L_valeurs)/len(L_valeurs):.3f}"

class moyenne_avecCombiner(MRJob):
    def mapper(self, _, x):
        yield _, float(x)

    def combiner(self, _, valeurs):
        L_valeurs = list(valeurs)
        yield _, sum(L_valeurs)/len(L_valeurs)

    def reducer(self, _, valeurs):
        L_valeurs = list(valeurs)
        yield "Moyenne (avec combiner) : ", f"{sum(L_valeurs)/len(L_valeurs):.3f}"

if __name__ == '__main__':
    moyenne_sansCombiner.run()
    moyenne_avecCombiner.run()