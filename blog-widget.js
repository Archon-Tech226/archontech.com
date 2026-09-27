// Archon Tech — footer widget for "Behind the Build"
// Shows the most recent posts in the footer on any page that includes this script.

import { watchPosts, initials, formatWhen } from "./blog-data.js";

const mount = document.getElementById("footer-posts");
if (mount) {
  const max = Number(mount.dataset.limit || 2);

  function render(posts, state) {
    if (state === "unconfigured") {
      mount.innerHTML = '<p class="empty-note">Notes are coming soon.</p>';
      return;
    }
    if (state === "error") {
      mount.innerHTML = '<p class="empty-note">Couldn\u2019t load notes right now.</p>';
      return;
    }
    if (!posts.length) {
      mount.innerHTML = '<p class="empty-note">No notes yet. Check back soon.</p>';
      return;
    }
    mount.innerHTML = posts
      .map(
        (p) => `
      <article class="post">
        <div class="post-head">
          <span class="avatar" aria-hidden="true">${initials(p.author)}</span>
          <span class="who">${escapeHtml(p.author || "Team")}</span>
          <span class="when">${formatWhen(p.createdAt)}</span>
        </div>
        <p class="post-body">${escapeHtml(p.body || "")}</p>
      </article>`
      )
      .join("");
  }

  function escapeHtml(s) {
    const d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  watchPosts(max, render);
}
