const site = new URL("../", location);

for (const root of document.querySelectorAll(".kb-apps")) show(root);

async function show(root) {
  const pack = root.dataset.pack;
  const { source, apps } = await (await fetch(new URL(`apps/${pack}.json`, site))).json();
  const groups = [...new Set(apps.map((a) => a.group).filter(Boolean))];

  const bar = (cls) => root.appendChild(Object.assign(document.createElement("nav"), { className: `kb-bar ${cls}` }));
  const groupBar = groups.length ? bar("kb-groups") : null;
  const appBar = bar("kb-list");
  const frame = root.appendChild(Object.assign(document.createElement("iframe"), {
    className: "kb-frame", title: "Kivy app", allow: "autoplay; clipboard-read; clipboard-write",
  }));
  const tab = (parent, text, onclick) =>
    parent.appendChild(Object.assign(document.createElement("button"), { type: "button", textContent: text, onclick }));
  const mark = (parent, el) => {
    for (const b of parent.querySelectorAll("button")) b.setAttribute("aria-selected", String(b === el));
    el.scrollIntoView({ block: "nearest", inline: "nearest" });
  };

  let group;
  const showGroup = (name) => {
    group = name;
    appBar.replaceChildren();
    for (const app of apps.filter((a) => a.group === name)) app.tab = tab(appBar, app.title, () => run(app));
    appBar.appendChild(Object.assign(document.createElement("a"), { className: "kb-source", target: "_blank", textContent: "source ↗" }));
    if (groupBar) mark(groupBar, [...groupBar.children][groups.indexOf(name)]);
  };
  const run = (app) => {
    if (app.group !== group) showGroup(app.group);
    mark(appBar, app.tab);
    appBar.querySelector(".kb-source").href = source + encodeURI(app.path);
    history.replaceState(null, "", `#${encodeURI(app.path)}`);
    const runner = frame.contentWindow;
    if (runner?.kivyRun) runner.kivyRun(pack, app.path);
    else frame.src = new URL(`runner/?pack=${pack}&app=${encodeURIComponent(app.path)}`, site);
  };

  for (const name of groups) tab(groupBar, name, () => run(apps.find((a) => a.group === name)));
  const wanted = decodeURI(location.hash.slice(1));
  run(apps.find((a) => a.path === wanted) ?? apps[0]);
}
