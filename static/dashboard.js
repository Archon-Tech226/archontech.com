(function () {
  "use strict";

  var toggle = document.getElementById("sidebar-toggle");
  var sidebar = document.getElementById("dash-sidebar");
  if (toggle && sidebar) {
    toggle.addEventListener("click", function () {
      sidebar.classList.toggle("is-open");
    });
    document.addEventListener("click", function (e) {
      if (window.innerWidth > 860) return;
      if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
        sidebar.classList.remove("is-open");
      }
    });
  }

  // Auto-dismiss toasts after a few seconds
  document.querySelectorAll(".toast").forEach(function (toast, i) {
    setTimeout(function () {
      toast.style.transition = "opacity 0.3s";
      toast.style.opacity = "0";
      setTimeout(function () { toast.remove(); }, 300);
    }, 3500 + i * 300);
  });
})();
