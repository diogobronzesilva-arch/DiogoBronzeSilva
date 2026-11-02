/* Same-origin controls for the real VitaChart demonstration. No analytics or clinical calculations. */
(() => {
  "use strict";
  const frame = document.getElementById("vitachart-live-demo");
  if (!frame) return;
  const tabs = ["today", "dayLog", "chart", "settings"];
  const methods = ["CREIGHTON", "BILLINGS"];
  const languages = ["pt", "en", "es", "fr"];
  const buttons = [...document.querySelectorAll("[data-demo-tab]")];
  const method = document.getElementById("demo-method");
  const language = document.getElementById("demo-language");
  const fullscreen = document.querySelectorAll("[data-demo-fullscreen]");
  let state = { tab: "today", method: "CREIGHTON", lang: "en" };
  let connected = false;

  function paint() {
    buttons.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.demoTab === state.tab)));
    method.value = state.method;
    language.value = state.lang;
    fullscreen.forEach(link => {
      const url = new URL(frame.getAttribute("src"), window.location.origin);
      url.searchParams.set("demo", "1");
      url.searchParams.set("tab", state.tab);
      url.searchParams.set("method", state.method);
      url.searchParams.set("lang", state.lang);
      link.href = url.pathname + url.search;
    });
  }

  function send() {
    if (connected) frame.contentWindow.postMessage({ type: "VITACHART_NAVIGATE", ...state, report: false }, window.location.origin);
  }

  function choose(patch) {
    state = { ...state, ...patch };
    paint();
    send();
  }

  buttons.forEach(button => button.addEventListener("click", () => choose({ tab: button.dataset.demoTab })));
  method.addEventListener("change", () => { if (methods.includes(method.value)) choose({ method: method.value }); });
  language.addEventListener("change", () => { if (languages.includes(language.value)) choose({ lang: language.value }); });

  window.addEventListener("message", event => {
    if (event.origin !== window.location.origin || event.source !== frame.contentWindow) return;
    const value = event.data;
    if (!value || value.type !== "VITACHART_DEMO_STATE") return;
    if (!connected) {
      // Apply any choice made before the application finished loading.
      connected = true;
      send();
      return;
    }
    if (tabs.includes(value.tab)) state.tab = value.tab;
    if (methods.includes(value.method)) state.method = value.method;
    if (languages.includes(value.lang)) state.lang = value.lang;
    paint();
  });
  paint();
})();
