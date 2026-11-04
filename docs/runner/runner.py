import asyncio
import builtins
import itertools
import os
import runpy
import sys
import traceback
import types

import js
import kivy.base
from kivy.app import App
from kivy.base import EventLoop, stopTouchApp
from kivy.lang import Builder

HOME = '/home/pyodide'
APP = HOME + '/app'
PLAY = HOME + '/playground'
OURS = (APP + '/', PLAY + '/')
task = None
_ran = False
_path = list(sys.path)
_strings = itertools.count()


def _report(fut):
    if not fut.cancelled() and fut.exception() is not None:
        js.kivyError(''.join(traceback.format_exception(fut.exception())))


def _watch(fut):
    global task
    if isinstance(fut, asyncio.Future):
        task = fut
        fut.add_done_callback(_report)
    return fut


_app_run = App.run
App.run = lambda self: _watch(_app_run(self))
_run_touch_app = kivy.base.runTouchApp
kivy.base.runTouchApp = \
    lambda widget=None, embedded=False: _watch(_run_touch_app(widget, embedded))

# kv strings from app code get a filename, so they can be unloaded
_load_string = Builder.load_string


def _load_string_tracked(string, **kwargs):
    if kwargs.get('filename') is None \
            and sys._getframe(1).f_code.co_filename.startswith(OURS):
        kwargs['filename'] = f'{APP}/<string {next(_strings)}>'
    return _load_string(string, **kwargs)


Builder.load_string = _load_string_tracked


def started():
    return EventLoop.status == 'started'


async def run(path):
    global _ran
    await _stop()
    _ran = True
    folder = os.path.dirname(path)
    os.chdir(folder)
    sys.path[:0] = [folder, APP]
    sys.argv = [path]
    try:
        runpy.run_path(path, run_name='__main__')
    except BaseException:
        js.kivyError(traceback.format_exc())


async def play(py, kv):
    global _ran
    await _stop()
    _ran = True
    os.makedirs(PLAY, exist_ok=True)
    for name, text in (('app.py', py), ('app.kv', kv)):
        with open(os.path.join(PLAY, name), 'w') as f:
            f.write(text)
    os.chdir(PLAY)
    sys.path.insert(0, PLAY)
    module = types.ModuleType('__main__')
    module.__file__ = os.path.join(PLAY, 'app.py')
    module.__builtins__ = builtins
    sys.modules['__main__'] = module
    try:
        exec(compile(py, module.__file__, 'exec'), module.__dict__)
    except BaseException:
        js.kivyError(traceback.format_exc())


async def _stop():
    '''Stops the last app and drops what it left in Kivy.'''
    if not _ran:
        return
    from kivy.animation import Animation
    from kivy.clock import Clock
    from kivy.core.window import Window
    from kivy.factory import Factory
    from kivy.uix.behaviors import ToggleButtonBehavior

    app = App.get_running_app()
    if app:
        app.stop()
    else:
        stopTouchApp()
    if task is not None and not task.done():
        await asyncio.wait([task], timeout=2)

    local = {'__main__'} | {
        name for name, mod in list(sys.modules.items())
        if (getattr(mod, '__file__', None) or '').startswith(OURS)}

    def ours(cb):
        return getattr(getattr(cb, 'func', cb), '__module__', None) in local

    Animation.cancel_all(None)
    for event in Clock.get_events():
        if ours(event.get_callback()):
            event.cancel()
    for name in [*Window.properties(), *Window.events()]:
        for cb, _, _, is_ref, uid in Window.get_property_observers(name, True):
            cb = cb() if is_ref else cb
            if cb is None or not ours(cb):
                continue
            if uid:
                Window.unbind_uid(name, uid)
            else:
                Window.unbind(**{name: cb})
    for child in list(Window.children):
        Window.remove_widget(child)
    ToggleButtonBehavior._toggle_groups.clear()

    files = {rule[1].ctx.filename for rule in Builder.rules} | set(Builder.files) \
        | {entry.get('filename') for entry in Factory.classes.values()}
    for filename in files:
        if filename and filename.startswith(OURS):
            Builder.unload_file(filename)
    for name, entry in list(Factory.classes.items()):
        cls = entry.get('cls')
        if cls is not None and cls.__module__ in local:
            Factory.unregister(name)
    for name in local - {'__main__'}:
        sys.modules.pop(name, None)

    Window.clearcolor = (0, 0, 0, 1)
    sys.path[:] = _path
    os.chdir(HOME)
