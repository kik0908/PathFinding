from math import ceil
from typing import Tuple, List

import pygame

from algos import create_graph, path_finding_bfd


class GameObject:
    def __init__(self, scene=None, rect: pygame.Rect = pygame.Rect(0, 0, 0, 0), parent=None, name=''):
        self.rect = rect
        self.parent = parent
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
    def __init__(self, kind=None, scene=None, parent=None, name=''):
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


class ZeroPoint(GameUnit):
    def __init__(self, x, y, size, scene, parent=None, name='startPoint', kind='person'):
        super().__init__(kind, scene, parent, name)
        k = 1
        self.rect = pygame.Rect((x, y), (size - k, size - k))
        self.rect.center = (x, y)
        self.center = self.rect.center


class Start(ZeroPoint):
    def __init__(self, x, y, size, scene, index, parent=None, name='startPoint'):
        super().__init__(x, y, size, scene, parent, name)

        self.index = index

    def render(self, display):
        pygame.draw.rect(display, (0, 255, 0), self.rect)


class End(ZeroPoint):
    def __init__(self, x, y, size, scene, index, parent=None, name='startPoint'):
        super().__init__(x, y, size, scene, parent, name)

        self.index = index

    def render(self, display):
        pygame.draw.rect(display, (255, 0, 0), self.rect)


class Point(ZeroPoint):
    def __init__(self, x, y, size, scene, parent=None, name='startPoint'):
        super().__init__(x, y, size, scene, parent, name)

    def render(self, display):
        pygame.draw.rect(display, (150, 205, 116), self.rect)


class Wall(ZeroPoint):
    def __init__(self, x, y, size, scene, parent=None, name='startPoint'):
        super().__init__(x, y, size, scene, parent, name)

    def render(self, display):
        pygame.draw.rect(display, (126, 126, 126), self.rect)


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

    def del_obj(self, i, j):
        self.grid[i][j] = GameObject()


class MyGrid(Grid):
    def __init__(self, pos: Tuple[int, int], size_of_cell: int, num_of_cell: Tuple[int, int], matrix: List, width=1,
                 color=(255, 255, 255), scene=None, name=''):
        super().__init__(pos, size_of_cell, num_of_cell, width, color, scene, name)

        self.matrix = matrix
        self.graph = create_graph(self.matrix, True)

        self.start = Start(*self.get_centre(0, 0), size_of_cell, scene, (0, 0), parent=self)
        self.end = End(*self.get_centre(num_of_cell[0] - 1, num_of_cell[1] - 1), size_of_cell, scene,
                       (num_of_cell[0] - 1, num_of_cell[1] - 1), parent=self)

    def render(self, display):
        super().render(display)

        self.start.render(display)
        self.end.render(display)

    def reset_objs(self, name=None):
        if name is None:
            self.grid = [[GameObject() for _ in range(self.cells_count[1])] for _ in range(self.cells_count[0])]
        else:
            for i, _ in enumerate(self.grid):
                for j, obj in enumerate(_):
                    if obj.name == name:
                        self.grid[i][j] = GameObject()

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.reset_objs('path')
            but, pos = event.button, event.pos
            coords = self.get_ceil_pos(*pos)
            y, x = coords
            if but == 1:
                self.start = Start(*self.get_centre(*coords), self.cells_size, self.scene, coords, parent=self)
            elif but == 3:
                self.end = End(*self.get_centre(*coords), self.cells_size, self.scene, coords, parent=self)
            elif but == 4:
                self.matrix[x][y] = 1
                self.edit(x, y, Wall(*self.get_centre(*coords), self.cells_size, self.scene, parent=self))
            elif but == 5:
                self.matrix[x][y] = 0
                self.del_obj(x, y)

            self.graph = create_graph(self.matrix, True)

            # num1 = coords[1] * self.cells_count[0] + coords[0]
            num_start = self.start.index[1] * self.cells_count[0] + self.start.index[0]
            num_end = self.end.index[1] * self.cells_count[0] + self.end.index[0]

            path = path_finding_bfd(num_start, num_end, self.graph)
            if path is not None:
                path = list(reversed(path[1:-1]))

                for point in path:
                    i, j = point // self.cells_count[0], point % self.cells_count[0]
                    self.edit(i, j, Point(*self.get_centre(j, i), self.cells_size, self.scene, name='path'))
