/* Fictional display data only. No calculations, storage or network requests. */
(() => {
  "use strict";
  const days = [
  {
    "day": 1,
    "stamp": "red",
    "code": "H",
    "desc": "Heavy flow",
    "sensation": "Wet",
    "mucus": "None (Menses)",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 2,
    "stamp": "red",
    "code": "H",
    "desc": "Heavy flow",
    "sensation": "Wet",
    "mucus": "None (Menses)",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 3,
    "stamp": "red",
    "code": "M",
    "desc": "Moderate flow",
    "sensation": "Damp",
    "mucus": "None (Menses)",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 4,
    "stamp": "red",
    "code": "L",
    "desc": "Light flow",
    "sensation": "Damp",
    "mucus": "None (Menses)",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 5,
    "stamp": "red",
    "code": "VL",
    "desc": "Very light / spotting",
    "sensation": "Dry",
    "mucus": "None (Menses)",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 6,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": true,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 7,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 8,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": true,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 9,
    "stamp": "green",
    "code": "2X1",
    "desc": "Dry, single observation",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 10,
    "stamp": "white",
    "code": "4",
    "desc": "Damp, cloudy discharge",
    "sensation": "Damp",
    "mucus": "Thick, cloudy",
    "stretch": "< 0.5 cm",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 11,
    "stamp": "white",
    "code": "6C",
    "desc": "Damp, cloudy mucus",
    "sensation": "Damp",
    "mucus": "Cloudy",
    "stretch": "1.0 cm",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 12,
    "stamp": "white",
    "code": "8CX1",
    "desc": "Wet, stretchy mucus",
    "sensation": "Wet",
    "mucus": "Cloudy / clear",
    "stretch": "2.0 cm",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 13,
    "stamp": "white",
    "code": "10K",
    "desc": "Lubricative, clear",
    "sensation": "Lubricative",
    "mucus": "Clear, transparent",
    "stretch": "> 2.5 cm",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 14,
    "stamp": "peak",
    "code": "10KL",
    "desc": "Clear, stretchy, lubricative",
    "sensation": "Lubricative",
    "mucus": "Clear, highly elastic",
    "stretch": "> 5.0 cm",
    "intimacy": false,
    "peak": "P (example annotation)",
    "postPeak": "Not recorded"
  },
  {
    "day": 15,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation · Example P+1",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "P + 1"
  },
  {
    "day": 16,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation · Example P+2",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "P + 2"
  },
  {
    "day": 17,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation · Example P+3",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "P + 3"
  },
  {
    "day": 18,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": true,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 19,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 20,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": true,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 21,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 22,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 23,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": true,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 24,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 25,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 26,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 27,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  },
  {
    "day": 28,
    "stamp": "green",
    "code": "2",
    "desc": "Dry sensation",
    "sensation": "Dry",
    "mucus": "None",
    "stretch": "None",
    "intimacy": false,
    "peak": "Not marked in this example",
    "postPeak": "Not recorded"
  }
];
  const timeline = document.getElementById("timelineStrip");
  const title = document.getElementById("selectedDayTitle");
  const summary = document.getElementById("selectedDaySummary");
  if (!timeline || !title || !summary) return;

  const buttons = [];
  function selectDay(index, moveFocus = false) {
    const day = days[index];
    buttons.forEach((button, i) => {
      button.setAttribute("aria-pressed", String(i === index));
      button.tabIndex = i === index ? 0 : -1;
    });
    title.textContent = `Day ${day.day} observations (${day.code})`;
    const values = {
      ...day,
      bleeding: day.stamp === "red" ? day.desc : "None",
      intimacy: day.intimacy ? "Yes (I)" : "No"
    };
    document.querySelectorAll("[data-field]").forEach(field => {
      field.textContent = values[field.dataset.field];
    });
    summary.textContent = `Fictional day ${day.day}: ${day.desc}. Code ${day.code}.` +
      (day.day === 14 ? " P is an example annotation." : "");
    if (moveFocus) buttons[index].focus();
  }

  days.forEach((day, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "demo-day";
    button.setAttribute("aria-label", `Day ${day.day}, example code ${day.code}`);
    button.setAttribute("aria-controls", "deckGrid");
    const number = document.createElement("span");
    number.textContent = day.day;
    const stamp = document.createElement("span");
    stamp.className = `demo-stamp demo-stamp--${day.stamp}`;
    stamp.setAttribute("aria-hidden", "true");
    stamp.textContent = day.stamp === "peak" ? "P" : "";
    const code = document.createElement("span");
    code.className = "demo-code";
    code.textContent = day.code;
    button.append(number, stamp, code);
    button.addEventListener("click", () => selectDay(index));
    button.addEventListener("keydown", event => {
      const columns = getComputedStyle(timeline).gridTemplateColumns.split(" ").length;
      const targets = {
        ArrowRight: (index + 1) % days.length,
        ArrowLeft: (index - 1 + days.length) % days.length,
        ArrowDown: Math.min(index + columns, days.length - 1),
        ArrowUp: Math.max(index - columns, 0),
        Home: 0,
        End: days.length - 1
      };
      if (!(event.key in targets)) return;
      event.preventDefault();
      selectDay(targets[event.key], true);
    });
    buttons.push(button);
    timeline.append(button);
  });
  selectDay(13);
  timeline.hidden = false;
})();
