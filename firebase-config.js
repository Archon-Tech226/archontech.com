// Archon Tech — Firebase configuration
//
// Replace the values below with the config object Firebase gives you when
// you register a web app (Project settings → General → Your apps → Web app).
// This file is loaded by every page before blog-widget.js / blog.html's script,
// so it only needs to be edited in one place.

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.13.0/firebase-app.js";

export const firebaseConfig = {
  apiKey: "REPLACE_ME",
  authDomain: "REPLACE_ME.firebaseapp.com",
  projectId: "REPLACE_ME",
  storageBucket: "REPLACE_ME.appspot.com",
  messagingSenderId: "REPLACE_ME",
  appId: "REPLACE_ME",
};

// Set to true once real config values above are filled in.
// Widgets check this so the site doesn't throw errors while it's still a placeholder.
export const firebaseReady = false;

export const app = firebaseReady ? initializeApp(firebaseConfig) : null;
