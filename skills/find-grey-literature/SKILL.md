---
name: find-grey-literature
description: Finds grey literature on a topic — practitioner blog posts, engineering write-ups, newsletters, vendor and institutional posts — by discovering the top sites in the field, searching them, independently verifying every result, and writing a Markdown report of links, titles, and summaries. Use when the user asks to find grey literature, survey what practitioners or industry are writing about a topic, scan the top blogs in a field, do a non-academic or multivocal literature scan, or collect recent posts on a subject into a report. Not for peer-reviewed paper search, and not for a quick one-off web lookup.
---

# Find Grey Literature

Turns a topic into a verified, citable report of practitioner writing from the web.

The defining constraint: **nothing in the report may be invented.** Every item is
a real URL that a separate verifier agent fetched and confirmed. A run that
returns four solid items is a success. A run that returns ten, two of which were
padded from memory, is a failure.

## Requirements

This skill needs `WebSearch`, `WebFetch`, and the `Agent` tool. If any is
unavailable, **stop and tell the user.** Do not fall back on recalled URLs or
remembered blog posts — model recall of specific post titles and links is
exactly the failure mode this skill exists to prevent.

## Invocation

Triggers on natural phrasing, including:

- "find grey literature on <topic>"
- "what are practitioners writing about <topic>"
- "survey the top blogs on <topic>"
- "scan industry writing about <topic>, give me 15 max"
- "grey lit review of <topic>, last 6 months"
- "collect recent posts about <topic> into a report"

Parse whatever the user already gave — topic, item count, area, time window,
named sources — and **never re-ask for something they already said.** The
clarification steps below exist to fill gaps, not to run a script.

### Defaults

| Setting | Default | Override |
| --- | --- | --- |
| Item limit | 10 | Any number the user states |
| Time window | Last 12 months | "last 6 months", "since 2024", etc. |
| Report path | `./grey-lit-<topic-slug>-<YYYY-MM-DD>.md` | Any path the user names |

**The item limit is a ceiling, not a target.** Returning fewer verified items
than requested is correct and expected. Never pad toward the number.

## Procedure

### 1. Confirm the topic

Restate the topic as you understand it and confirm. Where the keyword is
genuinely ambiguous, ask — but ask about *this* keyword, not from a checklist.
Things worth asking about when they apply:

- An acronym or term with a collision ("RAG", "ACL", "transformers")
- A term that spans disciplines, where the user's field changes everything
- Whether a nearby subtopic is in or out of scope
- Whether the user wants a specific angle: benchmarks, failure reports,
  migration write-ups, cost analyses, adoption experiences

Ask only what will change the search. One round, batched into a single message.

### 2. Settle the area

Name the field or community this search will target and confirm it. The area
determines which sites are credible, so getting it wrong wastes the whole run.
"Machine learning" and "MLOps platform engineering" produce different source
lists for the same keyword.

### 3. Discover the source list

**Search for the sources. Do not list them from memory.** Run `WebSearch`
queries designed to surface where the field actually publishes:

- `best blogs <area> <current year>`
- `<area> engineering blog`
- `top <area> newsletters`
- `<topic> writeup OR postmortem OR "lessons learned"`

Assemble 6–12 candidate sources. For each, record the site name, its type
(independent blog, company engineering blog, vendor, newsletter, forum,
institutional), and one line on why it belongs. Institutional sources — lab
reports, white papers, standards bodies — belong on the list when they are
genuinely a top venue for this area; do not go hunting for them separately, and
do not include preprint servers as general-purpose sources.

Present the list and ask the user to add, drop, or approve.

When the user names a source, **check it before adding it** — it gets the same
scrutiny as anything your own search surfaced. Fetch the site and confirm it
resolves, that it is a live publication rather than a parked domain or an
abandoned archive, that it publishes on this area, and that it has posts inside
the window. Then:

- **Checks out** — add it.
- **Dead, parked, or off-area** — say what you found and ask whether to drop it
  or proceed anyway. The user may know something the homepage does not show:
  a feed that moved, a section behind a different path.
- **Live and on-area but thin in the window** — add it, and say how little is
  there, so the low yield is not a surprise at report time.

The user's judgement wins on a borderline call. What is not negotiable is that
the check happens and its result is reported before the source is searched.

### 4. Search within the approved sources

For each approved source, search for posts on the topic inside the time window.
Use site-scoped queries (`site:example.com <topic>`) alongside plain topical
queries, since some sites index poorly.

Collect candidates as: title, URL, source, apparent publication date. Gather
noticeably more candidates than the item limit — verification will reject some,
and backfilling from a pool beats re-searching.

Drop immediately, before verification: pure marketing pages with no substance,
link roundups with no original content, and anything outside the window.
Paywalled pages are dropped as well — see below.

### 4a. Paywalled pages

A page you cannot read in full is not a page you can summarize. Paywalled
candidates are dropped here, not worked around.

The tells: a "Member-only story" banner, a subscribe or register wall over the
body, an article that cuts off a few paragraphs in, or a metered "you have N
free articles left" notice.

- **Drop the candidate** and record it in the exclusion table as
  `paywalled-unreadable`.
- **Never** summarize a paywalled post from its preview, its title, its
  metadata, or prior knowledge of it.
- **Do not** route it through a mirror, a reader proxy, a cache, an archive
  snapshot, or any other paywall bypass. If the publisher gated the text, the
  post is out of scope for the report.

Backfill from the candidate pool instead — this is why step 4 collects more
candidates than the item limit.

### 5. Draft summaries

Fetch each surviving candidate with `WebFetch` and write a 2–4 sentence summary:
what it covers, what is actually new or useful in it, and who it is for. Summaries
describe what the page says — not what the title suggests it probably says.

### 6. Verify — mandatory

Every item goes to a verifier agent that did not do the searching. See
[references/verifier-prompt.md](references/verifier-prompt.md) for the prompt to pass.

Spawn verifiers with the `Agent` tool using `subagent_type: general-purpose`,
batching **at most 4 items per verifier** and running the batches in parallel.

A verifier returns, per item: `PASS`, `FAIL`, or `FLAG` with a reason. Then:

- **PASS** — include it.
- **FAIL** — drop it. Record it in the report's exclusion table with the reason.
- **FLAG** (summary overstates, date uncertain, content thin) — correct the
  summary from the verifier's notes and include it, or drop it. Never ship a
  flagged summary unchanged.

If verified items come in under the limit, backfill from the remaining candidate
pool and verify those too. If the pool is exhausted, **report fewer items** and
say so. Do not loosen the window or the source list to hit a number without
asking the user first.

### 7. Write the report

Follow [references/report-template.md](references/report-template.md). Write it to
`./grey-lit-<topic-slug>-<YYYY-MM-DD>.md` unless the user named a path.

Then reply in the terminal with: the path, the verified count against the
requested limit, how many were excluded and why, and any gap worth knowing about
— a dead area, a source that returned nothing, a window that was too narrow.

## Failure modes to avoid

- **Padding to the number.** The limit is a ceiling. Say "6 of up to 10".
- **Recalling URLs.** If you did not get a URL from a search result this run,
  it does not go in the report.
- **Rubber-stamp verification.** The verifier forms its own read of the page
  before it sees the draft summary. Preserve that ordering in the prompt.
- **Title-based summaries.** Summarize fetched content, not the headline.
- **Silent drops.** Every excluded candidate appears in the exclusion table.
- **Taking a source on trust** because the user named it. Check it, then report
  what you found.
- **Skipping clarification when the topic is ambiguous** — or grinding through
  all three clarification steps when the user already specified everything.
