# Tower Defense Game

Basic backend and framework for a simple tower defense game.

## Rules of the game

- A stage is an m by n grid of tiles
- Each stage consists of one or more lanes, which are contiguous set of tiles, leading to a main building with a set amount of health points
- The stage state is updated once per server tick, with tick speed being part of the engine parameters.
- Enemy monsters walk down the lanes, dealing damage to the main building when they reach it, disappearing afterwards
- The Player builds Towers on non-lane tiles, in order to stop the monsters from reaching the main buidling
- Bulding towers costs gold. Gold is acquired by killing towers and finishing waves.
- Each monster is defined by the following parameters:
  - HP/Health Points (Int): Is reduced every time the monster takes damage, and the monster is destroyed when HP reaches zero or negative
  - Speed (positive float): defines the number of tiles traversed by the monster per engine tick
  - Damage (positive float): defines the damage dealt to the main building once the monster reaches it
  - Armour (int): the amount of flat damage reduction for hits against the monster.
  - Bounty (positive int): the gold bonus for destroying the monster. it won't be awarded if the monster dies by reaching the main building
  - Position (type TBD): a custom data structure to define the position of the monster in the board.
  - Modifiers (list of Any): the set of modifiers that can positively or negatively affect the monster. possible modifiers TBD
  - In addition to the aforementioned parameters, there are global HP/Speed/Damage Multipliers that can affect the monster parameters in a stage.
- Each tower has the following parameters:
  - Damage (positive int): The amount of damage dealt with each hit from the tower
  - Attack Speed (float): Attacks per server tick
  - Cost to build (positive int): The amount of gold required for building the tower
- In addition to building towers, it's also possible to scrap or upgrade towers:
  - scrapping a tower destroys it, but returns a (set) percentage of building cost to player
  - Upgrading a tower replaces it with another tower. Upgrade paths are based on a design TBD

## Technical Requirements

- The engine should support reading the config from files with a chosen format. The format can be one of the following: YAML, JSON, TOML
- There should be a debug mode, with specificities TBD