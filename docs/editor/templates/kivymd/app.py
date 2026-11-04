import os

from kivy.lang import Builder

from kivymd.app import MDApp


class PlaygroundApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        return Builder.load_file(os.path.join(os.path.dirname(__file__), "app.kv"))

    def greet(self, name):
        self.root.ids.title.text = f"Hello, {name or 'KivyMD'}!"


if __name__ == "__main__":
    PlaygroundApp().run()
