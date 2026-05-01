# kokinwakashu-prototype

## Project Overview

Standalone TEI XML reference data for the Kokinwakashu (古今和歌集), extracted
from a merged annotation source. This repository is self-contained — it has no
runtime dependency on the parent annotation pipeline.

## Language Policy

- **Conversation**: Japanese
- **Documentation (AGENTS.md, README)**: English
- **Code and commit messages**: English
- **XML content**: Japanese (original text)

## Data Files

```
kokinwakashu.xml     — Kokinwakashu main body (Karoku 2 manuscript transcription)
reading-index.xml    — Dict A: kana reading → lemma homonym index (~40k entries)
lemma-index.xml      — Dict B: lemma definitions with POS and WLSP sense (~27k entries)
wlsp-index.xml       — WLSP semantic classification taxonomy
wlsph-index.xml      — WLSPH (historical kana variant) taxonomy
person-list.xml      — listPerson: poets and historical figures
```

Each file is a complete standalone TEI P5 document.

## ID Scheme

Cross-file references use fragment IDs. Key patterns:

- **Dict B entry IDs**: `xml:id="lemmakey"` (e.g. `w.あし`, `w.ある`)
- **Dict A homonym IDs**: `xml:id="reading.lemma"` (e.g. `あさ.朝`, `あさ.浅し`)
- **Dict A → Dict B**: `<ref target="#lemmakey">` inside each `<hom>`
- **WLSP codes**: `WLSP.X.YYYY` / `WLSPH.X.YYYY` (e.g. `WLSP.1.1000`)

Never rename an `xml:id` without a global search across all files.

## Tech Stack

- **Data format**: TEI XML (P5)
- **Scripting**: Python (`lxml`), managed via `uv`
- **Environment**: Nix flake (`nix develop`); provides `python3`, `uv`, `xmllint`

## Session Initialization

Enter the dev environment before running any scripts:

```bash
nix develop
```

The `shellHook` runs `uv sync` automatically to create and pin the virtual
environment from `uv.lock`. Run scripts with:

```bash
uv run python <script>.py
```

## Important Constraints

- Do not modify original Japanese text content in XML
- Preserve TEI namespace (`http://www.tei-c.org/ns/1.0`) in all XML processing
- Validate after any structural modification:
  ```bash
  xmllint --noout --schema http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng <file>.xml
  ```
- When serializing XML with Python/lxml: use `pretty_print=False` on mixed-content
  nodes (text + elements interleaved) — pretty-printing inserts spurious whitespace

## Commit Message Format

```
<type>: <description>
```

Types: `feat`, `fix`, `refactor`, `docs`, `chore`

## Agent Self-Maintenance

When conventions or constraints change during a session, update this file
(`AGENTS.md`) directly. Claude Code users: see `CLAUDE.md`.
