"""Site data: slim wheels, one zip per app folder, a manifest per pack."""
import argparse
import ast
import hashlib
import json
import re
import tomllib
import zipfile
from pathlib import Path

MAX_FILE = 2_000_000
SKIP_NAMES = {'__pycache__', '.DS_Store', '.git'}
SKIP_SUFFIXES = {'.c', '.cpp', '.h', '.pyx', '.pxd', '.pxi', '.pyc'}
KIVYMD_SHAPES = {  # need materialshapes
    'bottomappbar.py', 'bottomsheet.py', 'carousel.py', 'dialog.py', 'expansionpanel.py',
    'hero.py', 'imagelist.py', 'ios_buttons.py', 'ios_dialog.py', 'ios_liquid_dropdown.py',
    'ios_tabs.py', 'ios_textfielld.py', 'list.py', 'loadingindicator.py', 'material_scroll.py',
    'navigationdrawer.py', 'ripple_m3.py', 'search.py', 'apps/calls/main.py'}
PYSHADER_GROUPS = (('ShaderTransitions', 'transitions'), ('EffectWidget', 'effects'),
                   ('RenderContext', 'render'))
GLES2_NAMES = ('position-attribute', 'texcoord-attribute', 'color-attribute', 'color-uniform',
               'opacity-uniform', 'uv-varying', 'color-varying', 'content-sampler')


def slim_wheel(src, dest_dir):
    dest = dest_dir / src.name
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(src) as zin, \
            zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zout:
        drop = {i.filename for i in zin.infolist()
                if Path(i.filename).suffix in SKIP_SUFFIXES
                or i.filename.startswith('kivy/tests/')}
        for info in zin.infolist():
            if info.filename in drop:
                continue
            data = zin.read(info)
            if info.filename.endswith('.dist-info/RECORD'):
                data = ''.join(line for line in data.decode().splitlines(True)
                               if line.split(',', 1)[0] not in drop).encode()
            zout.writestr(info, data, zipfile.ZIP_DEFLATED)
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()[:12]
    (dest_dir / digest).mkdir()
    dest.rename(dest_dir / digest / dest.name)
    return f'{digest}/{dest.name}'


def folder_of(path):
    parent = Path(path).parent.as_posix()
    return '' if parent == '.' else parent


def zip_name(folder):
    return (re.sub(r'[^\w.-]+', '-', folder) or 'root') + '.zip'


def pack(name, root, apps, site, source):
    out = site / 'apps' / name
    out.mkdir(parents=True, exist_ok=True)
    folders = sorted({folder_of(a['path']) for a in apps})
    for folder in folders:
        nested = [f for f in folders if f != folder and f.startswith(folder + '/' if folder else '')]
        with zipfile.ZipFile(out / zip_name(folder), 'w', zipfile.ZIP_DEFLATED) as z:
            for p in sorted((root / folder).rglob('*')):
                rel = p.relative_to(root).as_posix()
                if p.is_dir() or SKIP_NAMES & set(p.parts) or p.suffix == '.pyc' \
                        or p.stat().st_size > MAX_FILE \
                        or any(rel.startswith(f + '/') for f in nested):
                    continue
                z.write(p, rel)
            for app in apps:
                if folder_of(app['path']) == folder:
                    for extra in app.pop('extra', []):
                        for p in [root / extra, *(root / extra).rglob('*')]:
                            if p.is_file():
                                z.write(p, p.relative_to(root).as_posix())
    for app in apps:
        app['zip'] = zip_name(folder_of(app['path']))
    (site / 'apps' / f'{name}.json').write_text(json.dumps({'source': source, 'apps': apps}, indent=1))
    print(f'{name}: {len(apps)} apps, {len(folders)} zips')


def kivy_apps(root, listing):
    apps = []
    for line in listing.read_text().splitlines():
        path, *extra = line.split('#', 1)[0].split() or [None]
        if not path:
            continue
        for f in (path, *extra):
            if not (root / f).exists():
                raise SystemExit(f'missing example file {f}')
        p = Path(path)
        apps.append({'group': p.parts[0], 'title': p.parent.name if p.stem == 'main' else p.stem,
                     'path': path, 'extra': extra})
    return apps


def carbonkivy_apps(root):
    return [{'group': None, 'title': p.parent.name, 'path': p.relative_to(root).as_posix()}
            for p in sorted(root.glob('*/main.py'), key=lambda p: p.parent.name.lower())
            if 'carbonkivy.devtools' not in p.read_text()]  # kaki hot reload


