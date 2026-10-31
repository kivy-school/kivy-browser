# kivy-browser

Kivy 3.0.0 running as wasm (Pyodide + SDL3 + WebGL2), published to GitHub
Pages: Kivy's examples, the CarbonKivy examples and a playground.

Kivy comes from [psychowasp/kivy `wasm-support`](https://github.com/psychowasp/kivy/tree/wasm-support),
CarbonKivy from [CarbonKivy/CarbonKivy](https://github.com/CarbonKivy/CarbonKivy).
`.github/workflows/pages.yml` builds both and deploys the site.

## Local build

    # in the kivy checkout
    tools/build_emscripten_dependencies.sh
    tools/build_emscripten_wheel.sh

    # here
    KIVY=../kivy CARBONKIVY=../CarbonKivy ./build.sh serve

Open http://127.0.0.1:8000/.

- `kivy_examples.txt`: the Kivy examples on the Examples tab.
- `docs/runner/`: boots Pyodide, installs the wheels, runs an example
  (`?pack=kivy&app=canvas/lines.py`) or the playground (`?playground`).
- `docs/editor/`: the playground, Monaco editors for `app.kv` and `app.py`.
