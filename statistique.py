import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# On importe le fichier .csv en tant que DataFrame
census = pd.read_csv('Census_2016_2021.csv', index_col = 0)

# On conserve uniquement les municipalités
census_filtre = census[census['Type'] == 'MÉ']

# On calcule le nombre de municipalités, puis on montre cette donnée à l'utilisateur
nombre_de_municipalite = len(census_filtre)
print('Il y a ', nombre_de_municipalite, ' minucipalités dans le census 2016 - 2021.')

# On trouve le population moyenne des municipalités en 2016 et en 2021, puis on montre les données à l'utilisateur
population_moyenne_2016 = int(census_filtre[['Pop16']].mean().values[0] + 0.5)
population_moyenne_2021 = int(census_filtre[['Pop21']].mean().values[0] + 0.5)
print('La population moyenne des municipalités en 2016 était de ', population_moyenne_2016, ' habitants.')
print('La population moyenne des municipalités en 2021 était de ', population_moyenne_2021, ' habitants.')

# On calcule la croissance de chaque municipalité
croissance = census_filtre['Pop21'] / census_filtre['Pop16']
croissance.index = census_filtre['Pop21']

# On définit nos barèmes au cas où on voudrait les changer plus tard
bareme_petit = 2000
bareme_moyen = 10000
bareme_grand = 25000
bareme_tres_grand = 100000

# On créé des Series qui contiennent les municipalités correspondant à chaque catégorie
tres_petites_municipalites = census_filtre[census_filtre['Pop21'] < bareme_petit]
petites_municipalites = census_filtre[(census_filtre['Pop21'] >= bareme_petit) & (census_filtre['Pop21'] < bareme_moyen)]
moyennes_municipalites = census_filtre[(census_filtre['Pop21'] >= bareme_moyen) & (census_filtre['Pop21'] < bareme_grand)]
grandes_municipalites = census_filtre[(census_filtre['Pop21'] >= bareme_grand) & (census_filtre['Pop21'] < bareme_tres_grand)]
tres_grandes_municipalites = census_filtre[census_filtre['Pop21'] >= bareme_tres_grand]

# On définit quelques paramètres pour le graphique
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 150
figure_trace = plt.figure()

# On trace le nuage de points
croissance_trace = figure_trace.add_subplot(121)
plt.scatter(croissance.index, croissance.values)
plt.xlabel('Population en 2021')
plt.ylabel('Croissance entre 2016 et 2021')
plt.grid()
plt.title('Croissance de la population entre 2016 et 2021\nselon le nombre d\'habitants en 2021')

# On définit les axes du graphique à bars
categories = ["< "+str(bareme_petit), "< "+str(bareme_moyen),"< "+str(bareme_grand),"< "+str(bareme_tres_grand),"≥ "+str(bareme_tres_grand)]
nombre_de_municipalites_par_categorie = [len(tres_petites_municipalites), len(petites_municipalites), len(moyennes_municipalites),
     len(grandes_municipalites), len(tres_grandes_municipalites)]

# On trace le graphique à bars
taille_trace = figure_trace.add_subplot(122)
plt.bar(categories, nombre_de_municipalites_par_categorie)
plt.xlabel("Catégorie")
plt.ylabel("Nombre de municipalités")
taille_trace.set_yscale('log')
plt.ylim(1, 2*bareme_tres_grand)
plt.grid()
plt.title("Nombre de municipalités rangées par catégorie de taille")


# On dessine la valeur du nombre de municipalités par catégorie, et si elle est égale à 0 on la dessine avec un offset
alignement_y = 1.2
for i in range(len(categories)):
    if nombre_de_municipalites_par_categorie[i] != 0:
        plt.text(i,nombre_de_municipalites_par_categorie[i]*alignement_y,str(nombre_de_municipalites_par_categorie[i]),
                 ha='center')
    else:
        plt.text(i, alignement_y, str(nombre_de_municipalites_par_categorie[i]), ha='center')


# On maximise la fenêtre et on montre le graphique
# (Peut faire planter le programme si vous n'utilisez pas Windows)
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
plt.show()