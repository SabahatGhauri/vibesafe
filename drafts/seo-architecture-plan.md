# VibeSafe SEO/GEO plan — grounded version

Synthesised from the two pasted strategy documents, checked against the actual
site inventory, real Search Console signal, and what's already scheduled.

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
