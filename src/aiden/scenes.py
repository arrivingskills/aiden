from panda3d.core import (
    NodePath,
    CollisionNode,
    CollisionPlane,
    Plane,
    BitMask32,
    Vec3,
    Point3,
)
from .utils import make_colored_triangle


def _attach_flat_ground_plane(root: NodePath):
    """Attach an invisible collision plane at z=0 for grounding fallback (mask bit 2)."""
    cnode = CollisionNode("ground-plane")
    plane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
    cnode.addSolid(plane)
    cnode.setIntoCollideMask(BitMask32.bit(2))
    root.attachNewNode(cnode)


def load_environment(loader) -> NodePath:
    """Load the world; try Panda3D's sample environment or a fallback."""
    try:
        env = loader.loadModel("models/environment")
        env.reparentTo(NodePath())
        env.setScale(0.25)
        env.setPos(-8, 42, 0)
        # Add a flat ground collision plane as a fallback surface
        _attach_flat_ground_plane(env)
        return env
    except Exception:
        # Fallback: just a flat node with triangles as landmarks
        root = NodePath("fallback-world")
        for i in range(10):
            tri = make_colored_triangle(color=(0.2 * (i % 5), 0.5, 1.0 - 0.1 * i, 1))
            # CHANGE: NodePath uses camelCase methods
            tri.setPos((i % 5) * 3, 10 + i * 2, 0)
            tri.reparentTo(root)
        # Ground plane for fallback as well
        _attach_flat_ground_plane(root)
        return root
