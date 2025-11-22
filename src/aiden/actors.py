from panda3d.core import NodePath, CollisionNode, CollisionSphere
from direct.actor.Actor import Actor
import time


class ActorBase:
    def __init__(self, node: NodePath, name: str):
        self.node = node
        self.name = name
        self.node.set_tag("actor", name)

    def set_pos(self, x, y, z):
        self.node.set_pos(x, y, z)
        return self

    def reparent_to(self, parent: NodePath):
        self.node.reparent_to(parent)
        return self


class NPC(ActorBase):
    def __init__(self, node: NodePath, name: str, dialog_lines=None):
        super().__init__(node, name)
        self.dialog_lines = dialog_lines or []
        # collision for clicking
        cnode = CollisionNode(f"npc-{name}")
        cnode.add_solid(CollisionSphere(0, 0, 0.5, 1.0))
        self.node.attach_new_node(cnode)


class Item(ActorBase):
    def __init__(self, node: NodePath, name: str, description: str = ""):
        super().__init__(node, name)
        self.description = description
        cnode = CollisionNode(f"item-{name}")
        cnode.add_solid(CollisionSphere(0, 0, 0.25, 0.5))
        self.node.attach_new_node(cnode)
        self.node.set_tag("collectible", "1")

class Zombie(ActorBase):
    def __init__(self, node: NodePath, name: str, dialog_lines=None):
        super().__init__(node, name)
        self.dialog_lines = dialog_lines or []
        # collision for clicking
        cnode = CollisionNode(f"npc-{name}")
        cnode.add_solid(CollisionSphere(0, 0, 0.5, 1.0))
        self.node.attach_new_node(cnode)
        zombie = Actor('simpleEnemy.egg', {
            'walk': 'simpleEnemy-walk.egg',
            'attack': 'simpleEnemy-attack.egg',
            'spawn': 'simpleEnemy-spawn.egg',
            'die': 'simpleEnemy-die.egg',
        })
        zombie.play('spawn')
        zombie.loop('attack')
        zombie.stop()
