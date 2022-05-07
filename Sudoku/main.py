import time
import pygame
import argparse
from gui import Sudoku

Num_Keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
Cube_Width, Cube_Height = 60, 60


def main():
    win_width = args.size * Cube_Width
    win_height = (args.size + 1) * Cube_Height

    pygame.display.set_caption("Sudoku")
    pygame.font.init()
    win = pygame.display.set_mode((win_width, win_height))

    start = time.time()
    run = True
    grid = Sudoku(size=args.size, difficulty=args.difficulty)

    while run:
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                for i in range(len(Num_Keys)):
                    if event.key == Num_Keys[i]:
                        key = i + 1
                if event.key == pygame.K_0:
                    grid.clear_cube()
                    key = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                cor = pygame.mouse.get_pos()
                grid.check_click(cor)

        if grid.game_on and key:
            grid.place_num(key)
            if grid.game_over():
                print("Success")
                run = False

        win.fill((250, 249, 222))
        grid.draw(win, start)
        pygame.display.update()

    time.sleep(5)
    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", default=9, help='Sudoku game board: 4,6,9')
    parser.add_argument("--difficulty", default=0.1, help='Difficulty of the game')
    args = parser.parse_args()

    main()
