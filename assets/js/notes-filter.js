"use strict";

const filters = document.querySelector(".notes-filters");
const groups = document.querySelectorAll("[data-note-group]");
const topic = filters.querySelector('[name="topic"]');
const language = filters.querySelector('[name="language"]');
const query = filters.querySelector('[name="query"]');
const status = filters.querySelector('[role="status"]');

function normalize(text) {
  return text.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase().trim();
}

const archive = Array.from(groups, (group) => ({
  group,
  entries: Array.from(group.querySelectorAll("[data-topic]"), (entry) => ({
    entry,
    text: normalize(entry.querySelector(".entry__title").textContent + " " +
      entry.querySelector(".entry__dek").textContent),
  })),
}));

function updateArchive() {
  const search = normalize(query.value);
  let total = 0;

  for (const { group, entries } of archive) {
    let visible = 0;
    for (const { entry, text } of entries) {
      const languages = (entry.dataset.lang || "").split(/\s+/).filter(Boolean);
      const matches = (!topic.value || entry.dataset.topic === topic.value) &&
        (!language.value || languages.includes(language.value)) &&
        text.includes(search);
      entry.hidden = !matches;
      if (matches) visible += 1;
    }
    group.hidden = visible === 0;
    total += visible;
  }

  status.textContent = total ? `${status.dataset.count} · ${total}` : status.dataset.empty;
}

topic.addEventListener("change", updateArchive);
language.addEventListener("change", updateArchive);
query.addEventListener("input", updateArchive);
updateArchive();
filters.hidden = false;
