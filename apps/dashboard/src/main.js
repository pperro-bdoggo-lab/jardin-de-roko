const $ = (id) => document.getElementById(id);

const status = (message, isError = false) => {
  $("status").textContent = message;
  $("status").classList.toggle("error", isError);
};

const setText = (id, value) => {
  $(id).textContent = value === undefined || value === null ? "—" : String(value);
};

const format = (value) =>
  typeof value === "number" && Number.isFinite(value) ? value.toFixed(3) : String(value ?? "—");

const fillList = (id, items, render = (item) => String(item)) => {
  const target = $(id);
  target.replaceChildren();
  if (!items || items.length === 0) {
    const li = document.createElement("li");
    li.textContent = "sin datos";
    target.append(li);
    return;
  }
  for (const item of items) {
    const li = document.createElement("li");
    li.textContent = render(item);
    target.append(li);
  }
};

const fillKV = (id, entries) => {
  const target = $(id);
  target.replaceChildren();
  for (const [key, value] of entries) {
    const dt = document.createElement("dt");
    dt.textContent = key;
    const dd = document.createElement("dd");
    dd.textContent = value === undefined || value === null ? "—" : String(value);
    target.append(dt, dd);
  }
};

const renderBars = (lenses) => {
  const target = $("ecro-lenses");
  target.replaceChildren();
  for (const [name, value] of Object.entries(lenses ?? {})) {
    const row = document.createElement("div");
    row.className = "bar";

    const label = document.createElement("span");
    label.textContent = name;

    const track = document.createElement("div");
    track.className = "bar-track";
    const fill = document.createElement("div");
    fill.className = "bar-fill";
    fill.style.width = `${Math.max(0, Math.min(100, Number(value) * 100))}%`;
    track.append(fill);

    const number = document.createElement("span");
    number.textContent = format(value);

    row.append(label, track, number);
    target.append(row);
  }
};

const renderCandidates = (deliberation) => {
  const target = $("candidates");
  target.replaceChildren();
  setText("selected-candidate", `Seleccionado: ${deliberation?.selected ?? "—"}`);

  for (const candidate of deliberation?.candidates ?? []) {
    const card = document.createElement("article");
    card.className = "candidate";
    if (candidate.name === deliberation?.selected) {
      card.classList.add("selected");
    }

    const head = document.createElement("header");
    const title = document.createElement("h3");
    title.textContent = candidate.name;
    const score = document.createElement("span");
    score.className = "score";
    score.textContent = `score ${format(candidate.score)}`;
    head.append(title, score);

    const rationale = document.createElement("p");
    rationale.textContent = candidate.rationale ?? "";

    const text = document.createElement("p");
    text.textContent = candidate.generation?.text ?? "(sin generación)";

    const route = document.createElement("span");
    route.className = "badge";
    route.textContent = candidate.generation?.route ?? "—";

    card.append(head, rationale, text, route);
    target.append(card);
  }
};

const renderTrace = (trace) => {
  $("app").hidden = false;

  setText("request-prompt", trace.request?.prompt);
  setText("trace-id", trace.trace_id);
  setText("schema-version", trace.schema_version);
  setText("route", trace.route);
  setText("blocked", trace.blocked ? "sí" : "no");

  setText("safety-status", trace.safety?.status);
  fillList("safety-reasons", trace.safety?.reasons, (item) => item);

  setText("affect-label", trace.affect?.label);
  setText("affect-valence", format(trace.affect?.valence));
  setText("affect-arousal", format(trace.affect?.arousal));
  setText("affect-tension", format(trace.affect?.tension));

  setText("verdict-status", trace.verdict?.status);
  fillList("verdict-reasons", trace.verdict?.reasons, (item) => item);

  setText("regime", trace.impact?.regime);
  fillKV("impact-metrics", [
    ["wellbeing", format(trace.impact?.wellbeing)],
    ["gini", format(trace.impact?.gini)],
    ["infrapower", format(trace.impact?.infrapower)],
    ["stability", format(trace.impact?.stability)],
    ["huella ecológica", format(trace.impact?.ecological_footprint)],
  ]);

  setText("ecro-description", trace.ecro?.description);
  renderBars(trace.ecro?.lenses);

  fillKV("complex-state", [
    ["real", format(trace.complex_state?.real)],
    ["imag", format(trace.complex_state?.imag)],
    ["módulo", format(trace.complex_state?.modulus)],
    ["fase", format(trace.complex_state?.phase)],
    ["colapso |z|²", format(trace.complex_state?.collapsed)],
    ["is_collapsed", trace.complex_state?.is_collapsed],
  ]);

  renderCandidates(trace.deliberation);
  fillList(
    "memories",
    trace.memories,
    (item) => `${format(item.score)} · ${item.text}`,
  );
  fillKV(
    "timings",
    Object.entries(trace.timings ?? {}).map(([key, value]) => [key, `${format(value)} ms`]),
  );

  status(`Traza ${trace.trace_id} cargada.`);
};

const parseAndRender = (raw, source) => {
  try {
    const trace = JSON.parse(raw);
    renderTrace(trace);
    status(`Cargada desde ${source}.`);
  } catch (error) {
    status(`JSON inválido: ${error.message}`, true);
  }
};

$("file").addEventListener("change", (event) => {
  const file = event.target.files?.[0];
  if (!file) return;
  const reader = new FileReader();
  reader.addEventListener("load", () => parseAndRender(String(reader.result), file.name));
  reader.addEventListener("error", () => status("No se pudo leer el archivo.", true));
  reader.readAsText(file);
});

$("fetch").addEventListener("click", async () => {
  try {
    const response = await fetch("trace.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    parseAndRender(await response.text(), "trace.json");
  } catch (error) {
    status(
      `No se encontró trace.json junto al dashboard (${error.message}). Usa el selector de archivo.`,
      true,
    );
  }
});

$("clear").addEventListener("click", () => {
  $("app").hidden = true;
  $("file").value = "";
  status("Esperando una traza.");
});
