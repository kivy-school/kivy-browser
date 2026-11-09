import { compile, CompileError } from "./pyshader.js";

const MONACO = "https://cdn.jsdelivr.net/npm/monaco-editor@0.52.2/min/vs";
const RELOAD_DELAY = 600;
const KEY = "kb-pyshader-preset";

const params = new URLSearchParams(location.search);
const status = document.getElementById("status");
const frame = document.getElementById("app");
const preset = document.getElementById("preset");
const problems = document.getElementById("problems");
const tabs = [...document.querySelectorAll(".files button")];
const rail = document.getElementById("rail");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

fold();

const text = async (url) => {
  const r = await fetch(url, { cache: "no-cache" });
  if (!r.ok) throw new Error(`${url}: ${r.status}`);
  return r.text();
};
const manifest = text("../apps/pyshader.json").then(JSON.parse);
const modules = text("../apps/pyshader/modules.json").then(JSON.parse, () => ({}));
const monaco = await loadMonaco();

const dark = matchMedia("(prefers-color-scheme: dark)");
const models = { py: monaco.editor.createModel("", "python"), glsl: monaco.editor.createModel("", "cpp") };
const editor = monaco.editor.create(document.getElementById("editor"), {
  model: models.py, automaticLayout: true, minimap: { enabled: false }, fontSize: 13, tabSize: 4,
  insertSpaces: true, scrollBeyondLastLine: false, theme: dark.matches ? "vs-dark" : "vs",
});
dark.addEventListener("change", (e) => monaco.editor.setTheme(e.matches ? "vs-dark" : "vs"));

let mode = null, current = null, quiet = false;

function showFile(name) {
  editor.setModel(models[name]);
  editor.updateOptions({ readOnly: mode !== "playground" || name === "glsl" });
  for (const b of tabs) b.setAttribute("aria-selected", String(b.dataset.file === name));
}
for (const b of tabs) b.onclick = () => showFile(b.dataset.file);

async function load(app) {
  current = app;
  const base = `../apps/pyshader/src/${app.shader}`;
  const [py, glsl] = await Promise.all([text(`${base}.py`), text(`${base}.glsl`)]);
  quiet = true;
  models.py.setValue(py);
  models.glsl.setValue(glsl);
  quiet = false;
  const name = app.shader.split("/")[1];
  tabs[0].textContent = `${name}.py`;
  tabs[1].textContent = `${name}.glsl`;
  rail.querySelector(".rail-label").textContent = `${name}.py`;
  showProblems([]);
  showFile("py");
}

function showProblems(errors) {
  const lines = models.py.getLineCount();
  monaco.editor.setModelMarkers(models.py, "pyshader", errors
    .filter((e) => e.line && !e.file && e.line <= lines)
    .map((e) => ({
      severity: monaco.MarkerSeverity.Error, message: e.message,
      startLineNumber: e.line, endLineNumber: e.line, startColumn: 1, endColumn: models.py.getLineMaxColumn(e.line),
    })));
  problems.hidden = !errors.length;
  problems.textContent = errors.map((e) => e.kivy ? `Kivy:\n${e.message}`
    : `${e.file ? e.file + ", " : ""}${e.line ? `line ${e.line}: ` : ""}${e.message}`).join("\n");
}

async function runner(appId) {
  if (!frame.getAttribute("src")) {
    frame.src = `../runner/?pack=pyshader${appId ? `&app=${encodeURIComponent(appId)}` : ""}`;
    if (appId) return null;
  }
  while (!frame.contentWindow?.kivyRun) await sleep(50);
  return frame.contentWindow;
}

globalThis.shaderShow = async (id) => {
  const { apps } = await manifest;
  const app = apps.find((a) => a.id === id) ?? apps[0];
  mode = "view";
  preset.hidden = true;
  status.textContent = "";
  await load(app);
  (await runner(app.id))?.kivyRun("pyshader", app.id);
};

globalThis.shaderPlayground = async (id) => {
  const { apps } = await manifest;
  if (!preset.options.length) {
    for (const group of new Set(apps.map((a) => a.group))) {
      const og = preset.appendChild(Object.assign(document.createElement("optgroup"), { label: group }));
      for (const a of apps.filter((x) => x.group === group)) og.appendChild(new Option(a.title, a.id));
    }
  }
  let saved = null;
  try { saved = localStorage.getItem(KEY); } catch {}
  const app = apps.find((a) => a.id === id) ?? apps.find((a) => a.id === saved) ?? apps.find((a) => a.id === "render/plasma");
  mode = "playground";
  preset.hidden = false;
  preset.value = app.id;
  await load(app);
  await runner(null);
  reload();
};

preset.addEventListener("change", async () => {
  const app = (await manifest).apps.find((a) => a.id === preset.value);
  try { localStorage.setItem(KEY, app.id); } catch {}
  parent.kbShaderHash?.(app.id);
  await load(app);
  reload();
});

let busy = false, again = false, timer = 0;
models.py.onDidChangeContent(() => {
  if (quiet || mode !== "playground") return;
  clearTimeout(timer);
  timer = setTimeout(reload, RELOAD_DELAY);
});

async function reload() {
  if (mode !== "playground") return;
  if (busy) { again = true; return; }
  busy = true;
  const app = current;
  try {
    status.textContent = "Compiling…";
    let glsl;
    try {
      glsl = await compile(models.py.getValue(), app.options, await modules);
    } catch (err) {
      if (!(err instanceof CompileError)) throw err;
      showProblems([err]);
      status.textContent = "PyShader error";
      return;
    }
    showProblems([]);
    quiet = true;
    models.glsl.setValue(glsl);
    quiet = false;
    status.textContent = "Reloading…";
    const kivy = await (await runner(null)).kivyShader(app.id, glsl);
    if (kivy) showProblems([{ kivy: true, message: kivy }]);
    status.textContent = kivy ? "Kivy error" : "Running";
  } catch (err) {
    status.textContent = "Error";
    console.error(err);
  } finally {
    busy = false;
    if (again) { again = false; reload(); }
  }
}

function fold() {
  const FOLD = "kb-pyshader-folded";
  let folded = null;
  try { folded = JSON.parse(localStorage.getItem(FOLD)); } catch {}
  folded ??= matchMedia("(orientation: portrait)").matches;
  const editors = document.querySelector(".editors");
  const show = () => {
    editors.classList.toggle("collapsed", folded);
    rail.title = folded ? "Show the code" : "Hide the code";
    rail.querySelector(".chevron").textContent = folded ? "›" : "‹";
  };
  rail.addEventListener("click", () => {
    folded = !folded;
    show();
    try { localStorage.setItem(FOLD, JSON.stringify(folded)); } catch {}
  });
  show();
}

function loadMonaco() {
  return new Promise((resolve, reject) => {
    globalThis.require.config({ paths: { vs: MONACO } });
    globalThis.require(["vs/editor/editor.main"], () => resolve(globalThis.monaco), reject);
  });
}

if (params.has("playground")) shaderPlayground(params.get("playground"));
else if (params.has("app")) shaderShow(params.get("app"));
