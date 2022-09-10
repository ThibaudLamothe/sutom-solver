# Contexte 

Ce projet vise à résoudre de manière automatisée le jeu [SUTOM](https://sutom.nocle.fr/#) inspiré de Motus.


# Installation

- prérequis: installation de python
- prérequis: un environnement virtuel python avec les dépendances du projet

> `Optionnel`: installation d'anaconda/miniconda pour créer l'environnemnt virtuel comme indiqué ci-dessous. Vous pouvez aussi créer l'environnement virtuel avec la commande `python -m venv env` et l'activer avec `source env/bin/activate`.
  
```bash
git clone https://github.com/ThibaudLamothe/sutom-solver.git
cd sutom-solver
conda create -n sutom -y
conda activate sutom
conda install pip -y
pip install -r requirements.txt
```

> Si vous avez déjà créé et activé l'environnement virtuel, executez simplement ceci
```bash
git clone https://github.com/ThibaudLamothe/sutom-solver.git
cd sutom-solver
pip install -r requirements.txt
```

- A ce stade il ne reste plus qu'à télécharger le chromedriver
- Pour cela, rendez-vous sur [cette page](https://chromedriver.chromium.org/downloads) et téléchargez le chromedriver correspondant à **votre version de chrome**
- Le placer dans le dossier `sutom-solver`

- Ensuite, si c'est la première fois que vous utilisez chromedriver, il faut le valider (détail à venir #TODO)

# Execution 

### Bash
- Pour lancer le programme, il suffit de lancer le fichier `entrypoint.py` avec python

```
python entrypoint.py
```
- Le détail de l'exécution est affiché dans le terminal (dans un log dédié par jour, à venir #TODO)


### Jupyter Notebook
- Il est aussi possible d'exécuter le code depuis le notebook `execution.ipynb`
```
jupyter notebook
`ouvrir le fichier execution.ipynb
`run all
```

# Utilisation

- Initialisation
```python
# Imports de la classe principale
from src.selenium_sutom import SeleniumSutom

# Définition des chemins
words_path   = "../data/mots.txt"
chromedriver = "../chromedriver"
```

- Utilisation classique, résolution en utilisant à chaque tentative le mot qui a le plus en commun avec tous les autres (voir script [word_detection.py](../src/word_detection.py)) (résolution en 2 à 5 coups)
```python
# Standard
sutom = SeleniumSutom(driver_path=chromedriver, words_path=words_path)
sutom.run()
sutom.close_driver()
```

- Possibilité d'intervention humaine pour simplifier les derniers rounds (résolution en 2 à 3 coups)
```python
# Standard - Aide Humain
sutom = SeleniumSutom(driver_path=chromedriver, words_path=words_path, humain=True)
sutom.run()
sutom.close_driver()
```

- Possibilité de détection des mots éligibles en se connectant au site de Larousse (long et élimine parfois le bon mot => la fonctionnalité a été créée mais n'est n'est pas très utile à l'usage...)
```python
# Standard - Aide Larousse
sutom = SeleniumSutom(driver_path=chromedriver, words_path=words_path, larousse=True)
sutom.run()
sutom.close_driver()
```

- De la bonne grosse triche comme on aime. Se base sur le fait qu'il est possible de retrouver la solution dans le corps HTML de la page. (résolution en 1 coup)
```python
# Hack
sutom = SeleniumSutom(driver_path=chromedriver, words_path=words_path)
sutom.run_hack()
import time ; time.sleep(30)
sutom.close_driver()
```

# Ressources complémentaires
- [Liste des mots utilisés par l'app](https://framagit.org/JonathanMM/sutom/-/raw/main/ts/mots/listeMotsProposables.ts)
- [Repo](https://framagit.org/JonathanMM/sutom/-/tree/main/ts) de l'app SUTOM réalisée par [JonathanMM](https://framagit.org/JonathanMM)
