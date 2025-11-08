from panda3d.core import NodePath, Geom, GeomNode, GeomVertexData, GeomVertexFormat, GeomVertexWriter, GeomTriangles


def make_colored_triangle(name: str = "tri", color=(1, 0, 0, 1)) -> NodePath:
    """Create a tiny colored triangle as a fallback model."""
    format = GeomVertexFormat.get_v3c4()
    vdata = GeomVertexData(name, format, Geom.UH_static)

    vwriter = GeomVertexWriter(vdata, "vertex")
    cwriter = GeomVertexWriter(vdata, "color")

    # Simple right triangle in X-Y plane
    verts = [(0, 0, 0), (0.3, 0, 0), (0, 0.3, 0)]
    for v in verts:
        vwriter.add_data3(*v)
        cwriter.add_data4(*color)

    tris = GeomTriangles(Geom.UH_static)
    tris.add_vertices(0, 1, 2)

    geom = Geom(vdata)
    geom.add_primitive(tris)

    node = GeomNode(name)
    node.add_geom(geom)
    return NodePath(node)
