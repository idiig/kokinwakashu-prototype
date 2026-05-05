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
- For compound-entry cleanup, fix `<pron>` first and derive
  `<form type="compound">` from that pronunciation analysis; do not treat the
  pre-existing compound refs as the source of truth when they conflict
- Validate after any structural modification:
  ```bash
  xmllint --noout --schema http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng <file>.xml
  ```
- When serializing XML with Python/lxml: use `pretty_print=False` on mixed-content
  nodes (text + elements interleaved) — pretty-printing inserts spurious whitespace

## Helper Scripts

### `check_lemma.py` — cross-file reference audit

The primary diagnostic tool. Before editing any lemma, run this first.

```bash
uv run python check_lemma.py <lemma-id>
```

**Output sections:**

1. `[lemma-index] ENTRY FOUND` — shows `type`, `form` (orth), `pron`, `pos`
2. `[reading-index] N hom(s) point to li:<id>` — lists Dict A homs that
   reference this lemma; each line shows `reading entry=<kana>` and
   `hom=<reading.lemma>`
3. `[lemma-index] Used as component in N compound(s)` — compounds in
   `lemma-index.xml` whose `<form type="compound">` or `<pron><w>` references
   this entry
4. `[kokinwakashu] N token(s) reference this lemma` — poem tokens with a
   matching `lemmaRef`; shows surface and full `lemmaRef` value

**Typical edit sequence:**

1. Run `check_lemma.py <id>`
2. Identify what needs fixing (pron, hom ID, compound ref, poem token)
3. Edit `lemma-index.xml`, then `reading-index.xml`, then `kokinwakashu.xml`
   in that order
4. Re-run `check_lemma.py` to verify all refs are consistent

### Other helpers

- `apply_pron.py` — apply unambiguous `<pron>` decompositions to
  `lemma-index.xml`
- `check_compounds.py` — audit compound entries and report OK / ambiguous /
  failed pronunciation decompositions
- `count_pron.py` — count compound entries with plain vs decomposed `<pron>`

Treat these scripts as developer aids. Validate XML after applying their output.

## Lemma Review Workflow

Flagged entries are listed in `issues.txt` (one per line, TSV-formatted).
Flags: `?` = needs review, `!` = needs decomposition, `!?` = both.

**Review loop for each entry:**

1. Run `uv run python check_lemma.py <lemma-id>`
2. Identify the problem class (see below)
3. Confirm action with the user before editing
4. Edit the three files in order: `lemma-index.xml` → `reading-index.xml` →
   `kokinwakashu.xml`
5. Re-run `check_lemma.py` to verify; then move to the next entry

**Common problem classes:**

| Problem | Symptom | Fix |
|---------|---------|-----|
| Modern kana in `<pron>` | e.g. `みず`, `つえ`, `すえ` | Replace with 歴史的仮名遣い |
| Wrong/missing `<pron>` | Reading not attested in corpus | Remove or correct |
| Hom ID uses kanji when entry renamed to kana | e.g. `うれ.末` after split | Rename hom to `うれ.うれ` |
| Compound ref to old ID | `<ref target="#旧ID">` | Update to new ID |
| kokinwakashu.xml stale lemmaRef | `ri:旧reading.旧lemma` | Update with sed or direct edit |

**Lemma split rule** (when one entry has multiple distinct readings):
- Create two separate `<entry>` elements with kana `xml:id` values
- Flatten structure: no `<hom>`/`<sense>` sub-elements when only one reading
  per entry
- Update hom IDs in `reading-index.xml` to match new kana-based lemma IDs
- Update all `ri:` and `li:` refs in `kokinwakashu.xml`

## Kana Spelling Policy

All `<pron>` values must use **歴史的仮名遣い** (classical kana orthography).
Modern kana spellings are not allowed:

| Modern | Historical | Notes |
|--------|-----------|-------|
| みず | みづ | 水 |
| つえ | つゑ | 杖 |
| すえ | すゑ | 末 |
| ふるさと | ふるさと | (same) |
| に (number 2) | ふた | 二 |
| まん | よろづ | 万 |

When a `<pron>` is found in modern kana, replace it. Do not add the modern
form as an alternate reading.

## Commit Message Format

```
<type>: <description>
```

Types: `feat`, `fix`, `refactor`, `docs`, `chore`

## Cross-File Reference Convention (prefixDef)

`kokinwakashu.xml` declares five URI prefixes in `<encodingDesc><listPrefixDef>`.
Use these when adding annotations that reference the standalone index files:

| Prefix | Expands to | Use for |
|--------|-----------|---------|
| `ri:あさ.朝` | `reading-index.xml#あさ.朝` | Dict A hom IDs |
| `li:w.あし` | `lemma-index.xml#w.あし` | Dict B entry IDs |
| `wlsp:WLSP.1.1000` | `wlsp-index.xml#WLSP.1.1000` | WLSP taxonomy |
| `wlsph:WLSPH.1.1000` | `wlsph-index.xml#WLSPH.1.1000` | WLSPH taxonomy |
| `person:紀貫之` | `person-list.xml#紀貫之` | Person IDs |

Example annotation:
```xml
<w lemmaRef="ri:あさ.朝">あさ</w>
```

Do **not** use bare `#fragment` references for cross-file links — they only
work for within-document IDs. Use the prefix form above.

## Agent Self-Maintenance (Routine)

At the end of every session, perform the following updates before closing:

### 1. Update `PLAN.md`
- Mark completed phases as `✓`
- Add or revise **Open Questions / Next Steps** to reflect what remains
- Record any key decisions made during the session under **Key Decisions**

### 2. Update `AGENTS.md`
- Add new conventions, constraints, or ID patterns discovered during the session
- Update file descriptions if new files were added or existing ones changed
- Update the Cross-File Reference table if new prefixes were defined

### 3. Update project memory (Claude Code only)
- Write or update `~/.claude/projects/.../memory/submodule_prototype.md`
- Record: what changed, why, and what is next
- Update `MEMORY.md` index if a new memory file was created

This routine ensures the next agent session starts with full context.
