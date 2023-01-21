#!/usr/bin/python3
"""
Description: Synchronize a watch episode or movie to trakt
Author: Brandon Guigo

Important:
Make sure that the './config' file is writeable

Settings:
./config
    [Plex]
    user_ids: a comma separated list of user ids, only entries for these users will be synced
    The user id for a user can be found in your url in Tautulli when you click on a user.

    [Trakt]:
    Update `client_id` with the `client_id` of your registered application, see here:
    https://trakt.tv/oauth/applications > Choose your application

    To set the access code use `urn:ietf:wg:oauth:2.0:oob` as a redirect URI on your application.
    Then execute the script:
    python ./trakt_letterboxd_sync.py --contentType trakt_authenticate --userId -1
    And follow the instructions shown.

Adding the script to Tautulli:
Tautulli > Settings > Notification Agents > Add a new notification agent > Script

Configuration:
Tautulli > Settings > Notification Agents > New Script > Configuration:

  Script Folder: /path/to/your/script
  Script File: ./trakt_syncer.py (Should be selectable in dropdown list)
  Script Timeout: timeout
  Description: Trakt.tv sync
  Save

Triggers:
Tautulli > Settings > Notification Agents > New Script > Triggers:

  Check: Watched
  Save

Conditions:
Tautulli > Settings > Notification Agents > New Script > Conditions:

  Set the condition that you want (for example filter on user_id, etc...)

Script Arguments:
Tautulli > Settings > Notification Agents > New Script > Script Arguments:

  Select: Watched
  Arguments:  --userId {user_id} --contentType {media_type}
              <movie>--imdbId {imdb_id} --progress {progress_percent}</movie>
              <episode>--tvdbId {thetvdb_id} --season {season_num} --episode {episode_num} --progress {progress_percent}</episode>

  Save
  Close
"""
import argparse
import json
import sys
from datetime import datetime

from utils.config import Config
from utils.trakt_client import TraktClient
from utils.trakt_movie import TraktMovie
from utils.trakt_episode import TraktEpisode


from threading import Condition
import os

from utils.trakt_show import TraktShow

TAUTULLI_ENCODING = os.getenv('TAUTULLI_ENCODING', 'UTF-8')
APP_VERSION = "trakt-sync"
APP_DATE = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

config = Config()


def decodeArgs(arg):
    """Decode args, encode UTF-8"""
    return arg.decode(TAUTULLI_ENCODING).encode('UTF-8')


