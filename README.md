# skills-no-where-to-be-found

Agent skills I went looking for, couldn't find anywhere, and ended up writing.

The repo is packaged as a Claude Code plugin marketplace, so the whole
collection installs with two commands — but each skill is a plain directory with
a `SKILL.md`, so you can also just copy the one you want.

## Install

```
/plugin marketplace add atiqur-rahman-0041/skills-no-where-to-be-found
/plugin install skills-no-where-to-be-found@skills-no-where-to-be-found
```

That's it. Skills load themselves when a task matches their description; there
is nothing to configure and nothing to invoke by hand.

To update later:

```
/plugin marketplace update skills-no-where-to-be-found
```

### Without the plugin system, with `npx`

Skills are portable directories, not a framework. The
[`skills`](https://github.com/vercel-labs/skills) CLI installs one straight out
of this repo — no clone, nothing installed globally:

```bash
npx skills add atiqur-rahman-0041/skills-no-where-to-be-found --skill <skill-name>
```

For example, for the one skill in here today:

```bash
npx skills add atiqur-rahman-0041/skills-no-where-to-be-found --skill find-grey-literature
```

That puts the skill in `.agents/skills/` in the current project, symlinks it
into `.claude/skills/` and the equivalent directory for every other agent it
detects, and records the source and a content hash in `skills-lock.json`.

Add `-g` to install into your user-level skills directory instead of the
project, or `--all` to take every skill in the repo:

```bash
npx skills add atiqur-rahman-0041/skills-no-where-to-be-found --all -g
```

The full `https://github.com/...` URL works in place of the `owner/repo`
shorthand. `npx skills list` shows what is installed, and `npx skills update`
pulls later changes.

The `git` equivalent, if you would rather not reach for `npx`:

```bash
git clone https://github.com/atiqur-rahman-0041/skills-no-where-to-be-found.git
cp -r skills-no-where-to-be-found/skills/<skill-name> ~/.claude/skills/
```

Use `.claude/skills/` inside a project instead of `~/.claude/skills/` if the
skill should only apply to that project and be shared with the team through the
repo.

## What's in here

| Skill | What it does |
| --- | --- |
| [find-grey-literature](skills/find-grey-literature/SKILL.md) | Surveys practitioner blogs and industry writing on a topic, verifies every result with an independent agent, and writes a Markdown report of links, titles, and summaries. |

## Layout

```
.claude-plugin/marketplace.json   # marketplace manifest — the install entry point
skills/<skill-name>/SKILL.md      # one directory per skill
templates/skill-template/         # starting point for a new skill
scripts/validate_skills.py        # frontmatter + manifest consistency check
```

A skill is a directory with a `SKILL.md` whose frontmatter carries a `name` and
a `description`. The description is the part that is always in context — it is
what decides whether the skill loads at all. Everything below the frontmatter
loads only after it triggers.

The `skills` array in `.claude-plugin/marketplace.json` is the source of truth
for what ships. A directory that isn't listed there is invisible to anyone
installing through the marketplace.

## Adding a skill

```bash
cp -r templates/skill-template skills/my-skill
$EDITOR skills/my-skill/SKILL.md          # name must match the directory
$EDITOR .claude-plugin/marketplace.json   # add "./skills/my-skill"
python3 scripts/validate_skills.py
```

The validator checks that names match their directories, that descriptions
exist and fit the size limit, and that the manifest and the filesystem agree.
CI runs the same check on every push and pull request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the longer version, including the bar
for what belongs here.

## License

[MIT](LICENSE).
