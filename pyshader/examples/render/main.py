import sys

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window  # noqa: F401, opens the window
from kivy.graphics import Rectangle, RenderContext
from kivy.uix.widget import Widget

from kivy_pyshader import glsl

SHADER = sys.argv[1] if len(sys.argv) > 1 else "plasma"
GLSL = sys.argv[2] if len(sys.argv) > 2 else SHADER


class ShaderView(Widget):
    def __init__(self, **kwargs):
        self.canvas = RenderContext(use_parent_projection=True, use_parent_modelview=True)
        self.canvas.shader.source = glsl(f"render/{GLSL}")
        if not self.canvas.shader.success:
            raise Exception(f"Kivy could not compile render/{GLSL}.glsl")
        with self.canvas:
            self.rect = Rectangle()
        super().__init__(**kwargs)
        self.mouse = [0.0, 0.0]
        self.bind(pos=self._layout, size=self._layout)
        Clock.schedule_interval(self._tick, 0)

    def _layout(self, *_):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _tick(self, dt):
        self.canvas["time"] = Clock.get_boottime()
        self.canvas["resolution"] = [float(self.width), float(self.height)]
        self.canvas["mouse"] = self.mouse

    def on_touch_down(self, touch):
        return self.on_touch_move(touch)

    def on_touch_move(self, touch):
        self.mouse = [touch.x - self.x, touch.y - self.y]
        return True


class RenderApp(App):
    def build(self):
        return ShaderView()


if __name__ == "__main__":
    RenderApp().run()
