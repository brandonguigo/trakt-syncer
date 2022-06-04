from utils.trakt_item import TraktItem


class TraktShow(TraktItem):
    def __init__(self, tvdb_id):
        self.tvdb_id = tvdb_id

    def generateTraktDict(self):
        return {
            'ids': {
                'tvdb': self.tvdb_id,
            }
        }
