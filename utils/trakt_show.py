from utils.trakt_item import TraktItem


class TraktShow(TraktItem):
    def __init__(self, m: int):
        self.tmdb_id = m

    def generateEpisodeTraktDict(self) -> dict:
        return {
            'ids': {
                'tvdb': self.tmdb_id,
            }
        }
