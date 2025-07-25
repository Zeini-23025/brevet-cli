# brevet-cli

`brevet-cli` est un outil en ligne de commande développé en Python pour l'analyse des résultats des élèves à l'examen du BEPC 2025.

Il permet aux utilisateurs d'explorer les données de manière interactive, de rechercher des élèves spécifiques, de consulter des statistiques globales et de générer des visualisations de données pertinentes.

## Caractéristiques

*   **Chargement des données** : Charge les résultats des élèves à partir d'un fichier CSV (`data/RESU_BEPC_2025_74821.csv`).
*   **Recherche d'élèves** :
    *   **Recherche avancée** : Trouvez un élève grâce à son `Num_Bepc` pour afficher toutes ses informations.
    *   **Recherche simple** : Trouvez un élève grâce à son `Num_Bepc` pour afficher son nom, sa moyenne et sa décision finale.
*   **Analyse statistique** :
    *   **Statistiques générales** : Calculez et affichez le nombre total d'élèves, le nombre d'admis, le taux de réussite global et la moyenne générale.
    *   **Statistiques groupées** : Affichez des statistiques groupées par `WILAYA` (département) ou par `Âge`.
*   **Visualisation des données** :
    *   Générez un diagramme circulaire montrant la répartition des décisions (par ex., "Admis", "Ajourné").
    *   Générez des diagrammes en barres montrant le taux de réussite par `WILAYA` et par `Âge`.
    *   Tous les graphiques sont sauvegardés dans le répertoire `fig/`.

## Prérequis

*   Python 3
*   La bibliothèque `matplotlib`. Si elle n'est pas installée, le script vous proposera de l'installer automatiquement.

## Utilisation

Pour lancer l'application, exécutez le script `student_analyzer.py` depuis votre terminal :

```bash
python student_analyzer.py
```

Cela lancera un menu interactif dans la console, vous permettant de choisir parmi les différentes fonctionnalités disponibles.


