# Practice Content Platform

A repeatable system for turning one client intake into every piece of
client-facing copy a therapy practice needs: directory profiles (Psychology
Today, Zencare, Zocdoc, Google Business Profile, the Private Practice
Directory) and website content (homepage, approach page, clinician bios,
FAQ). One dataset, one positioning document, many deliverables - so a
practice's voice, specialties, and trust signals stay consistent everywhere
a prospective client encounters them.

This repo grew out of a Psychology Today-only tool (see
`docs/sessions/2026-06-15-1244-pt-profile-optimizer-buildout.md` for that
history); the PT module is still the most complete one and the reference
pattern every other module follows.

## How it fits together

```
_ref/intake-questionnaire.md   <- raw client answers (practice-wide, multi-platform)
        |
        v
_templates/icp-profile-template.md   <- one ICP/positioning doc per client,
                                         built once, reused by every deliverable
        |
        v
deliverables/<module>/          <- one folder per output type:
  field-map.md                     maps ICP/intake answers -> that platform's fields
  limits.json                      that platform's character limits (if any) - single
                                    source of truth, sourced and dated
  template.md                      blank, paste-ready deliverable template
```

Every engagement lives in `clients/<slug>/`, with the client's `intake.md`
and `icp.md` at the top level and one subfolder under `deliverables/` per
platform being optimized for that client.

## The three goals, on every surface

Whether it's a directory profile field or a website page, every deliverable
is optimizing for the same three things without erasing the clinician's
voice:

1. **Search visibility** - appearing in the right filters/keywords and
   ranking for the terms real seekers type.
2. **First-impression conversion** - making the preview text and the top of
   the page/profile earn the click and the inquiry.
3. **Trust consistency** - the same credentials, consult length, and voice
   everywhere, so nothing quietly contradicts itself between the website and
   a directory listing.

## Modules (deliverable types)

| Module | Status |
|---|---|
| `deliverables/psychology-today/` | Complete - limits confirmed, field map, template, full playbook. |
| `deliverables/website-content/` | New - no platform character caps, so it's structural (page/section) rather than field-by-field. Same ICP, same voice rules. |
| `deliverables/google-business-profile/` | New - limits confirmed (description, Posts). |
| `deliverables/zencare/` | Stub - field map pending; **character limits unverified**, confirm in the provider portal before first use. |
| `deliverables/zocdoc/` | Stub - field map pending; **character limits unverified**, confirm in the provider dashboard before first use. |
| `deliverables/private-practice-directory/` | Stub - internal MHM product; schema/limits owned by whoever runs that product, not a public source. |

Adding a new module means adding a new `deliverables/<name>/` folder in the
same shape - `field-map.md`, `limits.json` if the platform has real limits,
and `template.md`. `tools/check_limits.py` and `tools/build_docx.py` are
shared across every module; they infer which `limits.json` applies from the
deliverable file's parent folder name.

## Psychology Today character limits (reference)

Source: https://reframepractice.com/answers/psychology-today/best-psychology-today-profiles
(confirmed current as of the April 2026 version of that guide).

### Personal statement boxes

| Field | Box label | Limit |
|---|---|---|
| Part 1 - Ideal Client | "What can I help you with?" | 640 |
| Part 2 - Approach | "What's my approach?" | 360 |
| Part 3 - About Me / Authority + CTA | "About me" | 360 |

- Total cap across all three boxes: **1,360 characters**.
- The **first 270 characters of Box 1** appear as the directory search-result
  preview, so the strongest symptom keywords and hook belong up front.

### Structured note fields

| Field | Limit |
|---|---|
| Intro to new clients | 140 |
| Note on Finance | 300 |
| Note on Credentials (Qualifications) | 300 |
| Note on Top Specialties | 400 |
| Note on Therapy Types (Treatment Approach) | 400 |

### Other

| Field | Limit |
|---|---|
| Tagline | 160 |

### Drafting rule of thumb

Write to roughly **80% of each limit** so copy does not truncate on smaller
screens. Treat the numbers above as hard ceilings and the 80% figure as the
comfort target. `deliverables/psychology-today/limits.json` is the single
source of truth for the numbers; the checker reads from it, so update it
there if PT changes a limit. Never eyeball length: run the checker before
delivery. Each other module keeps its own `limits.json` the same way.

## Running an engagement

See `PROCESS.md` for the full playbook. In short:

1. Build (or update) the client's ICP: copy
   `_templates/icp-profile-template.md` into `clients/<slug>/icp.md` and fill
   it from the intake questionnaire (or an existing profile/website, in
   refine mode).
2. For each platform/page being optimized, copy that module's
   `deliverables/<module>/template.md` into
   `clients/<slug>/deliverables/<module>/` and draft the copy from the ICP.
3. Verify and set counts:
   ```
   python3 tools/check_limits.py clients/<slug>/deliverables/<module>/<file>.md --update
   python3 tools/check_limits.py clients/<slug>/deliverables/<module>/<file>.md
   ```
   The second run must report PASSED. It also blocks em/en dashes. Beyond
   what the checker enforces, house style also rules out AI-isms generally
   (see `PROCESS.md` Hard rules) - clear, direct, and warm, not generated.
4. Generate the client document and deliver:
   ```
   python3 tools/build_docx.py clients/<slug>/deliverables/<module>/<file>.md
   ```
   This writes a namespaced, datetimestamped `.docx` into the deliverable
   folder (e.g. `michael-lydon-psychology-today-optimized-2026-09-03-113341.docx`)
   so revision runs never overwrite an earlier delivery. Upload it to Google
   Drive, open it as a Google Doc, and share the link. Each copy block is a
   boxed table the client can copy cleanly.

## Setup

```
pip install -r requirements.txt
```

## Repo layout

- `_ref/` - shared source material (the practice-wide intake questionnaire).
- `_templates/icp-profile-template.md` - blank ICP/positioning template, the
  shared foundation for every deliverable.
- `deliverables/<module>/` - one per output type (see table above): that
  platform's `field-map.md`, `limits.json` (if it has real limits), and
  `template.md`.
- `tools/check_limits.py` - verifies a deliverable fits its module's limits
  (or lints dash-cleanliness/counts only, for modules with no hard caps).
- `tools/build_docx.py` - builds the client-facing boxed `.docx` from a
  module's `.md`, for any module.
- `requirements.txt` - Python dependencies (`python-docx`).
- `PROCESS.md` - the general playbook: build the ICP first, then run any
  number of deliverable modules from it.
- `clients/<slug>/` - per client: `intake.md`, `icp.md`, and
  `deliverables/<module>/` (each with its own `source/` inputs, working
  `.md`, and namespaced `.docx` deliverables, git-ignored) per platform/page
  set optimized for that client.
- `docs/sessions/` - dated session summaries (project history).