class Application(object):
    def __init__(self, user_id, action, tvdb_id=None, season=None, episode=None, progress=None, tmdbId=None):
        self.userId = user_id
        self.action = action
        self.traktClient = TraktClient(config)

        if tvdb_id is not None and season is not None and episode is not None and progress is not None:
            self.show = TraktShow(tvdb_id)
            self.episode = TraktEpisode(season, episode, progress, self.show)
        elif tmdbId is not None and progress is not None:
            self.movie = TraktMovie(tmdbId, progress)
        else:
            print("Wrong parameters")

    def run(self):
        print(str(config) + "\n\n\n")
        if config.access_token is None:
            #TODO: request access token
            print("INFO: access_token not found, requesting it...")
            auth_result = self.traktClient.authenticate()
            if not auth_result:
                print("ERROR: authentication failed")
                sys.exit(1)

        if self.userId not in config.user_ids and not self.userId == -1:
            print('We will not sync for this user')
            sys.exit(0)

        if self.action == 'startScrobble':
            #TODO: redo the action using the Trakt Official API with custom client
            self.traktClient.startScrobble(show=self.show if hasattr(self, 'show') else None,
                                            episode=self.episode if hasattr(self, 'episode') else None,
                                            movie=self.movie if hasattr(self, 'movie') else None)
        elif self.action == 'pauseScrobble':
            #TODO: redo the action using the Trakt Official API with custom client
            self.traktClient.pauseScrobble(show=self.show if hasattr(self, 'show') else None,
                                            episode=self.episode if hasattr(self, 'episode') else None,
                                            movie=self.movie if hasattr(self, 'movie') else None)
        elif self.action == 'stopScrobble':
            #TODO: redo the action using the Trakt Official API with custom client
            self.traktClient.stopScrobble(show=self.show if hasattr(self, 'show') else None,
                                            episode=self.episode if hasattr(self, 'episode') else None,
                                            movie=self.movie if hasattr(self, 'movie') else None)
        else:
            print('ERROR: %s not found - invalid action' % opts.action)

        # # Simulate expired token
        # self.authorization['expires_in'] = 0

        # # Test authenticated calls
        # with Trakt.configuration.oauth.from_response(self.authorization):
        #     # Expired token, requests will return `None`
        #     print(Trakt['sync/collection'].movies())
        #
        # with Trakt.configuration.oauth.from_response(self.authorization, refresh=True):
        #     # Expired token will be refreshed automatically (as `refresh=True`)
        #     print(Trakt['sync/collection'].movies())
        #
        # with Trakt.configuration.oauth.from_response(self.authorization):
        #     # Current token is still valid
        #     print(Trakt['sync/collection'].movies())

    #TODO: move the logic of authentication inside a new trakt client
    def on_aborted(self):
        """Device authentication aborted.

        Triggered when device authentication was aborted (either with `DeviceOAuthPoller.stop()`
        or via the "poll" event)
        """

        print('Authentication aborted')

        # Authentication aborted
        self.is_authenticating.acquire()
        self.is_authenticating.notify_all()
        self.is_authenticating.release()

    def on_authenticated(self, authorization):
        """Device authenticated.

        :param authorization: Authentication token details
        :type authorization: dict
        """

        # Acquire condition
        self.is_authenticating.acquire()

        # Store authorization for future calls
        self.authorization = authorization

        print('Authentication successful - authorization: %r' % self.authorization)

        # Authentication complete
        self.is_authenticating.notify_all()
        self.is_authenticating.release()

    def on_expired(self):
        """Device authentication expired."""

        print('Authentication expired')

        # Authentication expired
        self.is_authenticating.acquire()
        self.is_authenticating.notify_all()
        self.is_authenticating.release()

    def on_poll(self, callback):
        """Device authentication poll.

        :param callback: Call with `True` to continue polling, or `False` to abort polling
        :type callback: func
        """

        # Continue polling
        callback(True)

    def on_token_refreshed(self, authorization):
        # OAuth token refreshed, store authorization for future calls
        self.authorization = authorization

        print('Token refreshed - authorization: %r' % self.authorization)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Syncing viewing activity to Trakt.tv.")

    parser.add_argument('--userId', required=True, type=int,
                        help='The user_id of the current user.')

    parser.add_argument('--action', required=True, type=str,
                        help='The action required, including pushMovie or pushEpisode.')

    parser.add_argument('--season', type=int,
                        help='Season number.')

    parser.add_argument('--episode', type=int,
                        help='Episode number.')

    parser.add_argument('--progress', type=int,
                        help='Progress inside the episode.')

    parser.add_argument('--tmdbId', type=str,
                        help='TMDB ID for a movie')
    
    parser.add_argument('--tvdbId', type=str,
                        help='TVDB ID for a show, needs to be combined with season and episode parameters.')

    opts = parser.parse_args()

    app = Application(opts.userId,
                      opts.action,
                      opts.tvdbId if hasattr(opts, 'tvdbId') else None,
                      opts.season if hasattr(opts, 'season') else None,
                      opts.episode if hasattr(opts, 'episode') else None,
                      opts.progress if hasattr(opts, 'progress') else None,
                      opts.tmdbId if hasattr(opts, 'tmdbId') else None)

    # Trakt.base_url = 'https://api.trakt.tv'
    #
    # Trakt.configuration.defaults.client(
    #     id=config.client_id,
    #     secret=config.client_secret
    # )
    app.run()
