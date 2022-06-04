from utils.trakt_item import TraktItem


class TraktShow(TraktItem):
    def __init__(self, tvdb_id: int):
        self.tvdb_id = tvdb_id

    def generateTraktDict(self) -> dict:
        return {
            'ids': {
                'tvdb': self.tvdb_id,
            }
        }
