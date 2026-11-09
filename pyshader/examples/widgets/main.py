import sys

from kivy.app import App
from kivy.core.window import Window  # noqa: F401, opens the window
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kivy_pyshader.buttons import GearButton, MorphButton, MorphToggle, RippleButton

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
    BoxLayout:
        id: row
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
            button = RippleButton(shader=shader, tint=tint, size=("180dp", "64dp"))
            button.add_widget(Label(text=text, bold=True, font_size="18sp", pos_hint={"x": 0, "y": 0}))
            buttons.append(button)
        return "Press anywhere on a button", buttons
    return "Toggle: A to B, B to A", [
        MorphToggle(shader=shader, tint=t, shape_a=a, shape_b=b) for t, (a, b) in zip(TINTS, ((4, 1), (0, 2), (3, 0)))]


class WidgetsApp(App):
    def build(self):
        demo = Demo()
        demo.ids.title.text, children = widgets()
        for widget in children:
            widget.size_hint = (None, None)
            if SHADER != "ripple":
                widget.size = ("160dp", "160dp")
            cell = AnchorLayout()
            cell.add_widget(widget)
            demo.ids.row.add_widget(cell)
        return demo


if __name__ == "__main__":
    WidgetsApp().run()
