# Les attaques de requin dans le monde depuis 1800

## Introduction

Dans le jeu de données que nous allons analyser, les données fournies nous renseignent sur les attaques de requins recensées dans le monde depuis 1800. Les données sont, selon toute vraisemblance, rentrées manuellement dans le jeu de données, un nettoyage approfondi est donc nécessaire pour plusieurs catégories. Les données disponible pour chaque observation sont:

| Donnée | Description |
| ------ | ------ |
| Date | La date de l'incident |
| Year | L'année de l'incident |
| Type | L'origine de l'incident (provoqué ou non provoqué) |
| Country | Pays |
| Area | État ou département |
| Location | Lieu précis (ville, plage, ...) |
| Activity | Activité faite par la victime lors de l'attaque (plongée, peche, ...) |
| Name | Nom de la victime |
| Sex | Sexe de la victime |
| Age | Age de la victime |
| Injury | Blessure précise de la victime |
| Fatal (Y/N) | Si l'incident a été fatal ou non |
| Time | Heure de l'incident |
| Species | Espèce du requin |

D'autres données sont disponibles comme l'id de l'incident ou la source du rapport, mais nous ne les utiliserons pas ici. Les données proviennent de ce [site web ](https://www.kaggle.com/datasets/felipeesc/shark-attack-dataset)

## User Guide

http://127.0.0.1:8050/
?
##  Rapport d’analyse

#### "Years"
Dans l'onglet "Years", on peut observer l'évolution du nombre d'attaques de requins par année, et l'on remarque que ce nombre est en constante croissance, avec un pic important vers les années 60, qu'on peut peut-être associer à l'augmentation de la fréquentation des plages ou au développement de l'industrie de la pêche. On peut aussi supposer que des campagnes de sensibilisation et des réglementations mises en place sont responsables de la chute de ce pic. L'augmentation importante depuis les années 90 est probablement due aux mêmes facteurs, on doit cependant nuancer cela avec le fait qu'avec l'arrivée d'internet et la démocratisation du téléphone portable, il est bien plus facile de signaler les incidents.

#### "Gender"
Sur le deuxième graphique, on remarque que la grande majorité des victimes d'attaques de requin (80%) sont des hommes. 

#### "Not fatal attack"
Pour le troisième graphique, qui consiste de deux bar graphs, on peut observer les attaques.
Lorsque l’on choisit ‘fatal attack’, on observe le nombre d’attaque fatale(qui induit le décès de la personne) en fonction de l’espèce de requin : on remarque que le requin tigre est le plus meurtrier. Si on choisit ‘not fatal attack’, on observe le nombre d’attaque non fatale(qui induit au maximum une blessure) en fonction de l’espèce de requin : on voit beaucoup de requins entre 1 et 2 mètres de long (la taille assez globale de requin), mais l’espèce de requin n’est pas spécifiée. L’espèce de requin connue qui attaque le plus est aussi le requin tigre.

#### "Activity"
Sur ce graphique, un bar graph, on peut observer quelles étaient les activités pratiquées par les victimes lors de chaque attaque, lorsque c'est renseigné. Sans surprise, c'est la pêche qui est responsable d'une écrasante majorité des attaques.

#### "Shark attack map"
Ce graphique permet de représenter sur une carte du monde les différentes attaques de requins par pays à travers le monde. On peut alors observer que la plupart des attaques de requins sont subies dans trois pays, à savoir les États-Unis, l'Australie et l'Afrique du Sud. 
On peut aussi observer que la quasi-totalité des pays bordant une mer ou un océan ont subi au moins une attaque.
Il y a sur cet onglet un menu déroulant permettant de naviguer entre la carte du monde et celles des États-Unis, de l'Australie et de l'Afrique du Sud, et sur chacune d'entre elles, on observe que les attaques sont généralement concentrées sur quelques États/Département à éviter. On notera particulièrement que la Floride, aux États-Unis, subit près de 20% des attaques recensées (~18,6%).

#### "Time"
Il y a deux graphiques sur la temporalité des attaques. Le premier est un histogramme montrant le nombre d’attaque par heure, avec un pic à 11h mais le taux est aussi élevé durant l’après-midi. Cela se traduit peut-être par le fait que c’est à ces heures-là que les personnes sortent le plus en mer, et non à ces heures-là que les requins attaquent le plus. Le deuxième graphique est un camembert qui appuie ces observations plus visuellement, avec plus de 50% des attaques se déroulant durant l’après-midi. 

#### "Attacks by age"

Ce dernier graphique est un histogramme montrant les attaques selon l’âge des victimes. Il y a une checkbox qui, appuyée permet de montrer les détails de si ces attaques ont été meurtrières ou non. 

## Developer Guide

u
