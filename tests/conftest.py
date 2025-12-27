import sys
from types import ModuleType
from pathlib import Path


def _install_fakes():
    repo_root = Path(__file__).resolve().parents[1]
    src_dir = repo_root / "src"
    sys.path.insert(0, str(src_dir))

    core = ModuleType("panda3d.core")

    class FakeNodePath:
        def __init__(self, node=None, name=None):
            self._pos = (0, 0, 0)
            self._tags = {}
            self._parent = None
            self._node = node
            self._name = name or "node"
            self._children = []

        def setTag(self, k, v):
            self._tags[k] = v

        def getTag(self, k):
            return self._tags.get(k, "")

        def setPos(self, *args):
            if len(args) == 1 and hasattr(args[0], "x"):
                v = args[0]
                self._pos = (v.x, v.y, v.z)
            else:
                self._pos = tuple(args)

        def getPos(self, *args):
            class P:
                def __init__(self, pos):
                    self.x, self.y, self.z = pos

            return P(self._pos)

        def setZ(self, z):
            x, y, _ = self._pos
            self._pos = (x, y, z)

        def reparentTo(self, parent):
            self._parent = parent
            if hasattr(parent, "_children"):
                parent._children.append(self)
            return self

        def attachNewNode(self, node):
            child = FakeNodePath(node)
            self._children.append(child)
            return child

        def setColorScale(self, *args, **kwargs):
            self._color = args

        def node(self):
            return self._node

        def isEmpty(self):
            return False

        def getName(self):
            return self._name

        def getKey(self):
            return id(self)

        def findNetTag(self, tag):
            # simplification: return self if tag present
            class NP:
                def __init__(self, empty):
                    self._empty = empty

                def isEmpty(self):
                    return self._empty

                def getName(self):
                    return "node"

                def getKey(self):
                    return 0

            return NP(False)

    core.NodePath = FakeNodePath

    class CollisionNode:
        def __init__(self, name):
            self.name = name

        def addSolid(self, s):
            pass

        def setIntoCollideMask(self, m):
            self._mask = m

        def setFromCollideMask(self, m):
            self._from = m

        def setIntoCollideMask(self, m):
            self._into = m

        def addSolid(self, s):
            pass

    core.CollisionNode = CollisionNode

    class CollisionPlane:
        def __init__(self, plane):
            self.plane = plane

    core.CollisionPlane = CollisionPlane

    class Plane:
        def __init__(self, normal, point):
            pass

    core.Plane = Plane

    class Vec3:
        def __init__(self, x=0, y=0, z=0):
            self.x = x
            self.y = y
            self.z = z

        def __sub__(self, other):
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

        def __truediv__(self, s):
            return Vec3(self.x / s, self.y / s, self.z / s)

        def length(self):
            import math

            return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    core.Vec3 = Vec3

    class Point3(Vec3):
        pass

    core.Point3 = Point3

    class BitMask32:
        @staticmethod
        def bit(i):
            return 1 << i

        @staticmethod
        def allOff():
            return 0

    core.BitMask32 = BitMask32

    # Simple minimal CollisionRay and helpers
    class CollisionRay:
        def __init__(self, *args, **kwargs):
            pass

    core.CollisionRay = CollisionRay

    class CollisionSphere:
        def __init__(self, *a, **k):
            pass

    core.CollisionSphere = CollisionSphere

    # Minimal Geom/Vertex stubs used by utils.make_colored_triangle
    class Geom:
        UHStatic = 0

        def __init__(self, vdata=None):
            self.vdata = vdata
            self.primitives = []

        def addPrimitive(self, p):
            self.primitives.append(p)

    class GeomNode:
        def __init__(self, name):
            self.name = name
            self.geoms = []

        def addGeom(self, g):
            self.geoms.append(g)

    class GeomVertexFormat:
        @staticmethod
        def getV3c4():
            return object()

    class GeomVertexData:
        def __init__(self, name, fmt, usage):
            self.name = name
            self.format = fmt

    class GeomVertexWriter:
        def __init__(self, vdata, name):
            self.vdata = vdata
            self.name = name

        def addData3(self, x, y, z):
            pass

        def addData4(self, *args):
            pass

    class GeomTriangles:
        def __init__(self, usage):
            self.verts = []

        def addVertices(self, a, b, c):
            self.verts.append((a, b, c))

    core.Geom = Geom
    core.GeomNode = GeomNode
    core.GeomVertexFormat = GeomVertexFormat
    core.GeomVertexData = GeomVertexData
    core.GeomVertexWriter = GeomVertexWriter
    core.GeomTriangles = GeomTriangles

    # Expose to sys.modules
    sys.modules["panda3d.core"] = core

    # Minimal direct.actor.Actor
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
    sys.modules["direct.actor"] = actor_pkg
    sys.modules["direct"] = ModuleType("direct")
    # Provide a module object for direct.actor.Actor path used by imports
    actor_module_alias = ModuleType("direct.actor.Actor")
    actor_module_alias.Actor = FakeActor
    sys.modules["direct.actor.Actor"] = actor_module_alias


def pytest_configure(config):
    _install_fakes()
