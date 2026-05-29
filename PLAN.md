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
  apply_pron.py          ← helper: auto-apply unambiguous compound pron decomposition
  check_compounds.py     ← helper: audit compound pron decomposition candidates
  count_pron.py          ← helper: count plain vs decomposed compound pron entries
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

## Key Decisions (2026-05-05 追加)

- **漢字レンマ優先ルール**: 漢字レンマが存在する場合、複合語の `<ref>` と `<pron>` の `<w lemmaRef>` は仮名IDではなく漢字IDを使用する（例: `#なつ`→`#夏`、`ri:なつ.なつ`→`ri:なつ.夏`）
- **てへ処理**: `てへ` は `てふ` の読みとして `reading-index` に残存させ、独立レンマは削除
- **かも区別**: `かも` (助詞P.fin) と `鴨` (名詞N.g/鳥) は別レンマ; 複合語 `蘆鴨` は `鴨` を使用
- **TSV全レンマ化**: `lemma-index-decomp.tsv` は複合語だけでなく全レンマを含む（simplex行はdecompカラムが空）
- **削除連鎖**: 漢字hom追加→複合語ref更新→旧仮名hom削除→旧仮名レンマ削除の順で実施

## Key Decisions (2026-05-06 追加)

- **Dict A / Dict B headword alignment**: if `reading-index.xml` and
  `kokinwakashu.xml` already consistently use a normalized headword label,
  rename the Dict B entry to match it (examples: `見る` → `見`, `言う` → `言ふ`)
- **Calendar-word normalization**: when a kana month-name lemma duplicates an
  existing kanji month lemma, keep the kanji lemma and point compounds to it
  (example: `さつき` → `五月`)
- **Okurigana split rule**: when corpus usage clearly distinguishes an
  okurigana form from the bare-kanji base, split them into separate lemmas
  instead of overloading one entry (example: `辺` vs `辺り`)
- **Reduplicative compound rule**: repeated-graph words should be marked as
  `type="compound"` when their internal structure is transparent
  (example: `色色` = `色 + 色`)
- **`check_lemma.py` caveat**: token counts can overmatch when one lemma ID is
  a prefix of another (for example `辺` vs `辺り`); verify exact `lemmaRef`
  values manually when counts look suspicious

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
- **Compound cleanup rule**: treat `<pron>` as the source of truth; derive
  `<form type="compound">` from the corrected pronunciation analysis rather
  than trusting the pre-existing component refs
- **reading-index restoration rule**: if `lemma-index.xml` already contains
  valid `ri:...` references, restore missing Dict A hom IDs in
  `reading-index.xml` before reworking the lemma entry again
- **Dict A link encoding**: Dict A homs point to Dict B entries with
  `corresp="li:..."` on `<hom>`; do not put `<ref>` directly inside `<hom>`

---

## Open Questions / Next Steps

- [x] Compound pronunciation decomposition cleanup pass (2026-05-05):
  - Fixed compound refs using kana lemma IDs where kanji lemmas exist
  - Added 5 new simplex lemma entries (撫子/榊/蓑/篝/鴨) with correct N.g/bird WLSP codes
  - Deleted 15 unreferenced kana lemma entries and their reading-index homs
  - Fixed `てへ` → redirected as reading of `てふ`; deleted `てへ` lemma
  - Expanded `lemma-index-decomp.tsv` to include all lemmas (simplex + compound)
  - Validation flags added to index; morphological decompositions updated
