# kivy-browser

Kivy 3.0.0 running as wasm (Pyodide + SDL3 + WebGL2), published to GitHub
Pages: Kivy's examples, the CarbonKivy and KivyMD examples, PyShader shaders
and a playground.

Kivy comes from [psychowasp/kivy `wasm-support`](https://github.com/psychowasp/kivy/tree/wasm-support),
CarbonKivy from [CarbonKivy/CarbonKivy](https://github.com/CarbonKivy/CarbonKivy)
(with `patches/carbonkivy-kivy3.patch` for Kivy 3's button API),
KivyMD from [kivymd/KivyMD](https://github.com/kivymd/KivyMD) (wheel built
without the `materialshapes` dependency and with `patches/kivymd-kivy3.patch`
for Kivy 3's button/toggle API, applied to the packed examples too; pillow and
materialyoucolor wasm wheels from
https://pypi.kivyschool.com/simple). KivyMD examples that need materialshapes
are left out (`KIVYMD_SHAPES` in `tools/pack.py`).
`.github/workflows/pages.yml` builds them and deploys the site.

`pyshader/` is `kivy-pyshader`, a package of [PyShader](https://github.com/NucleantUI/PyShader)
shaders: ShaderTransitions, EffectWidget effects and RenderContext shaders.
PyShader's build backend, `pyshader_builder` (`pyshader` from its `main`),
compiles each `.py` to a Kivy `.glsl` in the wheel; the apps in
`pyshader/examples/` load them from the package. The transitions are ported
from [KivyShaderTransitions](https://github.com/shashi278/KivyShaderTransitions)
(gl-transitions, MIT). `build.sh` takes the compiler, `pyshader.wasm`, from
PyShader's docs site (`PYSHADER_WASM` overrides), and the PyShader playground
runs it in the page.

## Local build

    # in the kivy checkout
    tools/build_emscripten_dependencies.sh
    tools/build_emscripten_wheel.sh

    # here
    KIVY=../kivy CARBONKIVY=../CarbonKivy KIVYMD=../KivyMD ./build.sh serve

Open http://127.0.0.1:8000/.

- `kivy_examples.txt`: the Kivy examples on the Examples tab.
- `docs/runner/`: boots Pyodide, installs the wheels, runs an example
  (`?pack=kivy&app=canvas/lines.py`) or the playground (`?playground`).
- `docs/editor/`: the playground, Monaco editors for `app.kv` and `app.py`.
- `docs/shaders/`: the PyShader tab, the shader's code beside its Kivy app,
  and the PyShader playground (`?playground`).
