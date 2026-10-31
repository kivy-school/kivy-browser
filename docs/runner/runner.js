const params = new URLSearchParams(location.search);
const statusEl = document.getElementById("status");
const errorEl = document.getElementById("error");
const say = (text) => { statusEl.textContent = text; statusEl.hidden = !text; };
globalThis.kivyError = (text) => {
  errorEl.textContent = text;
  errorEl.hidden = !text;
  if (text) say("");
};

const get = async (url) => {
  const r = await fetch(url, { cache: "no-cache" });
  if (!r.ok) throw new Error(`${url}: ${r.status}`);
  return r;
};

async function boot() {
  const pyodide = globalThis.pyodide = await loadPyodide();
  pyodide.canvas.setCanvas3D(document.getElementById("canvas"));
  say("Installing Kivy…");
  const [kivy, ...extra] = await (await get("../wheels/wheels.json")).json();
  await pyodide.loadPackage("micropip");
  const micropip = pyodide.pyimport("micropip");
  const wheel = (name) => new URL(`../wheels/${name}`, location).href;
  await micropip.install(wheel(kivy));
  for (const name of extra) await micropip.install.callKwargs(wheel(name), { deps: false });
  pyodide.FS.writeFile("/home/pyodide/kivy_runner.py", await (await get("runner.py")).text());
  pyodide.runPython("import sys; sys.path.insert(0, '/home/pyodide')");
  return pyodide.pyimport("kivy_runner");
}

const booted = boot();
const manifests = {}, unpacked = new Set();

async function started(runner) {
  for (let i = 0; i < 300 && !runner.started() && errorEl.hidden; i++) await new Promise((r) => setTimeout(r, 100));
  say("");
}

async function runApp(runner, pack, path) {
  manifests[pack] ??= get(`../apps/${pack}.json`).then((r) => r.json());
  const app = (await manifests[pack]).apps.find((a) => a.path === path);
  if (!app) throw new Error(`no app ${path} in ${pack}`);
  kivyError("");
  say(`Starting ${app.title}…`);
  const zip = `../apps/${pack}/${app.zip}`;
  if (!unpacked.has(zip)) {
    pyodide.unpackArchive(await (await get(zip)).arrayBuffer(), "zip", { extractDir: "/home/pyodide/app" });
    unpacked.add(zip);
  }
  await runner.run(`/home/pyodide/app/${path}`);
  await started(runner);
}

let next = null, busy = false;
globalThis.kivyRun = async (pack, path) => {
  next = [pack, path];
  if (busy) return;
  busy = true;
  try {
    const runner = await booted;
    while (next) {
      const [p, a] = next;
      next = null;
      await runApp(runner, p, a);
    }
  } catch (err) {
    kivyError(String(err?.message ?? err));
  } finally {
    busy = false;
  }
};

globalThis.kivyReady = booted.then((runner) => {
  say("");
  return params.has("playground") ? async (py, kv) => {
    kivyError("");
    await runner.play(py, kv);
    await started(runner);
  } : null;
}, (err) => {
  kivyError(String(err?.message ?? err));
  throw err;
});

if (params.has("app")) kivyRun(params.get("pack"), params.get("app"));
