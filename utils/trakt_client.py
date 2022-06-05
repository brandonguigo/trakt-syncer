import sys

import trakt

from utils.config import Config
from utils.trakt_episode import TraktEpisode
from utils.trakt_movie import TraktMovie


class TraktClient:
    def __init__(self, config):
        self.config = config

    #TODO
    def authenticate(self):
        print("Authenticating client_id %s" % self.config.client_id)
        print("Authenticated")

    #TODO
    def getShow(self, trakt_episode: TraktEpisode):
        print("Not yet implemented")
        print("Getting show with TVDB ID : %s with trakt client ID %s" % trakt_episode.tvdb_id % self.config.client_id)
        sys.exit(1)

    #TODO
    def getEpisode(self, trakt_episode: TraktEpisode):
        print("Not yet implemented")
        print(
            "Getting episode with the show %s TVDB ID : %s with trakt client ID %s" % trakt_episode.show.name % trakt_episode.tvdb_id % self.client_id)
        sys.exit(1)

    #TODO
    def getMovie(self, trakt_movie: TraktMovie):
        print("Not yet implemented")
        print("Getting movie with TMDB ID : %s with trakt client id %s" % trakt_movie.tmdb_id % self.config.client_id)
        sys.exit(1)

    #TODO
    def pushEpisodeWatchedEvent(self, trakt_episode: TraktEpisode):
        print("Pushing show with TVDB ID : %s for trakt client ID %s" % (trakt_episode.tvdb_id, self.config.client_id))
        print("Getting show")
        print("Getting episode")
        print("Scrobbling episode")
        sys.exit(0)

    #TODO
    def pushMovieWatchedEvent(self, trakt_movie: TraktMovie):
        print("Not yet implemented")
        print("Pushing movie with TMDB ID : %s for trakt client ID %s" % trakt_movie.tmdb_id % self.config.client_id)
        sys.exit(1)
