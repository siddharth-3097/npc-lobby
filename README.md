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
