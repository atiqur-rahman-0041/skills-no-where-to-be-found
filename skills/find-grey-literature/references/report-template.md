# Report template

Structure for the generated report. Drop sections that have no content — an
empty exclusion table is better omitted than shown empty — but keep Sources,
Findings, and Method always.

---

# Grey literature: [TOPIC]

| | |
| --- | --- |
| **Area** | [confirmed area] |
| **Compiled** | [YYYY-MM-DD] |
| **Window** | [START] to [END] ([description, e.g. last 12 months]) |
| **Requested** | up to [N] items |
| **Verified** | [M] items |

[One or two sentences on what this scan covered and anything the reader should
know up front — a thin area, a dominant source, a notable gap.]

## Sources searched

| Source | Type | Why included | Items found |
| --- | --- | --- | --- |
| [name] | [blog / company eng / vendor / newsletter / forum / institutional] | [one line] | [n] |

## Findings

### 1. [Title]

- **Link:** [canonical original url — always the citation, never the mirror]
- **Source:** [site] · [type]
- **Published:** [YYYY-MM-DD]
- **Read via:** [mirror url — only for Medium member-only posts; omit otherwise]

[2–4 sentence summary: what it covers, what is new or useful in it, who it is
for. Verified against the fetched page.]

### 2. [Title]

[...]

## Excluded after verification

| Candidate | URL | Reason |
| --- | --- | --- |
| [title] | [url] | [dead link / title mismatch / out of window / off-topic / summary unsupported / thin / paywalled-unreadable] |

## Method

- **Source discovery:** [queries used to find the sites]
- **Item search:** [query patterns used within sources]
- **Verification:** every item above was fetched and checked by an independent
  verifier agent for link resolution, title match, topical relevance,
  publication date, and summary accuracy. [M] passed, [X] were excluded,
  [Y] had summaries corrected.
- **Gaps:** [sources that returned nothing, subtopics with no coverage, date
  ranges that came up empty — anything that would change how the reader reads
  this report]
