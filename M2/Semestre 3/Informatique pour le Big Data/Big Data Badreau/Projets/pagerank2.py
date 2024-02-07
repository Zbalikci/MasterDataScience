from mrjob.job import MRJob
from mrjob.step import MRStep

class Pagerank(MRJob):
    def mapper(self, _, line):
        node_id, neighbor = line.split('\t')
        
        # Emit the original structure of the graph
        yield node_id, (neighbor, 1.0)
        # Emit contributions to neighbors
        yield neighbor, (None, 0.0)

    def reducer(self, node_id, values):
        # Initialize the page rank
        page_rank = 0.0
        structure = None

        for value in values:
            neighbor, contribution = value
            if neighbor is not None:
                structure = neighbor
            else:
                page_rank += contribution

        # Damping factor (typically 0.85) can be applied here
        page_rank = 0.15 + 0.85 * page_rank

        # Yield the result
        yield None, (node_id, (structure, page_rank))

    def reducer_sort(self, _, values):
        # Sort the results by node_id
        for node_id, (structure, page_rank) in sorted(values):
            yield node_id, (structure, page_rank)

    def steps(self):
        return [
            MRStep(mapper=self.mapper,),
        ]

    # def steps(self):
    #     return [
    #         MRStep(mapper=self.mapper, reducer=self.reducer),
    #         MRStep(reducer=self.reducer_sort)
    #     ]

if __name__ == '__main__':
    Pagerank.run()
