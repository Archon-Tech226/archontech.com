(function () {
  "use strict";

  // Theme toggle (the initial theme itself is set earlier, inline in <head>,
  // to avoid a flash of the wrong theme before this file loads)
  var themeBtn = document.querySelector(".theme-toggle");
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var root = document.documentElement;
      var isLight = root.getAttribute("data-theme") === "light";
      var next = isLight ? "dark" : "light";
      if (next === "dark") {
        root.removeAttribute("data-theme");
      } else {
        root.setAttribute("data-theme", "light");
      }
      try { localStorage.setItem("archon-theme", next); } catch (e) {}
      themeBtn.setAttribute("aria-pressed", String(next === "light"));
      themeBtn.setAttribute("aria-label", next === "light" ? "Switch to dark theme" : "Switch to light theme");
    });
    var startedLight = document.documentElement.getAttribute("data-theme") === "light";
    themeBtn.setAttribute("aria-pressed", String(startedLight));
    themeBtn.setAttribute("aria-label", startedLight ? "Switch to dark theme" : "Switch to light theme");
  }

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
