import sys
import pygame
from pygame.locals import QUIT, Rect, KEYDOWN, KEYUP, K_SPACE

from gamestatus import GameStatus
import config
import gameroutine


def main():
    font_1 = pygame.font.SysFont(None, 72)
    font_2 = pygame.font.SysFont(None, 36)

    title_gametitle = font_1.render("Jump Jump Go 2 !", True, (200, 200, 200))
    title_gameover = font_1.render("Game Over !", True, (200, 100, 100))
    title_prompt = font_2.render("Push SPACE to Start.", True, (200, 200, 200))
    title_reset = font_2.render("Push SPACE to Reset.", True, (200, 200, 200))

    game_status = GameStatus.WAITING

    game_routine = gameroutine.GameRoutine(screen)

    while True:
        space_pressed = False
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    space_pressed = True
        keys = pygame.key.get_pressed()

        if game_status == GameStatus.WAITING:
            # ゲーム開始待機
            screen.blit(title_gametitle, (50, 200))
            screen.blit(title_prompt, (50, 300))
            if space_pressed:
                game_status = GameStatus.GAMING
        elif game_status == GameStatus.GAMING:
            # ゲーム中
            game_status = game_routine.step(keys, space_pressed)
            title_score = font_2.render(
                f"SCORE: {game_routine.score}", True, (50, 50, 200)
            )
            screen.blit(title_score, (50, 50))
        elif game_status == GameStatus.GAME_OVER:
            # ゲームオーバー
            screen.blit(title_gameover, (50, 200))
            screen.blit(title_reset, (50, 300))
            if space_pressed:
                game_status = GameStatus.WAITING
                game_routine.__init__(screen)  # 初期化し直す

        pygame.display.update()
        fpsclock.tick(config.FPS)


pygame.init()
pygame.display.set_caption(config.WINDOW_CAPTION)
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
fpsclock = pygame.time.Clock()

if __name__ == "__main__":
    main()
