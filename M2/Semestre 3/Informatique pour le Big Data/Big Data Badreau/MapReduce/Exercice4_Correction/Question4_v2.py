#! /usr/bin/env python3

from mrjob.job import MRJob
from mrjob.step import MRStep

class utilisateurs_plus_visites_liste_pages(MRJob):
    def mapper1(self, _, line):
        line_split = line.split(',')
        if line_split[0]=='C' :
            for i in range(3,len(line_split)) :
                if line_split[i] == 'V' :
                    yield line_split[i+1], line_split[2] # id_page, id_user
        elif line_split[0]=='A' :
            yield line_split[1], line_split[3] # id_page, titre_page

    def reducer1(self, id_page, valeurs):
        list_id_users = []
        for val in valeurs :
            try :
                int(val)
                list_id_users.append(val)
            except ValueError :
                title = val
        for id_user in list_id_users:
            yield id_user,title

    def reducer2(self, id_user, titles):
        list_titles = list(titles)
        yield None, (len(list_titles),id_user,list_titles)

    def reducer3(self, _, valeurs):
        ordered_val = sorted(valeurs, reverse=True)[:5]
        for nbVisites,user,list_titles in ordered_val :
            yield user,f"{nbVisites} visites : {', '.join(list_titles)}"

    def steps(self):
        return [
            MRStep(mapper=self.mapper1,
                    reducer=self.reducer1),
            MRStep(reducer=self.reducer2),
            MRStep(reducer=self.reducer3)
        ]
        
if __name__ == '__main__':
    utilisateurs_plus_visites_liste_pages.run()