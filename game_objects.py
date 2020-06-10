from math import ceil
from typing import Tuple, Dict

import pygame


class GameObject:
    def __init__(self, scene=None, rect: pygame.Rect = pygame.Rect(0, 0, 0, 0), name=''):
        self.rect = rect
        self.name = name
        self.scene = scene

    def update(self):
        pass

    def render(self, display):
        pass

    def click(self, event):
        pass

    def check_event(self, event):
        if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            return self.rect.collidepoint(*event.pos)


class GameUnit(GameObject):
    def __init__(self, kind=None, scene=None, name=''):
        super().__init__(scene, name=name)
        self.value = kind

    def __eq__(self, other):
        if type(other) == type(self):
            return True
        return False

    def __ne__(self, other):
        if type(other) != type(self):
            return True
        return False


class Сharacter(GameUnit):
    def __init__(self, x, y, scene, kind='person', name='mainPerson'):
        super().__init__(kind, scene, name)

    def search(self, x, y):
        pass


class Grid(GameObject):
    def __init__(self, pos: Tuple[int, int], size_of_cell: int, num_of_cell: Tuple[int, int], width=3,
                 color=(255, 255, 255), scene=None, name=''):
        super().__init__(scene, name=name)

        self.pos = pos
        self.cells_size = size_of_cell
        self.cells_count = num_of_cell

        self.width = width
        self.color = color

        self.dy = self.cells_count[0] * self.cells_size
        self.dx = self.cells_count[1] * self.cells_size

        self.dys = self.dy // num_of_cell[0]
        self.dxs = self.dx // num_of_cell[1]

        self.grid = [[GameObject() for _ in range(num_of_cell[1])] for _ in range(num_of_cell[0])]

        self.rect = pygame.Rect(pos, (size_of_cell * num_of_cell[0] + width, size_of_cell * num_of_cell[1] + width))

    def render(self, display):
        pygame.draw.lines(display, self.color, True,
                          [self.pos,
                           (self.pos[0] + self.dx, self.pos[1]),
                           (self.pos[0] + self.dx,
                            self.pos[1] + self.dy),
                           (self.pos[0], self.pos[1] + self.dy)],
                          self.width)

        for i in range(1, self.cells_count[0]):
            pygame.draw.line(display, self.color,
                             (self.pos[0], self.pos[1] + self.dys * i),
                             (self.pos[0] + self.dx, self.pos[1] + self.dys * i), self.width)

        for i in range(1, self.cells_count[1]):
            pygame.draw.line(display, self.color,
                             (self.pos[0] + self.dxs * i, self.pos[1]),
                             (self.pos[0] + self.dxs * i, self.pos[1] + self.dy), self.width)

        for i in self.grid:
            for obj in i:
                obj.render(display)

    def get_ceil_pos(self, x, y):
        if x < self.pos[0] or y < self.pos[1]:
            return None

        x -= self.pos[0]
        y -= self.pos[1]

        x_coord = ceil(x / self.cells_size) - 1
        x_coord = 0 if x_coord < 0 else x_coord

        y_coord = ceil(y / self.cells_size) - 1
        y_coord = 0 if y_coord < 0 else y_coord

        if x_coord < self.cells_count[0] and y_coord < self.cells_count[1]:
            return x_coord, y_coord
        else:
            return None

    def edit(self, x: int, y: int, obj: GameObject):
        self.grid[x][y] = obj
        return True

    def get_centre(self, x: int, y: int):
        a = self.pos[0] + self.cells_size * (x + 1) - round(self.cells_size / 2)
        b = self.pos[1] + self.cells_size * (y + 1) - round(self.cells_size / 2)
        return a, b
