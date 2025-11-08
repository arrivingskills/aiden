# Vision and Camera Control Changes

This document explains the changes made to stabilize the player’s view, prevent “seeing through” the ground, and make the first-person camera more manageable.

## Problem Summary
- Movement was applied relative to the camera’s own orientation:
  - `self.camera.setPos(self.camera, mov)` moved the camera in its local space.
  - When the camera was pitched up/down, its local forward included a vertical component, causing the camera to rise or sink while moving forward/back.
- There was no grounding or steady eye-height maintenance, so looking down and moving forward could drive the camera beneath the ground plane, making the player “see through” the ground.

## High-Level Fix
Introduce a player node that owns yaw and horizontal movement, and make the camera a child at a fixed eye height that only handles pitch. This decouples movement from pitch so forward/strafe remain horizontal regardless of where the player looks.

## What Changed (by file and location)

File: `src/aiden/adventure/game.py`

1) Initialization: create player hierarchy and define tunables
- Replaced the initial camera positioning block with:
  - New attributes:
    - `self.eye_height = 1.7`
    - `self.max_pitch = 60.0`
    - `self.mouse_sens = 0.2`
    - `self.yaw = 0.0`
    - `self.pitch = 0.0`
  - Created a `player` node at `(0, -20, 0)` and reparented `camera` to it at local `(0, 0, eye_height)`.
  - Ensured camera HPR starts at zero.

2) Runtime update: separate yaw (player) from pitch (camera); horizontal-only motion
- In `_update_camera`:
  - Movement now applies to `self.player` in its local plane:
    - `self.player.setPos(self.player, mov)`
    - Then `self.player.setZ(0.0)` clamps to the flat ground plane to maintain steady height.
  - Mouse look now updates `self.yaw` and `self.pitch` separately using `self.mouse_sens` and clamps pitch to `[-self.max_pitch, +self.max_pitch]`.
  - Applied orientation:
    - `self.player.setH(self.yaw)` (yaw only)
    - `self.camera.setH(0); self.camera.setP(self.pitch); self.camera.setR(0)` (pitch-only camera, no roll)

## Why This Works
- Movement no longer uses the pitched camera’s forward vector; only yaw affects direction. This keeps the camera at a constant height above the ground during movement.
- Clamping the player’s Z to `0.0` ensures we do not drift below/above a flat ground plane.
- Separating yaw (player) and pitch (camera) is a standard FPS setup that avoids unintended vertical motion due to look direction.

## Tuning
- `eye_height` (default 1.7): Adjust to change the camera’s perceived height above ground.
- `max_pitch` (default 60°): Tighten/loosen look up/down range.
- `mouse_sens` (default 0.2): Increase for faster turn rate; decrease for finer control.
- Movement speed remains as before; you can modify the scalar in `_update_camera` if needed.
- If you ever notice near-plane clipping when very close to geometry, consider slightly decreasing the near plane: `self.camLens.setNear(0.05)` (optional).

## Terrain-Aware Grounding
Implemented a downward collision ray from the player to determine ground height each frame.

- Setup (game):
  - Added `_init_grounding()` in `src/aiden/adventure/game.py` to create:
    - `self.ground_trav` (CollisionTraverser)
    - `self.ground_queue` (CollisionHandlerQueue)
    - A `CollisionRay` attached to the player, casting from `(0, 0, 10)` straight down.
    - From-collide mask uses bit 2.
  - In `_update_camera`, we traverse collisions, sort entries, and set `player.setZ(hit_z)` from the nearest hit. If no hit, we fallback to `z=0.0`.

- Setup (scenes):
  - Added an invisible ground collision plane at `z=0` with into-collide mask bit 2 in `src/aiden/adventure/scenes.py`.
  - This guarantees a hit for flat worlds and serves as a fallback if the visual environment lacks collision meshes.

Notes and limitations:
- True terrain following requires collision solids on your terrain geometry. The sample environment model does not ship with collision by default. You can add collision solids via EGG `<Collide>` tags, generate `CollisionPolygon`s, or integrate a physics/collision system (e.g., Bullet) with a proper heightfield/mesh.
- Until terrain meshes provide collisions, the ray will intersect our flat ground plane at z=0.

## Testing Checklist
- Look forward and move: height remains constant.
- Look fully up and move: no rising.
- Look fully down and move: no sinking; no “seeing through” the ground.
- Rapid mouse movement: no camera roll; pitch stops at clamp limits.

These changes bring the controller in line with common first-person camera architecture and should make the player’s vision stable and predictable.
