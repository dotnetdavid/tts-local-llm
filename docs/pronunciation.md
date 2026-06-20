# Pronunciation Rules

Pronunciation rules are ordered exact replacements applied before chunking.

Example:

```yaml
pronunciations:
  - source: "Mara Vey"
    replacement: "Mara Vay"
  - source: "Rec Center"
    replacement: "wreck center"
```

Use this for spoken rendering only. Do not mutate the manuscript just to satisfy TTS.

Rules are intentionally simple:

- Exact phrase replacement.
- Applied in file order.
- Case-sensitive.

If a later version needs regex, add it deliberately with tests. Do not casually make pronunciation substitution clever; clever text replacement is where small tools become fragile.
