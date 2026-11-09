(async () => {
  const root = document.querySelector(".kb-shaders");
  if (!root) return;
  const site = new URL("../", location);
  const { source, apps } = await (await fetch(new URL("apps/pyshader.json", site))).json();
  const PLAYGROUND = "Playground";
  const groups = [...new Set(apps.map((a) => a.group)), PLAYGROUND];

  const bar = (cls) => root.appendChild(Object.assign(document.createElement("nav"), { className: `kb-bar ${cls}` }));
  const groupBar = bar("kb-groups");
  const appBar = bar("kb-list");
  const frame = root.appendChild(Object.assign(document.createElement("iframe"), {
    className: "kb-frame", title: "PyShader", allow: "autoplay; clipboard-read; clipboard-write",
  }));
  const tab = (parent, text, onclick) =>
    parent.appendChild(Object.assign(document.createElement("button"), { type: "button", textContent: text, onclick }));
  const mark = (parent, el) => {
    for (const b of parent.querySelectorAll("button")) b.setAttribute("aria-selected", String(b === el));
    el?.scrollIntoView({ block: "nearest", inline: "nearest" });
  };
  const call = (fn, id, query) => {
    if (frame.contentWindow?.[fn]) frame.contentWindow[fn](id);
    else frame.src = new URL(`shaders/?${query}`, site);
  };

  let group;
  const groupTabs = groups.map((name) =>
    tab(groupBar, name, () => (name === PLAYGROUND ? playground() : run(apps.find((a) => a.group === name)))));
  const showGroup = (name) => {
    group = name;
    mark(groupBar, groupTabs[groups.indexOf(name)]);
    appBar.replaceChildren();
    appBar.hidden = name === PLAYGROUND;
    for (const app of apps.filter((a) => a.group === name)) app.tab = tab(appBar, app.title, () => run(app));
    appBar.appendChild(Object.assign(document.createElement("a"), { className: "kb-source", target: "_blank", textContent: "source ↗" }));
  };
  const run = (app) => {
    if (app.group !== group) showGroup(app.group);
    mark(appBar, app.tab);
    appBar.querySelector(".kb-source").href = source + app.shader + ".py";
    history.replaceState(null, "", `#${app.id}`);
    call("shaderShow", app.id, `app=${encodeURIComponent(app.id)}`);
  };
  const playground = (id) => {
    showGroup(PLAYGROUND);
    history.replaceState(null, "", `#playground${id ? `/${id}` : ""}`);
    call("shaderPlayground", id, `playground=${encodeURIComponent(id ?? "")}`);
  };
  globalThis.kbShaderHash = (id) => history.replaceState(null, "", `#playground/${id}`);

  const wanted = decodeURIComponent(location.hash.slice(1));
  if (wanted.split("/")[0] === "playground") playground(wanted.split("/").slice(1).join("/") || undefined);
  else run(apps.find((a) => a.id === wanted) ?? apps[0]);
})();
