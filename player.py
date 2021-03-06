from pygame import Rect
import config


class Player:
    def __init__(self):
        self.p_x = config.SCREEN_WIDTH / 2
        self.p_y = config.SCREEN_HEIGHT - config.PLAYER_SIZE - config.START_FLOOR_HEIGHT
        self.jump_v = 0
        self.is_going_jump = False
        self.is_landing = False

    def rect(self):
        return Rect(
            (self.p_x - 10, self.p_y), (config.PLAYER_SIZE, config.PLAYER_SIZE),
        )
