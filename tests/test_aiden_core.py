import sys
from types import ModuleType
from pathlib import Path


def _inject_fakes():
    # Ensure src is importable as a package root
    repo_root = Path(__file__).resolve().parents[1]
    src_dir = repo_root / "src"
    sys.path.insert(0, str(src_dir))

    # Minimal fake panda3d.core
    panda = ModuleType("panda3d")
    core = ModuleType("panda3d.core")

    class FakeNodePath:
        def __init__(self, node=None):
            self._pos = (0, 0, 0)
            self._tags = {}
            self._parent = None
            self._node = node

        def setTag(self, k, v):
            self._tags[k] = v

        def setPos(self, *args):
            if len(args) == 1 and hasattr(args[0], "x"):
                v = args[0]
                self._pos = (v.x, v.y, v.z)
            else:
                self._pos = tuple(args)

        def reparentTo(self, parent):
            self._parent = parent

        def attachNewNode(self, node):
            child = FakeNodePath(node)
            return child

        def setColorScale(self, *args, **kwargs):
            self._color = args

        def node(self):
            return self._node

    core.NodePath = FakeNodePath

    # Minimal collision/collision node types used in actors.py
    class FakeCollisionNode:
        def __init__(self, name):
            self.name = name

        def addSolid(self, s):
            pass

        def setIntoCollideMask(self, m):
            self._mask = m

    core.CollisionNode = FakeCollisionNode

    class FakeCollisionSphere:
        def __init__(self, *a, **k):
            pass

    core.CollisionSphere = FakeCollisionSphere

    class FakeBitMask32:
        @staticmethod
        def bit(i):
            return 1 << i

    core.BitMask32 = FakeBitMask32

    # Put core under panda3d.core
    panda.core = core
    sys.modules["panda3d"] = panda
    sys.modules["panda3d.core"] = core

    # Minimal direct.actor.Actor
    direct = ModuleType("direct")
    actor_pkg = ModuleType("direct.actor")

    class FakeActor:
        def __init__(self, *args, **kwargs):
            self._current = None

        def reparentTo(self, parent):
            self._parent = parent

        def setScale(self, s):
            self._scale = s

        def loop(self, anim):
            self._current = anim

        def getCurrentAnim(self):
            return self._current

        def play(self, anim):
            self._current = anim

        def stop(self):
            self._current = None

        def setColorScale(self, *args):
            self._color = args

    actor_pkg.Actor = FakeActor
    sys.modules["direct"] = direct
    sys.modules["direct.actor"] = actor_pkg
    sys.modules["direct.actor.Actor"] = actor_pkg


def test_actorbase_set_pos_variants():
    _inject_fakes()
    # import after fakes injected
    from aiden.actors import ActorBase

    class Vec:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    node = sys.modules["panda3d.core"].NodePath()
    a = ActorBase(node, "bob")

    # three-arg form
    a.set_pos(1, 2, 3)
    assert node._pos == (1, 2, 3)

    # vector-like object
    a.set_pos(Vec(4, 5, 6))
    assert node._pos == (4, 5, 6)

    # sequence
    a.set_pos((7, 8, 9))
    assert node._pos == (7, 8, 9)


def test_zombie_damage_and_death():
    _inject_fakes()
    from aiden.actors import Zombie

    node = sys.modules["panda3d.core"].NodePath()
    z = Zombie(node, "z1")

    # initial health
    assert z.health == z.max_health

    # apply damage
    rem = z.take_damage(30)
    assert rem == z.max_health - 30
    assert z.alive is True

    # lethal damage
    rem = z.take_damage(70)
    assert rem == 0
    assert z.alive is False

    # further damage doesn't change health
    rem2 = z.take_damage(10)
    assert rem2 == 0


def test_zombie_set_walking_switches_animation():
    _inject_fakes()
    from aiden.actors import Zombie

    node = sys.modules["panda3d.core"].NodePath()
    z = Zombie(node, "z2")

    # ensure actor exists and starts in 'stand'
    if getattr(z, "actor", None) is None:
        # fallback: create a fake actor and attach
        z.actor = sys.modules["direct.actor"].Actor()
        z.actor.loop("stand")

    z.set_walking(True)
    assert z.actor.getCurrentAnim() == "walk"

    z.set_walking(False)
    assert z.actor.getCurrentAnim() == "stand"
