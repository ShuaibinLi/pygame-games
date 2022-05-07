import pygame
import time
import numpy as np
from board_generator import SudokuBoard

Num_Keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
Cube_Width, Cube_Height = 60, 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)


class Cube(object):
    def __init__(self, value, position):
        self.val = value
        self.temp_val = 0
        self.row = position[0]
        self.col = position[1]
        self.be_chosen = False
        if self.val:
            self.origin = True
        else:
            self.origin = False

    def set_value(self, val):
        self.val = val

    def draw(self, win):
        font = pygame.font.SysFont("KaiTi", 40)
        x = self.col * Cube_Width
        y = self.row * Cube_Height
        # Highlight the cube when be chosen
        if self.be_chosen and not self.origin:
            pygame.draw.rect(win, (234, 234, 239), (x, y, Cube_Width, Cube_Height), Cube_Width)
        #
        if self.origin:
            pygame.draw.rect(win, (255, 242, 226), (x, y, Cube_Width, Cube_Height), Cube_Width)
        # Fill in the correct num in black
        if self.val != 0:
            text = font.render(str(self.val), 1, BLACK)
            win.blit(text, (x + (Cube_Width / 2 - text.get_width() / 2), y + (Cube_Height / 2 - text.get_height() / 2)))
        # show the Wrong Num in red
        if self.val == 0 and self.temp_val != 0:
            text = font.render(str(self.temp_val), 1, RED)
            win.blit(text, (x + (Cube_Width / 2 - text.get_width() / 2), y + (Cube_Height / 2 - text.get_height() / 2)))


class Sudoku(object):
    def __init__(self, size=9, difficulty=0.5):
        self.sudoku_board = SudokuBoard(size=size, difficulty=difficulty)
        self.size = size
        self.difficulty = difficulty
        self.available_nums = self.sudoku_board.nums
        self.board = self.sudoku_board.masked_board
        self._ground_board = self.sudoku_board.board

        self.invalid_num = False
        self.wrong_num = False
        self.mistakes = 0
        self.grid_width = Cube_Width * self.size
        self.grid_height = Cube_Height * self.size

        # initiate cubes
        self.cubes = [[Cube(self.board[i][j], (i, j)) for j in range(self.size)] for i in range(self.size)]
        self.game_on = None
        self.win = False
        self.temp = None

    # Check click validity, then get the pos
    def check_click(self, pos):
        if pos[0] < self.grid_width and pos[1] < self.grid_height:
            x, y = pos[0] // Cube_Width, pos[1] // Cube_Height
            pos = [int(y), int(x)]
            # lock other positions
            for i in range(self.size):
                for j in range(self.size):
                    self.cubes[i][j].be_chosen = False
            self.cubes[pos[0]][pos[1]].be_chosen = True
            self.game_on = pos
            return pos
        return None

    def place_num(self, num):
        self.temp = num
        pos = self.game_on
        if self.cubes[pos[0]][pos[1]].val == 0:
            if self._ground_board[pos[0]][pos[1]] == num:
                self.cubes[pos[0]][pos[1]].set_value(num)
                self.board[pos[0]][pos][1] = num
                self.wrong_num = False
            elif num not in self.available_nums:
                self.cubes[pos[0]][pos[1]].temp_val = num
                self.invalid_num = True
            else:
                self.cubes[pos[0]][pos[1]].temp_val = num
                self.mistakes += 1
                self.wrong_num = True

    def clear_cube(self):
        pos = self.game_on
        if pos:
            if self.invalid_num:
                self.cubes[pos[0]][pos[1]].temp_val = 0
                self.invalid_num = False
            elif self.wrong_num:
                self.cubes[pos[0]][pos[1]].temp_val = 0
                self.wrong_num = False

    def game_over(self):
        for i in range(len(self.cubes)):
            for j in range(len(self.cubes[0])):
                if self.cubes[i][j].val == 0:
                    return False
        self.win = True
        if self.mistakes > 3:
            return True
        return True

    def draw(self, win, start_time):
        # Draw cubes
        for i in range(len(self.cubes)):
            for j in range(len(self.cubes[0])):
                cube = self.cubes[i][j]
                cube.draw(win)

        # Draw grid lines
        box_w = int(np.sqrt(self.size))
        box_h = self.size // box_w
        # 1. draw rows
        for i in range(self.size + 1):
            if i % box_w == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, BLACK, (0, i * Cube_Width), (self.grid_width, i * Cube_Width), thick)
        # 2. draw columns
        for i in range(self.size + 1):
            if i % box_h == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, BLACK, (i * Cube_Height, 0), (i * Cube_Height, self.grid_height), thick)

        self._show_text(win, start_time)

    def _show_text(self, win, start_time):
        fnt = pygame.font.SysFont("KaiTi", Cube_Width // 4)
        text = fnt.render(f"Difficulty: {self.difficulty}" * 1, 1, (0, 0, 0))
        win.blit(text, (20, self.grid_height + 10))
        time_text = fnt.render(f"Time: {str(round(time.time() - start_time))} s", 1, (0, 0, 0))
        win.blit(time_text, (20, self.grid_height + text.get_height() + 15))
        error_text = fnt.render(f"Errors: {self.mistakes}", 1, (255, 0, 0))
        win.blit(error_text, (20, self.grid_height + text.get_height() + time_text.get_height() + 20))

        # acton feedback
        fnt = pygame.font.SysFont("KaiTi", Cube_Width // 3)
        if self.win:
            text = fnt.render("Congratulation!", 1, RED)
            win.blit(text, (self.grid_width // 2 - text.get_width() // 2, self.grid_height + 20))
        # if self.mistakes > 3:
        #     text = fnt.render("Game Over!", 1, RED)
        #     win.blit(text, (self.grid_width // 2 - text.get_width() // 2, self.grid_height + 20))
        if self.wrong_num:
            text = fnt.render(f"{self.temp} is a Wrong Num!", 1, RED)
            win.blit(text, (self.grid_width // 2 - text.get_width() // 2, self.grid_height + 20))

        if self.invalid_num:
            text = fnt.render(f"{self.temp} is an Invalid num!", 1, RED)
            win.blit(text, (self.grid_width // 2 - text.get_width() // 2, self.grid_height + 20))
