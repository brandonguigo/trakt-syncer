# Trakt-syncer
Push your scrobbling activity to Trakt.tv for movies and tv shows

## Setup
1. Clone this repo inside your Tautulli host.
2. Edit `config` file and add the `user_ids`, `client_id`, `client_secret`. See below for more info on these settings.
3. Launch `git clone --recurse-submodules https://github.com/brandonguigo/trakt-syncer.git` or install via pip the requirement file `python3 -m pip install -r requirements.txt`. Since tautulli can be running inside a Docker container which we sometimes don't have access on some seedbox providers, Tautulli will launch the script his python3 which don't have trakt.py so we need to have the trakt module source inside our source dir. 
4. `chmod a+x trakt-syncer.py`

**Important!** Make sure `config` is writable


### Settings
`./config
```
  [Plex]
  user_ids: a comma separated list of user ids, only entries for these users will be synced
    The user id for a user can be found in your url in Tautulli when you click on a user.
  
  [Trakt]:
  Update `client_id` with the `client_id` of your registered application, see here:
    https://trakt.tv/oauth/applications > Choose your application
  
  Then, launch manually a stopScrobble command to generate and store autorization for Trakt.tv API : 
  ./trakt_syncer.py --action stopScrobble --userId {tautulli_user_id}  --tmdbId {tmdb_id} --progress 60
```

### Tautulli
```
Adding the script to Tautulli:
Tautulli > Settings > Notification Agents > Add a new notification agent > Script

Configuration:
Tautulli > Settings > Notification Agents > New Script > Configuration:

  Script Folder: /path/to/your/scripts
  Script File: ./trakt_syncer.py (Should be selectable in a dropdown list)
  Script Timeout: {timeout}
  Description: Trakt.tv sync
  Save

Triggers:
Tautulli > Settings > Notification Agents > New Script > Triggers:
  
  Check: 
    Playback Start
    Playback Stop
    Playback Pause
    Playback Resume
  Save
  
Conditions:
Tautulli > Settings > Notification Agents > New Script > Conditions:
  
  (Optional)Set the Condition you want : send only is username match...
  Save
  
Script Arguments:
Tautulli > Settings > Notification Agents > New Script > Script Arguments:
  
  Select: 
        Playback Start
        Arguments: --action startScrobble --userId {user_id}  --progress {progress_percent} <movie>--tmdbId {themoviedb_id}</movie> <episode>--tvdbId {thetvdb_id} --season {season_num} --episode {episode_num}</episode>
        
        Playback Stop
        Arguments: --action pauseScrobble --userId {user_id}  --progress {progress_percent} <movie>--tmdbId {themoviedb_id}</movie> <episode>--tvdbId {thetvdb_id} --season {season_num} --episode {episode_num}</episode>
        
        Playback Pause
        Arguments: --action pauseScrobble --userId {user_id}  --progress {progress_percent} <movie>--tmdbId {themoviedb_id}</movie> <episode>--tvdbId {thetvdb_id} --season {season_num} --episode {episode_num}</episode>
        
        Playback Resume
        Arguments: --action startScrobble --userId {user_id}  --progress {progress_percent} <movie>--tmdbId {themoviedb_id}</movie> <episode>--tvdbId {thetvdb_id} --season {season_num} --episode {episode_num}</episode>
        
        Watched
        Arguments: --action stopScrobble --userId {user_id}  --progress {progress_percent} <movie>--tmdbId {themoviedb_id}</movie> <episode>--tvdbId {thetvdb_id} --season {season_num} --episode {episode_num}</episode> 

  Save
  Close
```
