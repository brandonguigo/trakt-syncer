from abc import ABC, abstractmethod


class TraktItem(ABC):
    @abstractmethod
    def generateTraktDict(self) -> dict:
        pass
