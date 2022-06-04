from utils.trakt_client import TraktClient
from utils.trakt_item import TraktItem


class TraktEpisode(TraktItem):
    def __init__(self, tvdb_id: str):
        self.tvdb_id = tvdb_id

    def generateTraktDict(self) -> dict:
        return {
            'ids': {
                'tvdb': self.tvdb_id
            }
        }


