import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT

import config
from gamestatus import GameStatus

class GameRoutine:

    # ゲーム初期化処理
    def __init__(self, screen):
        self.p_x = 400
        self.p_y = config.SCREEN_HEIGHT - config.PLAYER_SIZE - config.FLOOR_HEIGHT
        self.jump_v = 0
        self.is_jumping = False
        self.is_landing = True
        self.screen = screen
        
        self.screen.fill((0, 0, 0))

    # ゲーム進行処理
    def step(self, keycode):

        if keycode == K_LEFT:
            self.p_x -= config.MOVE_X_STEP
        elif keycode == K_RIGHT:
            self.p_x += config.MOVE_X_STEP

        # 横歩行の壁を超えない
        if self.p_x <= 0:
            self.p_x = 0
        elif self.p_x >= config.SCREEN_WIDTH:
            self.p_x = config.SCREEN_WIDTH

        player_char = Rect((self.p_x - 10, self.p_y), (config.PLAYER_SIZE, config.PLAYER_SIZE))
        r1 = Rect(700, 450, 50, 100)     # TODO ジャンプ実験用ブロック
        r2 = Rect(50, 400, 50, 100)    # TODO 終了判定実験用ブロック

        # TODO 実験用の地面
        floors = []
        floors.append(Rect(0, config.SCREEN_HEIGHT - 20, 200, config.FLOOR_HEIGHT))
        floors.append(Rect(300, config.SCREEN_HEIGHT - config.FLOOR_HEIGHT, 450, config.FLOOR_HEIGHT))

        for f in floors:
            if player_char.colliderect(f):
                self.is_landing = True
                self.p_y = f.top - config.PLAYER_SIZE
                player_char = Rect((self.p_x - config.PLAYER_SIZE / 2, self.p_y), (config.PLAYER_SIZE, config.PLAYER_SIZE))
            
        # 描画
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (200, 0, 0), player_char)
        pygame.draw.rect(self.screen, (0, 100, 200), r1)
        pygame.draw.rect(self.screen, (100, 100, 200), r2)
        for f in floors:
            pygame.draw.rect(self.screen, (100, 200, 100), f)

        # TODO お邪魔ブロックとの衝突で終了判定実験
        if player_char.colliderect(r2):
            return GameStatus.GAME_OVER

        # 穴に落ちた判定
        if (self.p_y + config.PLAYER_SIZE) >= config.SCREEN_HEIGHT:
            return GameStatus.GAME_OVER

        # 自動的にジャンプする
        if self.is_landing:
            self.is_landing = False
            self.jump_v = -30
        else:
            self.jump_v += 2
        self.p_y += self.jump_v

        return GameStatus.GAMING
