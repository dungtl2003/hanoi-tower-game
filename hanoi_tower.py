"""
Ha Noi Tower game with visual animation
"""
from collections.abc import Iterable
from enum import Enum
import pygame
from config import (
    WIDTH,
    MAX_DISK_WIDTH,
)


class Pillar(Iterable):
    """Pillar that contains disks"""

    def __init__(self, number) -> None:
        self.number = number
        self.__storage = []
        self.__index = 0

    def size(self):
        """Get number of disks in the pillar"""
        return len(self.__storage)

    def append(self, disk):
        """Add a disk on top of the pillar"""
        self.__storage.append(disk)

    def pop(self):
        """Remove the top disk of the pillar"""
        return self.__storage.pop()

    def top(self):
        """Get the top disk of the pillar"""
        return self.__storage[-1]

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index >= len(self.__storage):
            raise StopIteration

        value = self.__storage[self.__index]
        self.__index += 1
        return value


class STATE(Enum):
    """State of the disk"""

    START = "Start"
    TAKE_OUT = "Take out"
    TRANSFER = "Transfer"
    PUT_IN = "Put in"
    END = "End"


class Disk(pygame.sprite.Sprite):
    COLUMN_CENTERS = {
        1: MAX_DISK_WIDTH // 2 + 30,
        2: WIDTH // 2,
        3: WIDTH - (MAX_DISK_WIDTH // 2 + 30),
    }

    def __init__(self, col, y, width, height, color="#E41717"):
        self.rect = pygame.Rect(
            self.COLUMN_CENTERS[col] - (min(MAX_DISK_WIDTH, width) // 2),
            y,
            min(MAX_DISK_WIDTH, width),
            height,
        )
        self.color = color
        self.column = col
        self.state = STATE.START

    def move(self, dx, dy):
        """Move"""
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, win):
        """Draw a rectangle"""
        pygame.draw.rect(win, self.color, self.rect)
