# JSON Data

These files are fixed data tables. Preserve their keys, values, and ordering when formatting them.

## Character Generation

- `roles.json` maps title-cased role names to their role skill names.
- `statitics_role.json` maps title-cased role names to lists of ten-stat profiles. The filename is misspelled but is kept for compatibility with `Kitty.py`.
- `skills.json` maps lowercase role names to skill-name/rank objects.

Role names therefore use different casing between the stat table and skills table. Normalize role names in code when combining these files; do not rename the stored keys without updating their consumers.

Skill names are descriptive lookup keys, not a normalized vocabulary. Their capitalization, punctuation, and spelling are retained as stored data.

## Critical Injuries

- `body_crits.json` and `head_crits.json` map injury names to `Effect`, `Quick Fix`, and `Treatment` text.
- Entry order is significant to `red_die.py`, which selects an injury by its position in the object keys.

## Other Data

- `cat.json` is a list of strings used as cat expressions.
- `moons/<year>.json` contains lunar phase events with `Date` and `Phase` fields. These files are cached data, not fixed game tables.

## Validation

All files must remain valid UTF-8 JSON. Formatting changes should not change parsed values or object key order.