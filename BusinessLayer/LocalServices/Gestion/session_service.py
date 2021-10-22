from session.py import Session
from hashlib import sha512

@Singleton
class SessionServices:

    def ouvrir_session(nom_utilisateur, mot_de_passe):
        hache = sha512(nom_utilisateur + mot_de_passe)
        # Avec la DAO, on récupère le mot de passe sauvegardé dans la BDD qui correspond à l'id de l'agent
        mdp = 
        if hache == mdp:
            agent_id = recuperer_agent_id(nom_utilisateur, mot_de_passe) # On fait appel à une méthode de la DAO qui récupère l'id de l'agent
            identité = recuperer_agent_identite(nom_utilisateur, mot_de_passe) # On fait appel à une méthode de la DAO qui récupère le prénom et le nom de l'agent
            # On fait appel à une méthode de la DAO qui regarde si l'Agent qui se connecte est un gestionnaire ou un superviseur
            if regarder_si_superviseur(nom_utilisateur, mot_de_passe):
                return Session()
            else: # l'Agent est un gestionnaire
                return Session()
        else:
            return "Vous n'avez pas dis le mot magique !"