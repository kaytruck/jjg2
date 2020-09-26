import pygame
import random
from pygame.locals import Rect, K_LEFT, K_RIGHT, K_SPACE

import config
from player import Player
from gamestatus import GameStatus


class GameRoutine:
    def __init__(self, screen):
        """
        ゲーム初期化処理
        """
        self.player = Player()
        self.gap_to_next = self.get_gap_to_next()
        self.screen = screen
        self.score = 0
        self.new_floor_level = 0
        self.scroll_step = config.SCROLL_STEP

        # 地面の配列を初期化し、スタート位置の地面を配置する
        self.floors = []
        self.floors.append(
            Rect(
                0,
                config.SCREEN_HEIGHT - config.START_FLOOR_HEIGHT,
                700,
                config.START_FLOOR_HEIGHT,
            )
        )

        self.screen.fill((0, 0, 0))

    def step(self, keys, space_pressed):
        """
        ゲーム進行処理
        """
        self.score += config.SCORE_INC_STEP
        # レベルアップ
        self.level_up()

        if keys[K_LEFT]:
            self.player.p_x -= config.MOVE_X_STEP + config.SCROLL_STEP
        if keys[K_RIGHT]:
            self.player.p_x += config.MOVE_X_STEP
        if space_pressed and self.player.is_landing:
            self.player.is_going_jump = True
        if not (keys[K_LEFT] or keys[K_RIGHT]):
            # キー未入力時は画面スクロールとともに自機も左へ流れる
            self.player.p_x -= self.scroll_step

        # 横歩行の壁を超えない
        if self.player.p_x <= 0:
            self.player.p_x = 0
        elif self.player.p_x >= config.SCREEN_WIDTH:
            self.player.p_x = config.SCREEN_WIDTH

        # スクロール
        self.scroll()

        # ジャンプ、重力
        self.jump_and_gravity()

        # 接触判定のため、自機オブジェクトを仮で生成
        player_char = Rect(
            (self.player.p_x - 10, self.player.p_y),
            (config.PLAYER_SIZE, config.PLAYER_SIZE),
        )
        # 自機と地面の接触判定
        for f in self.floors:
            if player_char.colliderect(f):
                # print("地面と接触")
                self.player.is_landing = True
                self.player.is_going_jump = False
                self.player.p_y = f.top - config.PLAYER_SIZE
                # 地面と接触した場合、自機位置の補正
                player_char = Rect(
                    (self.player.p_x - config.PLAYER_SIZE / 2, self.player.p_y),
                    (config.PLAYER_SIZE, config.PLAYER_SIZE),
                )

        # 描画
        player_char = Rect(
            (self.player.p_x - 10, self.player.p_y),
            (config.PLAYER_SIZE, config.PLAYER_SIZE),
        )
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (200, 0, 0), player_char)
        for f in self.floors:
            pygame.draw.rect(self.screen, (100, 200, 100), f)

        # 穴に落ちたらゲームオーバー
        if (self.player.p_y + config.PLAYER_SIZE) >= config.SCREEN_HEIGHT:
            return GameStatus.GAME_OVER

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
            f_x = f.left - self.scroll_step
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
                # 新しいブロックは前のブロックよりも下
                floor_y = random.randint(self.floors[-1].top, config.SCREEN_HEIGHT - 30)
            floor_length = random.randint(
                90 - self.new_floor_level, 200 - self.new_floor_level
            )
            new_floor = Rect(
                (config.SCREEN_WIDTH, floor_y), (floor_length, config.FLOOR_HEIGHT)
            )
            self.floors.append(new_floor)

            # 新しい床の出現までランダムに間隔を空ける
            self.gap_to_next = self.get_gap_to_next()

    def level_up(self):
        """
        スコアが上がるごとに難易度を上げる
        """
        if self.score % 10000 == 0 and self.scroll_step < 10:
            self.scroll_step += 1

        if self.score % 5000 == 0 and self.new_floor_level < 70:
            self.new_floor_level += 5

    def jump_and_gravity(self):
        """
        ジャンプする
        """
        if self.player.is_going_jump:
            # 着地している場合はジャンプする
            self.player.is_landing = False
            self.player.is_going_jump = False
            self.player.jump_v = -30

        # 重力加速度
        self.player.jump_v += 2

        # 重力加速度の最大値を制限する
        if self.player.jump_v >= config.GRAVITY_V_MAX:
            self.player.jump_v = config.GRAVITY_V_MAX

        # 重力加速度の反映
        self.player.p_y += self.player.jump_v
