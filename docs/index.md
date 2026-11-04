# Kivy in the browser

[Kivy](https://kivy.org) 3 compiled to WebAssembly: the Kivy wheel is built
with [Pyodide](https://pyodide.org), SDL3 (image, mixer, ttf) and ThorVG are
built for wasm, and Kivy draws with WebGL2. Nothing is installed: Python,
Kivy and the app all run in the page.

- [Examples](examples.md): Kivy's own examples, pick one from the tab bar.
- [CarbonKivy](carbonkivy.md): the [CarbonKivy](https://github.com/CarbonKivy/CarbonKivy)
  examples, IBM's Carbon Design System for Kivy.
- [KivyMD](kivymd.md): the [KivyMD](https://github.com/kivymd/KivyMD)
  examples, Material Design for Kivy.
- [Playground](playground.md): edit `app.kv` and `app.py`, the Kivy app
  beside them reloads.

CarbonKivy and KivyMD are installed for every page, so the playground can
use them too.

## Your own app

```python
from kivy.app import App
from kivy.uix.button import Button


class HelloApp(App):
    def build(self):
        return Button(text="Hello from the browser")


HelloApp().run()
```

`App.run()` doesn't block in the browser: it schedules `App.async_run()` on
Pyodide's event loop and returns.

Kivy sources: [psychowasp/kivy, `wasm-support`](https://github.com/psychowasp/kivy/tree/wasm-support)
(`tools/build_emscripten_dependencies.sh`, `tools/build_emscripten_wheel.sh`).
