import pygame
import math
from settings import TILE_SIZE, WIDTH, HEIGHT


class World:
    def __init__(self):
        self.tile_size = TILE_SIZE
        self.tileset = pygame.image.load("assets/dungeon/PNG/walls_floor.png").convert_alpha()

        self.cols = math.ceil(WIDTH / TILE_SIZE)
        self.rows = math.ceil(HEIGHT / TILE_SIZE)

        self.map_data = self.generate_room()

    def generate_room(self):
        map_data = []

        for row in range(self.rows):
            current_row = []

            for col in range(self.cols):
                if row == 0 or row == self.rows - 1 or col == 0 or col == self.cols - 1:
                    current_row.append(1)
                else:
                    current_row.append(0)

            map_data.append(current_row)

        return map_data

    def get_tile(self, col, row):
        tile = pygame.Surface((32, 32), pygame.SRCALPHA)
        tile.blit(self.tileset, (0, 0), (col * 32, row * 32, 32, 32))
        return tile

    def is_blocked(self, x, y):
        col = int(x // self.tile_size)
        row = int(y // self.tile_size)

        if row < 0 or row >= len(self.map_data):
            return True
        if col < 0 or col >= len(self.map_data[0]):
            return True

        return self.map_data[row][col] == 1

    def draw(self, screen):
        for row_index, row in enumerate(self.map_data):
            for col_index, tile_code in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size

                if tile_code == 0:
                    tile = self.get_tile(0, 3)
                elif tile_code == 1:
                    tile = self.get_tile(0, 0)
                else:
                    tile = self.get_tile(0, 3)

                screen.blit(tile, (x, y))