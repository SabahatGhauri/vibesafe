# Original Research Report — plan and generator

The point of this report is backlinks. Synthesis of other people's studies does not
earn them: a journalist who wants the "45% of AI code has a vulnerability" figure
cites the original study, not our summary. Only data **nobody else has** gets cited,
and the scan corpus is the only such data VibeSafe owns.

The existing `state-of-vibe-coding-security-2026.html` is a synthesis and says so in
its own methodology. It should stay (it is a decent explainer), but it will never
attract links. This is the replacement.

---

## Do not publish before these thresholds are met

As of 2026-08-23 the corpus is **154 scans from 6 distinct users**. That is not a
study of the ecosystem — it is a handful of people, most likely including our own
testing. Publishing it as "we analysed 154 AI-built applications" would be
misleading, and in a security niche the methodology *will* be questioned.

Publish only when all three hold:

| Threshold | Why | Current |
|---|---|---|
| **≥ 300 distinct users** | The unit of study is an app/developer, not a scan. A few users running many scans is one sample, not many. | 6 |
| **≥ 1,000 scans** | Enough that per-category rates are stable rather than noise. | 154 |
| **Own scans excluded** | Founder/testing accounts skew everything and are indefensible if audited. | not excluded |

Run `sql/00_readiness.sql` below to check. Until it passes, do not publish numbers.

If you want to publish sooner, the honest option is to narrow the claim rather than
inflate it: "the first 200 applications scanned by VibeSafe" is credible at small N
**if the N is stated plainly in the headline**, not buried in a methodology note.

---

## Structure

Each section leads with a number only we can produce. That is the citable unit.

1. **Headline** — "We scanned N AI-generated applications. X% shipped at least one
   critical issue." One sentence, one number, quotable without context.
2. **What breaks most often** — ranked category table with % of apps affected.
   The strongest section: nobody else has per-category prevalence for AI-built apps.
3. **Severity mix** — critical / warning / info split. Frames how much of the
   finding volume is actually urgent.
4. **By language / stack** — where the differences are real and the N per group is
   large enough to report. Skip any group under ~30 apps.
5. **OWASP mapping** — share of findings that map to an OWASP category. Gives
   security readers a familiar frame and makes the report quotable in their terms.
6. **Methodology** — sample size, date range, how apps were collected, what was
   excluded, and the known limitations. Write this section honestly and in full;
   it is what makes the rest citable rather than dismissible.
7. **Citation block** — pre-written attribution line, as the current report already
   does. Make it trivially easy to cite correctly.

---

## Generator SQL

All queries normalise issue types with the same rules as `api/scan.js`
(`canonicalCategory`), so historical rows and new rows count together. New rows
also carry a stored `category`; these queries deliberately re-derive it so the two
eras stay consistent.

```sql
-- shared normaliser, matching api/scan.js CATEGORY_RULES (first match wins)
create or replace function canonical_category(t text) returns text language sql immutable as $$
  select case
    when t ~* 'row[- ]?level security|\mrls\M'            then 'Missing Row-Level Security'
    when t ~* 'exposed secret|hardcoded|api key|credential|token' then 'Exposed Secret'
    when t ~* 'sql injection|sqli'                        then 'SQL Injection'
    when t ~* 'xss|cross[- ]site scripting'               then 'Cross-Site Scripting'
    when t ~* 'csrf|cross[- ]site request'                then 'CSRF'
    when t ~* 'auth|access control|permission|authoriz'   then 'Broken Authentication & Access Control'
    when t ~* 'await|async'                               then 'Missing Await'
    when t ~* 'input validation|sanitiz|unvalidated'      then 'Missing Input Validation'
    when t ~* 'error handling|unhandled|try.?catch'       then 'Missing Error Handling'
    when t ~* 'dependency|package|cve|vulnerable lib'     then 'Vulnerable Dependency'
    when t ~* 'security header|csp|content[- ]security'   then 'Missing Security Header'
    when t ~* 'syntax error'                              then 'Syntax Error'
    when t ~* 'logic error|assignment instead'            then 'Logic Error'
    when t ~* 'code quality|readability|maintainab'       then 'Code Quality'
    else 'Other'
  end;
$$;
```

```sql
-- 00_readiness.sql — gate. Do not publish unless this says ready.
select count(*) scans,
       count(distinct user_id) users,
       min(created_at)::date first_scan,
       max(created_at)::date last_scan,
       case when count(distinct user_id) >= 300 and count(*) >= 1000
            then 'READY' else 'NOT READY — sample too small' end as verdict
from scans
where user_id is not null
  and user_id not in (/* founder + test account uuids go here */);
```

```sql
-- 01_headline.sql — the quotable number
with app as (
  select s.id,
         bool_or(i->>'sev' = 'critical') as had_critical
  from scans s left join lateral jsonb_array_elements(coalesce(s.results->'issues','[]'::jsonb)) i on true
  group by s.id
)
select count(*) as apps_scanned,
       count(*) filter (where had_critical) as apps_with_critical,
       round(100.0 * count(*) filter (where had_critical) / nullif(count(*),0), 1) as pct_with_critical
from app;
```

```sql
-- 02_categories.sql — the strongest section: % of apps affected per category
with per_app as (
  select distinct s.id, canonical_category(i->>'type') as category
  from scans s, lateral jsonb_array_elements(coalesce(s.results->'issues','[]'::jsonb)) i
), total as (select count(*)::numeric n from scans)
select category,
       count(*) as apps_affected,
       round(100.0 * count(*) / (select n from total), 1) as pct_of_apps
from per_app group by category order by apps_affected desc;
```

```sql
-- 03_severity.sql
select i->>'sev' as severity,
       count(*) as findings,
       round(100.0 * count(*) / sum(count(*)) over (), 1) as pct
from scans s, lateral jsonb_array_elements(coalesce(s.results->'issues','[]'::jsonb)) i
group by 1 order by 2 desc;
```

```sql
-- 04_by_language.sql — report only groups with n >= 30
select coalesce(nullif(language,''),'unknown') as language,
       count(*) as apps,
       round(avg(score),1) as avg_score,
       round(avg(issues_count),2) as avg_issues
from scans group by 1 having count(*) >= 30 order by apps desc;
```

```sql
-- 05_owasp.sql — share of findings carrying an OWASP mapping
select i->>'owasp' as owasp_category, count(*) findings
from scans s, lateral jsonb_array_elements(coalesce(s.results->'issues','[]'::jsonb)) i
where i ? 'owasp' and i->>'owasp' <> ''
group by 1 order by 2 desc;
```

---

## Promotion (this is where the links come from)

Publishing is not the work; distribution is. In order:

1. **Send it to people who cover this beat** before publishing publicly — a short
   note with the single headline number, not a press release.
2. **Post the finding, not the link**, on Reddit/HN/Dev.to. A number is discussable;
   a link is an ad. The link belongs in the comments or the byline.
3. **Cross-post to Dev.to and Hashnode** with canonical back to vibesafe.info, as
   the existing 6 Dev.to posts already do.
4. **Answer journalist requests** (Qwoted, Featured) on AI-code-security topics.
   Original data is what makes a source worth quoting.
5. **Refresh annually.** "State of X 2027" earns the links again, and year-over-year
   comparison is itself a story.

## Known limitations to state in the methodology, not hide

- Self-selected sample: people who run a security scanner are not a random sample of
  builders. Likely biases toward the security-aware, which understates real rates.
- Scans are of code submitted to VibeSafe, not necessarily of deployed apps.
- Findings are produced by an LLM-based scanner and carry its false-positive rate.
- Category prevalence reflects what the scanner looks for; it cannot report issue
  classes it does not check.
