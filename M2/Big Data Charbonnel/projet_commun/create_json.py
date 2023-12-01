#!/bin/env python3
import json
import os

topics = {'tensorflow' : {'definition': ['https://www.tensorflow.org/?hl=fr', 'https://fr.wikipedia.org/wiki/TensorFlow'],
                          'tuto': ['https://www.tensorflow.org/tutorials?hl=fr', 'https://www.tensorflow.org/tutorials/quickstart/beginner?hl=fr','https://www.datacamp.com/tutorial/tensorflow-tutorial'],
                        'forum': ['https://discuss.tensorflow.org/', 'https://discuss.tensorflow.org/c/general-discussion/6']},
          'pytorch' :{'definition': ['https://pytorch.org/', 'https://fr.wikipedia.org/wiki/PyTorch'],
                        'tuto': ['https://pytorch.org/tutorials/', 'https://pytorch.org/tutorials/beginner/pytorch_with_examples.html'],
                       'learning video': ['https://www.youtube.com/watch?v=Z_ikDlimN6A', 'https://www.youtube.com/watch?v=V_xro1bcAuA']},
          'multiprocesing' : {'definition': ['https://docs.python.org/3/library/multiprocessing.html', 'https://superfastpython.com/multiprocessing-in-python/'],
                              'tuto': ['https://www.datacamp.com/tutorial/python-multiprocessing-tutorial', 'https://tutorialedge.net/python/python-multiprocessing-tutorial/'],
                              'video': ['https://www.youtube.com/watch?app=desktop&v=PcJZeCEEhws&pp=ygUWI211bHRpcHJvY2Vzc2luZ21vZHVsZQ%3D%3D', 'https://www.youtube.com/watch?v=AZnGRKFUU0c'],},
          'web_scraping' :{'guide': ['https://realpython.com/python-web-scraping-practical-introduction/', 'https://brightdata.com/blog/how-tos/web-scraping-with-python'],
                            'tuto' : ['https://oxylabs.io/blog/python-web-scraping','https://www.geeksforgeeks.org/python-web-scraping-tutorial/'],
                            'video': ['https://www.youtube.com/watch?v=8dTpNajxaH0', 'https://www.youtube.com/watch?app=desktop&v=XVv6mJpFOb0'],}}

os.mkdir('dataset')
current_dir = os.getcwd()
dataset = f"{current_dir}/dataset"

with open(f"{dataset}/mydata.json", "w") as f:
    json.dump(topics, f)

annuaire = ["http://172.20.45.168:5000","http://172.20.45.176:5000","http://172.20.45.178:5000"]

with open(f"{dataset}/annuaire.json", "w") as f:
    json.dump(annuaire, f)

with open(f"{dataset}/data_commun.json", "w") as f:
    json.dump(topics, f)