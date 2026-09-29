# VibeSafe social pack — vibesafe.info

Every claim below is taken from vibesafe.info (home page, README, pricing).
No user counts, testimonials or scan statistics are invented. Add real numbers only if you have them.

Links use UTM tags so you can see which platform sends visitors.

---

## 1. Facebook post

**Image:** `facebook-1200x1200.png`

> You built your app with Lovable, Bolt or Cursor in a weekend. 🚀
> But did the AI leave your Stripe key sitting in the frontend? 🔑
>
> AI coding tools are great at "make the demo work". They are not great at "make it safe to put on the internet". The usual mistakes:
>
> 🔓 API keys and secrets hardcoded in the code
> 🗄️ Supabase tables with no row-level security, so any user can read everyone's data
> 🚪 Admin pages with no login check
> 📦 Imports for packages that don't exist (or were hallucinated)
>
> VibeSafe scans AI-generated code for exactly these problems and explains each one in plain English, with the fix. Results in seconds.
>
> ✅ Free demo scan, no signup
> ✅ 10 free scans every month, no card
> ✅ Your code is analysed and discarded, never stored or used for training
>
> Check your app before your users do 👉 https://www.vibesafe.info/try?utm_source=facebook&utm_medium=social&utm_campaign=launch_pack
>
> #VibeCoding #AppSecurity #IndieHackers #Lovable #Cursor #Supabase #NoCode #StartupTips

---

## 2. Short video (YouTube Shorts · TikTok · Instagram Reels)

**Video:** `short-1080x1920.mp4` (vertical, ~27 s, no voiceover so it works muted; add a trending sound inside each app)

**On-screen script** (already in the video):
1. "Built your app with AI?" — Lovable · Bolt · Cursor · Replit · v0
2. "Your Stripe key might be public." — `const stripe = "sk_live_…"` in the frontend
3. "3 things AI tools ship all the time" — exposed keys · no Supabase RLS · admin routes with no auth
4. "VibeSafe finds them in seconds" — plain-English fixes
5. "Scan free — no signup" — vibesafe.info

### YouTube Shorts
**Title:** Is your AI-built app leaking your API keys? 🔑 #shorts
**Description:**
Lovable, Bolt and Cursor build fast, but they often ship exposed API keys, open Supabase tables and admin pages anyone can open. VibeSafe scans your code and explains every issue in plain English.
Free demo scan, no signup: https://www.vibesafe.info/try?utm_source=youtube&utm_medium=shorts&utm_campaign=launch_pack
#vibecoding #appsecurity #cursor #lovable #supabase #shorts

