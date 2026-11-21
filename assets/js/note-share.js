"use strict";

const share = document.querySelector(".note-share");
const copy = share.querySelector("[data-copy-link]");
const status = share.querySelector('[role="status"]');
const fallback = share.querySelector("input");
const url = document.querySelector('link[rel="canonical"]').href;

copy.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(url);
    status.textContent = copy.dataset.copied;
    fallback.hidden = true;
  } catch {
    status.textContent = "";
    fallback.value = url;
    fallback.hidden = false;
    fallback.focus();
    fallback.select();
  }
});

share.hidden = false;
