#!/bin/sh
# ./build.sh [serve]  builds the site into ./site
#   KIVY        kivy checkout (psychowasp/kivy wasm-support), default ../kivy
#   KIVY_WHEEL  its Pyodide wheel, default $KIVY/dist-wasm/kivy-*.whl
#   CARBONKIVY  CarbonKivy checkout, default ../CarbonKivy
#   KIVYMD      KivyMD checkout, default ../KivyMD
#   PYSHADER_WASM  pyshader.wasm, default: the one in the newest PyShader release below 0.1.0
set -e
cd "$(dirname "$0")"
KIVY=${KIVY:-../kivy}
CARBONKIVY=${CARBONKIVY:-../CarbonKivy}
KIVYMD=${KIVYMD:-../KivyMD}
KIVY_WHEEL=${KIVY_WHEEL:-$(ls "$KIVY"/dist-wasm/kivy-*.whl | head -1)}
KIVY_SOURCE=${KIVY_SOURCE:-https://github.com/psychowasp/kivy/blob/wasm-support/examples/}
CARBONKIVY_SOURCE=${CARBONKIVY_SOURCE:-https://github.com/CarbonKivy/CarbonKivy/blob/master/examples/}
KIVYMD_SOURCE=${KIVYMD_SOURCE:-https://github.com/kivymd/KivyMD/blob/master/}
PYSHADER_SOURCE=${PYSHADER_SOURCE:-https://github.com/kivy-school/kivy-browser/blob/main/pyshader/src/kivy_pyshader/}
WASM_INDEX=https://pypi.kivyschool.com/packages
PYPI=https://files.pythonhosted.org/packages/py3

rm -rf site build/carbonkivy build/kivymd build/ck-src build/md-src build/pyshader build/pyshader-stdlib build/pyshader-releases
mkdir -p build/pyshader-releases

# kivy_pyshader: pyshader_builder compiles pyshader/src/**/*.py to Kivy .glsl,
# with the newest PyShader release below 0.1.0 (its wheel carries the compiler)
PYSHADER_TAG=$(git ls-remote --tags --refs https://github.com/NucleantUI/PyShader \
    | sed -n 's|.*refs/tags/\(0\.0\.[0-9][0-9]*\)$|\1|p' | sort -t. -k3,3n | tail -1)
echo "PyShader $PYSHADER_TAG"
PYSHADER_WHEEL=build/pyshader-releases/pyshader-$PYSHADER_TAG-py3-none-any.whl
curl -sSfL -o "$PYSHADER_WHEEL" \
    "https://github.com/NucleantUI/PyShader/releases/download/$PYSHADER_TAG/pyshader-$PYSHADER_TAG-py3-none-any.whl"
if [ -z "$PYSHADER_WASM" ]; then
    PYSHADER_WASM=build/pyshader.wasm
    unzip -p "$PYSHADER_WHEEL" pyshader_builder/pyshader.wasm > "$PYSHADER_WASM"
fi
PYSHADER_WASM=$(cd "$(dirname "$PYSHADER_WASM")" && pwd)/$(basename "$PYSHADER_WASM")
PYSHADER_WASM=$PYSHADER_WASM SOURCE_DATE_EPOCH=315532800 \
    uv build --directory pyshader --refresh-package pyshader --refresh-package pyshader-stdlib --wheel --out-dir ../build/pyshader
git clone -q --depth 1 https://github.com/NucleantUI/pyshader-stdlib build/pyshader-stdlib
cp -R "$CARBONKIVY" build/ck-src
patch -s -p1 -d build/ck-src < patches/carbonkivy-kivy3.patch
SOURCE_DATE_EPOCH=315532800 uv build --wheel --out-dir build/carbonkivy build/ck-src

# kivymd minus materialshapes dep; src path must not contain "kivymd/"
cp -R "$KIVYMD" build/md-src
sed -i.orig '/"materialshapes/s/^/#/' build/md-src/setup.py
patch -s -p1 -d build/md-src < patches/kivymd-kivy3.patch
SOURCE_DATE_EPOCH=315532800 uv build --wheel --out-dir build/kivymd build/md-src
for url in \
    $WASM_INDEX/pillow-12.3.0-cp313-cp313-pyemscripten_2025_0_wasm32.whl \
    $WASM_INDEX/materialyoucolor-3.0.2-cp313-cp313-pyemscripten_2025_0_wasm32.whl \
    $PYPI/a/asyncgui/asyncgui-0.6.3-py3-none-any.whl \
    $PYPI/a/asynckivy/asynckivy-0.6.4-py3-none-any.whl \
    $PYPI/f/faker/faker-40.44.0-py3-none-any.whl; do
    curl -sSfL --output-dir build/kivymd -O "$url"
done

uvx --with mkdocs-material mkdocs build
python3 tools/pack.py --site site \
    --kivy-examples "$KIVY/examples" --kivy-list kivy_examples.txt --kivy-source "$KIVY_SOURCE" \
    --carbonkivy-examples "$CARBONKIVY/examples" --carbonkivy-source "$CARBONKIVY_SOURCE" \
    --kivymd-root build/md-src --kivymd-source "$KIVYMD_SOURCE" \
    --pyshader-examples pyshader/examples --pyshader-source "$PYSHADER_SOURCE" \
    --pyshader-stdlib build/pyshader-stdlib/src \
    "$KIVY_WHEEL" build/carbonkivy/carbonkivy-*.whl build/kivymd/*.whl build/pyshader/kivy_pyshader-*.whl
mkdir -p site/pyshader
cp "$PYSHADER_WASM" site/pyshader/pyshader.wasm
du -sh site site/wheels/* | sort -h

if [ "$1" = "serve" ]; then
    python3 -m http.server --directory site --bind 127.0.0.1 "${PORT:-8000}"
fi
