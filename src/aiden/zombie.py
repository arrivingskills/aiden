'''Goal
Let the player attack zombies and deal damage (“injure”) when clicking them. Below is a small, clean set of changes that fits your current code structure.
I’ll show:
•
What to add to actors.Zombie (health, damage, death)
•
How to wire up attack input in game.AdventureGame
•
How to keep zombies from moving/attacking after death and remove them cleanly
You can copy/paste the snippets into the indicated spots.
1) Give zombies health and death in src/aiden/actors.py
Add fields, a tag for easy identification, and helpers to take damage and die. Place these inside the existing Zombie class.
'''
class Zombie(ActorBase):
    def __init__(self, node: NodePath, name: str, dialog_lines=None):
        super().__init__(node, name)
        self.dialog_lines = dialog_lines or []
        # Tag for easy identification during picking
        self.node.setTag("zombie", "1")
        # Basic health/state
        self.max_health = 100
        self.health = self.max_health
        self.alive = True
        ...

    # --- combat helpers ---
    def take_damage(self, amount: int) -> int:
        """Apply damage and return remaining health. If reaches zero, mark dead."""
        if not self.alive:
            return self.health
        self.health = max(0, self.health - int(amount))
        if self.health == 0:
            self.die()
        return self.health

    def die(self):
        if not self.alive:
            return
        self.alive = False
        try:
            if getattr(self, 'actor', None):
                # play a die animation if available; else stop anims
                try:
                    self.actor.play('die')
                except Exception:
                    self.actor.stop()
        except Exception:
            pass
'''Notes:
•
We also set self.node.setTag("zombie", "1") so picking can quickly identify zombie hits.
2) Add attack settings to the player in src/aiden/game.py
In AdventureGame.__init__ (near your other state like self.zombies, self.player_alive), add:'''
# Player attack config
self.attack_damage = 34           # tweak to taste
self.attack_cooldown = 0.35       # seconds between attacks
self._last_attack_time = 0.0
'''This gives you a simple, fast “click to attack” with a cooldown.
3) Detect zombie clicks and apply damage
You already send clicks to _handle_pick. Extend it to detect zombies, resolve which Zombie object was hit, and damage it (with cooldown).
Add these helpers somewhere in AdventureGame (e.g., under _handle_pick):'''
def _find_zombie_by_nodepath(self, np):
    """Given a NodePath from picking, return the Zombie instance if any."""
    # climb to the node that has tag zombie=1
    znode = np.findNetTag('zombie')
    if znode.isEmpty():
        return None
    # Match by comparing stored node paths
    for z in list(self.zombies):
        if znode == z.node or znode.getKey() == z.node.getKey():
            return z
    # Fallback: compare names
    for z in list(self.zombies):
        if znode.getName() == z.node.getName():
            return z
    return None

def _attack_zombie(self, z):
    now = time.time()
    if now - self._last_attack_time < self.attack_cooldown:
        return  # too soon
    self._last_attack_time = now

    if not z or not getattr(z, 'alive', True):
        return

    remaining = z.take_damage(self.attack_damage)
    self.hud.show_info(f"Hit {z.name}! HP: {remaining}/{getattr(z, 'max_health', remaining)}")

    # If dead, clean it up after a short delay (let death anim play if present)
    if not z.alive:
        # Stop movement immediately
        z.set_walking(False)
        # Schedule a small cleanup
        def _cleanup(task):
            try:
                z.node.detachNode()
            except Exception:
                pass
            try:
                self.zombies.remove(z)
            except ValueError:
                pass
            self.hud.show_info(f"{z.name} defeated!")
            return Task.done
        # 0.6s delay so a die anim can show
        self.taskMgr.doMethodLater(0.6, _cleanup, f"cleanup-{z.name}")
Now modify _handle_pick to call the attack when a zombie is clicked. Replace your current method body with this extended logic (keep existing item/gate handling):
def _handle_pick(self, np):
    if np.isEmpty():
        return

    # Attack zombies by clicking them
    if not self.player_alive:
        return  # cannot attack while dead
    if np.findNetTag('zombie') and not np.findNetTag('zombie').isEmpty():
        z = self._find_zombie_by_nodepath(np)
        if z:
            self._attack_zombie(z)
            return

    # Existing interactions
    if np.getNetTag('actor') == 'Elder':
        self._talk_elder()
        return
    if np.getNetTag('collectible') == '1' or 'item-' in np.getName():
        self._collect_item(np)
        return
    if np.getNetTag('gate') == '1' or np.getTag('gate') == '1':
        self._try_restore_gate()
        return
"""That’s enough to click zombies and injure them until they die.
4) Prevent dead zombies from moving or killing the player
Update your zombie update loop to skip dead zombies entirely and to remove them if their node has been detached.
In _update_zombies (inside the for z in self.zombies: loop) add guards:"""
# Skip dead or detached zombies
try:
    if not getattr(z, 'alive', True):
        z.set_walking(False)
        continue
    if z.node.isEmpty():  # already detached
        continue
except Exception:
    continue
# And use the same guard before doing contact damage:
# contact check (simple radius overlap)
if self.player_alive and getattr(z, 'alive', True) and dist < 1.0:
    self._on_player_killed()
#Optional cleanup: after the loop, you can compact the list so removed ones don’t linger:
self.zombies = [z for z in self.zombies if getattr(z, 'alive', True) and not z.node.isEmpty()]
P