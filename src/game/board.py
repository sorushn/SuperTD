# src/game/board.py
from typing import List, Optional

from .tower import Tower


class Tile:
    def __init__(self, is_lane: bool = False):
        self.is_lane = is_lane
        self.tower: Optional[Tower] = None


class MainBuilding:
    def __init__(self, hp: int):
        self.max_hp = hp
        self.hp = hp

    def take_damage(self, amount: float):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def is_destroyed(self) -> bool:
        return self.hp <= 0


class Board:
    def __init__(self, m: int, n: int, lanes: List[List[tuple]], main_building_hp: int = 100):
        self.m = m
        self.n = n
        self.tiles = [[Tile() for _ in range(n)] for _ in range(m)]
        for lane in lanes:
            for (x, y) in lane:
                self.tiles[x][y].is_lane = True
        self.lanes = lanes
        self.main_building = MainBuilding(main_building_hp)

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

    def scrap_tower(self, x: int, y: int, refund_ratio: float = 0.5) -> int:
        """Remove tower at (x, y) and return partial gold refund."""
        tile = self.tiles[x][y]
        if tile.tower:
            refund = int(tile.tower.cost * refund_ratio)
            tile.tower = None
            return refund
        return 0
