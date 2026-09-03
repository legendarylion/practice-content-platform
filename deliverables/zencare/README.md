# Zencare - module status: field map only, limits unverified

Zencare profiles don't publish character limits the way Psychology Today
does, and a web search (September 2026) didn't turn up a documented cap for
the bio/professional-statement fields. **Do not assume PT's limits transfer.**

Before running an engagement against this module:

1. Log into the client's (or a test) Zencare provider portal and check the
   actual field character counters live, or ask Zencare support directly.
2. Record confirmed limits in a `limits.json` here, in the same shape as
   `deliverables/psychology-today/limits.json`, with a `source` field noting
   how it was confirmed (portal screenshot, support reply, date).
3. Only then does `tools/check_limits.py` and `tools/build_docx.py` have
   something to enforce against - until a `limits.json` exists here, the
   checker will run in lint-only mode (dash rule + count accuracy, no caps).

## What's known and reusable now

- General expertise and treatment-approach tags: max 20 items each.
- Zencare has no per-zip/per-state profile limit like PT (one profile covers
  every area served, in-person and telehealth, with no extra charge).
- Positioning source is the same ICP (`_templates/icp-profile-template.md`)
  used for every other deliverable - build the field map
  (`field-map.md`, once limits are confirmed) the same way
  `deliverables/psychology-today/field-map.md` does.

Sources: https://therapist.zencare.co/zencare-faq ,
https://help.zencare.co/hc/en-us/articles/47048599472667-What-additional-fields-can-I-add-to-strengthen-my-profile
