# src/game/monster.py
from typing import Any, List
from abc import ABC, abstractmethod


class Position:
    def __init__(self, lane_idx: int, progress: float):
        self.lane_idx = lane_idx  # which lane
        self.progress = progress  # how far along the lane (in tiles)


class Monster(ABC):
    def __init__(self, hp: int, speed: float, damage: float, armour: int, bounty: int, position: Position, modifiers: List[Any] = None):
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.armour = armour
        self.bounty = bounty
        self.position = position
        self.modifiers = modifiers or []
        self.alive = True

    @abstractmethod
    def on_tick(self, board, engine):
        pass

    def take_damage(self, amount: int):
        effective = max(0, amount - self.armour)
        self.hp -= effective
        if self.hp <= 0:
            self.alive = False
        return effective


class BasicMonster(Monster):
    def on_tick(self, board, engine):
        self.position.progress += self.speed * engine.monster_speed_multiplier
