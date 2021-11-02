from BusinessLayer.BusinessObjects.session.py import Session
import DataLayer.DAO as dao
from hashlib import sha512

@Singleton
class SessionServices:

    def ouvrir_session(nom_utilisateur, mot_de_passe):
        hache = sha512(nom_utilisateur + mot_de_passe)
        # Avec la DAO, on récupère le mot de passe sauvegardé dans la BDD qui correspond à l'id de l'agent
        mdp = dao.recuperer_agent_mdp(nom_utilisateur, mot_de_passe) # On peut se demander s'il ne vaudrait pas mieux renseigner un id, 
                                                    # pour faire la recherche du mdp haché dans la BDD
        if hache == mdp: # si le mdp récupéré dans la BDD est le même que le salage_hacahage, l'agent peut ouvrir sa session
            # Pour ouvrir une session, on crée un Agent, et on lui donne un booléen (True si l'Agent est un superviseur, False sinon)
            # Pour créer un Agent, on a besoin : de son id, de son nom_utilisateur, de (nom, prénom) et de l'id de son superviseur
            agent_id = dao.recuperer_agent_id(hache) # On fait appel à une méthode de la DAO qui récupère l'id de l'agent
            identite = dao.recuperer_agent_identite(hache) # On fait appel à une méthode de la DAO qui récupère le prénom et le nom de l'agent
            # On fait appel à une méthode de la DAO qui regarde si l'Agent qui se connecte est un gestionnaire ou un superviseur
            if dao.regarder_si_superviseur(hache): # la méthode regarder_si_superviseur renvoie True si l'Agent est un superviseur
                from Superviseur.py import Superviseur
                equipe_deleguee = dao.recuperer_equipe_deleguee(hache)
                return Session(Superviseur(agent_id, nom_utilisateur, identite, equipe_deleguee), True)
            else: # l'Agent est un gestionnaire
                from Gestionnaire.py import Gestionnaire
                id_superviseur = dao.recuperer_id_superviseur(hache)
                return Session(Gestionnaire(agent_id, nom_utilisateur, identite, id_superviseur), False)
        else:
            return "Ah ah ah ! Vous n'avez pas dis le mot magique !"

    def fermer_session(Bool): # Prend un booléen en argument car on valide la fermeture
        