/* Read-only fictional records transcribed from the linked PDF exports.
   No clinical calculations, persistence or network calls. */
(() => {
  "use strict";
  const source = document.getElementById("vitachart-samples");
  const timeline = document.getElementById("timelineStrip");
  if (!source || !timeline) return;
  const samples = JSON.parse(source.textContent);
  let current = samples["28"];
  let selected = 14;
  let buttons = [];
  const title = document.getElementById("selectedDayTitle");
  const summary = document.getElementById("selectedDaySummary");
  const previous = document.getElementById("previous-day");
  const next = document.getElementById("next-day");
  const formatDate = iso => new Intl.DateTimeFormat("en-GB", {day:"numeric", month:"short", year:"numeric", timeZone:"UTC"}).format(new Date(iso + "T12:00:00Z"));

  function selectDay(index, focusDay = false, revealRecord = false) {
    selected = Math.max(0, Math.min(index, current.days.length - 1));
    const day = current.days[selected];
    buttons.forEach((button, i) => {
      button.setAttribute("aria-pressed", String(i === selected));
      button.tabIndex = i === selected ? 0 : -1;
    });
    const values = {
      code: day.code || "No sign observation",
      temperature: day.temperature + " °C",
      observed: day.observed ? "Recorded" : "Not recorded; temperature only",
      marker: day.marker ? (day.marker === "P" ? "P (for review)" : "P + " + day.marker + " (example)") : "None in this example",
      question: day.question || "None in this example",
      medication: day.medication || "None in this example",
      note: day.note || "None in this example"
    };
    document.querySelectorAll("#deckGrid [data-field]").forEach(field => {
      field.textContent = values[field.dataset.field];
    });
    title.textContent = "Day " + day.day + " · " + formatDate(day.date);
    summary.textContent = "Fictional day " + day.day + ": " + values.code + ", " + values.temperature + "." +
      (day.marker ? " Report annotation: " + values.marker + "." : "") +
      (day.question ? " Includes a question for consultation." : "") +
      (day.medication ? " Includes a medication note." : "");
    previous.disabled = selected === 0;
    next.disabled = selected === current.days.length - 1;
    if (focusDay) buttons[selected].focus();
    if (revealRecord) {
      document.querySelector(".demo-observations").scrollIntoView({behavior: "instant", block: "start"});
      title.focus({preventScroll: true});
    }
  }

  function createDay(day, index) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "demo-day";
    button.dataset.day = day.day;
    button.setAttribute("aria-controls", "deckGrid");
    button.setAttribute("aria-label", `Day ${day.day}, ${formatDate(day.date)}, ${day.code || "no sign observation"}`);
    const number = document.createElement("span");
    number.className = "demo-day-number";
    number.textContent = day.day;
    const date = document.createElement("small");
    date.textContent = day.shortDate;
    number.append(date);
    const stamp = document.createElement("span");
    stamp.className = "demo-stamp demo-stamp--" + day.stamp;
    stamp.setAttribute("aria-hidden", "true");
    stamp.textContent = day.marker || (day.question ? "?" : "");
    const code = document.createElement("span");
    code.className = "demo-code";
    code.textContent = day.code || "Not recorded";
    const temperature = document.createElement("span");
    temperature.className = "demo-temperature";
    temperature.textContent = day.temperature + " °C";
    button.append(number, stamp, code, temperature);
    button.addEventListener("click", () => selectDay(index, false, true));
    button.addEventListener("keydown", event => {
      const columns = getComputedStyle(timeline).gridTemplateColumns.split(" ").length;
      const targets = {
        ArrowRight: Math.min(index + 1, current.days.length - 1),
        ArrowLeft: Math.max(index - 1, 0),
        ArrowDown: Math.min(index + columns, current.days.length - 1),
        ArrowUp: Math.max(index - columns, 0),
        Home: 0,
        End: current.days.length - 1
      };
      if (!(event.key in targets)) return;
      event.preventDefault();
      selectDay(targets[event.key], true);
    });
    return button;
  }

  function selectCycle(length) {
    current = samples[String(length)];
    const fragment = document.createDocumentFragment();
    buttons = current.days.map((day, index) => {
      const button = createDay(day, index);
      fragment.append(button);
      return button;
    });
    timeline.replaceChildren(fragment);
    document.querySelectorAll("[data-cycle]").forEach(button => {
      button.setAttribute("aria-pressed", String(button.dataset.cycle === String(length)));
    });
    document.getElementById("cycle-dates").textContent = formatDate(current.start) + " – " + formatDate(current.end);
    document.getElementById("cycle-length").textContent = current.length + " days";
    document.getElementById("cycle-recorded").textContent = current.recorded + " of " + current.length;
    document.getElementById("report-preview-link").href = current.pdf;
    const preview = document.getElementById("report-preview");
    preview.src = current.preview;
    preview.alt = `VitaChart sample report in Portuguese: ${current.length} fictional days, page 1 of ${current.pages}.`;
    document.getElementById("report-caption").textContent = `${current.length}-day example · Page 1 of ${current.pages} · Report in Portuguese · Select the preview to open the PDF.`;
    selectDay(Math.min(selected, current.days.length - 1));
  }

  document.querySelectorAll("[data-cycle]").forEach(button => button.addEventListener("click", () => selectCycle(button.dataset.cycle)));
  document.querySelectorAll("[data-select-day]").forEach(button => button.addEventListener("click", () => selectDay(Number(button.dataset.selectDay) - 1, false, true)));
  previous.addEventListener("click", () => selectDay(selected - 1));
  next.addEventListener("click", () => selectDay(selected + 1));
  selectCycle(28);
  document.querySelectorAll(".demo-cycle-picker, .demo-highlights, .demo-day-controls").forEach(element => { element.hidden = false; });
  if (new URLSearchParams(window.location.search).get("demo") === "1" && !window.location.hash) {
    const showDemo = () => requestAnimationFrame(() => {
      document.getElementById("demo-title").focus({preventScroll: true});
      document.getElementById("demo").scrollIntoView({behavior: "instant", block: "start"});
    });
    if (document.readyState === "complete") showDemo();
    else window.addEventListener("load", showDemo, {once: true});
  }
})();
