README – Projet DataViz
Répartition des ressources et charge de travail
1. Objectif du projet

Ce projet vise à analyser la répartition de la charge de travail entre les centres, phases de projet, modules et postes de l’organisation. L’objectif est de fournir un tableau de bord permettant d’identifier les zones de surcharge ou de sous-activité et d’aider les responsables à mieux allouer leurs ressources.

2. Données utilisées

Source : fichier data_complet_v2.xlsx contenant environ 7 800 lignes.
Colonnes principales :

Centre

NOM_SI (module)

Types_phases

utilisateur_id2 (poste)

ChargeTotaleEstimee

ChargeTotaleActualisee

Les données ont été nettoyées, standardisées et agrégées avant d’être utilisées dans Tableau Public.

3. Méthodologie

Le projet est structuré en trois notebooks :

Notebook 01 – EDA : audit des données, analyses univariées et bivariées, validation des hypothèses.

Notebook 02 – Préparation : nettoyage approfondi, calcul des indicateurs (écart, surcharge), création des agrégations et export final.

Notebook 03 – Pipeline : construction d’un pipeline complet, génération d’un script Python et d’un exécutable (.exe).

4. Indicateurs produits

Charge estimée et réelle

Écart de charge

Taux de surcharge (%)

Charge par centre, phase, module, poste

Tables Centre × Phase et Module × Phase

Fichier final généré : data_aggregations.xlsx.

5. Tableau de bord Tableau Public

Le tableau de bord contient :

KPI principaux (surcharge globale, centres en surcharge)

Charge par centre

Répartition par phase

Top 5 modules les plus consommateurs

Matrice centre × phase

Filtre interactif par centre

6. Livrables

Notebooks 01, 02, 03

Script Python : 03_Application_Client.py

Fichier export : data_aggregations.xlsx

Tableau de bord Tableau Public

Application client .exe (non versionnée sur GitHub)

7. Limitations et pistes d’amélioration

Charges nulles pouvant influencer certains ratios

Absence d’information temporelle

Absence des compétences des utilisateurs

Possibilité de développer un modèle prédictif ou une analyse en continu
