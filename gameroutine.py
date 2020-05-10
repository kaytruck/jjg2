import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT

import config
from gamestatus import GameStatus

class GameRoutine:
    # ゲーム変数
    # p_x = 0
    # p_y = 0
    # jump_v = 0
    # is_jumping = False
    # is_landing = True

    # ゲーム初期化処理
    def __init__(self, screen):
        # global p_x, p_y, jump_v, is_jumping, is_landing
        self.p_x = 400
        self.p_y = config.SCREEN_HEIGHT - config.PLAYER_SIZE
        self.jump_v = 0
        self.is_jumping = False
        self.is_landing = True
        self.screen = screen
        
        self.screen.fill((0, 0, 0))

    # ゲーム進行処理
    def step(self, keycode):
        # global p_x, p_y, jump_v, is_jumping, is_landing

        if keycode == K_LEFT:
            self.p_x -= config.MOVE_X_STEP
        elif keycode == K_RIGHT:
            self.p_x += config.MOVE_X_STEP

        # 横歩行の壁を超えない
        if self.p_x <= 0:
            self.p_x = 0
        elif self.p_x >= config.SCREEN_WIDTH:
            self.p_x = config.SCREEN_WIDTH

        # 描画
        self.screen.fill((0, 0, 0))
        player_char = Rect((self.p_x - 10, self.p_y), (config.PLAYER_SIZE, config.PLAYER_SIZE))
        r1 = Rect(700, 550, 50, 70)
        r2 = Rect(100, 500, 50, 100) # 終了判定実験用ブロック

        if player_char.colliderect(r1):
            self.is_landing = True
            self.p_y = r1.top - config.PLAYER_SIZE
            player_char = Rect((self.p_x - 10, self.p_y), (config.PLAYER_SIZE, config.PLAYER_SIZE))
            
        pygame.draw.rect(screen, (200, 0, 0), player_char)
        pygame.draw.rect(screen, (0, 100, 200), r1)
        pygame.draw.rect(screen, (100, 100, 200), r2)
        
        if player_char.colliderect(r2):
            return GameStatus.GAME_OVER

        if self.p_y + config.PLAYER_SIZE >= config.SCREEN_HEIGHT:
            self.is_landing = True

        # 自動的にジャンプする
        if self.is_landing:
            self.is_landing = False
            self.jump_v = -30
        else:
            self.jump_v += 2
        self.p_y += self.jump_v

        return GameStatus.GAMING
