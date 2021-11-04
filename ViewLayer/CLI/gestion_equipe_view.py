from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session

class GestionEquipeView(AbstractView):

    def __init__(self, session : Session) -> None:
        self.__questions = [{'type': 'list','name': 'choix','message': 'Que voulez-vous faire ?',
                            'choices': ["1) Consulter le pot d'un agent", "2) Ajouter un agent dans l'équipe", '3) Supprimer un agent']}]

    def make_choice(self, session : Session)