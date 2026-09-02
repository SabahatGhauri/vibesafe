# VibeSafe — AI code security scanner for AI-built apps

**This repository holds the source of the [vibesafe.info](https://www.vibesafe.info) website.**
It is not an installable scanner — the product itself runs at
[vibesafe.info](https://www.vibesafe.info), and the editor extension is linked below.

---

## What VibeSafe is

VibeSafe reads code produced by AI coding tools — **Lovable, Bolt, Cursor, Replit,
v0, Windsurf, Firebase Studio** — and flags the security problems those tools
routinely ship, explained in plain English rather than security jargon.

It exists because AI coding assistants optimise for *"make the demo work"*, not
*"make it safe to put on the internet"*. The gap between those two goals is where
founders get hurt: a live Stripe key sitting in a frontend bundle, a Supabase table
with no row-level security, an admin route with no auth check.

## What it checks

| Category | Examples |
|---|---|
| **Secrets** | Hardcoded `sk_live_` keys, Supabase `service_role` keys, JWT signing secrets |
| **Injection** | SQL injection, XSS, command and template injection |
| **Access control** | Missing Supabase RLS, unauthenticated admin routes, path traversal, IDOR |
| **Authentication** | Plaintext password comparison, weak JWT config, missing auth middleware |
| **Supply chain** | Vulnerable dependencies (checked against [OSV.dev](https://osv.dev)), hallucinated / slopsquatted packages |
| **Configuration** | Missing security headers, permissive CORS, exposed `.env` and `.git/config` |
| **Reliability** | Missing awaits, unhandled errors, and stateful flows that only implement the happy path |

Findings are mapped to the [OWASP Top 10:2025](https://owasp.org/Top10/2025/) —
A01 Broken Access Control, A03 Software Supply Chain Failures, A05 Injection, and so
on. Reliability defects are deliberately left unmapped rather than forced into a
security category, so OWASP coverage reflects what was actually assessed.

## How to use it

- **Web, no signup** — paste code at [vibesafe.info/try](https://www.vibesafe.info/try)
- **VS Code & Cursor** — [VS Marketplace](https://marketplace.visualstudio.com/items?itemName=vibesafe-info.vibesafe-scanner) · [Open VSX](https://open-vsx.org/extension/vibesafe-info/vibesafe-scanner)
- **Live URL scan** — checks a deployed site's security headers and exposed paths
- **Launch Check** — opens your app in a real browser, clicks through it like a first-time
  visitor, and reports broken pages, console errors and failed requests with screenshots

## What it deliberately does not do

Being clear about limits matters more in security than most categories — a tool that
overstates its coverage is worse than no tool at all.

- It is **not a penetration test** and does not replace a professional security audit
- It does **not detect whether a site has already been compromised** — no malware,
  defacement or backdoor detection. It checks whether you *can* be attacked, not
  whether you already have been
- Launch Check is **passive**: it never submits forms or clicks destructive buttons on
  a live app, so it won't catch problems that only appear mid-way through a multi-step flow
- It does not guarantee complete vulnerability coverage. It targets the mistakes that
  appear over and over in AI-generated code

## About this repository

Static site: marketing pages, blog, product dashboard, and sitemap for vibesafe.info.
The scanning API lives separately and is not open source.

- **Website** — [vibesafe.info](https://www.vibesafe.info)
- **How it works** — [vibesafe.info/how-it-works](https://www.vibesafe.info/how-it-works)
- **Security & data handling** — [vibesafe.info/security](https://www.vibesafe.info/security)
- **About** — [vibesafe.info/about](https://www.vibesafe.info/about)

Your code is analysed and discarded. It is not stored, and it is not used to train models.

---

Built and operated by **SG Digital Ventures LLC** (Wyoming, USA).
Contact: [contact@vibesafe.info](mailto:contact@vibesafe.info)
