from aiden.actors import ActorBase, NPC, Item
from panda3d.core import NodePath


def test_actor_reparent_and_tagging():
    node = NodePath()
    parent = NodePath()
    a = ActorBase(node, "hero")
    a.reparent_to(parent)
    assert node._parent is parent
    assert node._tags.get("actor") == "hero"


def test_item_sets_collectible_and_collision():
    node = NodePath()
    it = Item(node, "coin", description="Shiny")
    # collectible tag set
    assert node._tags.get("collectible") == "1"
    # attached collision node should exist as a child
    assert len(node._children) >= 1


def test_npc_collision_mask():
    node = NodePath()
    n = NPC(node, "guard")
    # an attachNewNode should have been called and set mask on its node
    assert len(node._children) >= 1
