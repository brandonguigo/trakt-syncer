from utils.trakt_item import TraktItem


class TraktMovie(TraktItem):
    def __init__(self, tmdb_id, progress):
        self.tmdb_id = tmdb_id
        self.progress = progress

    def generateTraktDict(self):
        return {
            'ids': {
                'tmdb': self.tmdb_id
            }
        }

