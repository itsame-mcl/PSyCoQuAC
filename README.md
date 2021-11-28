# PSyCoQuAC
Projet de SYstème COllaboratif de QUalification d'Adresses Collectées

PSycoQuAC est un système collaboratif permettant de traiter des lots d'adresses postales françaises et de les qualifier en vérifiant leur existence et en les géolocalisant de manière précise grâce aux données de la [Base Adresse Nationale](https://adresse.data.gouv.fr/).

## Installation

### Depuis les binaires
Pour installer PSyCoQuAC depuis ses binaires, il suffit de télécharger la distribution compatible avec votre système, puis de la décompresser et de lancer l'exécutable dans le dossier PSyCoQuAC :
* PSyCoQuAC.exe pour Windows (10/11) 64 bits (amd64)
* PSyCoQuAC pour macOS Intel (x86_64)
* PSyCoQuAC pour Linux 64 bits (64bit_intel)

### Via l'interpréteur Python
Si vous avez une installation fonctionnelle de Python 3.8 ou 3.9 et de pip sur votre système, vous pouvez également l'utiliser pour exécuter PSyCoQuAC depuis les sources :

```
git clone https://github.com/maxence-lagalle/PSyCoQuAC.git
cd PSyCoQuAC
pip install -r requirements.txt
python main.py
```

Dans la mesure où l'application dépend de PyInquirer qui se base sur des librairies figées dans des versions anciennes (d'où l'incompatibilité avec Python 3.10), il est recommandé d'utiliser un environnement virtuel (venv) pour l'exécuter avec cette méthode.

## Configuration

### Avec l'assistant automatique de configuration
Si aucun fichier de configuration n'est détecté, PSyCoQuAC propose un assistant automatique d'installation lors de son lancement. Vous pouvez l'utiliser à condition de posséder les droits en écriture sur le dossier dans lequel se trouve l'exécutable ou la racine du code source.

Il vous permettra de configurer une nouvelle installation ou de vous connecter à une installation existante. PSyCoQuAC supporte actuellement les systèmes de base de données PostgreSQL et SQLite. Pour PostgreSQL, vous devez avoir des accès à la base de données avec les privilèges CREATE, SELECT, INSERT, UPDATE et DELETE.

### En créant manuellement un fichier de configuration
Vous pouvez également créér manuellement un fichier de configuration pour paramétrer l'application. Pour cela, vous devez créér un fichier ".env" à l'emplacement de l'exécutable ou du fichier main.py (touch .env), et le documenter de la manière suivante :

```
PSYCOQUAC_ENGINE='PostgreSQL ou SQLite'
PSYCOQUAC_HOST='chemin/nom d'hôte de la base de données'
PSYCOQUAC_PORT='port de connexion à la base de données, vide pour SQLite'
PSYCOQUAC_DATABASE='nom de la base de données, vide pour SQLite'
PSYCOQUAC_USER='nom d'utilisateur de connexion à la base de données, vide pour SQLite'
PSYCOQUAC_PASSWORD='mot de passe de connexion à la base de données, vide pour SQLite'
```

Si nécessaire, les scripts de configuration au format .sql pour chaque type de base de données sont disponibles dans le dossier /sql de l'exécutable ou des sources.

Une fois lancée, l'application proposera automatiquement de créer le premier superviseur.
Si vous le souhaitez, vous pouvez l'insérer manuellement dans la base de données, via une requête SQL du type :

```
INSERT INTO agents(est_superviseur, quotite, nom_utilisateur, mot_de_passe, prenom, nom)
VALUES (1, 1.0, nom_utilisateur, mot_de_passe, prenom, nom);
```

Dans ce cas, vous devrez enregistrer dans mot_de_passe une chaîne salée avec nom_utilisateur en préfixe et hashée avec l'algorithme SHA-512.

```
                              ,-'   ,"",
                             / / ,-'.-'
                   _,..-----+-".".-'_,..
           ,...,."'             `--.---'
         /,..,'                     `.
       ,'  .'                         `.
      j   /                             `.
      |  /,----._           ,.----.       .
     ,  j    _   \        .'  .,   `.     |
   ,'   |        |  ____  |         | ."--+,^.
  /     |`-....-',-'    `._`--....-' _/      |
 /      |     _,'          `--..__  `        '
j       | ,-"'    `    .'         `. `        `.
|        .\                        /  |         \
|         `\                     ,'   |          \
|          |                    |   ,-|           `.
.         ,'                    |-"'  |             \
 \       /                      `.    |              .
  ` /  ,'                        |    `              |
   /  /                          |     \             |
  /  |                           |      \           /
 /   |                           |       `.       _,
.     .                         .'         `.__,.',.----,
|      `.                     ,'             .-""      /
|        `._               _.'               |        /
|           `---.......,--"                  |      ,'
'                                            '    ,'
 \                                          /   ,'
  \                                        /  ,'
   \                                      / ,'
    `.                                   ,+'
      >.                               ,'
  _.-'  `-.._                      _,-'-._
,__          `",-............,.---"       `.
   \..---. _,-'            ,'               `.
          "                '..,--.___,-"""---' mh
          ```
