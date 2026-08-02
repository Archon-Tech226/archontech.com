// Mobile nav toggle
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('open');
    hamburger.setAttribute('aria-expanded', String(isOpen));
  });
  navLinks.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => navLinks.classList.remove('open'));
  });
}

// Contact form -> builds a WhatsApp message from the filled fields
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const status = document.getElementById('formStatus');
    const name = document.getElementById('cf-name').value.trim();
    const phone = document.getElementById('cf-phone').value.trim();
    const email = document.getElementById('cf-email').value.trim();
    const service = document.getElementById('cf-service').value;
    const message = document.getElementById('cf-message').value.trim();

    if (!name || !phone || !message) {
      status.textContent = 'Please fill in your name, phone number, and message.';
      status.className = 'err';
      return;
    }

    const lines = [
      `Hi, I'm ${name}.`,
      service ? `Service needed: ${service}` : null,
      email ? `Email: ${email}` : null,
      `Message: ${message}`
    ].filter(Boolean);

    const text = encodeURIComponent(lines.join('\n'));
    status.textContent = 'Opening WhatsApp with your message...';
    status.className = 'ok';
    window.open(`https://wa.me/918056394297?text=${text}`, '_blank');
  });
}
