# src/game/tower.py
from abc import ABC, abstractmethod


class Tower(ABC):
    def upgrade(self):
        """Upgrade the tower. Override in subclasses for specific upgrade paths."""
        self.damage = int(self.damage * 1.5)
        self.attack_speed *= 1.2
        self.cost = int(self.cost * 1.5)

    def __init__(self, damage: int, attack_speed: float, cost: int):
        self.damage = damage
        self.attack_speed = attack_speed
        self.cost = cost
        self.cooldown = 0.0

    @abstractmethod
    def on_tick(self, board, engine, x, y):
        pass


class BasicTower(Tower):
    def upgrade(self):
        super().upgrade()

    def on_tick(self, board, engine, x, y):
        # Attack the first monster in range (lane-adjacent)
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        for lane in board.lanes:
            for (lx, ly) in lane:
                if abs(lx - x) <= 1 and abs(ly - y) <= 1:
                    # Find monster at this position
                    for monster in engine.monsters:
                        if monster.position.lane_idx == board.lanes.index(lane) and \
                                int(monster.position.progress) == lane.index((lx, ly)):
                            monster.take_damage(self.damage)
                            self.cooldown = 1 / self.attack_speed
                            return
