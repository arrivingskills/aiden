from aiden import scenes


class LoaderRaises:
    def loadModel(self, *a, **k):
        raise RuntimeError("no models")


class LoaderOK:
    def __init__(self):
        from panda3d.core import NodePath

        self._model = NodePath()

    def loadModel(self, *a, **k):
        return self._model


def test_load_environment_fallback_when_loader_fails():
    loader = LoaderRaises()
    env = scenes.load_environment(loader)
    # Should be a NodePath-like object
    from panda3d.core import NodePath

    assert isinstance(env, NodePath)
    # fallback should have children added
    assert hasattr(env, "_children")


def test_load_environment_with_loader_success():
    loader = LoaderOK()
    env = scenes.load_environment(loader)
    from panda3d.core import NodePath

    assert isinstance(env, NodePath)
    # when loader succeeds, returned env should be reparented (parent exists)
    assert getattr(env, "_parent", None) is not None
