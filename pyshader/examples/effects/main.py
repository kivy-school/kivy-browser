import sys
from os.path import join

from kivy import kivy_data_dir
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.effectwidget import EffectWidget

from kivy_pyshader import PyShaderEffect

SHADER = sys.argv[1] if len(sys.argv) > 1 else "wave"
GLSL = sys.argv[2] if len(sys.argv) > 2 else SHADER
UNIFORMS = {"tint": {"tint": [1.0, 0.35, 0.6, 1.0], "strength": 0.6}}

Builder.load_string(f"""
<Demo>:
    canvas.before:
        Color:
            rgb: 0.12, 0.13, 0.18
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: "vertical"
        padding: "24dp"
        spacing: "12dp"
        Image:
            source: "{join(kivy_data_dir, "logo", "kivy-icon-512.png")}"
        Label:
            text: "EffectWidget + PyShader: {SHADER}"
            font_size: "28sp"
            size_hint_y: None
            height: "48dp"
        BoxLayout:
            size_hint_y: None
            height: "48dp"
            spacing: "12dp"
            Button:
                text: "Button"
            ToggleButton:
                text: "Toggle"
            Slider:
                value: 40
                max: 100
""")


class Demo(EffectWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.effect = PyShaderEffect(shader=GLSL, uniforms=UNIFORMS.get(SHADER, {}))
        self.effects = [self.effect]
        Window.bind(mouse_pos=self._mouse)

    def _mouse(self, window, pos):
        self.effect.uniforms = {**self.effect.uniforms, "mouse": [pos[0] - self.x, pos[1] - self.y]}


class EffectsApp(App):
    def build(self):
        return Demo()


if __name__ == "__main__":
    EffectsApp().run()
