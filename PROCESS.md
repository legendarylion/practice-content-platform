# Optimization Process (Playbook)

How to run a content engagement from intake to delivered copy, across any
number of platforms and pages for one client. The goal on every surface:
improve search visibility, first-impression conversion, and trust
consistency without erasing the clinician's voice.

## Step 0: build the client's ICP (do this once, reuse everywhere)

Every deliverable in this repo - a Psychology Today profile, a Zencare
profile, a homepage - draws from the same positioning document. Build it
once per client, before drafting any platform-specific copy:

1. Create `clients/<slug>/icp.md` from `_templates/icp-profile-template.md`.
2. Fill it from the intake questionnaire (`_ref/intake-questionnaire.md`),
   sections 2.2 (Who You Serve) and 2.3 (Positioning & Differentiation) are
   load-bearing, plus 2.5 (Trust Assets) and 3.2 (Conversion Behavior).
3. If the client has existing copy (a live profile, an existing website),
   fold anything written in their own words into the ICP's Voice section as
   a reference to preserve, not something to discard.
4. Update `icp.md` whenever positioning changes; every deliverable drafted
   after that point should reflect the update. Deliverables drafted before
   an ICP update don't automatically get revised - flag stale ones if it
   matters for the engagement.

## Step 1: pick which deliverables this engagement covers

Check `clients/<slug>/intake.md` (or the questionnaire's 4.1 Directory
Profile Optimization Brief) for which platforms/pages are in scope. Each one
is a folder under `deliverables/` at the repo root:

- `deliverables/psychology-today/` - complete, the reference pattern.
- `deliverables/website-content/` - homepage, approach page, clinician bios,
  FAQ, etc. No hard character caps; structural (page/section) instead of
  field-by-field.
- `deliverables/google-business-profile/` - description + posts.
- `deliverables/zencare/`, `deliverables/zocdoc/` - field maps only; confirm
  character limits directly with the platform before first use (see each
  module's README).
- `deliverables/private-practice-directory/` - internal MHM product; confirm
  schema with whoever owns it.

## Step 2: inputs - two modes, per deliverable

- **Mode A - Refine existing copy.** The client has a live profile or
  website. Capture the current copy verbatim into
  `clients/<slug>/deliverables/<module>/source/`. The job is re-sequencing,
  tightening, and limit-fitting from the ICP, not a ground-up rewrite.
- **Mode B - Build from intake.** Little or no existing copy for that
  surface. Draft fresh copy from the ICP and that module's `field-map.md`.

A single engagement often mixes modes - e.g. refine an existing PT profile
(Mode A) while building website copy from scratch (Mode B) - because they
share the same ICP.

## Steps (per deliverable)

1. **Set up the folder.** `clients/<slug>/deliverables/<module>/`, with a
   `source/` subfolder for inputs and the deliverable `.md` at the top level.
2. **Findings pass.** Identify high-impact issues for that surface. Recurring
   ones, regardless of platform:
   - opening line/hero buries the hook (PT: first 270 chars of Box 1 are the
     search preview; website: the hero is the equivalent real estate);
   - specialty/keyword selection chases saturated terms instead of the
     client's real differentiation (ICP Differentiation section);
   - conceptual language where plain symptom/outcome language (ICP Ideal
     Client, in-their-own-words phrasing) would convert better;
   - inconsistent consult length or other trust contradictions **between
     surfaces**, not just within one profile - check the website against
     every directory profile, not only each profile against itself;
   - licensure display vs. headline mismatch (check every time, everywhere
     licensure appears);
   - underused authority assets (ICP Trust & Authority Assets).
3. **Draft the copy** into a copy of that module's `deliverables/<module>/template.md`.
   Write each block as a single unwrapped paragraph so it pastes cleanly.
   Where the module has real limits, aim for roughly 80% of each (see that
   module's `limits.json`) so nothing truncates on small screens; never
   exceed 100%. Where it doesn't (website content), the template's "Target"
   numbers are a guide, not a ceiling.
4. **Verify limits and style.** Run the checker:
   ```
   python3 tools/check_limits.py clients/<slug>/deliverables/<module>/<file>.md --update
   python3 tools/check_limits.py clients/<slug>/deliverables/<module>/<file>.md
   ```
   The first sets the counts; the second must report PASSED (exit 0). It
   also blocks em/en dashes, a house-style rule that applies everywhere, not
   just PT.
5. **Punch list + guidance.** Add smaller fixes (typos, setting changes,
   category/keyword swaps), and an implementation checklist. Keep these
   separate from the paste-ready copy.
6. **Generate the client document.** The `.md` is the internal source of
   truth; the client gets a formatted document:
   ```
   python3 tools/build_docx.py clients/<slug>/deliverables/<module>/<file>.md
   ```
   This writes a namespaced deliverable into the folder, e.g.
   `michael-lydon-psychology-today-optimized-2026-09-03-113341.docx`, with
   each copy block in its own shaded, bordered box and the field name + live
   count as a caption above it. The datetimestamp means revision runs never
   overwrite an earlier delivery. The build refuses to run on over-limit or
   dash-dirty copy, so it doubles as a final gate.
7. **Deliver.** Upload the `.docx` to Google Drive, open it as a Google Doc,
   and share the link. The boxes survive the conversion as tables, so the
   client can click a box, select all, and paste it straight into the
   matching field without grabbing a label or count.

## Hard rules

- Every copy block fits its platform's character limit, where one exists.
  The checker is the gate; do not deliver on a FAIL.
- No em dashes or en dashes anywhere in client-facing copy, on any surface.
  Plain hyphens only.
- Avoid AI-isms generally, not just dashes. Watch for: rule-of-three lists
  used as a crutch ("clear, direct, and warm"-style triplets stacked
  reflexively); "it's not just X, it's Y" and other false-contrast framing;
  throat-clearing openers ("In today's world...", "Let's face it...");
  corporate-inspirational verbs (unlock, elevate, dive into, embark, harness,
  navigate, foster, seamless, robust, holistic, transformative journey);
  hedge-stacking ("might potentially help provide"); and over-symmetrical
  sentence pairs that sound generated rather than spoken. Read every
  deliverable back and ask whether a clinician would actually say it out
  loud. Copy should be clear, direct, and warm, in the client's own voice,
  not polished into sounding like everyone else's.
- Each module's `limits.json` is the single source of truth for that
  platform's limits. If a platform changes a limit, update that module's
  `limits.json` and re-run the checker on past deliverables; do not hardcode
  numbers elsewhere.
- Never fabricate a character limit. If a platform's real limit is unverified
  (see `deliverables/zencare/README.md`, `deliverables/zocdoc/README.md`),
  confirm it directly before adding a `limits.json` - a wrong number is worse
  than no enforcement, because it produces false confidence.
- Preserve the clinician's voice, on every surface. Re-sequence and tighten
  before rewriting. Apply the ICP's words-to-avoid list everywhere, not just
  on the platform where the client first mentioned it.
- Keep trust signals (licensure, consult length, CTA) identical across every
  surface for a client, not just internally consistent within one document.
