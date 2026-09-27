# Archon Tech — website

Plain HTML, CSS and JavaScript. No build step — open any `.html` file in a
browser, or push the whole folder to GitHub Pages / Netlify / Cloudflare Pages.

## Files

- `index.html`, `services.html`, `portfolio.html`, `about.html`, `team.html`,
  `contact.html`, `404.html` — the site's pages
- `styles.css` — the whole design system, shared by every page
- `main.js` — mobile menu, sticky header shadow, footer year
- `portfolio-filter.js` — the All / Websites / Web applications filter
- `contact-form.js` — submits the contact form and shows a status message
- `blog.html`, `blog-page.js`, `blog-widget.js`, `blog-data.js` —
  the "Behind the Build" team notes feature (see below)
- `firebase-config.js` — Firebase project keys (placeholder until you fill it in)
- `firestore.rules` — security rules to paste into the Firebase console
- `logo13.png`, `founder.png` — the only images the new site uses

## 1. Contact form

The form on `contact.html` posts to Formspree. Steps:

1. Create a free account at [formspree.io](https://formspree.io) and add a
   new form pointed at `founder.archon@gmail.com`.
2. Copy the form's endpoint URL (looks like
   `https://formspree.io/f/xxxxxxxx`).
3. In `contact.html`, replace `REPLACE_WITH_FORM_ID` in the `<form action="...">`
   line with your real endpoint.

Until you do this, the form shows a message asking people to email you
directly instead of failing silently.

## 2. "Behind the Build" team notes

This is the feature that lets you, Janaganandhini and Vel post short updates
that show on `blog.html` and as a preview in every page's footer. It needs a
free Firebase project, since the site itself has no server.

**A. Create the project**
Go to [console.firebase.google.com](https://console.firebase.google.com) →
Add project → name it (e.g. `archon-tech`) → skip Google Analytics.

**B. Register a web app**
Inside the project: click the `</>` icon → name it `archontech-site` → skip
Firebase Hosting (the site already lives elsewhere). Firebase shows a
`firebaseConfig` object — copy it.

**C. Fill in `firebase-config.js`**
Paste your real values into `firebaseConfig` in `firebase-config.js`, and
change `firebaseReady` from `false` to `true`. Save.

**D. Turn on Firestore**
Build → Firestore Database → Create database → Production mode → pick a
region close to India (e.g. `asia-south1`).

**E. Apply the security rules**
Build → Firestore Database → Rules tab → replace the contents with everything
in `firestore.rules` from this repo → Publish.

**F. Turn on email/password sign-in**
Build → Authentication → Get started → Sign-in method → Email/Password →
Enable.

**G. Create the 3 team accounts**
Still in Authentication → Users tab → Add user, once for each of you. Use
real email addresses and share the passwords with your teammates directly
(not over a public channel).

**H. Map emails to display names**
Open `blog-page.js` and fill in the `TEAM_NAMES` object near the top, e.g.:

```js
const TEAM_NAMES = {
  "abinaya@yourdomain.com": "Abinaya Sri",
  "nandhini@yourdomain.com": "Janaganandhini",
  "vel@yourdomain.com": "Vel",
};
```

This is what shows on a post instead of the raw email address.

Once A–H are done, refresh the site: the footer and `blog.html` will load
posts live, and the 3 accounts you created can sign in from `blog.html` to
post.

## Notes

- No prices are shown anywhere on the site, and no project-count or other
  stats are shown, by request.
- The 5 portfolio projects don't have live links yet — cards say
  "Web application" / "Website" instead of linking out. Add links to the
  `project-card` articles in `portfolio.html` once projects are deployed.
- Team bios on `team.html` are drafted based on each person's role and
  education — edit `team.html` directly to adjust wording.
