# Initiation à la recherche

## Description du travail effectué

Notre objectif a été d'implémenter la subdivision d'un pavage hyperbolique afin d'y construire un code quantique similaire au code torique. Nous avons ensuite pu simuler l'apparition d'erreurs sur ce code pour appliquer un algorithme de décodage et ainsi évaluer les performances des codes obtenus.

## Programmes réalisés

### toric.py

Ce programme permet de générer un code torique de la taille voulue et de lancer une simulation sur celui-ci.

Le programme toric.py nécessite des arguments nécessaires au lancement, voici la liste des arguments possibles :

- L : Largeur de notre code torique (nombre de faces). Type attendu : int. L > 0.
- pErrorX : Probabilité d'erreur physique X. Type attendu : float. pErrorX dans [0,1].
- pErrorZ : Probabilité d'erreur physique Z. Type attendu : float. pErrorZ dans [0,1].
- -P : Activer l'affichage Matplotlib. Optionnel.
- -V : Activer l'affichage des résultats intermédiaires. Optionnel.
- -M : Permet de placer des erreurs physiques manuellement au lieu de les générer avec la fonction de bruit. Optionnel.

### stats.py

Ce programme permet de générer un code de surface choisi et de réaliser une batterie de simulations sur celui-ci.

Le programme stats.py nécessite également des arguments nécessaires au lancement, voici la liste des arguments possibles :

- L : Largeur de notre code de surface (nombre de faces). Type attendu : int. L > 0.
- n : Nombre d'itérations par probabilité d'erreur physique. Type attendu : int. n > 0.
- pStep : Le pas de probabilité d'erreur physique.  Type attendu : float. pStep dans ]0,1[.
- pMax : Probabilité maximale d'erreur physique. Type attendu : float. pMax dans ]pStep,1[.
- -S : Activer la subdivision, dans le cas contraire, on génère un code torique.
- -l : Nombre de subdivisions à effectuer par face. (Ignoré si -S non-présent). Type attendu : int. l > 0. Nécessaire si -S présent.
- -lm : Nombre de subdivisions maximal à effectuer par face. (Ignoré si -S non-présent). Type attendu : int. lm > l.  Optionnel.
- -o : Ecrit  les résultats obtenus en format Tikz pour LaTeX dans le fichier spécifié. Type attendu : string. Chemin du fichier de sortie. Optionnel.
- -P : Activer l'affichage Matplotlib. Optionnel.
- -V : Activer l'affichage des résultats intermédiaires. Optionnel.
