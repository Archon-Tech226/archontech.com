(function () {
  "use strict";
  var root = document.getElementById("live-dash");
  if (!root || !root.dataset.calUrl) return;
  var calUrl = root.dataset.calUrl, dayUrl = root.dataset.dayUrl, statusUrl = root.dataset.statusUrl, csrf = root.dataset.csrf;
  var now = new Date(), cur = { y: now.getFullYear(), m: now.getMonth() + 1 }, selected = null;
  var STATUSES = ["new", "contacted", "quoted", "won", "lost"];
  var LABELS = { new: "New", contacted: "Contacted", quoted: "Quoted", won: "Won", lost: "Lost" };
  function $(id) { return document.getElementById(id); }
  function el(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function iso(d) { return cur.y + "-" + pad(cur.m) + "-" + pad(d); }

  function loadMonth() {
    fetch(calUrl + "?month=" + cur.y + "-" + pad(cur.m), { credentials: "same-origin" })
      .then(function (r) { return r.json(); }).then(function (d) {
        $("cal-label").textContent = d.label;
        var grid = $("cal-days"); grid.textContent = "";
        for (var i = 0; i < d.first_weekday; i++) { var e = el("div", "cal-cell empty"); e.setAttribute("aria-hidden", "true"); grid.appendChild(e); }
        for (var day = 1; day <= d.days_in_month; day++) {
          (function (day) {
            var info = d.days[String(day)] || { leads: 0, followups: 0 };
            var b = el("button", "cal-cell" + (info.leads ? " has-lead" : "") + (d.today === day ? " today" : "") + (selected === iso(day) ? " selected" : ""));
            b.type = "button"; b.setAttribute("aria-pressed", String(selected === iso(day)));
            b.setAttribute("aria-label", day + " " + d.label + ": " + info.leads + " enquiries, " + info.followups + " follow-ups due");
            b.appendChild(el("span", "", String(day)));
            var badges = el("span", "cal-badges");
            if (info.leads) badges.appendChild(el("span", "cal-badge cal-badge--lead", String(info.leads)));
            if (info.followups) badges.appendChild(el("span", "cal-badge cal-badge--fu", "⏰" + info.followups));
            b.appendChild(badges);
            b.addEventListener("click", function () { selected = iso(day); loadMonthSelectionOnly(); loadDay(selected); });
            grid.appendChild(b);
          })(day);
        }
      });
  }
  function loadMonthSelectionOnly() {
    document.querySelectorAll("#cal-days .cal-cell").forEach(function (c) { c.classList.remove("selected"); c.setAttribute("aria-pressed", "false"); });
    var n = selected ? parseInt(selected.slice(-2), 10) : 0;
    var cells = document.querySelectorAll("#cal-days .cal-cell:not(.empty)");
    if (cells[n - 1]) { cells[n - 1].classList.add("selected"); cells[n - 1].setAttribute("aria-pressed", "true"); }
  }

  function setStatus(id, status, name, date) {
    fetch(statusUrl, { method: "POST", credentials: "same-origin",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrf }, body: JSON.stringify({ id: id, status: status }) })
      .then(function (r) { return r.json(); }).then(function (d) {
        if (!d.ok) throw new Error(); var t = $("ld-toast"); t.textContent = name + " marked " + d.label; t.className = "ld-toast show";
        setTimeout(function () { t.className = "ld-toast"; }, 2400); loadDay(date);
      });
  }
  function loadDay(date) {
    fetch(dayUrl + "?date=" + date, { credentials: "same-origin" }).then(function (r) { return r.json(); }).then(function (d) {
      $("cal-day-title").textContent = d.label;
      var ul = $("cal-day-list"); ul.textContent = "";
      $("cal-day-hint").textContent = d.items.length ? d.items.length + " item" + (d.items.length > 1 ? "s" : "") + " on this day." : "Nothing on this day.";
      d.items.forEach(function (l) {
        var li = el("li"), top = el("div", "ld-row-top"), a = el("a", "", l.name); a.href = l.url; top.appendChild(a);
        top.appendChild(el("span", "ld-tag", l.kind)); li.appendChild(top);
        li.appendChild(el("div", "ld-meta", l.email + (l.service ? " · " + l.service : "") + (l.kind === "enquiry" ? " · " + l.time : "")));
        var acts = el("div", "ld-row-actions");
        STATUSES.forEach(function (st) {
          var b = el("button", "ld-chip", LABELS[st]); b.type = "button"; b.setAttribute("aria-pressed", String(l.status === st));
          b.addEventListener("click", function () { setStatus(l.id, st, l.name, d.date); }); acts.appendChild(b);
        });
        li.appendChild(acts); ul.appendChild(li);
      });
      var open = $("cal-day-open"); open.href = d.list_url; open.hidden = !d.items.length;
    });
  }
  function shift(n) { cur.m += n; if (cur.m < 1) { cur.m = 12; cur.y--; } if (cur.m > 12) { cur.m = 1; cur.y++; } loadMonth(); }
  $("cal-prev").addEventListener("click", function () { shift(-1); });
  $("cal-next").addEventListener("click", function () { shift(1); });
  $("cal-today").addEventListener("click", function () {
    var t = new Date(); cur = { y: t.getFullYear(), m: t.getMonth() + 1 }; selected = iso(t.getDate()); loadMonth(); loadDay(selected);
  });
  setInterval(function () { if (!document.hidden) loadMonth(); }, 30000);
  var t0 = new Date(); selected = iso(t0.getDate()); loadMonth(); loadDay(selected);
})();
