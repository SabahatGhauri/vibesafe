# VibeSafe SEO/GEO plan — grounded version

Synthesised from the two pasted strategy documents, checked against the actual
site inventory, real Search Console signal, and what's already scheduled.

> **Updated 2026-09-02 with real Google Search Console data (last 3 months).
> That data changes the priority order — read section 0 first.**

---

## 0. What Search Console actually says (2026-09-02 export, Jul 8 – Aug 30)

### The headline

**29 clicks / 815 impressions in three months. 100% of clicks came from brand
queries** ("vibesafe", "vibe safe"). **Zero non-brand clicks in three months.**

### Correction to an earlier claim in this document

An earlier version said *"supabase-security-checklist ranks position 7 — the only
page-one ranking on the site."* **That was wrong.** It came from third-party keyword
data that does not match Google's own numbers. Real GSC: best Supabase position is
**42**. Treat GSC as the only source of truth; the third-party positions were
unreliable across the board.

The "don't move URLs" rule still stands, but because there's no ranking worth the
risk and the `.html`→extensionless redirects are still consolidating — not because
of a page-one ranking that doesn't exist.

### Where demand actually is

| Cluster | Impressions | Clicks | Avg position |
|---|---|---|---|
| **Cursor** (how to secure cursor, cursor security, is cursor safe…) | **251** | 0 | ~64 |
| **Vibe coding** ("is vibe coding safe" alone = 176) | **211** | 0 | ~68 |
| Supabase | 20 | 0 | 42 |
| "ai code security scanner" | 5 | 0 | 41 |
| "website security scanner" | **0 impressions — never appears** | — | — |

Top pages by impressions: `/` (500), `/cursor-security-checklist` (**252, pos 64,
zero clicks**), `/vibe-coding-security` (212, pos 59).

### The uncomfortable implication

**Nothing non-brand sits in the winnable position 8–20 band.** Everything is
position 30–90. Per the autoseo skill's own rule: *"Position 40+ means an authority
gap that content alone won't close."*

Therefore:
- The four pages previously queued for Phase 1 (`/launch-check`, `/ai-code-security`,
  `/about`, `/website-security-scanner`) target queries with **near-zero measured
  demand**. "Website security scanner" has never produced a single impression.
- **On-page work cannot lift a position-65 page.** The research report is not a
  "phase 3 nice-to-have" — it is the only item on the whole list that earns links,
  and links are the ceiling everything else is stuck under.

### The one clearly winnable thing

**You rank position 4.95 for your own brand name.** 167 impressions, 14.37% CTR.
A brand query at #1 typically converts 30–60%. Roughly half the clicks on your
easiest query are going elsewhere — to the other "VibeSafe" products.

Brand-collision noise visible in the data: Google is matching vibesafe.info to
*wiresafe, bitsafe, baysafe, defibsafe, visafe, codesafe, "bobby safe", "vibi
homesafe"*. The collision is real and now quantified.

---

## 0b. Separate finding: the blog never explains what the product does

Measured across all 20 blog posts:

| Feature | Posts mentioning it |
|---|---|
| Code scan | 20/20 |
| Launch Check | 13/20 (mostly name-only) |
| Safety score | 4/20 |
| Live URL / DAST | 3/20 |
| GitHub repo scan | 1/20 |
| Continuous monitoring | 1/20 |
| **One-click AI fixes** | **0/20** |
| **VS Code / Cursor extension** | **0/20** |

And **16 of 20 CTAs are near-identical**: *"Scan your code free → 3 free scans every
month."*

That sells a **quota, not a capability**. A reader finishes a post about Cursor
risks and is offered three scans — with no stated reason an account is worth having.

This connects to a known funnel fact: **three users exhausted the free scan limit and
none converted.** If "3 scans/month" is the only thing they were ever told, hitting
the limit reads as *"the free thing ran out,"* not *"there's a better version."*

