# Zocdoc - module status: field map only, no hard limits (confirmed, not just unverified)

Zocdoc's public provider-help articles (checked September 2026) describe bio
best practices but don't publish an exact character limit for the bio field.
**Do not assume PT's limits transfer.** This was independently confirmed
during the Michael Lydon 2026-06-26 Zocdoc engagement (see `_local/` in the
repo root): "Zocdoc doesn't publish character limits for these fields."
`field-map.md` here reflects that engagement's real field names and observed
comfortable lengths - treat those as scannability guidance, not caps.

Before running an engagement against this module:

1. Log into the client's (or a test) Zocdoc provider dashboard and check the
   actual bio field's live character counter, or ask Zocdoc support/your
   account rep directly.
2. Record confirmed limits in a `limits.json` here, in the same shape as
   `deliverables/psychology-today/limits.json`, with a `source` field noting
   how it was confirmed (dashboard screenshot, support reply, date).
3. Only then does `tools/check_limits.py` and `tools/build_docx.py` have
   something to enforce against - until a `limits.json` exists here, the
   checker will run in lint-only mode (dash rule + count accuracy, no caps).

## What's known and reusable now

- Positioning source is the same ICP (`_templates/icp-profile-template.md`)
  used for every other deliverable - build the field map
  (`field-map.md`, once limits are confirmed) the same way
  `deliverables/psychology-today/field-map.md` does.
- Zocdoc's mental-health provider guidance emphasizes plain-language
  specialties and a bio that reads like it's speaking directly to a
  first-time patient - consistent with this project's existing house style.

Sources: https://www.zocdoc.com/provider-help/en/articles/8922648-best-practices-for-mental-health-provider-profiles ,
https://www.zocdoc.com/provider-help/en/articles/9613181-profile-guidelines