def kivymd_apps(root):
    ex = root / 'examples'
    apps = [{'group': 'ios' if p.stem.startswith('ios_') else 'material', 'title': p.stem,
             'path': p.relative_to(root).as_posix()}
            for p in sorted(ex.glob('*.py')) if '.run()' in p.read_text()]
    apps += [{'group': 'apps', 'title': p.parent.name, 'path': p.relative_to(root).as_posix()}
             for p in sorted(ex.glob('apps/*/main.py'))]
    return [a for a in apps if a['path'].removeprefix('examples/') not in KIVYMD_SHAPES]


def pyshader_options(section):
    '''The compiler options pyshader_builder passes pyshader.wasm for a [tool.pyshader] section.'''
    s = section
    parts = [f"target={s.get('target', 'fragment')}", f"format={s.get('format', 'spirv')}"]
    if s.get('content-top-down'):
        parts.append('content-top-down=1')
    elif s.get('content'):
        parts.append('content=1')
    if s.get('textures-top-down'):
        parts.append('textures-top-down=1')
    parts += [f'arg={a}' for a in s.get('arguments', [])]
    if s.get('single-file'):
        parts.append('single-file=1')
    parts += [f'{k}={s[k]}' for k in GLES2_NAMES if k in s]
    parts += [f'position-matrix={m}' for m in s.get('position-matrices', [])]
    parts.append('file=' + s['source'].rsplit('/', 1)[-1])
    return ' '.join(parts)


def pyshader_apps(wheel, pyproject, site):
    '''An app per shader in the kivy_pyshader wheel; its .py and .glsl copied for the code view.'''
    sections = {s['source']: s for s in tomllib.loads(pyproject.read_text())['tool']['pyshader'].values()
                if isinstance(s, dict)}
    out = site / 'apps' / 'pyshader' / 'src'
    apps = []
    with zipfile.ZipFile(wheel) as z:
        for group, kind in PYSHADER_GROUPS:
            for name in sorted(n for n in z.namelist()
                               if n.startswith(f'kivy_pyshader/{kind}/') and n.endswith('.glsl')):
                stem = name[:-5].rsplit('/', 1)[1]
                py = z.read(name[:-5] + '.py')
                for ext, data in (('.py', py), ('.glsl', z.read(name))):
                    (out / kind).mkdir(parents=True, exist_ok=True)
                    (out / kind / (stem + ext)).write_bytes(data)
                doc = ast.get_docstring(ast.parse(py))
                apps.append({'group': group, 'title': doc.splitlines()[0] if doc else stem,
                             'id': f'{kind}/{stem}', 'path': f'{kind}/main.py', 'args': [stem],
                             'shader': f'{kind}/{stem}',
                             'options': pyshader_options(sections[f'src/kivy_pyshader/{kind}/{stem}.py'])})
    return apps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--site', type=Path, required=True)
    ap.add_argument('--kivy-examples', type=Path, required=True)
    ap.add_argument('--kivy-list', type=Path, required=True)
    ap.add_argument('--kivy-source', required=True)
    ap.add_argument('--carbonkivy-examples', type=Path, required=True)
    ap.add_argument('--carbonkivy-source', required=True)
    ap.add_argument('--kivymd-root', type=Path, required=True)
    ap.add_argument('--kivymd-source', required=True)
    ap.add_argument('--pyshader-examples', type=Path, required=True)
    ap.add_argument('--pyshader-source', required=True)
    ap.add_argument('wheels', type=Path, nargs='+', help='kivy first')
    args = ap.parse_args()

    wheels = args.site / 'wheels'
    wheels.mkdir(parents=True, exist_ok=True)
    names = [slim_wheel(w, wheels) for w in args.wheels]
    (wheels / 'wheels.json').write_text(json.dumps(names))
    pack('kivy', args.kivy_examples, kivy_apps(args.kivy_examples, args.kivy_list),
         args.site, args.kivy_source)
    pack('carbonkivy', args.carbonkivy_examples, carbonkivy_apps(args.carbonkivy_examples),
         args.site, args.carbonkivy_source)
    pack('kivymd', args.kivymd_root, kivymd_apps(args.kivymd_root), args.site, args.kivymd_source)
    wheel = next(w for w in args.wheels if w.name.startswith('kivy_pyshader-'))
    pack('pyshader', args.pyshader_examples,
         pyshader_apps(wheel, args.pyshader_examples.parent / 'pyproject.toml', args.site),
         args.site, args.pyshader_source)


if __name__ == '__main__':
    main()