### TikTok
**Caption:** POV: the AI built your app in a weekend… and put your Stripe key in the frontend 💀 Scan it free (link in bio) #vibecoding #coding #startup #indiehacker #cybersecurity #cursor #lovable #techtok
*(TikTok doesn't make caption links clickable. Put https://www.vibesafe.info/try?utm_source=tiktok in your bio.)*

### Instagram Reels
**Caption:**
Built your app with AI? Check this before you launch 👇
🔓 exposed API keys
🗄️ Supabase tables with no RLS
🚪 admin pages with no login
VibeSafe finds them in seconds and tells you how to fix them in plain English. Free scan, no signup, link in bio 🛡️
#vibecoding #appsecurity #indiehackers #startup #buildinpublic #nocode #cursorai #supabase

---

## 3. Indie Hackers post

**Where:** Indie Hackers → Post (group: *Building in Public*, or *Growth*)
**Title:** I built a security scanner for apps made with Lovable, Bolt and Cursor — here's what AI keeps getting wrong

**Body:**

Hey IH 👋

A lot of us are shipping products that were mostly written by AI. I do it too. The speed is real. But I kept seeing the same problem: AI coding tools optimise for "make the demo work", not "make it safe to put on the internet".

The mistakes are not exotic. They are the same few, over and over:

- **Live secrets in frontend code.** `sk_live_` Stripe keys, Supabase `service_role` keys, JWT secrets. One push and they're public.
- **Supabase tables with no row-level security.** The app looks fine, but any logged-in user can query every other user's rows.
- **Admin routes with no auth check.** The page is "hidden", not protected.
- **Hallucinated packages.** Imports for packages that don't exist, which is also how slopsquatting attacks get in.
- **Happy-path-only code.** Missing awaits and unhandled errors that only break in production.

So I built **VibeSafe** (https://www.vibesafe.info). You paste code or connect your editor, and it flags these issues in plain English with the fix, mapped to the OWASP Top 10:2025. There's also a live URL scan for security headers and exposed paths like `.env` and `.git/config`.

What it deliberately **doesn't** claim: it's not a pen test, it doesn't replace an audit, and it can't tell you if you've already been hacked. I'd rather be clear about that than oversell a security tool.

**Pricing:** free forever for 10 scans a month, Pro $29/mo (7-day trial, no card), Team $99/mo.

I'd love feedback from anyone shipping AI-built apps:
1. Which of these have you actually hit?
2. Would you rather scan in the editor (VS Code / Cursor extension) or on the web?

Free demo, no signup: https://www.vibesafe.info/try?utm_source=indiehackers&utm_medium=community&utm_campaign=launch_pack

---

## 4. Peerlist post

**Where:** Peerlist → Scroll post. Also list it under **Project** with the Launchpad if you haven't yet.
**Image:** `facebook-1200x1200.png` (square works well on Peerlist)

> Shipped something with Lovable, Bolt or Cursor? 🛠️
>
> I built **VibeSafe**, a security scanner made specifically for AI-generated code.
>
> It catches what AI tools keep shipping:
> → hardcoded API keys and secrets
> → Supabase tables with no RLS
> → admin routes with no auth
> → hallucinated npm packages
> → missing awaits and unhandled errors
>
> Every finding is explained in plain English with the fix, and mapped to OWASP Top 10:2025. Works on the web and in VS Code / Cursor.
>
> Free: 10 scans/month, no card. Demo needs no signup 👇
> https://www.vibesafe.info/try?utm_source=peerlist&utm_medium=social&utm_campaign=launch_pack
>
> Would love your feedback, and an upvote on Launchpad if you find it useful 🙏
>
> #buildinpublic #security #vibecoding

---

## 5. DEV (dev.to) article

**Where:** dev.to → Create post. Tags (max 4): `security`, `ai`, `webdev`, `supabase`
**Cover image:** `devto-cover-1000x420.png`
**Tip:** set the canonical URL to your blog post if you also publish this on vibesafe.info/blog.

~~~markdown
---
title: 5 security mistakes AI coding tools keep shipping (and how to catch them)
published: false
tags: security, ai, webdev, supabase
cover_image: <upload devto-cover-1000x420.png>
---

AI coding tools like Lovable, Bolt, Cursor and v0 are brilliant at one thing: making the demo work.
They are much worse at a different goal: making the app safe to put on the internet.

After looking at a lot of AI-generated code, the same five mistakes keep showing up.

## 1. Live secrets in frontend code

```js
// src/lib/payments.js  ← ships to every visitor's browser
const stripe = new Stripe("sk_live_51H...");
```

Anything in your frontend bundle is public. A `sk_live_` key there lets anyone create charges and refunds on your account.

**Fix:** move secret keys to a server route or edge function and read them from environment variables. Only publishable keys (`pk_live_`) belong in the browser. If a secret was ever committed, rotate it: deleting the line doesn't remove it from git history.

## 2. Supabase tables without row-level security

The app shows each user only their own rows, so it *looks* secure. But the filtering happens in the frontend. With the public anon key (which is in your bundle, by design), anyone can query the table directly.

```sql
alter table public.invoices enable row level security;

create policy "Users read their own invoices"
  on public.invoices for select
  using (auth.uid() = user_id);
```

**Fix:** enable RLS on every table in the `public` schema and write a policy for each operation you allow.

## 3. Admin routes with no auth check

`/admin` isn't linked anywhere, so the AI treats it as private. It isn't. Hidden is not protected.

**Fix:** check the session *and* the role on the server for every admin route and API endpoint, not just in the UI.

## 4. Hallucinated packages

LLMs sometimes import packages that don't exist. Attackers register those names and publish malware (this is called *slopsquatting*).

**Fix:** before installing a package you didn't choose yourself, check it exists, has real download numbers and a real repo.

## 5. Happy-path-only code

```js
function saveOrder(order) {
  db.insert(order);        // missing await: errors vanish
  sendReceipt(order);      // receipt sent even if the insert failed
}
```

**Fix:** `await` every promise, handle the error case, and don't send the confirmation until the write succeeds.

## Catching these automatically

I built [VibeSafe](https://www.vibesafe.info/try?utm_source=devto&utm_medium=article&utm_campaign=launch_pack) to flag exactly these patterns in AI-generated code, explained in plain English and mapped to the OWASP Top 10:2025. It runs on the web (no signup for the demo) and in VS Code / Cursor.

It's not a pen test and it won't replace an audit, but it catches the mistakes that show up again and again before your users find them.

What's the worst thing you've seen an AI coding tool ship? 👇
~~~
