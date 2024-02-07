#!/usr/bin/python
from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol
from mrjob.step import MRStep

class MRPageRank(MRJob):

    def map_task(self, node_id, node):
        
        yield node_id, ('node', node)
	
        if 'links' in node:
                for dest_id, weight in node.get('links'):
                    if type(weight)==list:
                        yield dest_id, ('score', node['score'] * weight[1])
                    else:
                        yield dest_id, ('score', node['score'] * weight)

    def reduce_task(self, node_id, typed_values):
       
        node = {}
        total_score = 0
        prevScoreSet=False
        for value_type, value in typed_values:
            if value_type == 'node':
                node = value
                if not prevScoreSet:
                    node['prev_score'] = node['score']
                    prevScoreSet=True
            elif value_type == 'score':
                total_score += value
            else:
                raise Exception("Fishy business!!")
		
        d = 0.15
        node['score'] = 1 - d + d * total_score
	
        yield node_id, node

    def steps(self):
        return ([MRStep(mapper=self.map_task, reducer=self.reduce_task)] )


if __name__ == '__main__':
   	MRPageRank.run()