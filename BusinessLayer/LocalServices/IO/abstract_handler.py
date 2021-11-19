from abc import ABC, abstractmethod
from typing import List

from BusinessLayer.BusinessObjects.fiche_adresse import FicheAdresse
from BusinessLayer.BusinessObjects.modele import Modele


class AbstractHandler(ABC):
    @abstractmethod
    def import_from_file(self, path, id_agent: int, id_lot: int, model: Modele) -> List[FicheAdresse]:
        raise NotImplementedError

    def export_to_file(self, fiches: List[FicheAdresse], path, model: Modele) -> bool:
        raise NotImplementedError
