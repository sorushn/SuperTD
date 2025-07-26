# src/game/engine.py

import time
from typing import List

from .board import Board
from .config_loader import ConfigLoader
from .monster import Monster


class Engine:
    def __init__(
        self,
        board: Board,
        monsters: List[Monster],
        gold: int,
        tick_interval: float = 1.0,
        waves: list = None,
        config_path: str = None,
        debug: bool = False,
    ):

        self.board = board
        self.monster_speed_multiplier = 1.0
        self.monster_damage_multiplier = 1.0
        self.monster_hp_multiplier = 1.0
        self.tick_count = 0
        self.tick_interval = tick_interval  # seconds between ticks
        self.gold = gold
        self.waves = waves or []  # List[List[Monster]]
        self.current_wave = 0
        self.debug = debug
        # Load config if provided
        if config_path:
            config = ConfigLoader.load_config(config_path)
            self._apply_config(config)
        # Apply HP multiplier to all initial monsters
        self.monsters = []
        for m in monsters:
            m.hp = int(m.hp * self.monster_hp_multiplier)
            self.monsters.append(m)

    def _apply_config(self, config):
        if not config:
            return
        self.tick_interval = config.get('tick_interval', self.tick_interval)
        self.monster_speed_multiplier = config.get(
            'monster_speed_multiplier', self.monster_speed_multiplier)
        self.monster_damage_multiplier = config.get(
            'monster_damage_multiplier', self.monster_damage_multiplier)
        self.monster_hp_multiplier = config.get(
            'monster_hp_multiplier', self.monster_hp_multiplier)
        self.debug = config.get('debug', self.debug)

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
                    damage = monster.damage * self.monster_damage_multiplier
                    self.board.main_building.take_damage(damage)
                    monster.alive = False
                    self.monsters.remove(monster)
            else:
                self.gold += monster.bounty
                self.monsters.remove(monster)
        self.tick_count += 1
        # Award bonus gold and spawn next wave if wave is finished (no monsters left)
        if not self.monsters:
            self.gold += 50  # Example bonus, can be made configurable
            if self.current_wave < len(self.waves):
                # Spawn next wave
                for m in self.waves[self.current_wave]:
                    m.hp = int(m.hp * self.monster_hp_multiplier)
                    self.monsters.append(m)
                self.current_wave += 1

    def is_game_over(self) -> bool:
        return self.board.main_building.is_destroyed()

    def run(self, max_ticks: int = None):
        """Run the game loop, advancing by tick_interval seconds."""
        while not self.is_game_over():
            self.tick()
            if max_ticks is not None and self.tick_count >= max_ticks:
                break
            time.sleep(self.tick_interval)
