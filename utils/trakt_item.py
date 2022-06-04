from abc import ABC, abstractmethod

from utils.trakt_client import TraktClient


class TraktItem(ABC):
    @abstractmethod
    def generateTraktDict(self) -> dict:
        pass