**Fix pattern already proven today:** `/try`'s post-scan CTA now names the actual
critical issue found ("Critical: Hardcoded Stripe Live Secret Key → don't just find
it, fix it"). That specificity is what every blog CTA is missing.

---

## 0c. Revised priority order (supersedes the phases below)

1. **Blog CTA + feature communication rewrite** — cheapest, affects all 20 posts,
   fixes a proven conversion gap, needs no new pages and no new demand
2. **Brand-term ranking** — the only winnable query; entity signals, `/about`,
   Organization schema. Directly converts.
3. **The research report with real data** — the only lever that lifts position-65
   pages, because it's the only one that earns links
4. **Cursor cluster investigation** — 251 impressions and a page at position 64
   with zero clicks; understand it before writing more
5. **Hold** `/launch-check`, `/ai-code-security`, `/website-security-scanner` until
   something demonstrates demand

---

## 1. The correction that changes the whole plan

The proposal describes 40 pages to build. **Roughly 25 of them already exist.**

| Proposed as new | Already live |
|---|---|
| `/security-center/` | `security.html` — "Security & Data Handling" |
| `/docs/` | `user-guide.html` |
| homepage FAQ page | `faq.html` |
| `/vibe-coding-security/` | `vibe-coding-security.html` |
| `/platforms/lovable-security/` | `lovable-security-checklist.html` |
| `/platforms/bolt-security/` | `bolt-security-checklist.html` |
| `/platforms/cursor-security/` | `cursor-security-checklist.html` |
| `/platforms/replit-security/` | `blog/replit-app-security-guide.html` |
| `/security/supabase-rls/` | `supabase-security-checklist.html` ← **ranks position 7** |
| `/security/exposed-api-keys/` + `/tools/api-key-scanner/` | `exposed-api-key-scanner.html` |
| `/tools/ai-code-scanner/` | `ai-code-security-scanner.html` |
| `/comparisons/vibesafe-vs-snyk/` | `vs-snyk.html` |
| `/comparisons/vibesafe-vs-gitguardian/` | `vs-gitguardian.html` |
| `/research/state-of-vibe-coding-security-2026/` | `state-of-vibe-coding-security-2026.html` |
| `/guides/is-vibe-coding-safe/` | `blog/is-vibe-coding-safe-honest-answer.html` |
| `/guides/ai-code-security-checklist/` | `free-security-checklist.html`, `pre-launch-security-checklist.html` |
| `/security/hallucinated-packages/` | `blog/hallucinated-packages-slopsquatting.html` |

**Genuinely missing and worth building: about five pages, not forty.**

---

## 2. Two things in the proposal that would actively cause harm

### a) Moving existing URLs into `/platforms/`, `/security/`, `/tools/`

`supabase-security-checklist.html` currently sits at **position 7** — page one — for
"supabase row level security." Moving it to `/security/supabase-rls/` means a 301,
a re-crawl, and a re-evaluation of the only page on this site with a page-one
ranking. There is no ranking upside to a prettier URL path.

**Rule: no existing indexed URL moves. Ever, in this plan.** Hierarchy gets expressed
through internal linking, not directory structure. Google infers topical hierarchy
from links far more than from URL paths.

### b) The proposed architecture contains its own cannibalisation

Four pairs in the sitemap target near-identical intent:

- `/website-security-scanner/` vs `/tools/website-security-scanner/`
- `/security/exposed-api-keys/` vs `/tools/api-key-scanner/`
- `/launch-check/` vs `/tools/ai-website-tester/`
- `/ai-website-security/` vs `/website-security-scanner/`

This is the exact failure already live on this site (`try.html` and
`ai-code-security-scanner.html` share an identical H1 and neither ranks). Building
four more instances of it would undo the work already done.

---

## 3. Constraints the proposal doesn't account for

1. **~34 posts are already auto-publishing daily through Sep 30**, covering many of
   these same clusters. New pages built in parallel compete with content already in
   flight. Nothing new ships into a cluster the calendar is already covering.
2. **"VibeSafe" collides with 6+ other security products of the same name.** No
   architecture fixes a brand collision. Category terms are winnable; the brand term
   probably isn't.
3. **Solo founder.** A 40-page build is a content team's quarter. Ten excellent pages
   is a realistic quarter alongside product work.
4. **Only 3 clusters have measured Search Console signal** (positions 7, 10, 11).
   Everything else in this plan is a zero-data bet.

---

## 4. The plan

### Phase 0 — Fix and map before building (this week, ~2 hours)

- [ ] Fix the `try.html` / `ai-code-security-scanner.html` duplicate H1 — flagged three
      times now, still live, and it's the single clearest cannibalisation on the site
- [ ] Write the hierarchy as an **internal-linking map over pages that already exist**,
      not as new URLs. No page moves.
- [ ] Retrofit those links: every platform/checklist page links up to its pillar; the
      pillar links down to each. This is the highest-value item in both documents and
      it requires zero new content.

### Phase 1 — Build only what genuinely doesn't exist (weeks 1–3)

Ordered by value, and none of these compete with anything already live or scheduled:

1. **`/launch-check`** — a real product with real differentiation and *no landing page
   at all*. It only exists as a homepage section. Highest-value missing page by far.
2. **`/ai-code-security`** — the one genuinely missing pillar. Built as a **hub** that
   links out to the existing cluster pages, not as new competing prose.
3. **`/about`** — entity clarity for Google and AI systems. Cheap, no competition.
4. **`/website-security-scanner`** — distinct search intent (live URL scanning) not
   currently served by a dedicated page.

Homepage changes, same phase:
- Add FAQ block + FAQPage schema (visible questions matching schema exactly)
- Keep the Stripe hero headline; consider a more descriptive H1 **only as an A/B test
  once source tracking has a baseline** — not as an untested rewrite

### Phase 2 — Wait, then expand on evidence (week 4+)

Do nothing new until:
- The scheduled content calendar finishes its run, and
- Source tracking (live since Aug 28) has ~3–4 weeks of real data

Then expand into whichever clusters actually show impressions, rather than the ones
that look good on a diagram.

### Phase 3 — The one asset worth real effort

**Make `state-of-vibe-coding-security-2026` an actual research report.**

Both documents identify this as the highest-leverage item and both are right. It's the
only thing here that generates backlinks, and backlinks are the ceiling everything else
is stuck under.

But it needs real data. Current usage (~7 people have ever scanned) is not a dataset.
The honest way to build it:

- Scan a meaningful sample of **public GitHub repos** built with Lovable/Bolt/Cursor/Replit
- Report real percentages: exposed secrets, missing RLS, vulnerable deps, missing headers
- Publish the methodology and sample size openly, including limitations
- Never invent a number — a fabricated stat in a security product's research report is
  the single fastest way to lose the credibility this is meant to build

This is a project, not a content task. Worth scheduling deliberately.

---

## 5. What to ignore from both documents

- The 40-page sitemap as a build list (25 already exist)
- Any URL restructuring of indexed pages
- `/glossary/*` and the full `/security/*` knowledge base — thin-content risk, high
  volume, low differentiation, and mostly duplicative of the scheduled calendar
- Nav restructure (Product/Solutions/Resources) — reasonable eventually, not urgent,
  and a large IA change for a site this size

---

## 6. The positioning line, which both documents got right

> VibeSafe is the security layer for AI-built applications.

Everything above should reinforce that one sentence. Category terms — "AI code security,"
"vibe coding security," "AI-built app security" — are the territory worth owning.
"Website security scanner" is a supporting acquisition channel, not the identity.

---

# Backlink plan (added 2026-09-02)

Synthesised from a pasted backlink audit, corrected against what was verified
directly this session.

## Where the audit is right

- **Profile is underdeveloped, not bad.** Few links, but the ones that exist are
  topically relevant. That is a much better starting point than spammy volume.
- **Do not buy links.** Correct, and non-negotiable for a security product.
- **Spread links across pages**, not all at the homepage.
- **The research report is the single biggest asset.** This is now the third
  independent document to say so, and it matches the autoseo skill's own rule:
  position 40+ is an authority gap that content alone cannot close. Links are the
  ceiling everything else is stuck under.

## What the audit missed — both verified directly

### 1. The GitHub repo is invisible, and a competitor's ranks above the product

`github.com/SabahatGhauri/vibesafe`:
- description: **empty**
- topics: **none**
- homepage: **a Vercel preview URL**, not vibesafe.info

The competitor ranking #1 for "vibesafe free scanner" (`vibesafeio/vibesafe-action`)
has a keyword-rich description, 15 topics and 7 stars.

This is a 60-second fix that improves both a ranking competitor's advantage AND the
`sameAs` entity signal on /about, which currently points at a blank repo.

### 2. The brand is contested — this is why links matter more here than usual

Searching "vibesafe free scanner" returns **four other VibeSafe security scanners
ahead of vibesafe.info**: `vibesafeio/vibesafe-action`, `CodAngels/vibesafe`,
`vibesafe.net`, `vibe-safe.net`. vibesafe.info ranks **8th for its own name**.

The search engine also blended all of them into one description — mixing competitors'
features with VibeSafe's. AI assistants will do the same.

So links here are not only about authority. They are about **entity disambiguation**:
making the web state unambiguously which VibeSafe is which. That changes what a good
link looks like — a link that names the product AND the domain AND the company is
worth more than a higher-authority link that just says "VibeSafe".

### 3. Medium is missing from the confirmed list

Published there this session, canonical pointing back to vibesafe.info.

## Revised priority — sequenced by effort against value

| # | Action | Effort | Why this order |
|---|---|---|---|
| 1 | **Fix the GitHub repo** (description, 10 topics, correct homepage) | 1 min | A competitor's repo outranks the product; this is the cheapest possible correction, and it repairs an entity link that already exists |
| 2 | **Keep cross-posting to DEV/Medium with canonical** | ongoing | Already working; 8 DEV posts live. Scale to 10–15 as the audit suggests |
| 3 | **The research report with real data** | project | The only lever that lifts position-65 pages. Needs a real corpus — public GitHub repos built with these tools — with published methodology and no invented numbers |
| 4 | **Developer directories / AI tool listings** | low | Also entity-disambiguation work: each listing states which VibeSafe this is |
| 5 | **SourceBottle / journalist quotes** | slow, low hit rate | The audit ranks this #1; demoted here because it is the slowest item with the least predictable return, and it works far better once #3 exists to cite |

## The strategic point the audit almost reaches

Its Priority 1 is SourceBottle. That is the wrong first move for a product whose own
brand name returns four competitors ahead of it. Pitching journalists before the
entity is unambiguous risks coverage that credits the wrong VibeSafe.

Fix identity first (#1, #4), then earn citations (#3), then pitch (#5).
