from BusinessLayer.BusinessObjects.agent import Agent
from BusinessLayer.LocalServices.Gestion.interface_fiche_agent import InterfaceFicheAgent
from DataLayer.DAO.dao_agent import DAOAgent

class FicheSuperviseur(InterfaceFicheAgent):

    def creer_agent(self, est_superviseur : bool, quotite : float, id_superviseur : int, nom_utilisateur : str, mot_de_passe : str, prenom : str, nom : str) -> bool:
        return DAOAgent.creer_agent(est_superviseur, quotite, id_superviseur, nom_utilisateur, mot_de_passe, prenom, nom)

# La méthode modifier_agent prend un agent et un dict, mais doit donner seulement un dict à la méthode de la DAO 
#    def modifier_agent(self, agent_a_modifier : Agent, data : dict) -> bool: 
        est_superviseur : bool, quotite : float, id_superviseur : int, nom_utilisateur : str, mot_de_passe : str, prenom : str, nom : str
        if "est_superviseur" in data.keys():
            role = data['est_superviseur']
        else:
            role = agent_a_modifier
        nouvel_agent = (id_fiche,  nouvelles_informations["identifiant_pot"] if "identifiant_pot" in nouvelles_informations.keys else fa.identifiant_pot, 
                          nouvelles_informations["identifiant_lot"] if "identifiant_lot" in nouvelles_informations.keys else fa.identifiant_lot, 
                          nouvelles_informations["adresse_initiale"] if "adresse_initiale" in nouvelles_informations.keys else fa.adresse_initiale,
                          nouvelles_informations["adresse_finale"] if "adresse_finale" in nouvelles_informations.keys else fa.adresse_finale, 
                          nouvelles_informations["coordonnees_wgs84"] if "coordonnees_wgs84" in nouvelles_informations.keys else fa.coordonnees_wgs84, 
                          nouvelles_informations["champs_supplementaires"] if "champs_supplementaires" in nouvelles_informations.keys else fa.champs_supplementaires,
                          nouvelles_informations["code_resultat"] if "code_resultat" in nouvelles_informations.keys else fa.code_resultat)
        probleme = DAOAgent.modifier_agent(nouvel_agent)
        return probleme

    def changer_droits(self, agent_a_modifier : Agent) -> bool: # On change le Superviseur en Gestionnaire
        return DAOAgent.changer_droits(agent_a_modifier)

    def supprimer_agent(self, agent_a_supprimer : Agent) -> bool:
        return DAOAgent.supprimer_agent(agent_a_supprimer.agent_id)