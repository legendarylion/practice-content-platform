#!/usr/bin/env python3
"""
check_limits.py - verify a deliverable (profile copy or website content) fits
its platform's character limits and house style.

For every copy block in a deliverable it checks:
  1. the copy fits the platform's character limit for that field, if the
     field has one (some deliverable types, e.g. website content, don't),
  2. the "This copy: N" count printed in the file matches the real length,
  3. no em dash or en dash slipped into the copy (house style is plain hyphens).

It also cross-checks each block's declared "Limit N" against the module's
limits.json (the single source of truth for that platform), so a stale
number in a deliverable gets caught.

Which limits.json applies is inferred from the file's parent folder name,
which by convention is the platform/module slug, e.g.:
    clients/<client>/deliverables/psychology-today/optimized-profile.md
                                   ^^^^^^^^^^^^^^^^ -> deliverables/psychology-today/limits.json
Pass --limits to point at a different one explicitly. If no limits.json is
found for the module (e.g. website-content, which has no hard caps), blocks
are still checked for count accuracy and dash-cleanliness, just not against
a canonical per-field limit.

Usage:
    python3 tools/check_limits.py clients/<client>/deliverables/<platform>/<file>.md
    python3 tools/check_limits.py --update <file>   # rewrite "This copy: N" to the real count
    python3 tools/check_limits.py --limits deliverables/zencare/limits.json <file>

Exit code is 0 when everything passes, 1 when any block is over limit or
contains a banned dash. Count mismatches warn (or are fixed with --update).
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# A block is: divider, header lines (with a quoted label, optionally "Limit N"),
# divider, blank line, then one paragraph of copy ending at a blank line.
BLOCK_RE = re.compile(
    r'-{20,}\n'            # opening divider
    r'(?P<header>.*?)'     # header lines
    r'-{20,}\n\n'          # closing divider + blank line
    r'(?P<copy>.+?)\n\n',  # copy paragraph (non-greedy, up to next blank line)
    re.S,
)
LABEL_RE = re.compile(r'"([^"]+)"')
LIMIT_RE = re.compile(r'Limit\s+(\d+)', re.I)
COUNT_RE = re.compile(r'This copy:\s*(\d+)', re.I)
DASHES = ("—", "–")  # em dash, en dash


def find_limits_path(file_path, explicit=None):
    """Infer the module's limits.json from the file's parent folder name
    (the platform/module slug), e.g. .../deliverables/psychology-today/x.md
    or .../clients/<c>/deliverables/psychology-today/x.md both resolve to
    deliverables/psychology-today/limits.json. Returns None if there isn't one
    (some deliverable types have no hard character caps)."""
    if explicit:
        return explicit
    platform = os.path.basename(os.path.dirname(os.path.abspath(file_path)))
    candidate = os.path.join(ROOT, "deliverables", platform, "limits.json")
    return candidate if os.path.isfile(candidate) else None


def load_limits(limits_path):
    if not limits_path:
        return {}
    with open(limits_path, encoding="utf-8") as fh:
        data = json.load(fh)
    return {f["label"]: f["limit"] for f in data["fields"]}


def parse_blocks(text):
    blocks = []
    for m in BLOCK_RE.finditer(text):
        header, copy = m.group("header"), m.group("copy").strip()
        limit_m, count_m, label_m = (
            LIMIT_RE.search(header),
            COUNT_RE.search(header),
            LABEL_RE.search(header),
        )
        blocks.append({
            "label": label_m.group(1) if label_m else "(unlabeled)",
            "declared_limit": int(limit_m.group(1)) if limit_m else None,
            "claimed_count": int(count_m.group(1)) if count_m else None,
            "copy": copy,
            "span": m.span(),
        })
    return blocks


def check(path, update=False, limits_path=None):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    limits_path = find_limits_path(path, limits_path)
    canonical = load_limits(limits_path)
    blocks = parse_blocks(text)
    if not blocks:
        print("No copy blocks found. Is this a deliverable in the expected format?")
        return 1

    failures = 0
    print(f"Checking {path}")
    print(f"Limits source: {limits_path or '(none found - dash/count checks only, no caps enforced)'}\n")
    for b in blocks:
        actual = len(b["copy"])
        limit = b["declared_limit"]
        notes = []

        if limit is not None:
            over = actual - limit
            if over > 0:
                notes.append(f"OVER LIMIT by {over}")
                failures += 1

            if b["label"] in canonical and canonical[b["label"]] != limit:
                notes.append(f"declared limit {limit} != limits.json {canonical[b['label']]}")
                failures += 1
            elif b["label"] not in canonical and b["label"] != "(unlabeled)" and canonical:
                notes.append(f'label "{b["label"]}" not in limits.json')

        if b["claimed_count"] is not None and b["claimed_count"] != actual:
            notes.append(f"count says {b['claimed_count']}, real is {actual}"
                         + (" (will fix)" if update else ""))

        bad = [d for d in DASHES if d in b["copy"]]
        if bad:
            names = {"—": "em dash", "–": "en dash"}
            notes.append("contains " + ", ".join(names[d] for d in bad))
            failures += 1

        status = "OK" if not [n for n in notes if "OVER" in n or "dash" in n or "!=" in n] else "FAIL"
        flag = ("  <-- " + "; ".join(notes)) if notes else ""
        limit_disp = f"{limit}" if limit is not None else "-"
        print(f"  [{status:4}] {actual:4d}/{limit_disp:<4} {b['label']}{flag}")

    if update:
        text = update_counts(text, blocks)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("\nUpdated 'This copy: N' values to match real counts.")

    print()
    if failures:
        print(f"FAILED: {failures} issue(s) need attention before delivery.")
    else:
        print("PASSED: every block fits its limit and is dash-clean.")
    return 1 if failures else 0


def update_counts(text, blocks):
    # Rewrite the "This copy: N" number in each header to the real length.
    # Walk blocks in reverse so earlier spans stay valid as we edit.
    for b in sorted(blocks, key=lambda x: x["span"][0], reverse=True):
        start, end = b["span"]
        chunk = text[start:end]
        actual = len(b["copy"])
        new_chunk = COUNT_RE.sub(f"This copy: {actual}", chunk)
        text = text[:start] + new_chunk + text[end:]
    return text


def main():
    ap = argparse.ArgumentParser(description="Check a deliverable against its module's limits.json.")
    ap.add_argument("file", help="path to the deliverable markdown file")
    ap.add_argument("--update", action="store_true",
                    help="rewrite 'This copy: N' counts in place to match real lengths")
    ap.add_argument("--limits", help="explicit path to a limits.json (overrides auto-detection)")
    args = ap.parse_args()
    if not os.path.isfile(args.file):
        print(f"File not found: {args.file}")
        sys.exit(2)
    sys.exit(check(args.file, update=args.update, limits_path=args.limits))


if __name__ == "__main__":
    main()
