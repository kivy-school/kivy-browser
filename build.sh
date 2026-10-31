#!/bin/sh
# ./build.sh [serve]  builds the site into ./site
#   KIVY        kivy checkout (psychowasp/kivy wasm-support), default ../kivy
#   KIVY_WHEEL  its Pyodide wheel, default $KIVY/dist-wasm/kivy-*.whl
#   CARBONKIVY  CarbonKivy checkout, default ../CarbonKivy
set -e
cd "$(dirname "$0")"
KIVY=${KIVY:-../kivy}
CARBONKIVY=${CARBONKIVY:-../CarbonKivy}
KIVY_WHEEL=${KIVY_WHEEL:-$(ls "$KIVY"/dist-wasm/kivy-*.whl | head -1)}
KIVY_SOURCE=${KIVY_SOURCE:-https://github.com/psychowasp/kivy/blob/wasm-support/examples/}
CARBONKIVY_SOURCE=${CARBONKIVY_SOURCE:-https://github.com/CarbonKivy/CarbonKivy/blob/master/examples/}

rm -rf site build/carbonkivy
SOURCE_DATE_EPOCH=315532800 uv build --wheel --out-dir build/carbonkivy "$CARBONKIVY"
uvx --with mkdocs-material mkdocs build
python3 tools/pack.py --site site \
    --kivy-examples "$KIVY/examples" --kivy-list kivy_examples.txt --kivy-source "$KIVY_SOURCE" \
    --carbonkivy-examples "$CARBONKIVY/examples" --carbonkivy-source "$CARBONKIVY_SOURCE" \
    "$KIVY_WHEEL" build/carbonkivy/carbonkivy-*.whl
du -sh site site/wheels/* | sort -h

if [ "$1" = "serve" ]; then
    python3 -m http.server --directory site --bind 127.0.0.1 "${PORT:-8000}"
fi
