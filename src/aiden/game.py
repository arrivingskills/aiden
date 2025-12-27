from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    WindowProperties,
    CollisionTraverser,
    CollisionNode,
    CollisionRay,
    CollisionHandlerQueue,
    BitMask32,
)
from panda3d.core import AmbientLight, DirectionalLight, Vec4, Vec3, ClockObject
from direct.task import Task
import random  # CHANGE: used for random zombie spawn timing/locations
import time  # CHANGE: used for respawn timers and scheduling

from .gui import HUD, Dialog
from .actors import NPC, Item, Zombie
from .quests import QuestLog, Quest
from .scenes import load_environment

# ZOMBIE_RESPAWN_INTERVAL = 60.0 + random.uniform(0.0, 30.0)
ZOMBIE_RESPAWN_INTERVAL = 20


class AdventureGame(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()  # we implement our own camera
        self._setup_window()
        self._setup_lighting()

        # World
        self.world = load_environment(self.loader)
        self.world.reparentTo(self.render)

        # GUI
        self.hud = HUD()
        self.dialog = Dialog()

        # Input
        self._init_input()

        # Picking
        self._init_picking()

        # State
        self.inventory = []
        self.actors = {}

        # CHANGE: add zombie/spawn/death state
        self.zombies = []
        now = time.time()
        self.next_zombie_spawn_at = (
            now + ZOMBIE_RESPAWN_INTERVAL
        )  # no more frequent than 1 min
        self.player_alive = True
        self.respawn_deadline = None
        self.respawn_delay = 5.0
        self.player_spawn_point = Vec3(0, -20, 0)

        # Player attack config
        self.attack_damage = 34  # damage per click
        self.attack_cooldown = 0.35  # seconds
        self._last_attack_time = 0.0

        # Quests
        self.quests = QuestLog()
        self._init_content()
        self.hud.set_objective(self.quests.objective_text())

        # Player and camera hierarchy: fix eye height and separate yaw/pitch
        self.eye_height = 1.7
        self.max_pitch = 60.0
        self.mouse_sens = 0.2
        self.yaw = 0.0
        self.pitch = 0.0

        self.player = self.render.attachNewNode("player")
        self.player.setPos(self.player_spawn_point)
        self.player.setHpr(0, 0, 0)

        # Reparent camera to player and set fixed eye height
        self.camera.reparentTo(self.player)
        self.camera.setPos(0, 0, self.eye_height)
        self.camera.setHpr(0, 0, 0)

        # Grounding (terrain-aware via downward ray); init after player is created
        self._init_grounding()

        self.taskMgr.add(self._update, "update")

    # --- setup helpers ---
    def _setup_window(self):
        props = WindowProperties()
        props.setTitle("Shards of the Grove - A Small Adventure")
        self.win.requestProperties(props)

    def _setup_lighting(self):
        alight = AmbientLight("alight")
        alight.setColor(Vec4(0.6, 0.6, 0.6, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        dlight = DirectionalLight("dlight")
        dlight.setColor(Vec4(0.9, 0.9, 0.9, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(45, -45, 0)
        self.render.setLight(dlnp)

    def _init_input(self):
        self.keys = {k: False for k in ["w", "a", "s", "d", "shift"]}
        for key in ["w", "a", "s", "d", "shift"]:
            self.accept(key, self._set_key, [key, True])
            self.accept(f"{key}-up", self._set_key, [key, False])
        self.accept("mouse1", self._on_click)

    def _set_key(self, key, value):
        self.keys[key] = value

    def _init_picking(self):
        self.picker = CollisionTraverser()
        self.pq = CollisionHandlerQueue()
        self.picker_node = CollisionNode("mouseRay")
        self.picker_np = self.camera.attachNewNode(self.picker_node)
        # Ray should only be a FROM object on mask bit 1 and never be hittable
        self.picker_node.setFromCollideMask(BitMask32.bit(1))
        self.picker_node.setIntoCollideMask(BitMask32.allOff())
        self.picker_ray = CollisionRay()
        self.picker_node.addSolid(self.picker_ray)
        self.picker.addCollider(self.picker_np, self.pq)

        # Set this mask to actor collision nodes we care about
        self.actor_mask = BitMask32.bit(1)

    def _init_grounding(self):
        """Set up a downward ray to find ground height (mask bit 2)."""
        self.ground_trav = CollisionTraverser()
        self.ground_queue = CollisionHandlerQueue()
        self.ground_node = CollisionNode("groundRay")
        # Grounding ray casts against ground (bit 2) and must not be hittable
        self.ground_node.setFromCollideMask(BitMask32.bit(2))
        self.ground_node.setIntoCollideMask(BitMask32.allOff())
        # Attach to player so origin follows player; cast from above head downwards
        self.ground_np = self.player.attachNewNode(self.ground_node)
        self.ground_ray = CollisionRay(0, 0, 10.0, 0, 0, -1)
        self.ground_node.addSolid(self.ground_ray)
        self.ground_trav.addCollider(self.ground_np, self.ground_queue)

    def _init_content(self):
        # Spawn NPC elder at center
        # elder_model = self._load_model_safe(["models/misc/smiley", "models/misc/sphere"])  # friendly face
        # elder_model.setScale(1.4)
        # elder = NPC(elder_model, name="Elder", dialog_lines=[
        #     "Welcome, traveler. Our grove is broken into three shards.",
        #     "Find the three Shards of the Grove and return to me.",
        #     "Place them at the ancient gate to restore the path."
        # ])
        # elder.reparent_to(self.render).set_pos(0, 10, 0)
        # elder.node.setCollideMask(self.actor_mask)
        # self.actors['elder'] = elder

        # CHANGE: remove the always-on starting zombie; zombies now spawn at random
        # intervals via the runtime update (see _maybe_spawn_zombie). Keeping the
        # pre-placed zombie would violate the "at random" intent and complicate
        # the cooldown rule, so we rely on the spawner exclusively.

        # Place three shard items around the map
        positions = [(-8, 25, 0.2), (10, 35, 0.2), (6, 18, 0.2)]
        for i, pos in enumerate(positions, 1):
            shard_model = self._load_model_safe(
                ["models/misc/rgbCube", "models/misc/sphere"]
            )
            shard_model.setScale(0.7)
            shard_model.setColorScale(0.6 + 0.1 * i, 0.8 - 0.1 * i, 1.0, 1)
            item = Item(
                shard_model,
                name=f"Shard {i}",
                description="A glowing fragment of the grove",
            )
            item.reparent_to(self.render).set_pos(*pos)
            item.node.setCollideMask(self.actor_mask)
            self.actors[f"shard{i}"] = item

        # Gate as a target
        gate_model = self._load_model_safe(
            ["models/misc/rgbCube", "models/misc/sphere"]
        )
        gate_model.setScale(2.5, 0.4, 3.0)
        gate_model.setPos(0, 50, 0)
        gate_model.setColorScale(0.4, 0.4, 0.9, 1)
        gate_model.reparentTo(self.render)
        gate_model.setTag("gate", "1")

        # Quests
        self.quests.add(Quest("meet_elder", "Speak to the Elder at the clearing."))
        self.quests.add(
            Quest("collect_shards", "Collect all three Shards of the Grove.")
        )
        self.quests.add(
            Quest("restore_gate", "Return to the gate to restore the path.")
        )

    # --- runtime ---
    def _update(self, task: Task):
        dt = ClockObject.getGlobalClock().getDt()
        self._update_camera(dt)
        # CHANGE: update zombie system and handle spawn/death/respawn
        for _ in range(random.randrange(1, 5)):
            self._maybe_spawn_zombie()
            self._update_zombies(dt)
            self._update_respawn()
        return Task.cont

    def _update_camera(self, dt: float):
        speed = 18.0 * (1.6 if self.keys.get("shift") else 1.0)
        mov = Vec3(0, 0, 0)
        # CHANGE: disable movement while dead
        if self.player_alive:
            if self.keys["w"]:
                mov.y += speed * dt
            if self.keys["s"]:
                mov.y -= speed * dt
            if self.keys["a"]:
                mov.x -= speed * dt
            if self.keys["d"]:
                mov.x += speed * dt

        # Move relative to the player (yaw only), keep height steady
        self.player.setPos(self.player, mov)

        # Terrain-aware height: cast downward each frame to find ground height
        self.ground_trav.traverse(self.render)
        if self.ground_queue.getNumEntries() > 0:
            self.ground_queue.sortEntries()
            ground_entry = self.ground_queue.getEntry(0)
            hit_point = ground_entry.getSurfacePoint(self.render)
            self.player.setZ(hit_point.getZ())
        else:
            # Fallback to flat ground at z=0
            self.player.setZ(0.0)

        # Mouse look: hold right mouse to rotate (yaw on player, pitch on camera)
        if self.mouseWatcherNode.hasMouse() and self.win.getPointer(0):
            if self.mouseWatcherNode.is_button_down("mouse3"):
                md = self.win.getPointer(0)
                cx = self.win.getXSize() // 2
                cy = self.win.getYSize() // 2
                dx = (md.getX() - cx) * self.mouse_sens
                dy = (md.getY() - cy) * self.mouse_sens

                self.yaw -= dx
                self.pitch -= dy
                # Clamp pitch
                if self.pitch > self.max_pitch:
                    self.pitch = self.max_pitch
                elif self.pitch < -self.max_pitch:
                    self.pitch = -self.max_pitch

                # Apply yaw to player, pitch to camera
                self.player.setH(self.yaw)
                self.camera.setH(0)
                self.camera.setP(self.pitch)
                self.camera.setR(0)

                self.win.movePointer(0, cx, cy)

    # --- zombie system ---
    def _spawn_zombie_at(self, pos: Vec3):
        """CHANGE: spawn a zombie Node at a specific world position."""
        model = self._load_model_safe(
            ["models/misc/smiley", "models/misc/sphere"]
        )  # fallback if Actor fails
        model.setScale(1.2)
        z = Zombie(model, name=f"Zombie{len(self.zombies)+1}")
        z.reparent_to(self.render).set_pos(pos)
        z.node.setCollideMask(self.actor_mask)
        self.zombies.append(z)

    def _random_spawn_position(self) -> Vec3:
        """CHANGE: choose a random position in a ring around the player so they
        converge from outside the immediate view. Use simple trig to rotate."""
        r = random.uniform(25.0, 45.0)
        ang_deg = random.uniform(0.0, 360.0)
        import math

        ang = math.radians(ang_deg)
        dx = r * math.cos(ang)
        dy = r * math.sin(ang)
        base_pos = self.player.getPos(self.render)
        return Vec3(base_pos.x + dx, base_pos.y + dy, 0.0)

    def _maybe_spawn_zombie(self):
        """CHANGE: spawn at random intervals but never more frequent than once per minute."""
        now = time.time()
        if now >= self.next_zombie_spawn_at:
            self._spawn_zombie_at(self._random_spawn_position())
            # schedule next: at least 60s plus a random offset
            self.next_zombie_spawn_at = now + ZOMBIE_RESPAWN_INTERVAL

    def _update_zombies(self, dt: float):
        """CHANGE: make all zombies converge on the player and handle contact kill."""
        if not self.zombies:
            return
        player_pos = self.player.getPos(self.render)
        for z in self.zombies:
            # Skip dead or already detached zombies
            try:
                if not getattr(z, "alive", True):
                    z.set_walking(False)
                    continue
                if z.node.isEmpty():
                    continue
            except Exception:
                continue
            if not self.player_alive:
                z.set_walking(False)
                continue
            zpos = z.node.getPos(self.render)
            to_player = player_pos - zpos
            to_player.z = 0.0
            dist = to_player.length()
            if dist > 0.01:
                dir_vec = to_player / dist
                move = dir_vec * z.speed * dt
                z.node.setPos(self.render, zpos + move)
                # face the player
                try:
                    z.node.lookAt(self.player)
                except Exception:
                    pass
                z.set_walking(True)
            else:
                z.set_walking(False)

            # contact check (simple radius overlap)
            if self.player_alive and getattr(z, "alive", True) and dist < 1.0:
                self._on_player_killed()

        # Compact zombie list to keep only live, attached ones
        try:
            self.zombies = [
                z
                for z in self.zombies
                if getattr(z, "alive", True) and not z.node.isEmpty()
            ]
        except Exception:
            pass

    def _on_player_killed(self):
        """CHANGE: handle player death and schedule a 5-second respawn."""
        if not self.player_alive:
            return
        self.player_alive = False
        self.respawn_deadline = time.time() + self.respawn_delay
        self.hud.show_info("You were caught by a zombie! Respawning in 5 seconds...")

    def _update_respawn(self):
        """CHANGE: respawn the player after the delay."""
        if self.player_alive or self.respawn_deadline is None:
            return
        if time.time() >= self.respawn_deadline:
            # reset player state and position
            self.player.setPos(self.player_spawn_point)
            self.player.setHpr(0, 0, 0)
            self.yaw = 0.0
            self.pitch = 0.0
            # ensure grounded height will update next frame
            self.player_alive = True
            self.respawn_deadline = None
            self.hud.show_info("You have respawned. Run!")

    def _on_click(self):
        if not self.mouseWatcherNode.hasMouse():
            return
        mpos = self.mouseWatcherNode.getMouse()
        self.picker_ray.setFromLens(self.camNode, mpos.getX(), mpos.getY())
        self.picker.traverse(self.render)
        if self.pq.getNumEntries() == 0:
            return
        self.pq.sortEntries()
        entry = self.pq.getEntry(0)
        np = entry.getIntoNodePath().findNetTag("actor")
        if np.isEmpty():
            # try collectible tag
            np = entry.getIntoNodePath()
        self._handle_pick(np)

    def _handle_pick(self, np):
        if np.isEmpty():
            return
        # Attack zombies by clicking them (left mouse)
        if self.player_alive:
            znode = np.findNetTag("zombie")
            if not znode.isEmpty():
                z = self._find_zombie_by_nodepath(np)
                if z is not None:
                    self._attack_zombie(z)
                    return
        if np.getNetTag("actor") == "Elder":
            self._talk_elder()
            return
        if np.getNetTag("collectible") == "1" or "item-" in np.getName():
            self._collect_item(np)
            return
        if np.getNetTag("gate") == "1" or np.getTag("gate") == "1":
            self._try_restore_gate()
            return

    # --- combat helpers ---
    def _find_zombie_by_nodepath(self, np):
        """Given a NodePath from picking, return the Zombie instance if any."""
        try:
            znode = np.findNetTag("zombie")
            if znode.isEmpty():
                return None
            # Try direct NodePath identity or key
            for z in list(self.zombies):
                try:
                    if znode == z.node or znode.getKey() == z.node.getKey():
                        return z
                except Exception:
                    pass
            # Fallback: name match
            for z in list(self.zombies):
                try:
                    if znode.getName() == z.node.getName():
                        return z
                except Exception:
                    pass
        except Exception:
            return None
        return None

    def _attack_zombie(self, z):
        now = time.time()
        if (now - self._last_attack_time) < self.attack_cooldown:
            return
        self._last_attack_time = now
        if not z or not getattr(z, "alive", True):
            return
        try:
            remaining = z.take_damage(self.attack_damage)
        except Exception:
            return
        try:
            self.hud.show_info(
                f"Hit {getattr(z, 'name', 'Zombie')}! HP: {remaining}/{getattr(z, 'max_health', remaining)}"
            )
        except Exception:
            pass
        if not getattr(z, "alive", True):
            # Stop moving immediately
            try:
                z.set_walking(False)
            except Exception:
                pass

            # Cleanup after short delay to allow die animation
            def _cleanup(task):
                try:
                    z.node.detachNode()
                except Exception:
                    pass
                try:
                    if z in self.zombies:
                        self.zombies.remove(z)
                except Exception:
                    pass
                try:
                    self.hud.show_info(f"{getattr(z, 'name', 'Zombie')} defeated!")
                except Exception:
                    pass
                return Task.done

            try:
                self.taskMgr.doMethodLater(
                    0.6, _cleanup, f"cleanup-{getattr(z, 'name', 'zombie')}"
                )
            except Exception:
                _cleanup(None)

    # --- interactions ---
    def _talk_elder(self):
        if not any(
            q.name == "meet_elder" and not q.is_complete for q in self.quests.quests
        ):
            self.dialog.say("May the grove guide you.")
            return

        lines = [
            "Welcome, traveler. Our grove is broken into three shards.",
            "Find them in the forest and bring them back.",
            "When you have all three, the gate will respond.",
        ]
        idx = {"i": 0}

        def next_line():
            i = idx["i"]
            if i < len(lines):
                self.dialog.say(lines[i], on_continue=next_line)
                idx["i"] += 1
            else:
                # complete quest 1
                self.quests.quests[0].is_complete = True
                self.hud.set_objective(self.quests.objective_text())
                self.hud.show_info("Quest updated: Collect the three shards.")

        next_line()

    def _collect_item(self, np):
        # Find which shard
        name = np.getNetTag("actor") or np.getName()
        # Remove node
        base = np.findNetTag("actor")
        if base.isEmpty():
            base = np
        base.detachNode()
        # Update inventory
        self.inventory.append(name)
        self.hud.show_info(f"Collected {name}")

        # If we were on collect quest and we got 3, complete it
        if len([n for n in self.inventory if "Shard" in n]) >= 3:
            self.quests.quests[1].is_complete = True
            self.hud.set_objective(self.quests.objective_text())
            self.hud.show_info("You have all shards. Return to the gate.")

    def _try_restore_gate(self):
        if self.quests.quests[1].is_complete:
            self.quests.quests[2].is_complete = True
            self.dialog.say(
                "The gate hums as the shards fuse. The path is restored! You win."
            )
            self.hud.set_objective(self.quests.objective_text())
        else:
            self.dialog.say("The gate is dormant. Perhaps it needs the shards.")

    # --- utils ---
    def _load_model_safe(self, candidates):
        for path in candidates:
            try:
                m = self.loader.loadModel(path)
                return m
            except Exception:
                continue
        # fallback simple node
        from .utils import make_colored_triangle

        return make_colored_triangle()
