from DataLayer import DAO as dao
from utils.singleton import Singleton

@Singleton
class StatistiqueService:

    def fiches_par_agent(session_utilisateur): # On vérifie d'abord que c'est un Superviseur qui regarde les fiches des Gestionnaires de son équipe
        response = {}
        liste_agent = dao.DAOAgent.recuperer_liste_agents(session_utilisateur.utilisateur_connecte.agent_id)
        for agent_id in liste_agent:
            response[str(agent_id)] = len( dao.DAOAgent.recuperer_fiches_agent(agent_id) )
        return response

    def fiches_par_lot(session_utilisateur):
        num = dao.recuperer_num_lot() # On récupère le dernier numéro de lot utilisé
        response = {}
        for i in range(1, num+1):
            response["lot " + str(i)] = len( dao.DAOFicheAdresse.recuperer_lot(i) )
        return response

    def fiches_par_code_res(self, session_utilisateur):
        response = {"DI" : 0, "VA" : 0, "VC" : 0, "VR" : 0, "ER" : 0}
        id_fiche = dao.recuperer_id_fiche() # On récupère le dernier numéro de fiche adresse utilisé
        for i in range(1, id_fiche+1):
            code = dao.DAOFicheAdresse.recuperer_fiche_adresse(i).code_res
            response(code) += 1
        return response