# Contributing

This is a personal collection, but PRs are welcome if a skill fills a gap.

## Adding a skill

```bash
cp -r templates/skill-template skills/my-skill
$EDITOR skills/my-skill/SKILL.md
```

Then:

1. Set `name` in the frontmatter to match the directory name exactly.
2. Add `"./skills/my-skill"` to the `skills` array in
   `.claude-plugin/marketplace.json`.
3. Run the validator:

   ```bash
   python3 scripts/validate_skills.py
   ```

## Bar for inclusion

The point of this repo is skills that were *not* available elsewhere. Before
adding one, check that it isn't already covered by:

- the built-in skills shipped with Claude Code,
- [anthropics/skills](https://github.com/anthropics/skills),
- the official plugin marketplace (`/plugin marketplace add anthropics/claude-plugins-public`).

If something close already exists, contributing upstream is usually better than
adding a near-duplicate here.

## Style

- The `description` is the only part of a skill that is always in context, so it
  is the only thing deciding whether the skill loads. Write it for that job: say
  what the skill does, then when to use it; name the concrete nouns and verbs a
  user would actually type, since those are the match surface; state what it is
  *not* for when the topic is crowded, so it stays quiet during unrelated work.
  One or two sentences, third person.
- Bodies are procedures, not essays. Common path first.
- Anything over ~500 lines should be split out of `SKILL.md`. Supporting files
  go in `references/` (material the agent reads: prompts, templates, schemas),
  `scripts/` (executable code), or `assets/` (files copied into output).
- Skills must not require secrets to be committed. Read credentials from the
  environment and say so in the skill body.

## Testing a skill locally

```bash
/plugin marketplace add /path/to/this/repo
/plugin install skills-no-where-to-be-found@skills-no-where-to-be-found
```

Then run a prompt that *should* trigger it and one that should *not*, and check
`/context` to see whether it loaded.
