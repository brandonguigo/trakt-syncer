from utils.trakt_client import TraktClient
from utils.trakt_item import TraktItem


class TraktEpisode(TraktItem):
    def __init__(self, tvdb_id: str, season_num: int, episode_num: int, progress: float):
        self.tvdb_id = tvdb_id
        self.season_num = season_num
        self.episode_num = episode_num
        self.progress = progress

    def generateTraktDict(self) -> dict:
        return {
            "season": self.season_num,
            "number": self.episode_num
        }


