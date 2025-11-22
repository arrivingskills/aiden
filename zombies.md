### What I changed
- Implemented a complete zombie system that fulfills your requirements:
  - Random zombie spawns no more frequent than once per minute.
  - Zombies continuously move toward the player (converge behavior).
  - If a zombie touches the player, the player "dies" and respawns after 5 seconds.
- Added inline comments marked with `CHANGE:` to describe all modifications.

### Key implementation details
- Added spawn/death/respawn game state in `AdventureGame`:
  - `self.zombies`, `self.next_zombie_spawn_at`, `self.player_alive`, `self.respawn_deadline`, `self.respawn_delay`, `self.player_spawn_point`.
  - Spawns are scheduled with a minimum of 60s cooldown plus a small random offset.
- New runtime flow in `game.py`:
  - `_maybe_spawn_zombie()` enforces spawn timing and creates zombies in a random ring around the player.
  - `_update_zombies(dt)` moves all zombies toward the player, with simple facing and a contact check (distance < 1.0).
  - `_on_player_killed()` sets a respawn timer and shows a HUD message; `_update_respawn()` respawns the player after 5 seconds and re-enables control.
  - Player movement is disabled while dead.
- Cleaned up initial content:
  - Removed pre-placed zombie instance so zombies only appear via the randomized spawner.
- Improved `actors.Zombie`:
  - Safely load and attach the animated model (`Actor`) if assets are available; otherwise it still works with the fallback model.
  - Added a simple speed attribute and a `set_walking()` helper to switch idle/walk animations.

### Files modified
- `src/aiden/actors.py`
  - Attached Panda3D `Actor` under zombie node (try/except safe), added movement speed and `set_walking()`.
  - Added comments explaining changes.
- `src/aiden/game.py`
  - Added imports (`random`, `time`).
  - Added zombie/respawn state and initialization.
  - Removed initial hardcoded zombie. Added spawner and zombie update logic.
  - Disabled player movement while dead; added respawn logic.
  - Added comments explaining changes.

### Notes
- Initial zombie will spawn after 60–90 seconds of play. You can adjust timing and zombie speed by tweaking `self.next_zombie_spawn_at` scheduling and `Zombie.speed` respectively.
- Contact radius currently set to `1.0` units; change this to tune difficulty.
- If model/animation assets aren’t present, zombies still render via the fallback primitive from `_load_model_safe()`.