from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, CollisionTraverser, CollisionNode, CollisionRay, CollisionHandlerQueue, BitMask32
from panda3d.core import AmbientLight, DirectionalLight, Vec4, Vec3, ClockObject
from direct.task import Task

from gui import HUD, Dialog
from actors import NPC, Item
from quests import QuestLog, Quest
from scenes import load_environment


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

        self.player = self.render.attachNewNode('player')
        self.player.setPos(0, -20, 0)
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
        alight = AmbientLight('alight')
        alight.setColor(Vec4(0.6, 0.6, 0.6, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        dlight = DirectionalLight('dlight')
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
        self.picker_node = CollisionNode('mouseRay')
        self.picker_np = self.camera.attachNewNode(self.picker_node)
        self.picker_node.setFromCollideMask(BitMask32.bit(1))
        self.picker_ray = CollisionRay()
        self.picker_node.addSolid(self.picker_ray)
        self.picker.addCollider(self.picker_np, self.pq)

        # Set this mask to actor collision nodes we care about
        self.actor_mask = BitMask32.bit(1)

    def _init_grounding(self):
        """Set up a downward ray to find ground height (mask bit 2)."""
        self.ground_trav = CollisionTraverser()
        self.ground_queue = CollisionHandlerQueue()
        self.ground_node = CollisionNode('groundRay')
        self.ground_node.setFromCollideMask(BitMask32.bit(2))
        # Attach to player so origin follows player; cast from above head downwards
        self.ground_np = self.player.attachNewNode(self.ground_node)
        self.ground_ray = CollisionRay(0, 0, 10.0, 0, 0, -1)
        self.ground_node.addSolid(self.ground_ray)
        self.ground_trav.addCollider(self.ground_np, self.ground_queue)

    def _init_content(self):
        # Spawn NPC elder at center
        elder_model = self._load_model_safe(["models/misc/smiley", "models/misc/sphere"])  # friendly face
        elder_model.setScale(1.4)
        elder = NPC(elder_model, name="Elder", dialog_lines=[
            "Welcome, traveler. Our grove is broken into three shards.",
            "Find the three Shards of the Grove and return to me.",
            "Place them at the ancient gate to restore the path."
        ])
        elder.reparent_to(self.render).set_pos(0, 10, 0)
        elder.node.setCollideMask(self.actor_mask)
        self.actors['elder'] = elder

        # Place three shard items around the map
        positions = [(-8, 25, 0.2), (10, 35, 0.2), (6, 18, 0.2)]
        for i, pos in enumerate(positions, 1):
            shard_model = self._load_model_safe(["models/misc/rgbCube", "models/misc/sphere"])
            shard_model.setScale(0.7)
            shard_model.setColorScale(0.6 + 0.1*i, 0.8 - 0.1*i, 1.0, 1)
            item = Item(shard_model, name=f"Shard {i}", description="A glowing fragment of the grove")
            item.reparent_to(self.render).set_pos(*pos)
            item.node.setCollideMask(self.actor_mask)
            self.actors[f'shard{i}'] = item

        # Gate as a target
        gate_model = self._load_model_safe(["models/misc/rgbCube", "models/misc/sphere"])
        gate_model.setScale(2.5, 0.4, 3.0)
        gate_model.setPos(0, 50, 0)
        gate_model.setColorScale(0.4, 0.4, 0.9, 1)
        gate_model.reparentTo(self.render)
        gate_model.setTag("gate", "1")

        # Quests
        self.quests.add(Quest("meet_elder", "Speak to the Elder at the clearing."))
        self.quests.add(Quest("collect_shards", "Collect all three Shards of the Grove."))
        self.quests.add(Quest("restore_gate", "Return to the gate to restore the path."))

    # --- runtime ---
    def _update(self, task: Task):
        dt = ClockObject.getGlobalClock().getDt()
        self._update_camera(dt)
        return Task.cont

    def _update_camera(self, dt: float):
        speed = 18.0 * (1.6 if self.keys.get("shift") else 1.0)
        mov = Vec3(0, 0, 0)
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
            if self.mouseWatcherNode.is_button_down('mouse3'):
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
        np = entry.getIntoNodePath().findNetTag('actor')
        if np.isEmpty():
            # try collectible tag
            np = entry.getIntoNodePath()
        self._handle_pick(np)

    def _handle_pick(self, np):
        if np.isEmpty():
            return
        if np.getNetTag('actor') == 'Elder':
            self._talk_elder()
            return
        if np.getNetTag('collectible') == '1' or 'item-' in np.getName():
            self._collect_item(np)
            return
        if np.getNetTag('gate') == '1' or np.getTag('gate') == '1':
            self._try_restore_gate()
            return

    # --- interactions ---
    def _talk_elder(self):
        if not any(q.name == 'meet_elder' and not q.is_complete for q in self.quests.quests):
            self.dialog.say("May the grove guide you.")
            return

        lines = [
            "Welcome, traveler. Our grove is broken into three shards.",
            "Find them in the forest and bring them back.",
            "When you have all three, the gate will respond."
        ]
        idx = {'i': 0}

        def next_line():
            i = idx['i']
            if i < len(lines):
                self.dialog.say(lines[i], on_continue=next_line)
                idx['i'] += 1
            else:
                # complete quest 1
                self.quests.quests[0].is_complete = True
                self.hud.set_objective(self.quests.objective_text())
                self.hud.show_info("Quest updated: Collect the three shards.")
        next_line()

    def _collect_item(self, np):
        # Find which shard
        name = np.getNetTag('actor') or np.getName()
        # Remove node
        base = np.findNetTag('actor')
        if base.isEmpty():
            base = np
        base.detachNode()
        # Update inventory
        self.inventory.append(name)
        self.hud.show_info(f"Collected {name}")

        # If we were on collect quest and we got 3, complete it
        if len([n for n in self.inventory if 'Shard' in n]) >= 3:
            self.quests.quests[1].is_complete = True
            self.hud.set_objective(self.quests.objective_text())
            self.hud.show_info("You have all shards. Return to the gate.")

    def _try_restore_gate(self):
        if self.quests.quests[1].is_complete:
            self.quests.quests[2].is_complete = True
            self.dialog.say("The gate hums as the shards fuse. The path is restored! You win.")
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
