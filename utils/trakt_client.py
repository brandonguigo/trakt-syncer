import logging
import sys
import time
from datetime import datetime

from utils.trakt_api_client import TraktApiClient

from utils.trakt_episode import TraktEpisode
from utils.trakt_movie import TraktMovie
from utils.trakt_show import TraktShow

TRAKT_API_URL = "https://api.trakt.tv/"
class TraktClient:
    def __init__(self, config):
        self.config = config
        self.traktApiClient = TraktApiClient(config)

    def authenticate(self):
        print("Checking access and refresh tokens")
        if self.config.access_token is None:
            print("Tokens not found, authenticating...")
            #TODO: get user and device codes and print the link to the user
            status_code, data = self.traktApiClient.post(
                TRAKT_API_URL+"oauth/device/code",
                {"client_id": self.config.client_id})

            if status_code != 200:
                print("Error getting device code for authentication, status code : %s" % (status_code))
                sys.exit(1)
            print("Please connect to : %s\nFill the following code when asked : %s\n\n\n" % (data["verification_url"], data["user_code"]))
            device_code = data["device_code"]
            print('Device Code: %s' % (device_code))

            #TODO: poll the trakt api each seconds to fetch the token once the user has signed in

            while True:
                print("INFO: Polling for authorization...")
                status_code, data = self.traktApiClient.post(
                    TRAKT_API_URL + "oauth/device/token",
                    {
                        "code": device_code,
                        "client_id": self.config.client_id,
                        "client_secret": self.config.client_secret
                    }
                )
                if status_code != 200:
                    print("ERROR: no new access_token available")
                    time.sleep(5)
                else:
                    self.config.set_value('Trakt', 'access_token', data["access_token"])
                    self.config.set_value('Trakt', 'refresh_token', data["refresh_token"])
                    break
            print("INFO: Writing tokens inside the config file...")
            self.config.write_settings()
        else:
            print("Tokens found, already connected")

        return True
    #TODO
    def startScrobble(self, episode: TraktEpisode = None, show: TraktShow = None, movie: TraktMovie = None):
        if show is not None:
            if episode is not None:
                print("Send Start Scrobble %s - S%sE%s to Trakt.tv" % (show.tvdb_id, episode.season_num, episode.episode_num))
                status_code, data = self.traktApiClient.post(
                    TRAKT_API_URL + "scrobble/start",
                    {
                        "episode": episode.generateEpisodeTraktDict(),
                        "show": episode.generateShowTraktDict(),
                        "progress": episode.progress,
                        "app_version": "1.0",
                        "app_date": datetime.now().strftime("%Y-%m-%d")
                    }
                )
                if status_code == 403:
                    #TODO: refresh token here and retry
                    print("INFO: Forbidden, refreshing token and retry")
                elif status_code != 201:
                    print("ERROR: error during request\nstatus_code: %s\nmessage: %s" % (status_code, data))
                    sys.exit(1)

                print("Scrobble Start successful")
                sys.exit(0)
            else:
                print("episode is null, cennot continue")
                sys.exit(1)
        elif movie is not None:
            print("Send %s to Trakt.tv" % movie.tmdb_id)
            status_code, data = self.traktApiClient.post(
                TRAKT_API_URL + "scrobble/start",
                {
                    "movie": movie.generateEpisodeTraktDict(),
                    "progress": movie.progress,
                    "app_version": "1.0",
                    "app_date": datetime.now().strftime("%Y-%m-%d")
                }
            )
            if status_code == 403:
                #TODO: refresh token here and retry
                print("INFO: Forbidden, refreshing token and retry")
            elif status_code != 201:
                print("ERROR: error during request\nstatus_code: %s\nmessage: %s" % (status_code, data))
                sys.exit(1)
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
                #TODO: call the trakt api with the access token
                # Trakt['scrobble'].pause(
                #     show=show.generateTraktDict(),
                #     episode=episode.generateTraktDict(),
                #     progress=episode.progress
                # )
                status_code, data = self.traktApiClient.post(
                    TRAKT_API_URL + "scrobble/pause",
                    {
                        "episode": episode.generateEpisodeTraktDict(),
                        "show": episode.generateShowTraktDict(),
                        "progress": episode.progress,
                        "app_version": "1.0",
                        "app_date": datetime.now().strftime("%Y-%m-%d")
                    }
                )
                if status_code == 403:
                    #TODO: refresh token here and retry
                    print("INFO: Forbidden, refreshing token and retry")
                elif status_code != 201:
                    print("ERROR: error during request\nstatus_code: %s\nmessage: %s" % (status_code, data))
                    sys.exit(1)
            print("Scrobble Pause successful")
            sys.exit(0)
        elif movie is not None:
            print("send movie to scrobble")
            print("Send Pause Scrobble %s to Trakt.tv" % movie.tmdb_id)
            #TODO: call the trakt api with the access token
            status_code, data = self.traktApiClient.post(
                TRAKT_API_URL + "scrobble/pause",
                {
                    "movie": movie.generateEpisodeTraktDict(),
                    "progress": movie.progress,
                    "app_version": "1.0",
                    "app_date": datetime.now().strftime("%Y-%m-%d")
                }
            )
            if status_code == 403:
                #TODO: refresh token here and retry
                print("INFO: Forbidden, refreshing token and retry")
            elif status_code != 201:
                print("ERROR: error during request\nstatus_code: %s\nmessage: %s" % (status_code, data))
                sys.exit(1)
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
                #TODO: call the trakt api with the access token
                # Trakt['scrobble'].stop(
                #     show=show.generateTraktDict(),
                #     episode=episode.generateTraktDict(),
                #     progress=episode.progress
                # )
                status_code, data = self.traktApiClient.post(
                    TRAKT_API_URL + "scrobble/stop",
                    {
                        "episode": episode.generateEpisodeTraktDict(),
                        "show": episode.generateShowTraktDict(),
                        "progress": episode.progress,
                        "app_version": "1.0",
                        "app_date": datetime.now().strftime("%Y-%m-%d")
                    }
                )
                if status_code == 403:
                    #TODO: refresh token here and retry
                    print("INFO: Forbidden, refreshing token and retry")
                elif status_code != 201:
                    print("ERROR: error during request\nstatus_code: %s\nmessage: %s" % (status_code, data))
                    sys.exit(1)
            print("Scrobble Stop successful")
            sys.exit(0)
        elif movie is not None:
            print("Send movie to scrobble")
            print("Send Stop Scrobble %s to Trakt.tv" % movie.tmdb_id)
            status_code, data = self.traktApiClient.post(
                TRAKT_API_URL + "scrobble/stop",
                {
                    "movie": movie.generateEpisodeTraktDict(),
                    "progress": movie.progress,
                    "app_version": "1.0",
                    "app_date": datetime.now().strftime("%Y-%m-%d")
                }
            )
            if status_code == 403:
                #TODO: refresh token here and retry
                print("INFO: Forbidden, refreshing token and retry")
            elif status_code != 201:
                print("ERROR: error during request\nstatus_code: %s\nmessage: %s" % (status_code, data))
                sys.exit(1)
            print("Scrobble Stop successful")
            sys.exit(0)
        else:
            print("Don't know what to do, nor show+episode or movie passed.")
            sys.exit(1)

    def enableDebug(self):
        logging.basicConfig(level=logging.DEBUG)

        try:
            import http.client as http_client
        except ImportError:
            # Python 2
            import httplib as http_client
        http_client.HTTPConnection.debuglevel = 1

        # You must initialize logging, otherwise you'll not see debug output.
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
