# Plan: kokinwakashu-prototype Submodule

## Status: COMPLETE ✓

---

## What Was Done

This repository was created and populated in one session (2026-05-01) as a
submodule of `kokin-tei-merge` (branch `separate-tei-dicts`).

### Completed Phases

- **Phase 1** ✓ — GitHub repo `idiig/kokinwakashu-prototype` created; added as
  submodule at root of `kokin-tei-merge`
- **Phase 2** ✓ — `flake.nix` (python3, uv, xmllint; `uv sync` in shellHook),
  `AGENTS.md`, `CLAUDE.md` (@AGENTS.md), `pyproject.toml` + `uv.lock` (lxml)
- **Phase 3** ✓ — `kokinwakashu.xml` moved from `kokin-tei-merge` root to here
- **Phase 4–5** ✓ — `scripts/split.py` (lxml, recover=True) extracted all five
  files; script deleted after run
- **Phase 6–7** ✓ — Both repos committed and pushed
- **Phase 8** ✓ — `prefixDef` added to `kokinwakashu.xml` `<encodingDesc>`

---

## Repository State

```
kokinwakashu-prototype/
  AGENTS.md              ← agent instructions (tool-agnostic)
  CLAUDE.md              ← @AGENTS.md
  flake.nix              ← Nix devShell: python3, uv, xmllint
  pyproject.toml         ← uv project (lxml 6.1.0)
  uv.lock
  kokinwakashu.xml       ← Karoku 2 body; <back> stripped; prefixDef in header
  reading-index.xml      ← Dict A: kana reading → lemma homs  (~571 KB)
  lemma-index.xml        ← Dict B: lemma entries              (~1.1 MB)
  wlsp-index.xml         ← WLSP semantic classification       (~47 KB)
  wlsph-index.xml        ← WLSPH historical variant taxonomy  (~169 KB)
  person-list.xml        ← listPerson: poets / figures        (~75 KB)
```

---

## Key Decisions

- **No Go tooling** in this repo — Python + uv only
- **Extraction was one-time**: `scripts/split.py` used `lxml` with
  `recover=True` (source had duplicate `xml:id` values in WLSPH data)
- **Body cross-references are fully internal**: all 925 `target="#..."` in
  `kokinwakashu.xml` point to IDs within the same file; none reference the
  extracted index files
- **prefixDef convention** (see AGENTS.md): five prefixes defined for
  cross-file annotation

---

## Open Questions / Next Steps

- [ ] The parent repo (`kokin-tei-merge`, branch `separate-tei-dicts`) has not
  been merged to `main` yet — pending review
- [ ] `kokin-annotated.xml` in the parent repo still embeds Dict A/B/Classification
  inline in `<back>`; consider migrating its `lemmaRef="#..."` values to
  `lemmaRef="ri:..."` using the prefixDef scheme
- [ ] Duplicate `xml:id` values in `wlsph-index.xml` (`WLSPH.4.3100`,
  `WLSPH.9.0060`) are a pre-existing data issue — not introduced by extraction
