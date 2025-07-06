# src/game/engine.py
from typing import List
from .board import Board
from .monster import Monster
from .tower import Tower


class Engine:
    def __init__(self, board: Board, monsters: List[Monster], gold: int, main_building_hp: int):
        self.board = board
        self.monsters = monsters
        self.gold = gold
        self.main_building_hp = main_building_hp
        self.monster_speed_multiplier = 1.0
        self.monster_damage_multiplier = 1.0
        self.monster_hp_multiplier = 1.0
        self.tick_count = 0

    def tick(self):
        # Towers attack
        for x in range(self.board.m):
            for y in range(self.board.n):
                tile = self.board.tiles[x][y]
                if tile.tower:
                    tile.tower.on_tick(self.board, self, x, y)
        # Monsters move
        for monster in list(self.monsters):
            if monster.alive:
                monster.on_tick(self.board, self)
                # Check if reached end of lane
                lane = self.board.lanes[monster.position.lane_idx]
                if monster.position.progress >= len(lane):
                    self.main_building_hp -= monster.damage * self.monster_damage_multiplier
                    monster.alive = False
                    self.monsters.remove(monster)
            else:
                self.gold += monster.bounty
                self.monsters.remove(monster)
        self.tick_count += 1
