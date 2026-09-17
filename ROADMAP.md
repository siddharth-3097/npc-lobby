# NPC Lobby — Roadmap

A running list of ideas, loosely sequenced across 12 weeks. Nothing here is
committed or scheduled — it's a backlog to review and re-prioritize as we go.

**Priority key**
- **High** — features that drive the most engagement on the platform, or meaningfully improve the core experience.
- **Medium** — communication changes (emails, notifications) and engagement mechanics.
- **Low** — cosmetic/visual polish.

---

## Week 1 — Foundational polish
- **[High]** Public profile pages — see a person's recommendations, karma tier, and thank-yous received.
- **[High]** "Trending this week" section on the home page, surfacing the most-thanked recent picks.
- **[Medium]** Milestone celebration email the moment someone crosses into a new karma tier.
- **[Medium]** Social proof counter on the home page ("1,234 recommendations shared so far").
- **[Low]** Dark mode toggle.
- **[Low]** Random NPC sprite variations shown on each visit instead of always the same frog.

## Week 2 — Discovery
- **[High]** Search bar on the list page (match against title and description).
- **[High]** Sort controls — newest, most thanked, by type.
- **[Medium]** Weekly karma summary email ("this week you earned X karma").
- **[Medium]** "People you might want to thank" nudge shown on the list page.
- **[Low]** Loading skeleton states while the list fetches.
- **[Low]** Better empty-state illustration for "no recommendations yet."

## Week 3 — Social layer
- **[High]** Comment/reply thread on each recommendation, beyond just a thank-you.
- **[High]** Leaderboard page — top karma earners this week / month / all-time.
- **[Medium]** In-app notification bell for thank-yous and replies, not just email.
- **[Medium]** Re-engagement email for people who haven't visited in a while.
- **[Low]** Confetti animation when a checkpoint unlocks.
- **[Low]** Small hover/press micro-interactions on buttons.

## Week 4 — Rich content
- **[High]** Auto-fetch poster/cover art for movies, shows, and games via a free API.
- **[High]** Duplicate detection — flag when a title's already on the list.
- **[Medium]** "Your recommendation got 5 thank-yous" milestone email.
- **[Medium]** Short onboarding email series (day 1 / day 3 / day 7 tips).
- **[Low]** Rotating seasonal accent-color theme.
- **[Low]** Subtle sound effect on submit / thank-you.

## Week 5 — Sharing & growth
- **[High]** Shareable recommendation cards — generate an image for Instagram/Twitter.
- **[High]** Referral milestone rewards (bonus karma at 5 / 10 / 25 invites).
- **[Medium]** Anniversary email ("1 year on NPC Lobby").
- **[Medium]** Digest email of new recommendations since a person's last visit.
- **[Low]** Favicon badge showing unread activity count.
- **[Low]** Typography and spacing polish pass across the site.

## Week 6 — Mobile experience
- **[High]** PWA support — installable, add-to-home-screen, basic offline shell.
- **[High]** "Save for later" / bookmark a recommendation without committing to a thank-you.
- **[Medium]** Browser push notifications for thank-yous and replies.
- **[Medium]** Rework first-time onboarding flow to be more guided.
- **[Low]** Time-of-day theming (darker palette after sunset, on-brand for "late night").
- **[Low]** Sticky "back to top" button on long lists.

## Week 7 — Personalization
- **[High]** Personalized home feed — recommendations from people you've thanked before.
- **[High]** "For you" filter based on the types you interact with most.
- **[Medium]** Weekly personalized digest email highlighting relevant new picks.
- **[Medium]** Karma tier badge shown next to a person's name site-wide.
- **[Low]** Pick-your-own pixel NPC avatar.
- **[Low]** Animated tier-up badge reveal.

## Week 8 — Trust & quality
- **[High]** Report/flag a recommendation, with a lightweight moderation queue.
- **[High]** "Verified" badge after a person's picks earn a meaningful number of genuine thank-yous.
- **[Medium]** Email verification step before a first submission — directly avoids typo'd emails ending up on prod (see: the "chakrabartys@icloud.con" incident).
- **[Medium]** Real-time inline email format validation on all forms.
- **[Low]** Small empty-state animations.
- **[Low]** Icon set consistency audit.

## Week 9 — Community events
- **[High]** Weekly themed prompt ("this week: recommend a comfort show") to drive submissions.
- **[High]** Karma boost weekends (2x karma events).
- **[Medium]** Announcement banner system for events and updates.
- **[Medium]** "New here" welcome email highlighting a few community favorites.
- **[Low]** Event-themed visual accents (banners, badges).
- **[Low]** Countdown widget for time-limited events.

## Week 10 — Data & insight
- **[High]** Admin dashboard — karma leaderboard, top categories, growth over time.
- **[High]** Per-user stats page ("your impact": karma given, recommendations made, thank-yous received).
- **[Medium]** Lightweight monthly recap email.
- **[Medium]** PostHog dashboards/funnels for the key actions (submit, thank, invite).
- **[Low]** Visual polish on charts/stats.
- **[Low]** Shareable "karma card" image, similar to a stats wrap-up.

## Week 11 — Resilience & performance
- **[High]** Harden rate-limiting and abuse protection beyond the current daily caps.
- **[High]** Full-text search indexing so search stays fast as the list grows.
- **[Medium]** Simple status page / communication channel for outages.
- **[Medium]** Consistent toast/error messaging pass across every form.
- **[Low]** Image optimization pass (favicon, logo, sprite sizes).
- **[Low]** Accessibility polish — contrast, focus states, aria labels.

## Week 12 — Look ahead
- **[High]** Public API or embeddable "recommend on your site" widget.
- **[High]** Multi-language support.
- **[Medium]** Community feature-request/voting board.
- **[Medium]** Feedback form linked from the felt note.
- **[Low]** Explore a visual refresh for a potential rebrand milestone.
- **[Low]** Retro pixel loading transition between pages.
