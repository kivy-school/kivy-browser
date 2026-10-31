import os

from kivy.lang import Builder

from carbonkivy.app import CarbonApp


class PlaygroundApp(CarbonApp):
    def build(self):
        self.theme = "Gray100"
        return Builder.load_file(os.path.join(os.path.dirname(__file__), "app.kv"))

    def greet(self, name):
        self.root.ids.title.text = f"Hello, {name or 'Carbon'}!"

    def toggle_theme(self):
        self.theme = "White" if self.theme == "Gray100" else "Gray100"


if __name__ == "__main__":
    PlaygroundApp().run()
