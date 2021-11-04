from PyInquirer import prompt
from ViewLayer.CLI.session import Session
from ViewLayer.CLI import ModifierView as modif

class ModifierCompteView:

    def __init__(self, session : Session) -> None:
        self.__questions = [{'type': 'list','name': 'choix','message': 'Quelle(s) information(s) souhaitez-vous modifier ?',
                        'choices': ['1) Prénom', '2) Nom','3) Quotité de travail',"4) Nom d'utilisateur",'5) Mot de passe']}]

    def modifier(self, session: Session):
        answers = prompt(self.__questions)
        if '1' in answers['choix']:
            return modif.ModifierPrenomView(session)
        elif '2' in answers['choix']:
            return modif.ModifierNomView(session)
        elif '3' in answers['choix']:
            return modif.ModifierQuotiteoView(session)
        elif '4' in answers['choix']:
            return modif.ModifierUtilView(session)
        elif '5' in answers['choix'] :
            return modif.ModifierMDPView(session)