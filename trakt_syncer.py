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
              <movie>--imdbId {imdb_id}</movie>
              <episode>--tvdbId {thetvdb_id} --season {season_num} --episode {episode_num} --progress {progress_percent}</episode>

  Save
  Close
"""
import argparse
import os
import sys
from configparser import ConfigParser, NoSectionError, NoOptionError
from datetime import datetime

import trakt

from utils.config import Config
from utils.trakt_client import TraktClient
from utils.trakt_movie import TraktMovie
from utils.trakt_episode import TraktEpisode

TAUTULLI_ENCODING = os.getenv('TAUTULLI_ENCODING', 'UTF-8')
APP_VERSION = "trakt-sync"
APP_DATE = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

config = Config()


def decodeArgs(arg):
    """Decode args, encode UTF-8"""
    return arg.decode(TAUTULLI_ENCODING).encode('UTF-8')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Syncing viewing activity to Trakt.tv.")

    parser.add_argument('--userId', required=True, type=int,
                        help='The user_id of the current user.')

    parser.add_argument('--action', required=True, type=str,
                        help='The action required, including pushMovie or pushEpisode.')

    parser.add_argument('--serieTitle', type=str,
                        help='Title of the serie.')

    parser.add_argument('--season', type=int,
                        help='Season number.')

    parser.add_argument('--episode', type=int,
                        help='Episode number.')

    parser.add_argument('--progress', type=int,
                        help='Progress inside the episode.')

    parser.add_argument('--imdbId', type=str,
                        help='IMDB ID.')

    opts = parser.parse_args()

    traktClient = TraktClient(config)
    if opts.action == 'authenticateTrakt':
        traktClient.authenticate()
        sys.exit(0)

    if opts.userId not in config.user_ids and not opts.userId == -1:
        print('We will not sync for this user')
        sys.exit(0)

    if opts.action == 'pushMovie':
        traktMovie = TraktMovie(opts.imdbId)
        traktClient.pushMovieWatchedEvent(traktMovie)
    elif opts.action == 'pushEpisode':
        traktEpisode = TraktEpisode(opts.serieTitle, opts.season, opts.episode, opts.progress)
        traktClient.pushEpisodeWatchedEvent(traktEpisode)
    else:
        print('ERROR: %s not found - invalid action' % opts.action)
