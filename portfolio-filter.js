(function () {
  "use strict";
  var buttons = document.querySelectorAll(".filter-btn");
  var cards = document.querySelectorAll(".project-card");
  if (!buttons.length) return;

  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      buttons.forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
      btn.setAttribute("aria-pressed", "true");
      var filter = btn.dataset.filter;
      cards.forEach(function (card) {
        var show = filter === "all" || card.dataset.type === filter;
        card.hidden = !show;
      });
    });
  });
})();
