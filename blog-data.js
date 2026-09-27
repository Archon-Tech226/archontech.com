// Archon Tech — Behind the Build — shared data helpers
// Wraps Firestore + Auth calls so blog.html and the footer widget share one implementation.

import { app, firebaseReady } from "./firebase-config.js";
import {
  getFirestore, collection, addDoc, query, orderBy, limit, onSnapshot, serverTimestamp,
} from "https://www.gstatic.com/firebasejs/10.13.0/firebase-firestore.js";
import {
  getAuth, signInWithEmailAndPassword, signOut, onAuthStateChanged,
} from "https://www.gstatic.com/firebasejs/10.13.0/firebase-auth.js";

export const ready = firebaseReady && !!app;
export const db = ready ? getFirestore(app) : null;
export const auth = ready ? getAuth(app) : null;

const POSTS = "posts";
const MAX_LEN = 600;

export function initials(name) {
  return (name || "?")
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((w) => w[0])
    .join("")
    .toUpperCase();
}

export function formatWhen(ts) {
  if (!ts || !ts.toDate) return "";
  const d = ts.toDate();
  return d.toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" });
}

export function watchPosts(max, onData) {
  if (!ready) {
    onData([], "unconfigured");
    return () => {};
  }
  const q = query(collection(db, POSTS), orderBy("createdAt", "desc"), limit(max));
  return onSnapshot(
    q,
    (snap) => onData(snap.docs.map((d) => ({ id: d.id, ...d.data() })), "ok"),
    () => onData([], "error")
  );
}

export async function addPost(authorName, body) {
  const text = (body || "").trim();
  if (!text) throw new Error("Write something before posting.");
  if (text.length > MAX_LEN) throw new Error("Keep it under " + MAX_LEN + " characters.");
  if (!auth || !auth.currentUser) throw new Error("Sign in first.");
  await addDoc(collection(db, POSTS), {
    body: text,
    author: authorName,
    authorUid: auth.currentUser.uid,
    createdAt: serverTimestamp(),
  });
}

export function watchAuth(onChange) {
  if (!ready) {
    onChange(null);
    return () => {};
  }
  return onAuthStateChanged(auth, onChange);
}

export async function login(email, password) {
  if (!ready) throw new Error("Team sign-in isn't set up yet.");
  await signInWithEmailAndPassword(auth, email, password);
}

export async function logout() {
  if (ready) await signOut(auth);
}

export const MAX_POST_LENGTH = MAX_LEN;
