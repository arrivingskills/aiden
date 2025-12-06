from panda3d.core import NodePath, CollisionNode, CollisionSphere, BitMask32
from direct.actor.Actor import Actor
import time


class ActorBase:
    def __init__(self, node: NodePath, name: str):
        self.node = node
        self.name = name
        # CHANGE: Panda3D NodePath uses camelCase API (setTag)
        self.node.setTag("actor", name)

    def set_pos(self, x, y=None, z=None):
        """Set position on the underlying NodePath.

        Accepts either three coordinates (x, y, z) or a single Vec3/Point3/
        tuple/list of length 3.
        """
        if y is None and z is None:
            # Single-argument form: try to unpack common vector types
            v = x
            try:
                # Supports Vec3/Point3 (x, y, z properties) or sequences
                if hasattr(v, 'x') and hasattr(v, 'y') and hasattr(v, 'z'):
                    self.node.setPos(v.x, v.y, v.z)
                else:
                    self.node.setPos(*v)
            except Exception:
                # Fallback: re-raise with clearer context
                raise TypeError("set_pos() expected (x, y, z) or a 3-component vector/sequence")
        else:
            # Three-argument form
            self.node.setPos(x, y, z)
        return self

    def reparent_to(self, parent: NodePath):
        # CHANGE: use NodePath.reparentTo
        self.node.reparentTo(parent)
        return self


class NPC(ActorBase):
    def __init__(self, node: NodePath, name: str, dialog_lines=None):
        super().__init__(node, name)
        self.dialog_lines = dialog_lines or []
        # collision for clicking
        cnode = CollisionNode(f"npc-{name}")
        # CHANGE: CollisionNode.addSolid (camelCase)
        cnode.addSolid(CollisionSphere(0, 0, 0.5, 1.0))
        # CHANGE: NodePath.attachNewNode (camelCase)
        cnp = self.node.attachNewNode(cnode)
        # Make this clickable by the picking ray (mask bit 1)
        cnp.node().setIntoCollideMask(BitMask32.bit(1))


class Item(ActorBase):
    def __init__(self, node: NodePath, name: str, description: str = ""):
        super().__init__(node, name)
        self.description = description
        cnode = CollisionNode(f"item-{name}")
        cnode.addSolid(CollisionSphere(0, 0, 0.25, 0.5))
        cnp = self.node.attachNewNode(cnode)
        # Clickable by picking ray
        cnp.node().setIntoCollideMask(BitMask32.bit(1))
        # CHANGE: NodePath.setTag (camelCase)
        self.node.setTag("collectible", "1")

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
        # CHANGE: add a simple click-collision and attach a skinned model Actor to this node
        # so the zombie is visible and can animate.
        cnode = CollisionNode(f"npc-{name}")
        cnode.addSolid(CollisionSphere(0, 0, 0.5, 1.0))
        cnp = self.node.attachNewNode(cnode)
        cnp.node().setIntoCollideMask(BitMask32.bit(1))

        # CHANGE: load the simple enemy actor and parent it under this zombie node.
        # If assets are missing in runtime, the game will still work due to outer
        # code using a primitive model as a fallback for spawn, but we try to load
        # animations here so that when assets are available, zombies animate.
        try:
            self.actor = Actor('simpleEnemy.egg', {
                'stand': 'simpleEnemy-stand.egg',
                'walk': 'simpleEnemy-walk.egg',
                'attack': 'simpleEnemy-attack.egg',
                'spawn': 'simpleEnemy-spawn.egg',
                'die': 'simpleEnemy-die.egg',
            })
            # CHANGE: Actor API also uses camelCase
            self.actor.reparentTo(self.node)
            self.actor.setScale(0.8)
            self.actor.loop('stand')
            # CHANGE: give the simpleEnemy a zombie-like look by tinting the
            # model a desaturated green. This avoids needing new texture files
            # while achieving the visual intent.
            try:
                # ColorScale multiplies existing textures, preserving shading.
                self.actor.setColorScale(0.6, 0.8, 0.6, 1.0)
            except Exception:
                pass
        except Exception:
            # If Actor assets fail to load, silently ignore; a plain model can be used instead.
            self.actor = None
            # Apply the same zombie-like tint to the fallback primitive node so
            # it still reads as a zombie visually.
            try:
                self.node.setColorScale(0.6, 0.8, 0.6, 1.0)
            except Exception:
                pass

        # CHANGE: simple movement parameters used by the game loop to make
        # zombies converge on the player.
        self.speed = 4.0  # units per second

    def set_walking(self, walking: bool):
        """CHANGE: helper to swap between idle and walk animations if available."""
        if not getattr(self, 'actor', None):
            return
        try:
            if walking:
                if self.actor.getCurrentAnim() != 'walk':
                    self.actor.loop('walk')
            else:
                if self.actor.getCurrentAnim() != 'stand':
                    self.actor.loop('stand')
        except Exception:
            pass

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
                # play a die animation if available; otherwise stop anims
                try:
                    self.actor.play('die')
                except Exception:
                    self.actor.stop()
        except Exception:
            pass
