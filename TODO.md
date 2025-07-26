# Tower Defense Game - TODO List

## Stage & Board

- [x] Implement m x n grid of tiles
- [x] Support for lanes leading to main building
- [x] Main building with health points
- [x] Stage state updates per server tick
- [x] Configurable tick speed
- [ ] Support reading config from YAML, JSON, or TOML files
- [ ] Implement debug mode (details TBD)

## Monsters

- [x] Monster movement down lanes
- [x] Monster parameters: HP, Speed, Damage, Armour, Bounty
- [x] Monster Position: custom data structure
- [ ] Modifiers for monsters (list of Any) (types/effects TBD)
- [x] Global HP/Speed/Damage multipliers
- [x] Monster disappears after reaching main building

## Towers

- [x] Build towers on non-lane tiles
- [x] Tower parameters: Damage, Attack Speed, Cost
- [x] Building towers costs gold
- [x] Gold acquisition by killing monsters/finishing waves
- [x] Scrap tower for partial gold return
- [ ] Implement tower upgrade paths (design TBD)

## Game Flow

- [x] Player builds towers
- [x] Monsters deal damage to main building
- [x] Waves of monsters
