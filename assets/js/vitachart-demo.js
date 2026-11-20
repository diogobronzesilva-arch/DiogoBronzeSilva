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
  const pageLanguages = document.querySelectorAll("[data-demo-page-language]");
  const query = new URLSearchParams(window.location.search);
  const requestedMethod = query.get("method");
  const requestedLanguage = query.get("lang");
  let state = { tab: "today", method: "CREIGHTON", lang: language.value };
  if (methods.includes(requestedMethod)) state.method = requestedMethod;
  let keepAppLanguage = languages.includes(requestedLanguage);
  if (keepAppLanguage) state.lang = requestedLanguage;
  let receivedAppState = false;

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
    pageLanguages.forEach(link => {
      const url = new URL(link.getAttribute("href"), window.location.origin);
      if (state.method === "CREIGHTON") url.searchParams.delete("method");
      else url.searchParams.set("method", state.method);
      if (keepAppLanguage) url.searchParams.set("lang", state.lang);
      link.href = url.pathname + url.search + url.hash;
    });
  }

  function send() {
    frame.contentWindow?.postMessage({ type: "VITACHART_NAVIGATE", ...state, report: false }, window.location.origin);
  }

  function choose(patch) {
    state = { ...state, ...patch };
    paint();
    send();
  }

  buttons.forEach(button => button.addEventListener("click", () => choose({ tab: button.dataset.demoTab })));
  method.addEventListener("change", () => { if (methods.includes(method.value)) choose({ method: method.value }); });
  language.addEventListener("change", () => {
    if (!languages.includes(language.value)) return;
    keepAppLanguage = true;
    choose({ lang: language.value });
  });

  // The embedded app can finish loading before this deferred script runs.
  frame.addEventListener("load", send);

  window.addEventListener("message", event => {
    if (event.origin !== window.location.origin || event.source !== frame.contentWindow) return;
    const value = event.data;
    if (!value || value.type !== "VITACHART_DEMO_STATE") return;
    if (!receivedAppState) {
      // Apply any choice made before the application finished loading.
      receivedAppState = true;
      send();
      return;
    }
    if (tabs.includes(value.tab)) state.tab = value.tab;
    if (methods.includes(value.method)) state.method = value.method;
    if (languages.includes(value.lang) && value.lang !== state.lang) {
      keepAppLanguage = true;
      state.lang = value.lang;
    }
    paint();
  });
  paint();
  send();
})();
