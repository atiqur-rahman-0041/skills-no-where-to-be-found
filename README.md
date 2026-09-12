# skills-no-where-to-be-found

Agent skills I went looking for, couldn't find anywhere, and ended up writing.

Every skill here exists because the gap was real: nothing in the built-ins,
nothing in [anthropics/skills](https://github.com/anthropics/skills), nothing in
the official marketplace. If a good version shows up upstream, the one here
should go away.

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

### Just one skill

Skills are portable files, not a framework. Copy one into your personal skills
directory and it works the same way:

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
| [example-skill](skills/example-skill/SKILL.md) | Placeholder describing this repo's own conventions. Deleted as soon as a real skill lands. |

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
