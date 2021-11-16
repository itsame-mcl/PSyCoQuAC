from abc import ABC, abstractmethod

class AbstractView(ABC):

    def display_info(self):
        pass

    @abstractmethod
    def make_choice(self):
        raise NotImplementedError
