from PyInquirer import prompt
from DataLayer.DAO.db_connexion import DBConnexion  # Entorse à la séparation des couches, pour éviter de surcharger
#                                                       l'architecture d'un service d'installation
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.nouvel_utilisateur_view import NouvelUtilisateurView
import ViewLayer.CLI.menu as mp
from pathlib import Path
import dotenv
import os


class SetupView(AbstractView):
    def __init__(self) -> None:
        self.__first_try = True
        self.__choix_installation = None
        self.__questions = [{'type': 'list', 'name': 'nouvelle_installation', 'message': 'Que souhaitez-vous faire ?',
                             'choices': ["Créer une nouvelle installation PSyCoQuAC",
                                         "Se connecter à une installation PSyCoQuAC existante"],
                             'default': 'Créer une nouvelle installation PSyCoQuAC',
                             'filter': lambda val: self.__install_filter(val),
                             'when': lambda ans: self.__first_try},
                            {'type': 'list', 'name': 'engine', 'message': 'Quel est le moteur de '
                                                                          'base de données à utiliser ?',
                             'choices': ["PostgreSQL", "SQLite"], 'default': 'PostgreSQL'},
                            {'type': 'input', 'name': 'host', 'message': "Quel est le chemin/l'hôte "
                                                                         "de la base de données ?"},
                            {'type': 'input', 'name': 'port', 'message': 'Quel est le port de connexion ?',
                             'when': lambda ans: ans['engine'] == 'PostgreSQL'},
                            {'type': 'input', 'name': 'database', 'message': 'Quel est le nom de la base de données ?',
                             'when': lambda ans: ans['engine'] == 'PostgreSQL'},
                            {'type': 'input', 'name': 'user', 'message': "Quel est le nom d'utilisateur permettant de "
                                                                         "se connecter à la base de données\n(il doit "
                                                                         "posséder les privilèges CREATE, SELECT, "
                                                                         "INSERT, UPDATE et DELETE) ?",
                             'when': lambda ans: ans['engine'] == 'PostgreSQL'},
                            {'type': 'password', 'name': 'password', 'message': 'Quel est le mot de passe '
                                                                                'de connexion à la base de données ?',
                             'when': lambda ans: ans['engine'] == 'PostgreSQL'},
                            ]

    @staticmethod
    def __install_filter(val) -> bool:
        if val == "Créer une nouvelle installation PSyCoQuAC":
            return True
        elif val == "Se connecter à une installation PSyCoQuAC existante":
            return False

    def make_choice(self):
        answers = {}
        connexion_ok = False
        while not connexion_ok:
            answers = prompt(self.__questions)
            if self.__first_try:
                self.__choix_installation = answers['nouvelle_installation']
            Path(".env").touch(exist_ok=True)
            dotenv_file = dotenv.find_dotenv()
            dotenv.load_dotenv(dotenv_file, override=True)
            os.environ["PSYCOQUAC_ENGINE"] = str(answers.get('engine', ""))
            dotenv.set_key(dotenv_file, "PSYCOQUAC_ENGINE", str(answers.get('engine', "")))
            os.environ["PSYCOQUAC_HOST"] = str(answers.get('host', ""))
            dotenv.set_key(dotenv_file, "PSYCOQUAC_HOST", str(answers.get('host', "")))
            os.environ["PSYCOQUAC_PORT"] = str(answers.get('port', ""))
            dotenv.set_key(dotenv_file, "PSYCOQUAC_PORT", str(answers.get('port', "")))
            os.environ["PSYCOQUAC_DATABASE"] = str(answers.get('database', ""))
            dotenv.set_key(dotenv_file, "PSYCOQUAC_DATABASE", str(answers.get('database', "")))
            os.environ["PSYCOQUAC_USER"] = str(answers.get('user', ""))
            dotenv.set_key(dotenv_file, "PSYCOQUAC_USER", str(answers.get('user', "")))
            os.environ["PSYCOQUAC_PASSWORD"] = str(answers.get('password', ""))
            dotenv.set_key(dotenv_file, "PSYCOQUAC_PASSWORD", str(answers.get('password', "")))
            try:
                DBConnexion().connexion.cursor().close()
                connexion_ok = True
            except ConnectionError:
                print("Impossible d'établir la connexion à la base de données. Veuillez resaisir les paramètres.")
                self.__first_try = False
                connexion_ok = False
                DBConnexion.clear()
                try:
                    Path(".env").unlink()
                except FileNotFoundError:
                    pass
        if self.__choix_installation:
            prompt_confirm = [{'type': 'confirm', 'name': 'confirmer', 'message': "Confirmez-vous le lancement d'une "
                                                                                  "nouvelle installation ?\nTOUTES LES "
                                                                                  "INFORMATIONS RELATIVES A UNE "
                                                                                  "INSTALLATION PRECEDENTE DANS LA "
                                                                                  "MEME "
                                                                                  "BASE SERONT PERDUES !",
                               'default': False}]
            confirm = prompt(prompt_confirm)
            if confirm['confirmer']:
                curseur = DBConnexion().connexion.cursor()
                if answers['engine'] == "PostgreSQL":
                    curseur.execute(open("sql/postgresql.sql", "r").read())
                elif answers['engine'] == "SQLite":
                    curseur.executescript(open("sql/sqlite.sql", "r").read())
                    DBConnexion().connexion.commit()
                curseur.close()
                print("Configuration de la base de données terminée. Création du premier superviseur :")
                succes = NouvelUtilisateurView(on_setup=True).make_choice()
            else:
                succes = False
                try:
                    Path(".env").unlink()
                except FileNotFoundError:
                    pass
        else:
            succes = True
        if succes:
            return mp.MenuPrincipalView()
        else:
            return SetupView()
