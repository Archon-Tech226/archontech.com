(function () {
  "use strict";

  var header = document.querySelector(".site-header");
  var menuBtn = document.querySelector(".menu-btn");
  var nav = document.getElementById("site-nav");

  // Header gains a shadow once the page scrolls
  function onScroll() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 8);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Mobile menu
  function setMenu(open) {
    if (!menuBtn || !nav) return;
    menuBtn.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("is-open", open);
  }

  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      setMenu(menuBtn.getAttribute("aria-expanded") !== "true");
    });

    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setMenu(false);
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        setMenu(false);
        menuBtn.focus();
      }
    });

    window.matchMedia("(min-width: 861px)").addEventListener("change", function (e) {
      if (e.matches) setMenu(false);
    });
  }

  // Footer year
  var year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
})();
