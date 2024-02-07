# Utilisation des fichiers

## ETAPE 1

Téléchargez les fichiers Python et le dossier "templates" dans un même répertoire.

## ETAPE 2

Exécutez le fichier 'create_json.py' (à l'aide de la commande python create_json.py depuis le terminal) qui va créer un dossier nommé "dataset" contenant les données de départ (3 topics avec environ 3 items) et un fichier 'annuaire.json' qui contiendra le seul serveur que j'avais au départ.

## ETAPE 3

Exécutez le fichier 'recup_data.py' qui mettra à jour les données de départ en récupérant l'annuaire et les données des serveurs qui se trouvaient dans le fichier 'annuaire.json'.

## ETAPE 4

Exécutez le fichier 'serveur.py' pour vérifier l'apparence de l'application web dont l'URL est : http://127.0.0.1:5000 ou http://127.0.0.1:5000/ws

## Remarque :

Exécutez le fichier 'recup_data.py' plusieurs fois à la suite pour récupérer tous les serveurs participant au projet et mettre à jour les données.

# Explication de l'organisation des données

    - 'mydata.json' contient mes données de départ.
    - 'ip_adress.json' contient les données provenant des autres participants au projet. Ainsi, en mémorisant les serveurs déjà visités et en écrasant les anciennes données par les nouvelles, on pouvait suivre les modifications ou corrections apportées au contenu de leur application web.
    - 'data_commun.json' contient les données mises en commun aussi proprement que possible, provenant des autres participants au projet.

Même si ce n'est pas parfait, j'ai essayé de corriger les erreurs (ou même de ne pas les intégrer dans 'data_commun.json') des autres participants au projet, telles que les dictionnaires mal écrits, les URLs sous format str plutôt que dans une liste, ou encore les "URLs" considérées comme telles alors qu'elles ne le sont pas (exemple : "tuto" dans la liste d'URLs d'un item). 

Normalement, les doublons ont aussi été gérés, de tel sorte que si un autre item provient d'un autre participant, il est ajouté dans le topic correspondant. Si c'est le même item du même topic, on vérifie s'il y a des URLs manquantes dans 'data_commun.json'.

Je n'ai pas géré ni les accents ni les cas où c'était le même topic mais écrit différemment, tel que "web_scraping", "scraping" ou "functions" et "fonctions".