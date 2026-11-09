import sys

from kivy.app import App
from kivy.core.window import Window  # noqa: F401, opens the window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kivy_pyshader.buttons import (CombineToggle, GearButton, MergeToggle, MorphButton, MorphToggle,
                                   OnionButton, RippleButton, SwitchToggle)

SHADER = sys.argv[1] if len(sys.argv) > 1 else "gear"
GLSL = sys.argv[2] if len(sys.argv) > 2 else SHADER
TINTS = ("#3f7fe0", "#e0533f", "#3fbf7f")

Builder.load_string("""
<Demo>:
    orientation: "vertical"
    padding: "24dp"
    spacing: "16dp"
    canvas.before:
        Color:
            rgb: 0.1, 0.11, 0.15
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        id: title
        size_hint_y: None
        height: "40dp"
        font_size: "20sp"
    GridLayout:
        id: grid
        cols: 3
        spacing: "24dp"
""")


class Demo(BoxLayout):
    pass


def widgets():
    shader = f"widgets/{GLSL}"
    if SHADER == "gear":
        return "Press: one more tooth, back to 5 after 12", [
            GearButton(shader=shader, tint=t, teeth=n, last_teeth=n) for t, n in zip(TINTS, (5, 8, 11))]
    if SHADER == "morph":
        return "Press: morph to the next shape", [
            MorphButton(shader=shader, tint=t, shape=n, last_shape=n) for t, n in zip(TINTS, (0, 1, 2))]
    if SHADER == "ripple":
        buttons = []
        for tint, text in zip(TINTS, ("Save", "Delete", "Share")):
            button = RippleButton(shader=shader, tint=tint)
            label = Label(text=text, bold=True, font_size="18sp", pos=button.pos, size=button.size)
            button.bind(pos=label.setter("pos"), size=label.setter("size"))
            button.add_widget(label)
            buttons.append(button)
        return "Press anywhere on a button", buttons
    if SHADER == "combine":
        return "Toggle: union, smooth union, subtract, intersect", [
            CombineToggle(shader=shader, tint=t, op=n) for t, n in zip(TINTS + ("#b06fe0",), (0, 1, 2, 3))]
    if SHADER == "onion":
        return "Press: outlines run out from the shape", [
            OnionButton(shader=shader, tint=t, shape=n) for t, n in zip(TINTS, (2, 1, 3))]
    if SHADER == "merge":
        return "Toggle: melt together, pull apart", [MergeToggle(shader=shader, tint=t) for t in TINTS]
    if SHADER == "switch":
        return "Toggle: keeps its color, changes color, blooms", [
            SwitchToggle(shader=shader, tint=TINTS[0]),
            SwitchToggle(shader=shader, tint=TINTS[1], tint_on=TINTS[2]),
            SwitchToggle(shader=shader, tint=TINTS[0], glow=1.0)]
    return "Toggle: A to B, B to A", [
        MorphToggle(shader=shader, tint=t, shape_a=a, shape_b=b) for t, (a, b) in zip(TINTS, ((4, 1), (0, 2), (3, 0)))]


class WidgetsApp(App):
    def build(self):
        demo = Demo()
        demo.ids.title.text, children = widgets()
        grid = demo.ids.grid
        if SHADER == "combine":
            grid.cols = 2
        if SHADER in ("ripple", "switch"):
            grid.row_force_default = True
            grid.row_default_height = dp(64)
        # Each button is a cell of its own, pressed on its own.
        for widget in children:
            grid.add_widget(widget)
        return demo


if __name__ == "__main__":
    WidgetsApp().run()
