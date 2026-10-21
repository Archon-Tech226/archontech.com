# Archon Tech — Django site

A full rebuild of the Archon Tech website on Django, with a real **custom
admin dashboard** (not default Django admin) for managing blog posts,
testimonials, portfolio projects, and contact leads. Dark theme with a
teal + purple palette, matching the logo and brand poster, including an
atmospheric glow/lightning background used site-wide.

## What's inside

- **Public site:** Home, Services, Portfolio, About, Team, Contact, Behind
  the Build — all server-rendered from the database.
- **Custom admin dashboard:** at `/dashboard/` — hand-built to match the
  site's brand (sidebar nav, stat cards, branded colors, toast
  notifications), not Django's default admin look. Django's own `/admin/`
  still exists underneath as a technical fallback, but `/dashboard/` is
  what the team actually uses day to day.
- **4 database models:** `BlogPost`, `Testimonial`, `PortfolioProject`
  (now with an image field), `Lead` (contact form submissions).
- **Contact form:** saves straight to the database, shows a success message,
  and optionally emails you too if you set up `EMAIL_HOST_USER` (see below).
- **Portfolio:** seeded with your 2 real projects (SDS Food Products, Urban
  Spice Kitchen) with real screenshots — manageable from `/dashboard/portfolio/`.

## The admin dashboard, in detail

Sign in at `/dashboard/login/` (not `/admin/login/`) with either admin
account. From there:

- **Dashboard home** — stat cards (total leads, new/unreviewed, leads this
  week, published posts) plus recent activity.
- **Leads** — search, filter by status, click into any lead to read the
  full message and update status (New → Contacted → Quoted → Won/Lost)
  with private notes — saves instantly, no page reload (via htmx).
- **Behind the Build** — write, edit, delete posts, toggle Draft/Published.
- **Testimonials** — add, edit, delete, toggle visible/hidden.
- **Portfolio** — add, edit, delete projects, upload a screenshot per
  project, reorder with "Sort order," toggle visible/hidden.

### Important: uploaded images and Render's free tier

Render's free web services have an **ephemeral filesystem** — anything
written to disk after the app starts (including images uploaded through
`/dashboard/portfolio/`) is **lost on every restart or redeploy**. The 2
seed images that ship with this project are safe, since they're committed
to the repo and `build.sh` copies them back in every deploy. But if you
upload a *new* project screenshot through the dashboard later, it will
disappear the next time the app restarts — which can happen at any time
on the free tier, not just on deploys.

**To fix this properly later:** connect a free image host like
Cloudinary (free tier) as Django's storage backend, so uploads go there
instead of the app's own disk. Not set up yet — flagging it now so it
doesn't surprise you after you've uploaded a dozen real project photos.

## Running it locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_site      # loads the 5 default portfolio projects
python manage.py createsuperuser --username abinaya
python manage.py createsuperuser --username janaganandhini

python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site, `http://127.0.0.1:8000/admin/`
to sign in and manage content.

No `.env` file needed for local dev — it falls back to SQLite and `DEBUG=True`
automatically. Copy `.env.example` to `.env` if you want to override anything.

## Deploying to Render

### Option A — one-click with the Blueprint (recommended)

1. Push this whole folder to a GitHub repo.
2. In the Render dashboard: **New → Blueprint**, connect the repo. Render
   reads `render.yaml` and sets up both the web service and a free Postgres
   database automatically, including `DATABASE_URL` and a random `SECRET_KEY`.
3. Wait for the first deploy to finish (`build.sh` runs migrations and seeds
   the portfolio automatically).
4. Open a **Shell** tab on the web service in the Render dashboard and run:
   ```bash
   python manage.py createsuperuser --username abinaya
   python manage.py createsuperuser --username janaganandhini
   ```
5. Visit your `*.onrender.com` URL — the site works, and `/dashboard/login/`
   is where the team signs in day to day (`/admin/` also works, as a fallback).

### Option B — manual setup

If you'd rather click through it yourself: create a **Postgres** instance
(free tier) and a **Web Service** from the repo, set the build command to
`./build.sh`, the start command to `gunicorn config.wsgi:application`, and
add the environment variables listed in `render.yaml` under `envVars`
(`SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=.onrender.com`, `DATABASE_URL`
from the Postgres instance you created).

## About the 30-day free database reset

You chose to stay on Render's free Postgres, which **expires 30 days after
creation** (with a 14-day grace period before the data is actually deleted).
When that happens:

1. Create a new free Postgres instance in Render.
2. Update the web service's `DATABASE_URL` environment variable to point at it.
3. Redeploy — `build.sh` runs migrations automatically on every deploy.
4. Run the two `createsuperuser` commands again (see above) — logins don't
   survive a database swap, since they're stored in the same database.
5. `python manage.py seed_site` runs automatically during the build and
   re-creates the 5 default portfolio projects for you. Any testimonials,
   blog posts, or leads you'd added since the last reset are gone — there's
   no way around that with a database that gets deleted, short of upgrading
   to a paid plan (~$14/month total) for one that doesn't expire.

**If this cadence gets annoying:** the fix later is just changing where
`DATABASE_URL` points — to Render's paid Postgres, or to a separate always-free
option like Neon or Supabase. Nothing else about the app needs to change.

## Admin dashboard — what each person can do

Both `abinaya` and `janaganandhini` are full superusers, so either can:

- **Blog posts:** write, edit, delete, and set Draft vs Published. Only
  Published posts show on the public site.
- **Testimonials:** add a client quote, name, company, and star rating.
  Untick "Is published" to hide one without deleting it.
- **Portfolio projects:** add/edit projects, set category (Website / Web
  application), tech tags (comma-separated), and reorder with "Sort order."
- **Leads:** see every contact-form submission, with a status you can update
  (New → Contacted → Quoted → Won/Lost) and a private notes field.

## Email notifications for new leads (optional)

Leads always save to the database regardless. To also get an email the
moment someone submits the contact form:

1. In your Google Account, create an **App Password** (Google Account →
   Security → 2-Step Verification → App passwords) — don't use your real
   Gmail password here.
2. Set `EMAIL_HOST_USER` to your Gmail address and `EMAIL_HOST_PASSWORD` to
   the app password, either in Render's environment variables or your local
   `.env`.

Leave both blank to skip this — the form still works, leads just won't
trigger an email.

## Project structure

```
config/             Django project settings, root urls.py, wsgi.py
site_app/           The app: models, admin, views, forms, urls
  management/commands/seed_site.py   Reseed helper (see above)
templates/site_app/ All page templates (base.html + one per page)
static/              styles.css, main.js, portfolio-filter.js, logo, photo
build.sh             Render's build command
render.yaml           Render Blueprint (web service + database)
requirements.txt      Pinned Python dependencies
```

---

## October 2026 UI/UX upgrade: what changed

Commands to apply (Python 3.11, Django 5.2.x):

    pip install -r requirements.txt
    python manage.py migrate          # adds migration 0004 (additive only; existing data is kept)
    python manage.py seed_blog_posts  # 3 default articles; safe to re-run, never overwrites edits
    python manage.py test

Optional, local development only: `python manage.py seed_sample_testimonials` creates three
clearly labelled SAMPLE testimonials. They are flagged `is_sample` and are never shown when `DEBUG=False`.

Items that need a human decision before deploying:
- Set a "Project label" (client work / internal / concept) on each portfolio project in the dashboard.
- Confirm Janaganandhini's and Vel's portraits (initials are shown until approved photos exist).
- Confirm the contact promise "we'll reply" wording and add real, approved testimonials when available.
- Blog copy and service copy are drafts: proofread and verify every claim.
