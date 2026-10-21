(function () {
  "use strict";
  var root = document.getElementById("live-dash");
  if (!root) return;
  var statsUrl = root.dataset.statsUrl, statusUrl = root.dataset.statusUrl, csrf = root.dataset.csrf;
  var days = 14, paused = false, timer = null, first = true, seen = {}, INTERVAL = 8000;
  var STATUSES = ["new", "contacted", "quoted", "won", "lost"];
  var LABELS = { new: "New", contacted: "Contacted", quoted: "Quoted", won: "Won", lost: "Lost" };

  function $(s, r) { return (r || root).querySelector(s); }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }

  function toast(msg, isErr) {
    var t = document.getElementById("ld-toast");
    t.textContent = msg; t.className = "ld-toast show" + (isErr ? " err" : "");
    clearTimeout(toast._t); toast._t = setTimeout(function () { t.className = "ld-toast"; }, 2600);
  }
  function setState(ok, text) {
    $("#ld-dot").className = "ld-dot " + (ok ? "on" : "err");
    $("#ld-state").textContent = text;
  }

  function renderCards(c) {
    root.querySelectorAll("[data-card]").forEach(function (n) {
      var v = String(c[n.dataset.card]);
      if (n.textContent !== v) {
        var wasNum = n.textContent !== "–";
        n.textContent = v;
        if (wasNum) { n.classList.remove("bump"); void n.offsetWidth; n.classList.add("bump"); }
      }
    });
    $("#ld-drafts").textContent = c.posts_draft ? "(" + c.posts_draft + " draft" + (c.posts_draft > 1 ? "s" : "") + ")" : "";
  }

  function renderChart(series) {
    var box = $("#ld-chart"), max = Math.max.apply(null, series.map(function (s) { return s.count; }).concat([1]));
    box.textContent = "";
    series.forEach(function (s) {
      var b = el("div", "ld-bar"); b.style.height = Math.max(2, (s.count / max) * 100) + "%";
      b.dataset.tip = s.label + ": " + s.count; b.tabIndex = 0;
      b.setAttribute("aria-label", s.label + ": " + s.count + " leads");
      box.appendChild(b);
    });
  }

  function renderPipeline(counts, labels) {
    var box = $("#ld-pipeline"); box.textContent = "";
    STATUSES.forEach(function (k) { box.appendChild(el("span", "ld-pill st-" + k, labels[k] + " " + (counts[k] || 0))); });
  }

  function renderRecent(list) {
    var ul = $("#ld-recent"); ul.textContent = "";
    $("#ld-empty").hidden = list.length > 0;
    list.forEach(function (l) {
      var isNew = !first && !seen[l.id];
      var li = el("li", isNew ? "fresh" : "");
      var top = el("div", "ld-row-top");
      var a = el("a", "", l.name); a.href = l.url; top.appendChild(a);
      top.appendChild(el("span", "ld-meta", l.created));
      li.appendChild(top);
      li.appendChild(el("div", "ld-meta", l.email + (l.service ? " · " + l.service : "")));
      var acts = el("div", "ld-row-actions");
      STATUSES.forEach(function (st) {
        var b = el("button", "ld-chip", LABELS[st]); b.type = "button";
        b.setAttribute("aria-pressed", String(l.status === st));
        b.addEventListener("click", function () { setStatus(l.id, st, l.name); });
        acts.appendChild(b);
      });
      var mail = el("a", "ld-chip", "Reply"); mail.href = "mailto:" + l.email; mail.style.textDecoration = "none";
      acts.appendChild(mail);
      li.appendChild(acts); ul.appendChild(li);
      if (isNew) toast("New enquiry from " + l.name);
      seen[l.id] = true;
    });
  }

  function load() {
    return fetch(statsUrl + "?days=" + days, { credentials: "same-origin", headers: { "Accept": "application/json" } })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) {
        renderCards(d.cards); renderChart(d.series); renderPipeline(d.status_counts, d.status_labels); renderRecent(d.recent);
        first = false;
        setState(true, paused ? "Paused" : "Live, updates every 8s");
        $("#ld-time").textContent = "· last updated " + d.server_time;
      })
      .catch(function () { setState(false, "Connection lost, retrying…"); });
  }

  function setStatus(id, status, name) {
    fetch(statusUrl, {
      method: "POST", credentials: "same-origin",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
      body: JSON.stringify({ id: id, status: status })
    }).then(function (r) { return r.json(); }).then(function (d) {
      if (!d.ok) throw new Error(d.error);
      toast(name + " marked " + d.label); load();
    }).catch(function () { toast("Could not update the lead", true); });
  }

  function schedule() { clearInterval(timer); if (!paused) timer = setInterval(function () { if (!document.hidden) load(); }, INTERVAL); }

  root.querySelectorAll(".ld-seg button").forEach(function (b) {
    b.addEventListener("click", function () {
      days = parseInt(b.dataset.days, 10);
      root.querySelectorAll(".ld-seg button").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      load();
    });
  });
  $("#ld-pause").addEventListener("click", function () {
    paused = !paused; this.setAttribute("aria-pressed", String(paused));
    this.textContent = paused ? "Resume live updates" : "Pause live updates";
    setState(true, paused ? "Paused" : "Live, updates every 8s"); schedule();
  });
  $("#ld-refresh").addEventListener("click", function () { load().then(function () { toast("Refreshed"); }); });
  document.addEventListener("visibilitychange", function () { if (!document.hidden && !paused) load(); });

  load(); schedule();
})();
