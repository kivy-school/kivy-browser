const RELOAD_DELAY = 600;
const MONACO = "https://cdn.jsdelivr.net/npm/monaco-editor@0.52.2/min/vs";

const status = document.getElementById("status");
const frame = document.getElementById("app");
const select = document.getElementById("template");

fold();

const text = async (url) => {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${url}: ${r.status}`);
  return r.text();
};
const template = async (name) => {
  const [py, kv] = await Promise.all([text(`templates/${name}/app.py`), text(`templates/${name}/app.kv`)]);
  return { py, kv };
};

select.value = localStorage.getItem("kb-playground-template") ?? "kivy";
const [sources, monaco] = await Promise.all([template(select.value), loadMonaco()]);

registerKv(monaco);
const dark = matchMedia("(prefers-color-scheme: dark)");
const options = {
  automaticLayout: true, minimap: { enabled: false }, fontSize: 13, tabSize: 4,
  insertSpaces: true, scrollBeyondLastLine: false, theme: dark.matches ? "vs-dark" : "vs",
};
const editors = {
  kv: monaco.editor.create(document.getElementById("kv"), { ...options, value: sources.kv, language: "kv" }),
  py: monaco.editor.create(document.getElementById("py"), { ...options, value: sources.py, language: "python" }),
};
dark.addEventListener("change", (e) => monaco.editor.setTheme(e.matches ? "vs-dark" : "vs"));

let play = null, busy = false, again = false, timer = 0, quiet = false;
async function reload() {
  if (!play) return;
  if (busy) { again = true; return; }
  busy = true;
  status.textContent = "Reloading…";
  try {
    await play(editors.py.getValue(), editors.kv.getValue());
    status.textContent = "Running";
  } catch (err) {
    status.textContent = "Error";
    console.error(err);
  }
  busy = false;
  if (again) { again = false; reload(); }
}
for (const editor of Object.values(editors)) {
  editor.onDidChangeModelContent(() => {
    if (quiet) return;
    clearTimeout(timer);
    timer = setTimeout(reload, RELOAD_DELAY);
  });
}
select.addEventListener("change", async () => {
  localStorage.setItem("kb-playground-template", select.value);
  const { py, kv } = await template(select.value);
  quiet = true;
  editors.py.setValue(py);
  editors.kv.setValue(kv);
  quiet = false;
  reload();
});

status.textContent = "Starting Python…";
while (!frame.contentWindow?.kivyReady) await new Promise((r) => setTimeout(r, 100));
try {
  play = await frame.contentWindow.kivyReady;
  reload();
} catch (err) {
  status.textContent = `Could not start: ${err.message}`;
}

function loadMonaco() {
  return new Promise((resolve, reject) => {
    globalThis.require.config({ paths: { vs: MONACO } });
    globalThis.require(["vs/editor/editor.main"], () => resolve(globalThis.monaco), reject);
  });
}

function fold() {
  const KEY = "kb-playground-folded";
  let folded;
  try { folded = JSON.parse(localStorage.getItem(KEY)); } catch {}
  folded ??= { editors: matchMedia("(orientation: portrait)").matches };
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(folded)); } catch {} };

  const editorsEl = document.querySelector(".editors");
  const rail = document.getElementById("rail");
  const showRail = () => {
    editorsEl.classList.toggle("collapsed", !!folded.editors);
    rail.title = folded.editors ? "Show the code" : "Hide the code";
    rail.querySelector(".chevron").textContent = folded.editors ? "›" : "‹";
  };
  rail.addEventListener("click", () => { folded.editors = !folded.editors; showRail(); save(); });
  showRail();

  for (const pane of document.querySelectorAll(".panes .pane")) {
    const name = pane.dataset.pane;
    const toggle = pane.querySelector(".pane-toggle");
    const show = () => {
      pane.classList.toggle("collapsed", !!folded[name]);
      toggle.querySelector(".chevron").textContent = folded[name] ? "▸" : "▾";
    };
    toggle.addEventListener("click", () => { folded[name] = !folded[name]; show(); save(); });
    show();
  }
}

function registerKv(monaco) {
  monaco.languages.register({ id: "kv", extensions: [".kv"], aliases: ["KV", "kv"] });
  monaco.languages.setLanguageConfiguration("kv", {
    comments: { lineComment: "#" },
    brackets: [["(", ")"], ["[", "]"], ["{", "}"]],
    autoClosingPairs: [
      { open: "(", close: ")" }, { open: "[", close: "]" }, { open: "{", close: "}" },
      { open: "'", close: "'" }, { open: '"', close: '"' },
    ],
    onEnterRules: [{ beforeText: /:\s*$/, action: { indentAction: monaco.languages.IndentAction.Indent } }],
  });
  monaco.languages.setMonarchTokensProvider("kv", {
    keywords: ["True", "False", "None", "and", "or", "not", "if", "else", "in", "is", "lambda"],
    tokenizer: {
      root: [
        [/^\s*#:.*$/, "keyword"],
        [/#.*$/, "comment"],
        [/^\s*<[^>]+>:?/, "type"],
        [/^(\s*)([A-Z][\w.]*)(:)/, ["", "type", "delimiter"]],
        [/^(\s*)(canvas(?:\.before|\.after)?)(:)/, ["", "keyword", "delimiter"]],
        [/^(\s*)(on_\w+)(:)/, ["", "keyword", "delimiter"]],
        [/^(\s*)(\w+)(:)/, ["", "attribute.name", "delimiter"]],
        { include: "value" },
      ],
      value: [
        [/"([^"\\]|\\.)*"/, "string"],
        [/'([^'\\]|\\.)*'/, "string"],
        [/\d+(\.\d+)?/, "number"],
        [/\b(self|root|app|ids)\b/, "variable.predefined"],
        [/[a-zA-Z_]\w*/, { cases: { "@keywords": "keyword", "@default": "identifier" } }],
        [/[()[\]{},.:]/, "delimiter"],
      ],
    },
  });
}
