import sys


from utils.config import Config
from utils.trakt_episode import TraktEpisode
from utils.trakt_movie import TraktMovie


class TraktClient:
    def __init__(self, config):
        self.config = config

    #TODO
    def startScrobble(self, trakt_item: dict):
        print("Start scrobbling with TVDB ID : %s for trakt client ID %s" % (trakt_item["tvdb_id"], self.config.client_id))
        print("Getting show")
        print("Getting episode")
        print("Scrobbling episode")
        sys.exit(0)

    #TODO
    def pauseScrobble(self, trakt_item: dict):
        print("Not yet implemented")
        print("Pause scrobbling with TMDB ID : %s for trakt client ID %s" % (trakt_item["tvdb_id"], self.config.client_id))
        sys.exit(1)

    # TODO
    def stopScrobble(self, trakt_item: dict):
        print("Not yet implemented")
        print("Stop scrobbling with TMDB ID : %s for trakt client ID %s" % (trakt_item["tvdb_id"], self.config.client_id))
        sys.exit(1)
