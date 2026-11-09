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

async function runApp(runner, pack, id, args) {
  manifests[pack] ??= get(`../apps/${pack}.json`).then((r) => r.json());
  const app = (await manifests[pack]).apps.find((a) => (a.id ?? a.path) === id);
  if (!app) throw new Error(`no app ${id} in ${pack}`);
  kivyError("");
  say(`Starting ${app.title}…`);
  const zip = `../apps/${pack}/${app.zip}`;
  if (!unpacked.has(zip)) {
    pyodide.unpackArchive(await (await get(zip)).arrayBuffer(), "zip", { extractDir: "/home/pyodide/app" });
    unpacked.add(zip);
  }
  await runner.run(`/home/pyodide/app/${app.path}`, pyodide.toPy(args ?? app.args ?? []));
  await started(runner);
}

let next = null, busy = false;
globalThis.kivyRun = async (pack, id, args) => {
  next = [pack, id, args];
  if (busy) return;
  busy = true;
  try {
    const runner = await booted;
    while (next) {
      const [p, a, g] = next;
      next = null;
      await runApp(runner, p, a, g);
    }
  } catch (err) {
    kivyError(String(err?.message ?? err));
  } finally {
    busy = false;
  }
};

// PyShader playground: the compiled .glsl into the package, then the preset's app on it
globalThis.kivyShader = async (id, glsl) => {
  const runner = await booted;
  const [kind, name] = id.split("/");
  runner.write_shader(kind, "playground", glsl);
  await kivyRun("pyshader", id, [name, "playground"]);
  return errorEl.hidden ? "" : errorEl.textContent;
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
