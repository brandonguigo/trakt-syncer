from utils.trakt_item import TraktItem
from utils.trakt_show import TraktShow


class TraktEpisode(TraktItem):
    def __init__(self, season_num: int, episode_num: int, progress: float, show: TraktShow):
        self.season_num = season_num
        self.episode_num = episode_num
        self.progress = progress
        self.show = show

    def generateEpisodeTraktDict(self) -> dict:
        return {
            'season': self.season_num,
            'number': self.episode_num,
        }

    def generateShowTraktDict(self) -> dict:
        return {
            'ids': {
                'tvdb': self.show.tvdb_id,
            }
        }
