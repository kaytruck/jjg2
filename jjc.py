import sys
import pygame
from pygame.locals import QUIT, Rect, KEYDOWN, K_LEFT, K_RIGHT

MOVE_X_STEP = 10     # 横方向のステップ
SCREEN_WIDTH = 800  # 画面の横幅
SCREEN_HEIGHT = 600 # 画面の高さ

pygame.init()
pygame.key.set_repeat(5, 5)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
fpsclock = pygame.time.Clock()

def main():
    p_x = 400
    p_y = 580
    jump_v = 0
    is_jumping = False

    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == KEYDOWN:
                if e.key == K_LEFT:
                    p_x -= MOVE_X_STEP
                elif e.key == K_RIGHT:
                    p_x += MOVE_X_STEP

        # 横歩行の壁を超えない
        if p_x <= 0:
            p_x = 0
        elif p_x >= SCREEN_WIDTH:
            p_x = SCREEN_WIDTH

        # 描画
        screen.fill((0, 0, 0))
        p_polygon = ((p_x, p_y - 20), (p_x - 10, p_y), (p_x + 10, p_y))
        pygame.draw.polygon(screen, (200, 0, 0), p_polygon, 0)

        # 自動的にジャンプする
        if p_y == 580:
            jump_v = -30
        else:
            jump_v += 2
        p_y += jump_v

        pygame.display.update()
        fpsclock.tick(30)

if __name__ == '__main__':
    main()
