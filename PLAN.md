# Plan: kokinwakashu-prototype Submodule

## Status: AWAITING CONFIRMATION

---

## Overview

Extract the five reference structures currently embedded in `kokinwakashu.xml`
into standalone TEI files, housed in a new independent git repository
`kokinwakashu-prototype`, added as a submodule at the root of this repo.

The new repo is self-contained — no dependencies on the Go tools or data
pipeline in this repo.

---

## Target Structure (new repo)

```
kokinwakashu-prototype/         ← git repo (submodule here at root)
  AGENTS.md                     ← general AI agent instructions (tool-agnostic)
  CLAUDE.md                     ← Claude Code entry: @AGENTS.md
  flake.nix                     ← Nix devShell (python, uv, xmllint)
  pyproject.toml                ← uv project config (lxml dep)
  kokinwakashu.xml              ← main body (moved from current repo root)
  reading-index.xml             ← Dict A: kana reading → lemma homs
  lemma-index.xml               ← Dict B: lemma entries (27k)
  wlsp-index.xml                ← WLSP semantic classification taxonomy
  wlsph-index.xml               ← WLSPH (historical variant) taxonomy
  person-list.xml               ← listPerson: poets and historical figures
  scripts/
    split.py                    ← one-time extraction script (temporary)
```

Each extracted file is a complete standalone TEI document:
```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>…</teiHeader>
  <text><body>
    <!-- extracted div or list -->
  </body></text>
</TEI>
```

---

## Source Structure in kokinwakashu.xml

| Line  | Element | Target file |
|-------|---------|-------------|
| 43334 | `<div type="reading-index">` | `reading-index.xml` |
| 61369 | `<div type="dictionary">` | `lemma-index.xml` |
| 88648 | `<div type="classification" xml:id="classWLSP">` | `wlsp-index.xml` |
| 89949 | `<div type="classification" xml:id="classWLSPH">` | `wlsph-index.xml` |
| 93988 | `<listPerson>` | `person-list.xml` |

The `<back>` in `kokinwakashu.xml` will be emptied (or removed) after extraction.

---

## Implementation Phases

### Phase 1 — Create GitHub repo and submodule

```bash
gh repo create kokinwakashu-prototype --public --description "Kokinwakashu TEI reference data"
git submodule add https://github.com/<user>/kokinwakashu-prototype.git kokinwakashu-prototype
```

### Phase 2 — Bootstrap new repo files

In `kokinwakashu-prototype/`:
- Write `flake.nix`: provides `python3`, `uv`, `xmllint`; `shellHook` runs `uv sync` to create and pin the venv on entry
- Init uv project: `uv init && uv add lxml` (pins deps in `uv.lock`)
- Write `AGENTS.md` (see spec below)
- Write `CLAUDE.md`:
  ```markdown
  @AGENTS.md
  ```

### Phase 3 — Move kokinwakashu.xml

```bash
mv kokinwakashu.xml kokinwakashu-prototype/
```

Update `.gitignore` or submodule pointer accordingly.

### Phase 4 — Write extraction script

`scripts/split.py` — reads `kokinwakashu.xml`, extracts each `<back>` child into
its own TEI wrapper file. One-time use; delete after running.

Implementation notes:
- Use `lxml.etree` for namespace-aware parsing
- Wrap each extracted element in minimal TEI shell with matching `<teiHeader>`
- Preserve `xmlns` and all `xml:id` attributes (critical for cross-references)
- Use `etree.tostring(pretty_print=False)` on mixed-content nodes to avoid corrupting text

### Phase 5 — Run extraction, verify, clean up

```bash
cd kokinwakashu-prototype
nix develop --command bash -c "uv run python scripts/split.py"
# verify each file parses and IDs are intact
rm scripts/split.py
```

### Phase 6 — Initial commit in new repo

```bash
cd kokinwakashu-prototype
git add .
git commit -m "feat: initial TEI reference data split from kokinwakashu.xml"
```

### Phase 7 — Update submodule pointer in current repo

```bash
cd ..
git add kokinwakashu-prototype
git commit -m "feat: add kokinwakashu-prototype submodule"
```

---

## AGENTS.md Spec (for new repo)

Content mirrors the current `CLAUDE.md` in structure, adapted for the new repo:

- **Language policy**: same (conversation Japanese, docs/code English, XML Japanese)
- **Project overview**: standalone TEI reference data for Kokinwakashu
- **Data format**: TEI XML P5; no schema modifications without validation
- **Dev env**: `nix develop` provides `python3`, `uv`, `xmllint`; venv is created and pinned via `uv sync` in `shellHook`
- **File descriptions**: one-line purpose for each `.xml` file
- **Key constraints**:
  - Do not modify original text content; only structural/metadata annotations
  - Preserve TEI namespace in all processing
  - Do not call `Indent()` on mixed content
  - `xml:id` values are cross-referenced — never rename without global search
- **Editor**: Helix (`hx`)

---

## Risks

| Risk | Severity | Mitigation |
|---|---|---|
| `xml:id` uniqueness must hold within each split file | HIGH | Verify with `xmllint --valid` after split |
| `kokinwakashu.xml` body cross-references IDs in the back | MEDIUM | Audit `<ref target="#">` in body before stripping back |
| Nix flake copy-paste may bring unused deps | LOW | Trim to minimal set needed |

---

## Complexity: LOW–MEDIUM

- Repo setup + submodule wiring: straightforward
- Extraction script: ~80 LOC Go
- AGENTS.md authoring: ~60 lines

---

**WAITING FOR CONFIRMATION**: Proceed with this plan? (yes / no / modify)
