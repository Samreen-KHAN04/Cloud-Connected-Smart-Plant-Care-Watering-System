const ID = "plant-1", $ = s => document.querySelector(s);
const api = async (p, o) => { const r = await fetch("/api" + p, o); if (!r.ok) throw new Error((await r.json()).detail || r.status); return r.json(); };
const put = (m, b) => ({ method: m, headers: { "Content-Type": "application/json" }, body: JSON.stringify(b) });
const card = (a, b, c, pct, col) => `<div class="card"><div class="muted">${a}</div><div class="big">${b}</div>${c ? `<div class="muted">${c}</div>` : ""}${pct == null ? "" : `<div class="bar"><i style="width:${Math.max(2, Math.min(100, pct))}%;background:${col}"></i></div>`}</div>`;
const when = t => new Date(t).toLocaleString();
const pages = [["index", "Home"], ["dashboard", "Live Data"], ["watering", "Watering"], ["alerts", "Alerts"], ["help", "Help"]];
const page = document.body.dataset.page;
document.body.insertAdjacentHTML("afterbegin", "<nav><b>🌱 Smart Plant Care</b>" +
  pages.map(([p, n]) => `<a href="${p}.html" class="${p === page ? "on" : ""}">${n}</a>`).join("") + "</nav>");

function chart(rows, key, min, max, line) {
  if (rows.length < 2) return "<p class='muted'>Collecting data… check back in a few seconds.</p>";
  const X = i => 10 + i * 580 / (rows.length - 1), Y = v => 190 - (v - min) / (max - min) * 180;
  const pts = rows.map((r, i) => `${X(i)},${Y(r[key])}`).join(" ");
  return `<svg viewBox="0 0 600 200"><rect width="600" height="200" fill="none" stroke="#8886"/>
  ${line != null ? `<line x1="0" x2="600" y1="${Y(line)}" y2="${Y(line)}" stroke="#e53935" stroke-dasharray="6"/><text x="8" y="${Y(line) - 4}" font-size="13" fill="#e53935">watering level</text>` : ""}
  <polyline points="${pts}" fill="none" stroke="#2e7d32" stroke-width="3"/></svg>`;
}

const views = {
  async index() {
    const s = await api(`/devices/${ID}/summary`), l = await api(`/devices/${ID}/latest`);
    const face = { happy: "😊", thirsty: "💧", hot: "🔥", offline: "📴", waiting: "⏳" }[s.status];
    $("#hero").className = "card hero " + s.status;
    $("#hero").innerHTML = `<div class="big">${face} ${s.headline}</div><p>${s.advice}</p>`;
    $("#quick").innerHTML = l ? [card("Soil moisture", l.moisture + "%", "", l.moisture, "#1e88e5"), card("Temperature", l.temperature + " °C", "", l.temperature * 2, "#fb8c00"), card("Air humidity", l.humidity + "%", "", l.humidity, "#00acc1")].join("") : "";
  },
  async dashboard() {
    const [l, h, d] = await Promise.all([api(`/devices/${ID}/latest`), api(`/devices/${ID}/history`), api("/devices")]);
    if (!l) return;
    const light = l.light > 600 ? "Bright" : l.light > 100 ? "Dim" : "Dark (night)";
    $("#nums").innerHTML = [card("Soil moisture", l.moisture + "%", "How wet the soil is", l.moisture, "#1e88e5"), card("Temperature", l.temperature + " °C", "Air around the plant", l.temperature * 2, "#fb8c00"),
      card("Humidity", l.humidity + "%", "Moisture in the air", l.humidity, "#00acc1"), card("Light", light, l.light + " lux", l.light / 10, "#fbc02d"), card("Sensor", d[0].online ? "Online" : "Offline", "Last update " + when(l.ts))].join("");
    $("#c1").innerHTML = chart(h, "moisture", 0, 100, d[0].threshold);
    $("#c2").innerHTML = chart(h, "temperature", 10, 45);
  },
  async watering() {
    const [d, w] = await Promise.all([api("/devices"), api(`/devices/${ID}/watering-history`)]);
    if (!$("#th").dataset.set) { $("#th").value = d[0].threshold; $("#th").dataset.set = 1; }
    $("#thv").textContent = $("#th").value + "%";
    $("#wh").innerHTML = w.length ? w.map(x => `<tr><td>${when(x.ts)}</td><td>${x.kind === "automatic" ? "Automatic" : "You pressed the button"}</td><td>${x.moisture_before}%</td></tr>`).join("")
      : "<tr><td colspan=3 class='muted'>No watering yet.</td></tr>";
  },
  async alerts() {
    const a = await api("/alerts");
    $("#list").innerHTML = a.length ? a.map(x => `<div class="card al"><div>${x.acknowledged ? "✅" : "⚠️"} ${x.message}<div class="muted">${when(x.ts)}</div></div>
      ${x.acknowledged ? "" : `<button onclick="ack(${x.id})">Got it</button>`}</div>`).join("") : "<p class='muted'>No alerts. All good!</p>";
  },
  async help() {}
};
window.ack = async id => { await api(`/alerts/${id}/acknowledge`, put("PUT", {})); views.alerts(); };
window.waterNow = async () => { const r = await api(`/devices/${ID}/water`, { method: "POST" }); $("#msg").textContent = r.message; setTimeout(views.watering, 4000); };
window.saveTh = async () => { await api(`/devices/${ID}/threshold`, put("PUT", { threshold: +$("#th").value })); $("#msg").textContent = "Saved."; };
if ($("#th")) $("#th").oninput = () => $("#thv").textContent = $("#th").value + "%";
const run = () => views[page]().catch(e => { const m = $("#err"); if (m) m.textContent = "Cannot reach the server: " + e.message; });
run(); if (page !== "help") setInterval(run, 4000);
