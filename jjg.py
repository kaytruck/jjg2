import sys
import pygame
from pygame.locals import QUIT, Rect, KEYDOWN, K_LEFT, K_RIGHT, K_SPACE
from gamestatus import GameStatus
import config

# ゲーム変数
p_x = 0
p_y = 0
jump_v = 0
is_jumping = False
is_landing = True

# ゲーム初期化処理
def init():
    global p_x, p_y, jump_v, is_jumping, is_landing
    p_x = 400
    p_y = config.SCREEN_HEIGHT - config.PLAYER_SIZE
    jump_v = 0
    is_jumping = False
    is_landing = True

    screen.fill((0, 0, 0))

# ゲーム進行処理
def gaming(keycode):
    global p_x, p_y, jump_v, is_jumping, is_landing

    if keycode == K_LEFT:
        p_x -= config.MOVE_X_STEP
    elif keycode == K_RIGHT:
        p_x += config.MOVE_X_STEP

    # 横歩行の壁を超えない
    if p_x <= 0:
        p_x = 0
    elif p_x >= config.SCREEN_WIDTH:
        p_x = config.SCREEN_WIDTH

    # 描画
    screen.fill((0, 0, 0))
    player_char = Rect((p_x - 10, p_y), (config.PLAYER_SIZE, config.PLAYER_SIZE))
    r1 = Rect(700, 550, 50, 70)
    r2 = Rect(100, 500, 50, 100) # 終了判定実験用ブロック

    if player_char.colliderect(r1):
        is_landing = True
        p_y = r1.top - config.PLAYER_SIZE
        player_char = Rect((p_x - 10, p_y), (config.PLAYER_SIZE, config.PLAYER_SIZE))
        
    pygame.draw.rect(screen, (200, 0, 0), player_char)
    pygame.draw.rect(screen, (0, 100, 200), r1)
    pygame.draw.rect(screen, (100, 100, 200), r2)
    
    if player_char.colliderect(r2):
        return GameStatus.GAME_OVER

    if p_y + config.PLAYER_SIZE >= config.SCREEN_HEIGHT:
        is_landing = True

    # 自動的にジャンプする
    if is_landing:
        is_landing = False
        jump_v = -30
    else:
        jump_v += 2
    p_y += jump_v

    return GameStatus.GAMING

def main():
    font_1 = pygame.font.SysFont(None, 72)
    font_2 = pygame.font.SysFont(None, 36)

    title_gametitle = font_1.render("Jump Jump Go !", True, (200, 200, 200))
    title_gameover = font_1.render("Game Over !", True, (200, 100, 100))
    title_prompt = font_2.render("Push SPACE to Start.", True, (200, 200, 200))

    game_status = GameStatus.WAITING
    keycode = None

    init() # ゲーム初期化
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
            game_status = gaming(keycode)
        elif game_status == GameStatus.GAME_OVER:
            # ゲームオーバー
            screen.blit(title_gameover, (50, 200))
            screen.blit(title_prompt, (50, 300))
            if keycode == K_SPACE:
                game_status = GameStatus.WAITING
                init() # 初期化

        keycode = None

        pygame.display.update()
        fpsclock.tick(30)

pygame.init()
pygame.key.set_repeat(5, 5)
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
fpsclock = pygame.time.Clock()

if __name__ == '__main__':
    main()
