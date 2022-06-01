import pygame
from constants import *
from classes import *
import matrixGenerator
import time

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("すどく")
font = pygame.font.SysFont("Comic Sans MS", 28)
font_bold = pygame.font.SysFont("Comic Sans MS", 28, bold=True)
font_win = pygame.font.SysFont("Comic Sans MS", 44, bold=True)

bg = pygame.Surface(screen.get_size())
bg = bg.convert()

answer, question = matrixGenerator.generate_board()
block_ls = [[] for i in range(9)]
for i in range(9):
    for j in range(9):
        block_ls[i].append(Block(question[i][j], Pos((175 + j * 50, 60 + i * 50)), question[i][j] == 0))
chosen = Pos((-1, -1))


def render(by_mouse: bool) -> None:
    bg.fill(BG_COLOR)
    global chosen
    chosen = Pos((pygame.mouse.get_pos()))
    if by_mouse and chosen.is_in_range(175, 60, 450):
        chosen.to_index()
        pygame.draw.rect(bg, CHOSEN_COLOR, [chosen.x * 50 + 175, chosen.y * 50 + 60, 50, 50], 0)
    else:
        chosen = Pos((-1, -1))
    for i in range(0, 451, 50):
        ln_width = 5 if i % 450 == 0 else 3 if i % 150 == 0 else 1
        pygame.draw.line(bg, LINE_COLOR, (175 + i, 60), (175 + i, 510), ln_width)
        pygame.draw.line(bg, LINE_COLOR, (175, 60 + i), (625, 60 + i), ln_width)
    for row in block_ls:
        for b in row:
            if b.number != 0:
                text = (font if b.writable else font_bold).render(str(b.number),
                                                                  True,
                                                                  LINE_COLOR if b.valid else WRONG_COLOR)
                text_rect = text.get_rect(center=(b.pos.x + 25, b.pos.y + 25))
                bg.blit(text, text_rect)
    screen.blit(bg, (0, 0))
    pygame.display.update()


def check_valid(number: int, pos: Pos) -> bool:
    for i in range(9):
        if i != pos.y and number == block_ls[i][pos.x].number:
            return False
    for i in range(9):
        if i != pos.x and number == block_ls[pos.y][i].number:
            return False
    for i in range(pos.y // 3 * 3, pos.y // 3 * 3 + 3):
        for j in range(pos.x // 3 * 3, pos.x // 3 * 3 + 3):
            if i != pos.y and j != pos.x and number == block_ls[i][j].number:
                return False
    return True


def check_win() -> bool:
    for i in range(9):
        for j in range(9):
            if block_ls[i][j] == 0:
                return False
            if block_ls[i][j].number != answer[i][j]:
                return False
    return True


render(False)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            render(True)
        elif event.type == pygame.KEYDOWN and chosen != Pos((-1, -1)) and block_ls[chosen.y][chosen.x].writable:
            if pygame.K_1 <= event.key <= pygame.K_9:
                key_value = event.key - pygame.K_1 + 1
            elif pygame.K_KP1 <= event.key <= pygame.K_KP9:
                key_value = event.key - pygame.K_KP1 + 1
            else:
                continue
            block_ls[chosen.y][chosen.x].number = key_value
            block_ls[chosen.y][chosen.x].valid = check_valid(key_value, chosen)
            if check_win():
                running = False
            render(False)

text = font_win.render('Win!!', True, LINE_COLOR, CHOSEN_COLOR)
text_rect = text.get_rect(center=(400, 550))
bg.blit(text, text_rect)
screen.blit(bg, (0, 0))
pygame.display.update()

time.sleep(5)
pygame.quit()
