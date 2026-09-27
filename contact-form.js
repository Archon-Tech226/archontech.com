(function () {
  "use strict";
  var form = document.getElementById("contact-form");
  var status = document.getElementById("form-status");
  if (!form || !status) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Honeypot: if this hidden field got filled in, silently drop the submission
    if (form.company && form.company.value) return;

    if (form.action.indexOf("REPLACE_WITH_FORM_ID") !== -1) {
      status.dataset.state = "error";
      status.textContent = "The contact form isn't connected yet — please email founder.archon@gmail.com directly for now.";
      return;
    }

    var data = new FormData(form);
    status.dataset.state = "";
    status.textContent = "Sending\u2026";

    fetch(form.action, {
      method: "POST",
      body: data,
      headers: { Accept: "application/json" },
    })
      .then(function (res) {
        if (res.ok) {
          status.dataset.state = "ok";
          status.textContent = "Thanks — your message is on its way. We'll get back to you soon.";
          form.reset();
        } else {
          status.dataset.state = "error";
          status.textContent = "Something went wrong. Please try again or email founder.archon@gmail.com.";
        }
      })
      .catch(function () {
        status.dataset.state = "error";
        status.textContent = "Something went wrong. Please try again or email founder.archon@gmail.com.";
      });
  });
})();
