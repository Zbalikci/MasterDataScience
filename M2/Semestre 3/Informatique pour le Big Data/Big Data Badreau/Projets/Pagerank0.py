from mrjob.job import MRJob
from mrjob.step import MRStep

global N
N = 0

class PageRank(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper1, reducer=self.reducer_count_pages),
            MRStep(reducer=self.reducer_count_weight),
            MRStep(mapper=self.mapper2, reducer=self.reducer_count_pages2),
            MRStep(reducer=self.reducer_weight),
            MRStep(reducer=self.reducer_sort)
        ]

    def mapper1(self, _, line):
        # Mapper pour extraire toutes les pages
        ligne = line.strip().split('\t')
        page_i = ligne[0]
        page_j = ligne[1]
        yield page_i, {'cited_pages': [page_j], 'num_cited_pages': 1}
        yield page_j, {'cited_pages': [], 'num_cited_pages': 0}

    def reducer_count_pages(self, page, page_cite):
        global N
        # Reducer pour compter le nombre total de pages j citées par une page i et assembler la liste des pages j citées
        pages_cites = set()

        for value in page_cite:
            if value:
                pages_cites.update(value['cited_pages'])

        N += 1  # +1 pour compter le nombre de pages dans le réseau
        yield page, {'cited_pages': list(pages_cites), 'num_cited_pages': len(pages_cites)}

    def reducer_count_weight(self, page, values):
        global N
        # Reducer pour calculer le poids initial de chaque page
        poids_initial = 1 / N
        value = list(values)[0]
        yield [page, value['cited_pages'], value['num_cited_pages']], poids_initial

    def mapper2(self, data,poids_initial):
        # Mapper pour émettre les informations nécessaires à partir des pages citées
        page_i, cited_pages,num_cited_i, poids_i = data[0], data[1], data[2], poids_initial
        for page_j in cited_pages:
            if page_j:
                yield page_j, {'page_i': page_i, 'num_cited_i': num_cited_i, 'poids_i': poids_i}

    def reducer_count_pages2(self, page_j, infos_page_i):
        # Reducer pour assembler la liste des pages j qui citent la page i
        pages_j_qui_citent_i = []

        for info in infos_page_i:
            page_i = info['page_i']
            ni = info['num_cited_i']
            poids_i = info['poids_i']
            pages_j_qui_citent_i.append({'page_i': page_i, 'num_cited_i': ni, 'poids_i': poids_i})

        yield page_j, pages_j_qui_citent_i

    def reducer_weight(self, page, liste_pages):
        global N

        # Reducer pour calculer le poids final de chaque page
        poids_initial = 1 / N
        c = 0.15
        s = 0

        for infos_page in liste_pages:
            for info_page in infos_page:
                ni = info_page['num_cited_i']
                poids_i = info_page['poids_i']
                s += poids_i / ni if ni != 0 else 0  # Éviter la division par zéro

        poids_final = c * poids_initial + (1 - c) * s

        yield None, (page, poids_final)

    def reducer_sort(self, _, values):
        # Le dernier reducer trie les résultats par poids
        sorted_pages = sorted(values, key=lambda x: x[1], reverse=True)[:10]
        for page, poids in sorted_pages:
            yield page, poids


if __name__ == '__main__':
    PageRank.run()
