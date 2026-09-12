---
name: example-skill
description: Explains the layout and conventions of the skills-no-where-to-be-found repository. Use only when the user is adding, editing, or reviewing a skill inside this specific repository, or asks how this repo is structured. Not relevant to any other task.
---

# Example Skill

This is a placeholder so the collection is installable and testable before the
first real skill lands. Delete it once you have shipped something real.

## Repository layout

```
.claude-plugin/marketplace.json   # marketplace manifest; lists every skill
skills/<skill-name>/SKILL.md      # one directory per skill
templates/skill-template/         # copy this to start a new skill
scripts/validate_skills.py        # frontmatter + manifest consistency check
```

## Adding a skill

1. `cp -r templates/skill-template skills/<skill-name>`
2. Rewrite `SKILL.md`. The `name` in the frontmatter must match the directory
   name exactly.
3. Add `"./skills/<skill-name>"` to the `skills` array in
   `.claude-plugin/marketplace.json`. A skill that is not listed there is not
   installed for anyone.
4. Run `python3 scripts/validate_skills.py`.

## Writing the description

The `description` is the only part of a skill that is always in context, so it
is the only thing deciding whether the skill gets loaded. Write it for that job:

- Say what the skill does, then say when to use it.
- Name the concrete nouns and verbs a user would actually type. Those are the
  match surface.
- State what it is *not* for when the topic is crowded, so it stays quiet during
  unrelated work.
- Keep it to one or two sentences and write it in the third person.

## Writing the body

The body only loads once the skill triggers, so it can be longer — but every
line competes with the task at hand. Prefer procedures over prose, put the
common path first, and move anything reference-shaped (schemas, long tables,
API surfaces) into a sibling file the body points to.
