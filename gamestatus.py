from enum import Enum

class GameStatus(Enum):
    """
    ゲーム状態を示すenum
    """
    WAITING = 1
    GAMING = 2
    GAME_OVER = 3
