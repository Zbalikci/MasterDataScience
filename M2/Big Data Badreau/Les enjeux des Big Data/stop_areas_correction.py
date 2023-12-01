import json
with open('stop_areas.json','r') as f:
    data=json.load(f)

from pprint import pprint
pprint(data)

print(type(data))
print(data.keys())
print(type(data['stop_areas']))
print(data['stop_areas'][0].keys())
print(data['stop_areas'][0]['coord'])

import pandas as pd
df = pd.DataFrame(columns=["nomGare","latitude","longitude"]) # création d'un dataframe vide à 3 colonnes

for gare in data['stop_areas'] :
    lat,lon = gare["coord"]["lat"],gare["coord"]["lon"]
    df.loc[len(df),] = [gare['name'],lat,lon]  # ajoute une ligne au dataframe

print("Résultats Question 4 :")
print(df, end="\n\n")
df.to_csv("ex1_out.csv", index=False)
print("Création du fichier : ex1_out.csv")