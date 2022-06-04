from utils.trakt_item import TraktItem
from utils.trakt_show import TraktShow


class TraktEpisode(TraktItem):
    def __init__(self, season_num, episode_num, progress, show):
        self.season_num = season_num
        self.episode_num = episode_num
        self.progress = progress
        self.show = show

    def generateTraktDict(self):
        return {
            'season': self.season_num,
            'number': self.episode_num,
            'ids': {
                'tvdb': self.show.tvdb_id,
            }
        }

