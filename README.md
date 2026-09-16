# NPC Lobby

A tiny Django app for sharing what you're into: a movie, TV show, anime,
book, podcast, game, subreddit, IG handle, or track worth staying up for —
and earning karma for it.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit http://127.0.0.1:8000/.

## How it works

- **Home page** — an animated pixel NPC, and one input: "recommend
  something today that you found cool." Submitting it opens a short form
  (name, email, type, who'll love it & why). One recommendation per email
  per day.
- **Karma** — recommending something, thanking someone, and inviting a
  friend each award +1 karma to that person's email. The home page shows
  the karma checkpoints (tiers and what they unlock).
- **View the List** — every recommendation in a table, filterable by type,
  each with a checkbox and a love icon.
  - Select any number and a "Send me my list" bar appears; enter an email
    and we send the selected recommendations there.
  - The love icon asks for your name and email (optional message), then
    emails the original recommender that someone loved their pick. Capped
    at 2 per email per day.
- **Invite a Friend** — below the karma checkpoints; asks for your name/
  email and your friend's name/email, then emails your friend an invite.
  Capped at 3 invites per email per day.

## Email

Transactional email (welcome/contribution/love/invite/send-my-list) goes
through [Resend](https://resend.com) when `RESEND_API_KEY` is set. Without
it, email falls back to the console (dev-friendly, no setup needed).

Copy `.env.example` to `.env` and fill in your own values — `.env` is
gitignored, so this is where secrets live, not in the code:

```bash
cp .env.example .env
```

```
RESEND_API_KEY=re_...              # from resend.com
DEFAULT_FROM_EMAIL=NPC Lobby <noreply@yourdomain.com>  # must be a domain verified in Resend
SITE_URL=https://www.npclobby.in   # used in the invite email's link
```

The exact templated emails (welcome, per-recommendation, love notification,
invite) live in `recs/emails.py`; the copy they're built from is in
`emails.md`.

To send real email over SMTP instead of Resend, set `EMAIL_HOST` (and
friends) in `.env` — see `latenightlist/settings.py` for the full list.
This only affects the fallback path used when `RESEND_API_KEY` is unset.

## Admin

Create a superuser to browse recommendations, thank-yous, invites, and
karma in the admin:

```bash
python manage.py createsuperuser
```

Then visit `/admin/`.

## Database

Uses Postgres (tested against [Neon](https://neon.tech)) when `DATABASE_URL`
is set, falling back to a local sqlite file otherwise. Point `DATABASE_URL`
at your database in `.env`, then:

```bash
python manage.py migrate
```

There's no automated release step that runs migrations on deploy — after
changing models, run `migrate` locally against the production
`DATABASE_URL` before or right after pushing.

## Deploying on Vercel

The app is set up to run on Vercel as a Python WSGI serverless function:

- `api/index.py` — the entrypoint Vercel's Python runtime calls.
- `vercel.json` — routes every request to that entrypoint.
- Static files are served by [WhiteNoise](http://whitenoise.evans.io/)
  from the committed `staticfiles/` directory, since Vercel's filesystem
  is read-only at request time (no `collectstatic` step runs on deploy).

**One-time setup:**

1. In the Vercel dashboard, "Add New Project" → import this GitHub repo.
   Vercel will detect `vercel.json` automatically.
2. Add these environment variables in Project Settings → Environment
   Variables (same names as `.env.example`):
   - `SECRET_KEY` — generate with
     `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `DEBUG=False`
   - `DATABASE_URL` — your Postgres connection string
   - `RESEND_API_KEY`, `DEFAULT_FROM_EMAIL`, `SITE_URL`
   - `ALLOWED_HOSTS` — comma-separated, include your custom domain if any
     (Vercel's own `*.vercel.app` preview/prod URL is allowed automatically)
   - `CSRF_TRUSTED_ORIGINS` — comma-separated, full origins with scheme,
     e.g. `https://npclobby.in` (again, the `*.vercel.app` URL is handled
     automatically)
3. Deploy.

**Whenever templates, CSS, JS, or images change**, re-run before pushing so
the deployed static files stay in sync (they're committed, not built on
Vercel):

```bash
python manage.py collectstatic --noinput
git add staticfiles
```

**Whenever models change**, run `python manage.py migrate` locally against
the production `DATABASE_URL` (there's no release-phase hook on Vercel to
do this automatically).
