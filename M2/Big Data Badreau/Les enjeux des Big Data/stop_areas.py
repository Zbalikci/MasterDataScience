#!/bin/env python3

import json
import pprint
import pandas as pd

with open("stop_areas.json",'r') as file:
    data = json.load(file)
    print(data)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(data['stop_areas'])

nom_gare=[]
longitude=[]	
latitude=[]

for k in range(len(data['stop_areas'])):
    nom_gare.append(data['stop_areas'][k]['name'])
    longitude.append(data['stop_areas'][k]['coord']['lon'])
    latitude.append(data['stop_areas'][k]['coord']['lat'])

dict={'nom de la gare':nom_gare,'longitude':longitude,'latitude':latitude}

df=pd.DataFrame(dict)
print(df)
#df.to_csv('ex1.csv', encoding='utf-8',index=False)
