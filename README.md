# PSyCoQuAC
Projet de SYstème COllaboratif de QUalification d'Adresses Collectées

PSycoQuAC est un système collaboratif permettant de traiter des lots d'adresses postales françaises et de les qualifier en vérifiant leur existence et en les géolocalisant de manière précise grâce aux données de la [Base Adresse Nationale](https://adresse.data.gouv.fr/).

## Français
*For english version, please read [below](#english)*

### Installation

#### Depuis les binaires
Pour installer PSyCoQuAC depuis ses binaires, il suffit de télécharger la distribution compatible avec votre système, puis de la décompresser et de lancer l'exécutable dans le dossier PSyCoQuAC :
* PSyCoQuAC.exe pour Windows (10/11) 64 bits (amd64)
* PSyCoQuAC pour macOS Intel (x86_64)

#### Via l'interpréteur Python
Si vous avez une installation fonctionnelle de Python 3.8 ou 3.9 et de pip sur votre système, vous pouvez également l'utiliser pour exécuter PSyCoQuAC depuis les sources :

```
git clone 
cd PSyCoQuAC
pip install -r requirements.txt
python main.py
```

Dans la mesure où l'application dépend de PyInquirer qui se base sur des librairies figées dans des versions anciennes (d'où l'incompatibilité avec Python 3.10), il est recommandé d'utiliser un environnement virtuel (venv) pour l'exécuter avec cette méthode.

### Configuration

#### Avec l'assistant automatique de configuration
Si aucun fichier de configuration n'est détecté, PSyCoQuAC propose un assistant automatique d'installation lors de son lancement. Vous pouvez l'utiliser à condition de posséder les droits en écriture sur le dossier dans lequel se trouve l'exécutable ou la racine du code source.

Il vous permettra de configurer une nouvelle installation ou de vous connecter à une installation existante. PSyCoQuAC supporte actuellement les systèmes de base de données PostgreSQL et SQLite. Pour PostgreSQL, vous devez avoir des accès à la base de données avec les privilèges CREATE, SELECT, INSERT, UPDATE et DELETE.

#### En créant manuellement un fichier de configuration
Vous pouvez également créér manuellement un fichier de configuration pour paramétrer l'application. Pour cela, vous devez créér un fichier ".env" à l'emplacement de l'exécutable ou du fichier main.py (touch .env), et le documenter de la manière suivante :

```
PSYCOQUAC_ENGINE='PostgreSQL ou SQLite'
PSYCOQUAC_HOST='chemin/nom d'hôte de la base de données'
PSYCOQUAC_PORT='port de connexion à la base de données, vide pour SQLite'
PSYCOQUAC_DATABASE='nom de la base de données, vide pour SQLite'
PSYCOQUAC_USER='nom d'utilisateur de connexion à la base de données, vide pour SQLite'
PSYCOQUAC_PASSWORD='mot de passe de connexion à la base de données, vide pour SQLite'
```

Si nécessaire, les scripts de configuration au format .SQL pour chaque type de base de données sont disponibles dans le dossier /sql de l'exécutable ou des sources.

Toutefois, il est recommandé de n'utiliser cette méthode que pour se connecter à une base de données existante, car elle ne permet pas à l'heure actuelle de créer le premier superviseur et vous devrez l'insérer manuellement dans la base de données, via une requête SQL du type :

```
INSERT INTO agents(est_superviseur, quotite, nom_utilisateur, mot_de_passe, prenom, nom)
VALUES (1, 1.0, nom_utilisateur, mot_de_passe, prenom, nom);
```

Dans ce cas, vous devrez notamment vous assurer d'enregistrer dans mot_de_passe une chaîne salée avec nom_utilisateur en préfixe et hashée avec l'algorithme SHA-512.

## English
*Voir [ci-dessus](#franais) pour la version française*

#### From binaries
To install PSyCoQuAC from its binaries, simply download the distribution compatible with your system, then unpack it and run the executable in the PSyCoQuAC folder:
* PSyCoQuAC.exe for Windows (10/11) 64-bit (amd64)
* PSyCoQuAC for macOS Intel (x86_64)

#### Via the Python interpreter
If you have a working installation of Python 3.8 or 3.9 and pip on your system, you can also use it to run PSyCoQuAC from the sources :

```
git clone 
cd PSyCoQuAC
pip install -r requirements.txt
python main.py
```
Since the application depends on PyInquirer which is based on libraries frozen in old versions (hence the incompatibility with Python 3.10), it is recommended to use a virtual environment (venv) to run it with this method.

### Configuration

#### With the automatic configuration wizard
If no configuration file is detected, PSyCoQuAC offers an automatic setup wizard when it is launched. You can use this wizard if you have write access to the folder where the executable is located or the root of the source code.

It will allow you to set up a new installation or connect to an existing one. PSyCoQuAC currently supports PostgreSQL and SQLite database systems. For PostgreSQL you need to have access to the database with CREATE, SELECT, INSERT, UPDATE and DELETE privileges.

#### By creating a configuration file manually
You can also manually create a configuration file to set up the application. To do this, you must create a ".env" file in the location of the executable or main.py file (touch .env), and document it as follows:

```
PSYCOQUAC_ENGINE='PostgreSQL or SQLite
PSYCOQUAC_HOST='path/hostname of the database'
PSYCOQUAC_PORT='database connection port, empty for SQLite'
PSYCOQUAC_DATABASE='database name, empty for SQLite'
PSYCOQUAC_USER='database connection username, empty for SQLite'
PSYCOQUAC_PASSWORD='database login password, empty for SQLite'
```

If necessary, the configuration scripts in .sql format for each type of database are available in the /sql folder of the executable or sources.

However, it is recommended to use this method only to connect to an existing database, as it does not currently allow you to create the first supervisor and you will have to insert it manually into the database, with this SQL query :

```
INSERT INTO agents(est_superviseur, quotite, nom_utilisateur, mot_de_passe, prenom, nom)
VALUES (1, 1.0, username, password, first_name, last_name);
```

In this case, you will have to make sure to record as password a salted string with username as prefix and hashed with the SHA-512 algorithm.

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
