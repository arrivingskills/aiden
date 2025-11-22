Aiden Project

This repository includes assorted demos. It now also includes a small, structured Panda3D adventure game.

Adventure game: Shards of the Grove
- Engine: Panda3D (Python)
- Playtime: ~1 hour (casual exploration)
- Goal: Talk to the Elder, collect three shards scattered around, then return to the gate to restore the path.
- Controls: WASD to move, hold right mouse to look, left-click to interact.

Requirements
- Python 3.9+
- panda3d (pip install panda3d)

Run the game
- From the project root:

  python -m aiden.adventure.main

Notes
- The game uses Panda3D's sample models (models/environment, models/misc/rgbCube, models/misc/smiley). These are typically included with Panda3D. If unavailable, the game falls back to simple generated geometry so it still runs.
- GUI uses Panda3D's DirectGUI; no extra packages needed.
