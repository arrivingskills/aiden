from panda3d.core import NodePath, Geom, GeomNode, GeomVertexData, GeomVertexFormat, GeomVertexWriter, GeomTriangles


def make_colored_triangle(name: str = "tri", color=(1, 0, 0, 1)) -> NodePath:
    """Create a tiny colored triangle as a fallback model."""
    # CHANGE: Panda3D uses camelCase API for Geom/Vertex utilities
    format = GeomVertexFormat.getV3c4()
    vdata = GeomVertexData(name, format, Geom.UHStatic)

    vwriter = GeomVertexWriter(vdata, "vertex")
    cwriter = GeomVertexWriter(vdata, "color")

    # Simple right triangle in X-Y plane
    verts = [(0, 0, 0), (0.3, 0, 0), (0, 0.3, 0)]
    for v in verts:
        vwriter.addData3(*v)
        cwriter.addData4(*color)

    tris = GeomTriangles(Geom.UHStatic)
    tris.addVertices(0, 1, 2)

    geom = Geom(vdata)
    geom.addPrimitive(tris)

    node = GeomNode(name)
    node.addGeom(geom)
    return NodePath(node)
