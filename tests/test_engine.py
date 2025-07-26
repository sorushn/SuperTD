import pytest

from src.game.board import Board
from src.game.engine import Engine
from src.game.monster import BasicMonster, Position
from src.game.tower import BasicTower


def test_engine_config_loading(simple_board, basic_monster):
    # Use the example config file
    import os

    from src.game.engine import Engine
    config_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'config.toml'))
    engine = Engine(simple_board, [basic_monster],
                    gold=0, config_path=config_path)
    assert engine.tick_interval == 1.0
    assert engine.monster_speed_multiplier == 1.0
    assert engine.monster_damage_multiplier == 1.0
    assert engine.monster_hp_multiplier == 1.0
    assert engine.debug is False

# tests/test_engine.py


@pytest.fixture
def simple_board():
    # 3x3 board, one lane from (0,0) to (2,0)
    lanes = [[(0, 0), (1, 0), (2, 0)]]
    board = Board(3, 3, lanes, main_building_hp=20)
    return board


@pytest.fixture
def basic_monster():
    return BasicMonster(hp=10, speed=1.0, damage=5, armour=0, bounty=10, position=Position(0, 0.0))


@pytest.fixture
def basic_tower():
    return BasicTower(damage=5, attack_speed=1.0, cost=10)


def test_monster_moves(simple_board, basic_monster):
    engine = Engine(simple_board, [basic_monster], gold=0)
    engine.tick()
    assert basic_monster.position.progress > 0


def test_tower_attacks(simple_board, basic_monster, basic_tower):
    simple_board.place_tower(1, 1, basic_tower)
    engine = Engine(simple_board, [basic_monster], gold=0)
    # Move monster to (1,0)
    basic_monster.position.progress = 1.0
    engine.tick()
    assert basic_monster.hp < 10


def test_monster_reaches_end(simple_board, basic_monster):
    engine = Engine(simple_board, [basic_monster], gold=0)
    basic_monster.position.progress = 2.0
    engine.tick()
    assert simple_board.main_building.hp < 20
    assert not basic_monster.alive


def test_gold_awarded_on_kill(simple_board, basic_monster, basic_tower):
    simple_board.place_tower(1, 1, basic_tower)
    engine = Engine(simple_board, [basic_monster], gold=0)
    basic_monster.position.progress = 1.0
    basic_monster.hp = 5
    engine.tick()
    assert engine.gold == 60
