import sys
from os.path import join

from kivy import kivy_data_dir
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

from kivy_pyshader import PyShaderTransition

SHADER = sys.argv[1] if len(sys.argv) > 1 else "fade"
GLSL = sys.argv[2] if len(sys.argv) > 2 else SHADER
LOGO = join(kivy_data_dir, "logo", "kivy-icon-512.png")

Builder.load_string("""
<Card>:
    canvas.before:
        Color:
            rgba: root.color
        Rectangle:
            pos: self.pos
            size: self.size
""")


class Card(Screen):
    color = ColorProperty("white")

    def __init__(self, text, swap=False, horizontal=False, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation="horizontal" if horizontal else "vertical", padding="24dp")
        logo = Image(source=LOGO)
        label = Label(text=text, font_size="48sp", bold=True)
        if not horizontal:
            label.size_hint_y = 0.4
        for widget in (label, logo) if swap else (logo, label):
            box.add_widget(widget)
        self.add_widget(box)


class TransitionsApp(App):
    def build(self):
        sm = ScreenManager(transition=PyShaderTransition(shader=GLSL, duration=1.5))
        for i, color in enumerate(("#d9402f", "#2673d9", "#33a65a")):
            sm.add_widget(Card(f"Screen {i + 1}", swap=i == 1, horizontal=i == 2, name=str(i), color=color))
        Clock.schedule_interval(lambda dt: self.advance(sm), 2.5)
        return sm

    def advance(self, sm):
        names = sm.screen_names
        sm.current = names[(names.index(sm.current) + 1) % len(names)]


if __name__ == "__main__":
    TransitionsApp().run()
