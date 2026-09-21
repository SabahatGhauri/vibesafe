# SEO & security agents

Two small tool-using agents that share one hand-written agent loop. No
framework, stdlib plus the `anthropic` SDK.

```
agent.py       the loop + a code-security scanner's tools
seo_agent.py   the same loop, imported unchanged, with SEO/indexing tools
```

`seo_agent.py` opens with `from agent import AgentLoop, ...` — the loop is
reused byte for byte. Only the tool registry differs. That is the design: the
loop is invariant, the tools are the product.

## Run it

Both agents run with a scripted stand-in model, so you can watch the loop work
with no API key:

```bash
python3 seo_agent.py --offline --local .                    # audit this site
python3 agent.py     --offline .                            # security scan
```

With a key, the model drives:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python3 seo_agent.py --local . --live https://www.vibesafe.info
python3 agent.py --report /path/to/project
```

## What the SEO agent checks

It walks the gates in the order Google applies them and stops at the first
hard blocker:

| Gate | Tools |
|---|---|
| Crawlable | `fetch_url` (status, redirect chain, `X-Robots-Tag`, TTFB as Googlebot), `check_robots` |
| Indexable | `page_seo` (meta robots, canonical), `audit_pages` |
| Discoverable | `audit_sitemap` (sitemap ↔ files on disk, noindex conflicts, orphan pages), `read_robots` |
| Quality | `find_duplicates`, title/description length, h1 count, thin content |

The four `audit_*` / `read_*` / `find_*` tools work offline against a
directory. The four live tools fetch over HTTP as Googlebot.

A hard blocker (noindex, `Disallow`, 404, canonical pointing elsewhere) means
a page *cannot* rank. A soft issue (long title, thin content) means it ranks
worse. The agent is told to report the difference, and to say plainly when the
evidence points at domain age or authority rather than anything in the files.

## The loop

Five ingredients, marked `[1]`–`[5]` in `agent.py`:

1. **Message buffer** that grows — the whole `response.content` is appended,
   not just the text, so thinking and `tool_use` blocks replay correctly.
2. **Tool registry** — a tool that is not registered cannot be called. Least
   privilege is enforced by composition: `agent.py`'s write tool only exists
   with `--report`.
3. **Stop conditions** — `end_turn`, no tool calls, `refusal`, `max_tokens`.
4. **Turn budget** — a hard cap the model does not control.
5. **Observation formatter** — every failure becomes a string the model can
   read and recover from. Nothing raises out of `dispatch`.

Parallel tool calls return all their results in one user message, each tagged
with its `tool_use_id`, failures included and marked `is_error`.

## Boundaries

Tool output is untrusted input. The defenses are in code, not in the prompt:

- **Sandbox** — every path is resolved and checked against a root, so `../`
  and absolute paths fail as observations rather than reading the filesystem.
- **Least privilege** — destructive tools are not registered unless asked for.
- **Confirmation gate** — tools marked `destructive` stop for a human.
- **Taint marking** — file contents come back wrapped in
  `<untrusted-file-content>` and the system prompt says that is data, never
  instruction. This is the weakest layer, so it is the outermost one.

## Tools lie before prompts do

Both false positives found while building this were tool bugs, not prompt
problems: `glob` instead of `rglob` missed every page in `blog/`, and assuming
clean URLs turned `/demo.html` into `demo.html.html`. Neither was fixable by
rewording anything. Verify a finding against the filesystem before acting on
it.
