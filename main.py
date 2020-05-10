import sys
import pygame
from pygame.locals import QUIT, Rect, KEYDOWN, K_SPACE

from gamestatus import GameStatus
import config
import gameroutine

def main():
    font_1 = pygame.font.SysFont(None, 72)
    font_2 = pygame.font.SysFont(None, 36)

    title_gametitle = font_1.render("Jump Jump Go !", True, (200, 200, 200))
    title_gameover = font_1.render("Game Over !", True, (200, 100, 100))
    title_prompt = font_2.render("Push SPACE to Start.", True, (200, 200, 200))

    game_status = GameStatus.WAITING
    keycode = None

    game_routine = gameroutine.GameRoutine(screen)

    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == KEYDOWN:
                keycode = e.key

        if game_status == GameStatus.WAITING:
            # ゲーム開始待機
            screen.blit(title_gametitle, (50, 200))
            screen.blit(title_prompt, (50, 300))
            if keycode == K_SPACE:
                game_status = GameStatus.GAMING
        elif game_status == GameStatus.GAMING:
            # ゲーム中
            game_status = game_routine.step(keycode)
        elif game_status == GameStatus.GAME_OVER:
            # ゲームオーバー
            screen.blit(title_gameover, (50, 200))
            screen.blit(title_prompt, (50, 300))
            if keycode == K_SPACE:
                game_status = GameStatus.WAITING
                game_routine.__init__(screen) # 初期化し直す
                # init() # 初期化

        keycode = None

        pygame.display.update()
        fpsclock.tick(30)

pygame.init()
pygame.key.set_repeat(5, 5)
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
fpsclock = pygame.time.Clock()

if __name__ == '__main__':
    main()
