import logging
import sys

from trakt import Trakt

from utils.config import Config
from utils.trakt_episode import TraktEpisode
from utils.trakt_movie import TraktMovie
from utils.trakt_show import TraktShow

# # Uncomment to enable debug logs of the trakt python API
# logging.basicConfig(level=logging.DEBUG)

class TraktClient:
    def __init__(self, config):
        self.config = config

    #TODO
    def startScrobble(self, episode: TraktEpisode = None, show: TraktShow = None, movie: TraktMovie = None):
        if show is not None:
            if episode is not None:
                print("Send Start Scrobble %s - S%sE%s to Trakt.tv" % (show.tvdb_id, episode.season_num, episode.episode_num))
                Trakt['scrobble'].start(
                    show=show.generateTraktDict(),
                    episode=episode.generateTraktDict(),
                    progress=episode.progress
                )
                print("Scrobble Start successful")
                sys.exit(0)
            else:
                print("episode is null, cennot continue")
                sys.exit(1)
        elif movie is not None:
            print("Send movie to scrobble")
            print("Send %s to Trakt.tv" % movie.tmdb_id)
            Trakt['scrobble'].start(
                movie=movie.generateTraktDict(),
                progress=movie.progress
            )
            print("Scrobble Start successful")
            sys.exit(0)
        else:
            print("Don't know what to do, nor show+episode or movie passed.")
            sys.exit(1)

    #TODO
    def pauseScrobble(self, episode: TraktEpisode = None, show: TraktShow = None, movie: TraktMovie = None):
        if show is not None:
            if episode is not None:
                print("Send Pause Scrobble %s - S%sE%s to Trakt.tv" % (show.tvdb_id, episode.season_num, episode.episode_num))
                Trakt['scrobble'].pause(
                    show=show.generateTraktDict(),
                    episode=episode.generateTraktDict(),
                    progress=episode.progress
                )
                print("Scrobble Pause successful")
                sys.exit(0)
            else:
                print("episode is null, cennot continue")
                sys.exit(1)
        elif movie is not None:
            print("send movie to scrobble")
            print("Send Pause Scrobble %s to Trakt.tv" % movie.tmdb_id)
            Trakt['scrobble'].pause(
                movie=movie.generateTraktDict(),
                progress=movie.progress
            )
            print("Scrobble Pause successful")
            sys.exit(0)
        else:
            print("Don't know what to do, nor show+episode or movie passed.")
            sys.exit(1)

    # TODO
    def stopScrobble(self, episode: TraktEpisode = None, show: TraktShow = None, movie: TraktMovie = None):
        if show is not None:
            if episode is not None:
                print("Send Stop Scrobble %s - S%sE%s to Trakt.tv" % (show.tvdb_id, episode.season_num, episode.episode_num))
                Trakt['scrobble'].stop(
                    show=show.generateTraktDict(),
                    episode=episode.generateTraktDict(),
                    progress=episode.progress
                )
                print("Scrobble Stop successful")
                sys.exit(0)
            else:
                print("episode is null, cennot continue")
                sys.exit(1)
        elif movie is not None:
            print("Send movie to scrobble")
            print("Send Stop Scrobble %s to Trakt.tv" % movie.tmdb_id)
            Trakt['scrobble'].stop(
                movie=movie.generateTraktDict(),
                progress=movie.progress
            )
            print("Scrobble Stop successful")
            sys.exit(0)
        else:
            print("Don't know what to do, nor show+episode or movie passed.")
            sys.exit(1)
