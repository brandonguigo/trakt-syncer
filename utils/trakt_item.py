from abc import ABC, abstractmethod


class TraktItem(ABC):
    @abstractmethod
    def generateEpisodeTraktDict(self) -> dict:
        pass
