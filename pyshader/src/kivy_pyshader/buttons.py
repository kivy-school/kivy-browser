from kivy.animation import Animation
from kivy.graphics import Rectangle, RenderContext
from kivy.properties import AliasProperty, BoundedNumericProperty, ColorProperty, ListProperty, NumericProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.uix.widget import Widget

from . import glsl

__all__ = ("ShaderWidget", "ShaderToggle", "GearButton", "MorphButton", "RippleButton", "CombineToggle",
           "OnionButton", "MorphToggle", "MergeToggle", "SwitchToggle")

SHAPES = 5  # circle, star, heart, hexagon, rounded square (widgets/forms.py)


def uniform_value(value):
    """A property's value as Kivy takes it for a uniform: a float, or a list of floats."""
    if isinstance(value, (int, float)):
        return float(value)
    return [float(v) for v in value]


class ShaderWidget(Widget):
    """Draws its shader under its children.

    `uniforms` maps a property to the uniform it sets. Each uniform is sent
    when its own property changes, `resolution` when the size does: an
    `Animation` changes its property every frame while it runs, and a widget
    at rest sends nothing.
    """

    shader = StringProperty()
    tint = ColorProperty("#3f7fe0")
    progress = NumericProperty(1.0)

    uniforms = {"tint": "tint", "progress": "pressed"}

    def __init__(self, **kwargs):
        self.render = RenderContext(use_parent_projection=True, use_parent_modelview=True,
                                    use_parent_frag_modelview=True)
        with self.render:
            self.rect = Rectangle()
        super().__init__(**kwargs)
        self.canvas.before.add(self.render)
        self.fbind("shader", self._load)
        self.fbind("pos", self._move)
        self.fbind("size", self._resize)
        for name, uniform in self.uniforms.items():
            self.fbind(name, self._send, name, uniform)
        self._load()
        self._move()

    def _load(self, *_):
        self.render.shader.source = glsl(self.shader)
        if not self.render.shader.success:
            raise Exception(f"Kivy could not compile {self.shader}.glsl")
        # A new program: every uniform once.
        self._resize()
        for name, uniform in self.uniforms.items():
            self._send(name, uniform)

    # The properties are read back: a callback's value can still be what was
    # assigned (`size = ("160dp", "160dp")`), before the property converted it.
    def _move(self, *_):
        self.rect.pos = self.pos

    def _resize(self, *_):
        self.rect.size = self.size
        self.render["resolution"] = [float(self.width), float(self.height)]

    def _send(self, name, uniform, *_):
        self.render[uniform] = uniform_value(getattr(self, name))

    def play(self, duration=0.6):
        Animation.cancel_all(self, "progress")
        self.progress = 0.0
        Animation(progress=1.0, d=duration).start(self)


class GearButton(ButtonBehavior, ShaderWidget):
    """One more tooth per press, back to `min_teeth` after `max_teeth`."""

    shader = StringProperty("widgets/gear")
    min_teeth = NumericProperty(5)
    max_teeth = NumericProperty(12)
    teeth = NumericProperty(5)
    last_teeth = NumericProperty(5)

    uniforms = {**ShaderWidget.uniforms, "teeth": "teeth", "last_teeth": "last_teeth"}

    def on_press(self, *args):
        self.last_teeth = self.teeth
        self.teeth = self.min_teeth if self.teeth >= self.max_teeth else self.teeth + 1
        self.play()


class MorphButton(ButtonBehavior, ShaderWidget):
    """Every press morphs into the next shape."""

    shader = StringProperty("widgets/morph")
    shape = BoundedNumericProperty(0, min=0, max=SHAPES - 1)
    last_shape = NumericProperty(0)

    uniforms = {**ShaderWidget.uniforms, "shape": "shape_to", "last_shape": "shape_from"}

    def on_press(self, *args):
        self.last_shape = self.shape
        self.shape = (self.shape + 1) % SHAPES
        self.play(0.5)


class RippleButton(ButtonBehavior, ShaderWidget):
    """A ring runs out from where it was touched."""

    shader = StringProperty("widgets/ripple")
    touch = ListProperty([0.0, 0.0])

    uniforms = {**ShaderWidget.uniforms, "touch": "touch"}

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.touch = [touch.x - self.x, touch.y - self.y]
        return super().on_touch_down(touch)

    def on_press(self, *args):
        self.play(0.7)


class ShaderToggle(ToggleButtonBehavior, ShaderWidget):
    """Animates `morph` to 1 when down, back to 0 when up."""

    morph = NumericProperty(0.0)

    uniforms = {**ShaderWidget.uniforms, "morph": "morph"}

    def on_state(self, widget, state):  # Kivy 2
        self._morph_to(state == "down")

    def on_activated(self, widget, activated):  # Kivy 3: `state` became `activated`
        self._morph_to(activated)

    def _morph_to(self, down):
        Animation.cancel_all(self, "morph")
        Animation(morph=1.0 if down else 0.0, d=0.45).start(self)


class MorphToggle(ShaderToggle):
    """Down morphs `shape_a` into `shape_b`, up morphs it back."""

    shader = StringProperty("widgets/toggle")
    shape_a = BoundedNumericProperty(4, min=0, max=SHAPES - 1)
    shape_b = BoundedNumericProperty(1, min=0, max=SHAPES - 1)

    uniforms = {**ShaderToggle.uniforms, "shape_a": "shape_a", "shape_b": "shape_b"}


class MergeToggle(ShaderToggle):
    """Down melts a circle and a box into one, up pulls them apart."""

    shader = StringProperty("widgets/merge")


class SwitchToggle(ShaderToggle):
    """An on/off switch whose knob melts into its outline as it slides; on, it
    turns `tint_on` (the same as `tint` unless given) and blooms by `glow`."""

    shader = StringProperty("widgets/switch")
    tint_on = ColorProperty(None, allownone=True)
    glow = NumericProperty(0.0)
    active_tint = AliasProperty(lambda self: self.tint_on or self.tint, None, bind=("tint", "tint_on"))

    uniforms = {**ShaderToggle.uniforms, "active_tint": "tint_on", "glow": "glow"}


class CombineToggle(ShaderToggle):
    """Down slides a circle and a box together into `op`: 0 union, 1 smooth union,
    2 smooth subtract, 3 smooth intersect; up pulls them apart."""

    shader = StringProperty("widgets/combine")
    op = BoundedNumericProperty(0, min=0, max=3)

    uniforms = {**ShaderToggle.uniforms, "op": "op"}


class OnionButton(ButtonBehavior, ShaderWidget):
    """Every press sends outlines out from the shape."""

    shader = StringProperty("widgets/onion")
    shape = BoundedNumericProperty(2, min=0, max=SHAPES - 1)

    uniforms = {**ShaderWidget.uniforms, "shape": "shape"}

    def on_press(self, *args):
        self.play(0.9)
