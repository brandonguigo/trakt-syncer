import logging
import sys

from trakt import Trakt

from utils.config import Config
from utils.trakt_episode import TraktEpisode
from utils.trakt_movie import TraktMovie
from utils.trakt_show import TraktShow

logging.basicConfig(level=logging.DEBUG)

class TraktClient:
    def __init__(self, config):
        self.config = config

    #TODO
    def startScrobble(self, episode: TraktEpisode = None, show: TraktShow = None, movie: TraktMovie = None):
        if show is not None:
            if episode is not None:
                print("Send %s - S%sE%s to Trakt.tv" % (show.tvdb_id, episode.season_num, episode.episode_num))
                Trakt['scrobble'].start(
                    show=show.generateTraktDict(),
                    episode=episode.generateTraktDict(),
                    progress=episode.progress
                )
                print("Scrobble successful")
                sys.exit(0)
            else:
                print("episode is null, cennot continue")
                sys.exit(1)
        elif movie is not None:
            print("send movie to scrobble")
            print("Send %s to Trakt.tv" % movie.tmdb_id)
            Trakt['scrobble'].start(
                movie=movie.generateTraktDict(),
                progress=movie.progress
            )
            print("Scrobble successful")
            sys.exit(0)
        else:
            print("Don't know what to do, nor show+episode or movie passed.")
            sys.exit(1)

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
