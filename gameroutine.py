import pygame
import random
from pygame.locals import Rect, K_LEFT, K_RIGHT

import config
from gamestatus import GameStatus

class GameRoutine:

    # ゲーム初期化処理
    def __init__(self, screen):
        self.p_x = config.SCREEN_WIDTH / 2
        self.p_y = config.SCREEN_HEIGHT - config.PLAYER_SIZE - config.FLOOR_HEIGHT
        self.jump_v = 0
        self.is_jumping = False
        self.is_landing = True
        self.gap_to_next = self.get_gap_to_next()
        self.screen = screen
        
        self.screen.fill((0, 0, 0))

        self.floors = []
        self.floors.append(Rect(0, config.SCREEN_HEIGHT - config.FLOOR_HEIGHT, 700, config.FLOOR_HEIGHT))

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

        # 地面をスクロールする
        for f in self.floors:
            f_x = f.left - config.SCROLL_STEP
            f.left = f_x
        # 画面左端に達した地面を消す
        if self.floors[0].right < 0:
            del self.floors[0]
        # 画面右端にブロックを追加する
        if (config.SCREEN_WIDTH - self.floors[-1].right) > self.gap_to_next:
            floor_length = random.randint(1, 4) * config.FLOOR_LENGTH_COEFFICENT
            floor_height = random.randint(1, 7) * 20 # TODO 次の地面の高さは、前の高さを配慮する(極端に高いと登れないため)
            new_floor = Rect((config.SCREEN_WIDTH, config.SCREEN_HEIGHT - floor_height),
                (floor_length, config.FLOOR_HEIGHT))
            self.floors.append(new_floor)
            self.gap_to_next = self.get_gap_to_next()
        # 自機位置
        player_char = Rect((self.p_x - 10, self.p_y), (config.PLAYER_SIZE, config.PLAYER_SIZE))

        r1 = Rect(700, 450, 50, 100)     # TODO ジャンプ実験用ブロック
        r2 = Rect(50, 400, 50, 100)    # TODO 終了判定実験用ブロック

        for f in self.floors:
            if player_char.colliderect(f):
                self.is_landing = True
                self.p_y = f.top - config.PLAYER_SIZE
                player_char = Rect((self.p_x - config.PLAYER_SIZE / 2, self.p_y), (config.PLAYER_SIZE, config.PLAYER_SIZE))
            
        # 描画
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (200, 0, 0), player_char)
        pygame.draw.rect(self.screen, (0, 100, 200), r1)
        pygame.draw.rect(self.screen, (100, 100, 200), r2)
        for f in self.floors:
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

    def get_gap_to_next(self):
        return random.randint(1, 4) * config.GAP_TO_NEXT_COEFFICIENT