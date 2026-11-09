from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Rectangle, RenderContext
from kivy.properties import BoundedNumericProperty, ColorProperty, ListProperty, NumericProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.uix.floatlayout import FloatLayout

from . import glsl

__all__ = ("ShaderWidget", "GearButton", "MorphButton", "RippleButton", "MorphToggle")

SHAPES = 5  # circle, star, heart, hexagon, rounded square (widgets/forms.py)


class ShaderWidget(FloatLayout):
    """Draws its shader under its children; `uniforms()` is sent every frame."""

    shader = StringProperty()
    tint = ColorProperty("#3f7fe0")
    progress = NumericProperty(1.0)

    def __init__(self, **kwargs):
        self.render = RenderContext(use_parent_projection=True, use_parent_modelview=True,
                                    use_parent_frag_modelview=True)
        with self.render:
            self.rect = Rectangle()
        super().__init__(**kwargs)
        self.canvas.before.add(self.render)
        self.fbind("shader", self._load)
        self.fbind("pos", self._layout)
        self.fbind("size", self._layout)
        self._load()
        self._layout()
        Clock.schedule_interval(self._tick, 0)

    def _load(self, *_):
        self.render.shader.source = glsl(self.shader)
        if not self.render.shader.success:
            raise Exception(f"Kivy could not compile {self.shader}.glsl")

    def _layout(self, *_):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def uniforms(self):
        return {}

    def _tick(self, dt):
        self.render["resolution"] = [float(self.width), float(self.height)]
        self.render["tint"] = [float(c) for c in self.tint]
        self.render["pressed"] = float(self.progress)
        for name, value in self.uniforms().items():
            self.render[name] = value

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

    def on_press(self):
        self.last_teeth = self.teeth
        self.teeth = self.min_teeth if self.teeth >= self.max_teeth else self.teeth + 1
        self.play()

    def uniforms(self):
        return {"teeth": float(self.teeth), "last_teeth": float(self.last_teeth)}


class MorphButton(ButtonBehavior, ShaderWidget):
    """Every press morphs into the next shape."""

    shader = StringProperty("widgets/morph")
    shape = BoundedNumericProperty(0, min=0, max=SHAPES - 1)
    last_shape = NumericProperty(0)

    def on_press(self):
        self.last_shape = self.shape
        self.shape = (self.shape + 1) % SHAPES
        self.play(0.5)

    def uniforms(self):
        return {"shape_from": float(self.last_shape), "shape_to": float(self.shape)}


class RippleButton(ButtonBehavior, ShaderWidget):
    """A ring runs out from where it was touched."""

    shader = StringProperty("widgets/ripple")
    touch = ListProperty([0.0, 0.0])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.touch = [touch.x - self.x, touch.y - self.y]
        return super().on_touch_down(touch)

    def on_press(self):
        self.play(0.7)

    def uniforms(self):
        return {"touch": [float(v) for v in self.touch]}


class MorphToggle(ToggleButtonBehavior, ShaderWidget):
    """Down morphs `shape_a` into `shape_b`, up morphs it back."""

    shader = StringProperty("widgets/toggle")
    shape_a = BoundedNumericProperty(4, min=0, max=SHAPES - 1)
    shape_b = BoundedNumericProperty(1, min=0, max=SHAPES - 1)
    tint_on = ColorProperty("#f0a030")
    morph = NumericProperty(0.0)

    def on_state(self, widget, state):
        Animation.cancel_all(self, "morph")
        Animation(morph=1.0 if state == "down" else 0.0, d=0.45).start(self)

    def uniforms(self):
        return {"shape_a": float(self.shape_a), "shape_b": float(self.shape_b), "morph": float(self.morph),
                "tint_on": [float(c) for c in self.tint_on]}
