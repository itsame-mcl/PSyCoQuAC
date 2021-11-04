class Accueil(AbstractView):
def __initi__(self):
# Définition d'une variable qui va stocker notre ou nos interactions
self.questions = [
{
'type': 'list', # Il faut choisir dans un liste de choix,
alors le type est "list", d'autres sont possibles. Pour plus de choix allez
voir la documentation officielle
'name': 'authentification', # Le nom de la question. C'est
comme ça qu'on retrouvera la réponse
'message': 'Bonjour', # Un message à afficher avant de
proposer les choix. Cela peut-être une question
'choices': [
'Me créer un compte', # choix 1
Separator(), # une ligne de séparation
'Me connecter', # choix 2
]
}
]
def display_info(self):
"""
Permet d'afficher des infos en console. On va mettre ici la partie
non intéractive de la page
"""
# Récupération de la banière de notre application
with open('assets/banner.txt', 'r', encoding="utf-8") as asset:
print(asset.read())
def make_choice(self):
"""
Affiche la partie intéractive de notre page
"""
# On affiche le menu
reponse = prompt(self.questions)
#En fonction de la réponse on va retourner des pages différentes
if reponse['authentification'] == 'Me connecter':
# Si la réponse à la question authentification est "Me
connecter" on retourne la classe LogInView
next_view = LogInView()
else:
# Sinon on retourne la classe RegisterView
next_view RegisterView()
return next_view
