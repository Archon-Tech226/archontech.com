// Archon Tech — Behind the Build page logic

import {
  ready, watchAuth, login, logout, addPost, watchPosts, initials, formatWhen, MAX_POST_LENGTH,
} from "./blog-data.js";

// Map each team member's sign-in email to the name shown on their posts.
// Add a line here for each teammate you create in Firebase Authentication.
const TEAM_NAMES = {
  // "abinaya@example.com": "Abinaya Sri",
  // "nandhini@example.com": "Janaganandhini",
  // "vel@example.com": "Vel",
};

function nameFor(user) {
  if (!user) return "";
  return TEAM_NAMES[user.email] || user.email;
}

function escapeHtml(s) {
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

const authStatus = document.getElementById("auth-status");
const signinToggle = document.getElementById("signin-toggle");
const signoutBtn = document.getElementById("signout-btn");
const authPanel = document.getElementById("auth-panel");
const signinForm = document.getElementById("signin-form");
const authError = document.getElementById("auth-error");
const composer = document.getElementById("composer");
const postBody = document.getElementById("post-body");
const charCount = document.getElementById("char-count");
const postBtn = document.getElementById("post-btn");
const postStatus = document.getElementById("post-status");
const postList = document.getElementById("post-list");

let currentUser = null;

if (!ready) {
  authStatus.textContent = "Team notes aren't set up yet.";
  signinToggle.hidden = true;
}

signinToggle.addEventListener("click", function (e) {
  e.preventDefault();
  authPanel.hidden = !authPanel.hidden;
});

signinForm.addEventListener("submit", function (e) {
  e.preventDefault();
  authError.textContent = "";
  login(signinForm.email.value.trim(), signinForm.password.value)
    .then(function () {
      authPanel.hidden = true;
      signinForm.reset();
    })
    .catch(function () {
      authError.dataset.state = "error";
      authError.textContent = "Couldn't sign in. Check the email and password.";
    });
});

signoutBtn.addEventListener("click", function () {
  logout();
});

watchAuth(function (user) {
  currentUser = user;
  if (user) {
    authStatus.textContent = "Signed in as " + nameFor(user);
    signinToggle.hidden = true;
    signoutBtn.hidden = false;
    composer.hidden = false;
  } else {
    authStatus.textContent = "";
    signinToggle.hidden = false;
    signoutBtn.hidden = true;
    composer.hidden = true;
  }
});

if (postBody) {
  postBody.addEventListener("input", function () {
    charCount.textContent = postBody.value.length + " / " + MAX_POST_LENGTH;
  });
}

if (postBtn) {
  postBtn.addEventListener("click", function () {
    postStatus.textContent = "";
    if (!currentUser) {
      postStatus.dataset.state = "error";
      postStatus.textContent = "Sign in first.";
      return;
    }
    addPost(nameFor(currentUser), postBody.value)
      .then(function () {
        postBody.value = "";
        charCount.textContent = "0 / " + MAX_POST_LENGTH;
        postStatus.dataset.state = "ok";
        postStatus.textContent = "Posted.";
      })
      .catch(function (err) {
        postStatus.dataset.state = "error";
        postStatus.textContent = err.message || "Couldn't post. Try again.";
      });
  });
}

function renderPosts(posts, state) {
  if (state === "unconfigured") {
    postList.innerHTML = '<p class="empty-note">Notes are coming soon.</p>';
    return;
  }
  if (state === "error") {
    postList.innerHTML = '<p class="empty-note">Couldn\u2019t load notes right now.</p>';
    return;
  }
  if (!posts.length) {
    postList.innerHTML = '<p class="empty-note">No notes yet — check back soon.</p>';
    return;
  }
  postList.innerHTML = posts
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

watchPosts(Number(postList.dataset.limit || 30), renderPosts);