- [ ] **issues-compound.txt** — compound conversion pass in progress (2026-05-08):
  - Completed through `片方` (original line 1144 of issues-compound.txt)
  - Batch 1 (previous sessions): 御前、御吉野、御垣守、御影、御手洗
  - Batch 2 (this session): 御津、御笠、憂目（新規）、憂身（新規）、心づから
  - 2026-05-10: `物故` converted to compound; `物故に` merged into `物故`
    and poem-body `物ゆへに` tokens split into `物ゆへ` + `に`
  - 2026-05-10: `reading-index.xml` Dict A → Dict B links normalized to
    TEI-valid `hom/@corresp`; local RNG validation now passes for all three
    edited XML files
  - **Policy**: poem tokens keep single lemmaRef per `<w>`; compound structure lives only in lemma-index
  - 2026-05-11: `狭筵` converted to compound as `小` + newly added `筵`;
    user noted entries through `犬上` are already complete
  - 2026-05-11: `率爾に` reviewed as acceptable simplex; ID normalized to
    `いささめに`
  - 2026-05-11: `玉津` reviewed as acceptable simplex; removed from
    `issues-compound.txt`
  - 2026-05-11: `玉匣` converted to compound as `玉` + newly added `匣`
  - 2026-05-11: `玉桙` converted to compound as `玉` + newly added `桙`
  - 2026-05-11: `玉章` converted to compound as `玉` + `梓`; `梓` pron
    normalized to historical kana `あづさ`
  - 2026-05-11: `理無し` converted to compound as newly added `理` + `無し`
  - 2026-05-11: `瓶原` converted to compound as newly added `甕` + `の` + `原`
  - 2026-05-11: split `け.異なり` into new lemma `けなり`; kept
    `こと.異なり` under `異なり`
  - 2026-05-11: merged `異に` into `けなり` + existing following `に`;
    removed `異に`
  - 2026-05-11: `異異` converted to reduplicative compound as `異なり` +
    `異なり`
  - 2026-05-11: `四極` reviewed as acceptable simplex; removed from
    `issues-compound.txt`
  - 2026-05-11: `白妙` converted to compound as `白` + `栲`
  - 2026-05-11: `百千鳥` converted to compound as `百` + `千鳥`
  - 2026-05-11: `百敷` converted to compound as `百` + `敷く`
  - 2026-05-11: `百草` converted to compound as `百` + `草`
  - 2026-05-11: `皆がら` converted to compound as `皆` + newly added `がら`
  - 2026-05-11: `唯に` normalized to `唯なり` as a na-adjectival stem;
    `直路` converted to compound as `唯なり` + `路`
  - 2026-05-11: removed stale `相坂` / `逢坂` queue flags; `相坂` is already
    merged into compound `逢坂`
  - 2026-05-11: `真木` converted to compound as newly added `柾` + `木`
  - 2026-05-11: `真澄鏡` converted to compound as newly added `真澄なり` + `鏡`
  - 2026-05-12: `蚊遣火` converted to compound as newly added `蚊` + `遣る`
    + `火`
  - 2026-05-12: `衣手` converted to compound as `衣` + `手`
  - 2026-05-12: `覚ます` converted to compound as `覚む` + `使`
  - 2026-05-12: `言の葉` converted to compound as `言` + `の` + `葉`
  - 2026-05-12: `諸共に` renamed to `諸共なり` and converted to compound
    as `諸` + `共`
  - 2026-05-12: `責めて` converted to compound as `責む` + `て`
  - 2026-05-12: `走り火` converted to compound as `走る` + `火`
  - 2026-05-12: `轟かす` converted to compound as newly added `轟く` + `使`
  - 2026-05-12: `辰巳` converted to compound as newly added `辰` + `巳`
  - 2026-05-12: `返す返す` converted to reduplicative compound as `返す` + `返す`
  - 2026-05-12: `返る返る` converted to reduplicative compound as `返る` + `返る`
  - 2026-05-12: `逆様なり` converted to compound as newly added `逆` + `様`
  - 2026-05-12: `道行` added as nested compound `道` + `行く`; `道行振り`
    converted to compound as `道行` + `振る`
  - 2026-05-12: `遥遥` converted to reduplicative compound as `遥かなり` + `遥かなり`
  - 2026-05-12: `重荷` converted to compound as `重し` + newly added `荷`
  - 2026-05-12: `野中` converted to compound as `野` + `中`
  - 2026-05-12: `野山` converted to compound as `野` + `山`
  - 2026-05-12: `野良` converted to compound as `野` + `ら`
  - 2026-05-12: `野辺` converted to compound as `野` + `辺`
  - 2026-05-12: `長居` converted to compound as `長し` + `居る`
  - 2026-05-12: `長柄` reviewed as a place name and kept as simplex
  - 2026-05-12: `長浜` converted to compound as `長し` + `浜`
  - 2026-05-12: `門出` converted to compound as `門` + `出づ`
  - 2026-05-12: `間遠なり` converted to compound as `間` + `遠し`
  - 2026-05-12: `関守` converted to compound as `関` + `守る`
  - 2026-05-12: `阿武隈` reviewed as a place name and kept as simplex with
    reading `あぶくま`
  - 2026-05-12: `雲井` merged into `雲居`; `雲居` is compound as `雲` + `居る`
  - Next entry: 露けし (original line 1699)
- [ ] **issues.txt review in progress** — later-pass entries updated through
  `さつき` (2026-05-06)
- [ ] **Resolved in this session**: `狩り`, `狩衣`, `百`, `相坂`, `眼`,
  `睦まじ`, `社`, `筋`, `絃`, `緒`, `色々`, `見る`, `言う`, `辺`, `え`,
  `おろし`, `さつき`
- [ ] **Held / not changed after review**: `澪標`, `結果`, `衛る`, `躊躇`,
  `うらびる`, `がに`, `さす`
- [ ] **Earlier unresolved entries remain** near the top of `issues.txt`:
  current first items include `はも`, `ふるさと`, `まく`, `まし`, `ます`,
  `一`, `万`, `下紐`, `二`, `五つ`, `五月雨`, ...
- [ ] **Compound transparency annotation** — distinguish `type="compound"` entries
  into semantically transparent (compositional meaning derivable from components,
  e.g. 山川 = 山＋川) vs. semantically opaque (lexicalized/idiomatic, e.g. 憂目).
  Proposed mechanism: add a `@subtype` or `<note type="transparency">` attribute;
  exact encoding to be decided. Useful for downstream NLP and lexicographic display.

- [ ] **Lemma orth normalization against 日本国語大辞典 (Nikkoku)** — audit
  `<orth>` headwords in lemma-index.xml against Nikkoku standard forms and update
  where the current orth diverges (e.g. okurigana conventions, kanji choice).
  Priority: entries that appear in kokinwakashu.xml poem tokens.

- [ ] The parent repo (`kokin-tei-merge`, branch `separate-tei-dicts`) has not
  been merged to `main` yet — pending review
- [ ] `kokin-annotated.xml` in the parent repo still embeds Dict A/B/Classification
  inline in `<back>`; consider migrating its `lemmaRef="#..."` values to
  `lemmaRef="ri:..."` using the prefixDef scheme
- [ ] Duplicate `xml:id` values in `wlsph-index.xml` (`WLSPH.4.3100`,
  `WLSPH.9.0060`) are a pre-existing data issue — not introduced by extraction
- [ ] Helper scripts `add_proper_lemmas.py`, `add_proper_readings.py` (untracked)
  can be deleted once confirmed no longer needed
