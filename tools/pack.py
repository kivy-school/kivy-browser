"""Site data: slim wheels, one zip per app folder, a manifest per pack."""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

MAX_FILE = 2_000_000
SKIP_NAMES = {'__pycache__', '.DS_Store', '.git'}
SKIP_SUFFIXES = {'.c', '.cpp', '.h', '.pyx', '.pxd', '.pxi', '.pyc'}


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--site', type=Path, required=True)
    ap.add_argument('--kivy-examples', type=Path, required=True)
    ap.add_argument('--kivy-list', type=Path, required=True)
    ap.add_argument('--kivy-source', required=True)
    ap.add_argument('--carbonkivy-examples', type=Path, required=True)
    ap.add_argument('--carbonkivy-source', required=True)
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


if __name__ == '__main__':
    main()
