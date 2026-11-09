from importlib.resources import files

from kivy.properties import StringProperty
from kivy.uix.effectwidget import AdvancedEffectBase
from kivy.uix.screenmanager import ShaderTransition

__all__ = ("glsl", "names", "stages", "PyShaderEffect", "PyShaderTransition")


def glsl(name):
    return str(files(__name__) / f"{name}.glsl")


def names(kind):
    return sorted(p.name[:-5] for p in (files(__name__) / kind).iterdir() if p.name.endswith(".glsl"))


def stages(name):
    vs, fs = (files(__name__) / f"{name}.glsl").read_text().split("---FRAGMENT SHADER---")
    return vs.replace("---VERTEX SHADER---", "", 1), fs


class PyShaderTransition(ShaderTransition):
    shader = StringProperty("fade")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fbind("shader", self._load)
        self._load()

    def _load(self, *_):
        self.vs, self.fs = stages(f"transitions/{self.shader}")

    def add_screen(self, screen):
        super().add_screen(screen)
        self.render_ctx["resolution"] = [float(v) for v in screen.size]


class PyShaderEffect(AdvancedEffectBase):
    shader = StringProperty("identity")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fbind("shader", self.set_fbo_shader)

    def set_fbo_shader(self, *args):
        if self.fbo is None:
            return
        self.fbo.set_fs(stages(f"effects/{self.shader}")[1])
        self._update_uniforms()
