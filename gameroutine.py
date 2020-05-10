import pygame
import random
from pygame.locals import Rect, K_LEFT, K_RIGHT

import config
from gamestatus import GameStatus

class GameRoutine:

    def __init__(self, screen):
        """
        ゲーム初期化処理
        """
        self.p_x = config.SCREEN_WIDTH / 2
        self.p_y = config.SCREEN_HEIGHT - config.PLAYER_SIZE - config.FLOOR_HEIGHT
        self.jump_v = 0
        self.is_landing = True
        self.gap_to_next = self.get_gap_to_next()
        self.screen = screen
        self.screen.fill((0, 0, 0))

        self.score = 0

        self.floors = []
        self.floors.append(Rect(0, config.SCREEN_HEIGHT - config.FLOOR_HEIGHT, 700, config.FLOOR_HEIGHT))

    def step(self, keycode):
        """
        ゲーム進行処理
        """
        self.score += config.SCORE_INC_STEP

        if keycode == K_LEFT:
            self.p_x -= (config.MOVE_X_STEP + config.SCROLL_STEP)
        elif keycode == K_RIGHT:
            self.p_x += config.MOVE_X_STEP
        elif keycode == None:
            # キー未入力時は画面スクロールとともに自機も左へ流れる
            self.p_x -= config.SCROLL_STEP

        # 横歩行の壁を超えない
        if self.p_x <= 0:
            self.p_x = 0
        elif self.p_x >= config.SCREEN_WIDTH:
            self.p_x = config.SCREEN_WIDTH

        # スクロール
        self.scroll()
        
        # 自機位置の算出
        player_char = Rect((self.p_x - 10, self.p_y), (config.PLAYER_SIZE, config.PLAYER_SIZE))

        # 自機と地面の接触判定
        for f in self.floors:
            if player_char.colliderect(f):
                self.is_landing = True
                self.p_y = f.top - config.PLAYER_SIZE
                player_char = Rect((self.p_x - config.PLAYER_SIZE / 2, self.p_y), (config.PLAYER_SIZE, config.PLAYER_SIZE))
            
        # 描画
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (200, 0, 0), player_char)
        for f in self.floors:
            pygame.draw.rect(self.screen, (100, 200, 100), f)

        # 穴に落ちたらゲームオーバー
        if (self.p_y + config.PLAYER_SIZE) >= config.SCREEN_HEIGHT:
            return GameStatus.GAME_OVER

        # ジャンプする
        self.jump()

        return GameStatus.GAMING

    def get_gap_to_next(self):
        """
        次に右端に出現するブロックとの間隔を調整する
        """
        return random.randint(80, 240)
    
    def scroll(self):
        """
        右から左へスクロールする
        """
        # スクロールする
        for f in self.floors:
            f_x = f.left - config.SCROLL_STEP
            f.left = f_x
        # 画面左端に達した地面を消す
        if self.floors[0].right < 0:
            del self.floors[0]
        # 画面右端にブロックを追加する
        if (config.SCREEN_WIDTH - self.floors[-1].right) > self.gap_to_next:
            if random.choice([True, False]):
                # 新しいブロックは前のブロックよりも上
                floor_y_top = max(self.floors[-1].top - config.GAP_UP_Y_TO_NEXT, 230)
                floor_y = random.randint(floor_y_top, self.floors[-1].top)
            else:
                #新しいブロックは前のブロックよりも下
                floor_y = random.randint(self.floors[-1].top, config.SCREEN_HEIGHT - 20)
            floor_length = random.randint(90, 200)
            new_floor = Rect((config.SCREEN_WIDTH, floor_y), (floor_length, config.FLOOR_HEIGHT))
            self.floors.append(new_floor)
            self.gap_to_next = self.get_gap_to_next()

    def jump(self):
        """
        ジャンプする
        """
        if self.is_landing:
            # 着地した場合はジャンプする
            self.is_landing = False
            self.jump_v = -30
        else:
            # ジャンプ中は重力が働く
            self.jump_v += 2
        self.p_y += self.jump_v
