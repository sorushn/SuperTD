# src/game/board.py
from typing import List, Optional
from .monster import Monster
from .tower import Tower


class Tile:
    def __init__(self, is_lane: bool = False):
        self.is_lane = is_lane
        self.tower: Optional[Tower] = None


class Board:
    def __init__(self, m: int, n: int, lanes: List[List[tuple]]):
        self.m = m
        self.n = n
        self.tiles = [[Tile() for _ in range(n)] for _ in range(m)]
        for lane in lanes:
            for (x, y) in lane:
                self.tiles[x][y].is_lane = True
        self.lanes = lanes

    def place_tower(self, x: int, y: int, tower: Tower) -> bool:
        tile = self.tiles[x][y]
        if not tile.is_lane and tile.tower is None:
            tile.tower = tower
            return True
        return False

    def remove_tower(self, x: int, y: int) -> Optional[Tower]:
        tile = self.tiles[x][y]
        t = tile.tower
        tile.tower = None
        return t
