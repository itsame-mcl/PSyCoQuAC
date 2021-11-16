from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from BusinessLayer.BusinessObjects.session import Session
from BusinessLayer.BusinessObjects.agent import Agent
from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from DataLayer.DAO.dao_fiche_adresse import DAOFicheAdresse
from DataLayer.DAO.dao_agent import DAOAgent
from typing import List


class ControleRepriseService():

    def consulter_fiche(self, session_utilisateur : Session, id_fiche : int, etat_final : bool ) -> FicheAdresse :
        pot = DAOFicheAdresse.recuperer_pot(session_utilisateur.utilisateur_connecte) # Récupère le pot de l'agent 
        if session_utilisateur.droits_superviseurs == False and id_fiche not in pot : # Un agent ne peut pas consulter une fiche s'il est gestionnaire et que la fiche ne lui est pas attribué
            raise ValueError("L'agent n'a pas le droit de consulter la fiche")
        fa = DAOFicheAdresse.recuperer_fiche_adresse(id_fiche)
        return fa
    
    def modifier_fiche(self, id_fiche : int, nouvelles_informations : dict) -> bool:
        fa = DAOFicheAdresse.recuperer_fiche_adresse(id_fiche)
        nouvelle_fa = FicheAdresse(id_fiche,  nouvelles_informations["identifiant_pot"] if "identifiant_pot" in nouvelles_informations.keys else fa.identifiant_pot, 
                          nouvelles_informations["identifiant_lot"] if "identifiant_lot" in nouvelles_informations.keys else fa.identifiant_lot, 
                          nouvelles_informations["adresse_initiale"] if "adresse_initiale" in nouvelles_informations.keys else fa.adresse_initiale,
                          nouvelles_informations["adresse_finale"] if "adresse_finale" in nouvelles_informations.keys else fa.adresse_finale, 
                          nouvelles_informations["coordonnees_wgs84"] if "coordonnees_wgs84" in nouvelles_informations.keys else fa.coordonnees_wgs84, 
                          nouvelles_informations["champs_supplementaires"] if "champs_supplementaires" in nouvelles_informations.keys else fa.champs_supplementaires,
                          nouvelles_informations["code_resultat"] if "code_resultat" in nouvelles_informations.keys else fa.code_resultat)
        probleme = DAOFicheAdresse.modifier_fiche_adresse(nouvelle_fa)
        return probleme
    
    def consulter_pot(self, session_utilisateur : Session) -> List[FicheAdresse] :
        pot = DAOFicheAdresse.recuperer_pot(session_utilisateur.utilisateur_connecte)
        return pot

    def consulter_pot_agent(self, id_agent) -> dict:
        agent = DAOAgent.recuperer_agent(id_agent)
        return DAOFicheAdresse.recuperer_pot(agent)
