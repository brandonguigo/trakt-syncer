from abc import abstractmethod, ABCMeta


class TraktItem():
    __metaclass__ = ABCMeta
    @abstractmethod
    def generateTraktDict(self):
        pass
