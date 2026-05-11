# Handoff Notes

This file is for agent-to-agent communication only.

- Put session-specific change summaries here.
- Put held / deferred entries here.
- Put temporary validation or tooling caveats here.
- Do not move stable project rules here; those belong in `AGENTS.md`.

## 2026-05-11

### Changed

- `狭筵` converted from `simplex` to `compound` as `さ.小` + `むしろ.筵`.
- Added new simplex lemma `筵` and Dict A hom `むしろ.筵`.
- Removed `狭筵` from `issues-compound.txt` and updated
  `lemma-index-decomp.tsv`.
- `率爾に` was reviewed as acceptable simplex; normalized the Dict B ID to
  `いささめに`, updated Dict A hom `いささめ.いささめに`, and updated the
  poem token reference.
- Removed stale `片岡`, `片方`, `片枝`, `最上`, and `犬上` entries from
  `issues-compound.txt` per the user's note that entries through `犬上` are
  already complete; removed `最上` / `犬上` decomposition flags in
  `lemma-index-decomp.tsv`.
- `玉津` reviewed as acceptable simplex; removed from `issues-compound.txt`
  and cleared the decomposition flag in `lemma-index-decomp.tsv`.
- `玉匣` converted from `simplex` to `compound` as `たま.玉` + `くしげ.匣`.
- Added new simplex lemma `匣` and Dict A hom `くしげ.匣`.
- `玉桙` converted from `simplex` to `compound` as `たま.玉` + `ほこ.桙`.
- Added new simplex lemma `桙` and Dict A hom `ほこ.桙`.
- Corrected `桙` semantic class to `WLSPH.1.4550` / `WLSP.1.4550`.
- `玉章` converted from `simplex` to `compound` as `たま.玉` + `あづさ.梓`,
  with compound surface `づさ` for the second component.
- Corrected `梓` pronunciation in Dict B from modern kana `あずさ` to
  historical kana `あづさ`.
- `理無し` converted from `simplex` to `compound` as `わり.理` + `なし.無し`.
- Added new simplex lemma `理` and Dict A hom `わり.理`.
- `瓶原` converted from `simplex` to `compound` as `みか.甕` + `の.の` +
  `はら.原`.
- Added new simplex lemma `甕`; added `みか.甕` as a second hom under the
  existing `みか` reading entry.
- Split the `け` reading out of `異なり`: added new lemma `けなり`, renamed
  Dict A hom `け.異なり` to `け.けなり`, and updated the one poem token.
  `こと.異なり` remains pointed at `異なり`.
- Merged `異に` into `けなり` + existing following `に`: removed the Dict B
  entry and Dict A hom `け.異に`; updated the one poem token to `け.けなり`.
- `異異` converted from `simplex` to reduplicative `compound` as
  `こと.異なり` + `こと.異なり` with surface `こと` + `ごと`.

### Validation

- Local RNG validation with `schemas/tei_all.rng` passed for
  `lemma-index.xml`, `reading-index.xml`, and `kokinwakashu.xml`.
- `uv run python count_pron.py`: `Total: 559, Plain: 0, Decomposed: 559`.
- `uv run python check_compounds.py`: `OK 559`, `Ambiguous 0`, `Failed 0`.

### Next

- User noted entries through `犬上` are already complete.
- Continue `issues-compound.txt` from `白妙` (original line 1203) onward.

## 2026-05-10

### Changed

- `reading-index.xml` Dict A homs now use `corresp="li:..."` to point to
  Dict B lemma entries. This replaces the interim TEI-valid
  `<sense><ref target="li:..."/></sense>` structure and the older invalid
  direct `<hom><ref/></hom>` structure.
- `apply_pron.py` and `check_compounds.py` now read `hom/@corresp` first, with
  a fallback to descendant `<ref target="...">` for compatibility.
- `物故` converted from `simplex` to `compound` as `もの.物` + `ゆゑ.故`;
  the entry is kept in expanded XML structure.
- `物故に` was merged into `物故`: removed the Dict B entry and removed the
  `ものゆゑに` Dict A reading entry.
- Two poem-body tokens formerly annotated as single `<w lemmaRef="ri:ものゆゑに.物故に">物ゆへに</w>`
  were split into `<w lemmaRef="ri:ものゆゑ.物故">物ゆへ</w>` +
  `<w lemmaRef="ri:に.に">に</w>`.
- Removed `物故に` from `issues-compound.txt`; updated
  `lemma-index-decomp.tsv` so `物故` is recorded as a compound.

### Validation

- TEI manual check: `<hom>` permits global linking attributes such as
  `@corresp`; `@lemmaRef` is not a valid `<hom>` attribute, and `<ref>` is not a
  valid direct child of `<hom>`.
- Local RNG validation with `schemas/tei_all.rng` now passes for
  `reading-index.xml`, `lemma-index.xml`, and `kokinwakashu.xml`.
- `uv run python count_pron.py`: `Total: 552, Plain: 0, Decomposed: 552`.
- `uv run python check_compounds.py`: `OK 552`, `Ambiguous 0`, `Failed 0`.
- `nix develop --command xmllint --noout` passed for `lemma-index.xml`,
  `reading-index.xml`, and `kokinwakashu.xml`.
- TEI schema validation with the remote `tei_all.rng` URL failed because
  `xmllint` could not load the remote schema in this environment; both
  `--schema` and `--relaxng` were attempted.
- Downloaded the TEI RNG schema to `schemas/tei_all.rng` and updated
  `AGENTS.md` to use the local schema path for future validation.
- Earlier local RNG failures were due to the invalid direct `<hom><ref/>`
  structure in `reading-index.xml`; after switching Dict A links to
  `hom/@corresp`, validation passes.
- `check_lemma.py` could not be run because it is not present in this working
  tree; exact `rg` checks found no remaining `物故に`, `ものゆゑに`,
  `li:物故に`, or `ri:ものゆゑに` references.

## 2026-05-08

### Changed

**issues-compound.txt — compound conversion pass (batch 2, continued)**

- `御津` → compound (み.御 + つ.津); poem token unchanged (ri:みつ.御津)
- `御笠` → compound (み.御 + かさ.笠); poem token unchanged (ri:みかさ.御笠)
- `憂目` → new compound entry created (うき.憂し + め.目), WLSPH.1.3310;
  4 poem tokens merged from two separate `<w>` into single `<w lemmaRef="ri:うきめ.憂目">`;
  hom `うきめ.憂目` added to existing `うきめ` entry in reading-index (alongside 浮海布)
- `憂身` → new compound entry created (うき.憂し + み.身), WLSPH.1.3410;
  1 poem token merged; new `うきみ` entry added to reading-index;
  hom `づ.つ` added to reading-index as new `づ` entry (連濁形)
- `心づから` → compound (こころ.心 + づ.つ + から.から);
  reading-index: new `<entry xml:id="づ">` with `づ.つ` hom added before `て` section

**Policy clarification (from reverts this session)**

- `<w>` tokens in `kokinwakashu.xml` must keep a single lemmaRef per token —
  do NOT write space-separated multi-ref `lemmaRef="ri:A ri:B"` for compound tokens.
  Compound structure is expressed only in lemma-index.xml `<form type="compound">`;
  poem tokens retain their original single hom reference (e.g. ri:みまへ.御前).
  (Four tokens were mistakenly split and reverted this session: 御前、御垣守、御影×2)

### Held

- `あふひ` (逢ふ日): user chose to skip (two occurrences in poems 433/434)

### Next

- Continue `issues-compound.txt` from 最上 (original line 1148) onward

## 2026-05-09

### Changed

- `心地` converted from `simplex` to `compound`; `<pron>` now decomposes as
  `こころ.心` + `もち.持つ` with surface `ここ` + `ち`.
- Added `もち.持つ` hom to `reading-index.xml`.
- `忍び忍びなり` converted from `simplex` to `compound`; `<pron>` now
  decomposes the stem as `しのび.忍ぶ` + `しのび.忍ぶ` with no `なり`
  component.
- Added `どち` as a new simplex lemma for "fellows/companions" with
  WLSPH/WLSP `1.2200`; `思ふどち` converted from `simplex` to `compound`
  as `おもふ.思ふ` + `どち.どち`.
- Added `いたし.痛し` to `reading-index.xml`; `愛でたし` converted from
  `simplex` to `compound` as `めで.賞づ` + `いたし.痛し`.
- `我ら` converted from `simplex` to `compound` as `われ.我` + `ら.ら`;
  poem token remains `ri:われら.我ら`.
- Added `妹子` as a new compound (`いも.妹` + `こ.子`) and added
  `いもこ.妹子` to `reading-index.xml`.
- `我妹子` converted from `simplex` to `compound` as surface
  `わ` + `ぎ` + `もこ`, referencing `わ.我` + `が.が` + `いもこ.妹子`;
  poem token remains `ri:わぎもこ.我妹子`.
- `挿頭す` converted from `simplex` to `compound` as surface `か` + `ざす`,
  referencing `かみ.髪` + `さす.挿す`; poem tokens remain
  `ri:かざさ.挿頭す` / `ri:かざし.挿頭す`.
- Added `捩る` as a new simplex lemma and `もぢ.捩る` to `reading-index.xml`.
- `捩摺` converted from `simplex` to `compound` as surface `もぢ` + `ずり`,
  referencing `もぢ.捩る` + existing `すり.摺る`; poem token remains
  `ri:もぢずり.捩摺`.
- `散らす` converted from `simplex` to `compound` as `ちら.散る` + `す.使`;
  poem tokens remain `ri:ちらし.散らす` / `ri:ちらす.散らす`.
- `数々なり` converted from `simplex` to `compound` as `かず.数` +
  `かず.数`; no `なり` component was added.
- Added `栲` as a new simplex lemma with WLSPH/WLSP `1.4201` and
  `たへ.栲` in `reading-index.xml`.
- `敷妙` converted from `simplex` to `compound` as `しき.敷く` + `たへ.栲`;
  poem tokens remain `ri:しきたへ.敷妙`.
- Added `文` as a new simplex lemma with WLSPH/WLSP `1.1840` and
  `あや.文` in `reading-index.xml`.
- `文無し` converted from `simplex` to `compound` as `あや.文` + `なし.無し`;
  poem tokens remain `ri:あやな.文無し`, `ri:あやなく.文無し`, and
  `ri:あやなし.文無し`.
- `文目` converted from `simplex` to `compound` as `あや.文` + `め.目`;
  poem token remains `ri:あやめ.文目`.
- `斯かり` converted from `simplex` to `compound` as surface `かか` + `り`,
  referencing `かく.斯く` + existing `あり.有り`; poem token remains
  `ri:かかり.斯かり`.
- `斯くて` converted from `simplex` to `compound` as `かく.斯く` + `て.て`;
  poem token remains `ri:かくて.斯くて`.
- `旁` converted from `simplex` to `compound` as `かた.方` + `かた.方`;
  poem token remains `ri:かたがた.旁`.
- `旅寝` converted from `simplex` to `compound` as `たび.旅` + `ね.寝.v`;
  poem tokens remain `ri:たびね.旅寝`.
- `早苗` converted from `simplex` to `compound` as `さ.早` + `なへ.苗`;
  poem token remains `ri:さなへ.早苗`.
- `明かす` normalized to `明す` and converted from `simplex` to `compound`
  as `あか.明く` + `す.使`; added `あか.明く` to `reading-index.xml` and
  updated the poem token to `ri:あかし.明す`.
- `昔方` converted from `simplex` to `compound` as `むかし.昔` + `へ.辺`;
  poem tokens remain `ri:むかしべ.昔方`.
- `春日野` converted from `simplex` to `compound` as `かすが.春日` + `の.野`;
  poem tokens remain `ri:かすがの.春日野`.
- `春辺` converted from `simplex` to `compound` as `はる.春` + `へ.辺`;
  poem token remains `ri:はるべ.春辺`.
- `晩稲` was reviewed and left as `simplex`; removed the decomposition flag
  and the compound-review queue entry.
- `暗部` was reviewed and left as `simplex`; removed the decomposition flag
  and the compound-review queue entry.
- `更々に` was converted to a compound: `更なり` + `更なり`; the poem body
  already has following `に` as a separate token, so no body token change was made.
- `月影` was converted to a compound: `月` + `影`; poem tokens remain
  `ri:つきかげ.月影`.
- `有磯` was normalized to lemma `荒磯` and converted to a compound with
  surface `あり` + `そ`, referencing `荒し` + `磯`; `有磯海` was also normalized
  to lemma `荒磯海`, decomposing as `荒磯` + `海`.
- Added `朗なり` (`ほがら`) and converted `朗ら朗らと` to a compound:
  `朗なり` + `朗なり`; the following `と` remains a separate poem token.
- Added `夕な` (`ゆふな`) as `夕` + `な` and normalized `朝な夕なに` to lemma
  `朝な夕な`, decomposed as `朝な` + `夕な`; the poem body keeps following
  `に` as a separate `ri:に.に` token.
- Converted `朝な` to a compound: `朝` + `な`.
- Added `開く` (`ひらく`) and `ひらけ.開く`; converted `朝ぼらけ` to
  `朝` + `開く`, with surface `ぼらけ` referencing `ri:ひらけ.開く`.
- Converted `朝明` to a compound: `朝` + `明く`, with surface `け`
  referencing `ri:あけ.明く`.
- `四極` reviewed as acceptable simplex and removed from `issues-compound.txt`.
- `白妙` converted to `compound` as `白` + `栲`; poem tokens remain
  `ri:しろたへ.白妙`.
- `百千鳥` converted to `compound` as `百` + `千鳥`; poem token remains
  `ri:ももちどり.百千鳥`.
- `百敷` converted to `compound` as `百` + `敷く`; poem token remains
  `ri:ももしき.百敷`.
- `百草` converted to `compound` as `百` + `草`; poem token remains
  `ri:ももくさ.百草`.
- Added `がら` with the user's specified "すべて" sense and converted
  `皆がら` to `compound` as `皆` + `がら`; poem token remains
  `ri:みながら.皆がら`.
- Renamed `唯に` to `唯なり`, changed it from adverb to na-adjectival stem
  (`N.Suff.Ana`), and updated Dict A/body refs from `ただ.唯に` to
  `ただ.唯なり`.
- Converted `直路` to `compound` as `唯なり` + `路`; poem token remains
  `ri:ただぢ.直路`.
- Removed stale `相坂` / `逢坂` entries from the compound-review queue and
  updated `lemma-index-decomp.tsv`; `相坂` has no standalone Dict B entry and
  poem tokens point to `ri:あふさか.逢坂`.
- Added `柾` with Dict A hom `まさ.柾`; converted `真木` to `compound` as
  `柾` + `木`; poem token remains `ri:まさき.真木`.
- Added `真澄なり` with Dict A hom `ますみ.真澄なり`; `真澄なり` is a
  compound `真` + `澄む`, and `真澄鏡` is `真澄なり` + `鏡`; poem token
  remains `ri:ますかがみ.真澄鏡`.
- Latest validation: `lemma-index.xml`, `reading-index.xml`, and
  `kokinwakashu.xml` validate against `schemas/tei_all.rng`; `check_compounds.py`
  reports OK 567 / Ambiguous 0 / Failed 0; `count_pron.py` reports Total 567,
  Plain 0, Decomposed 567.

## 2026-05-06

### Changed

- `狩り` removed; `狩衣` now points to `狩る`
- `百` normalized to `pron=もも`
- `相坂` merged into `逢坂`; `逢坂` then converted to a compound
- `眼` merged into `目`
- `睦まじ` merged into `睦まし`
- `筋` modern kana removed; kept `すぢ`
- `絃` merged into `緒`
- `緒` reduced to reading `を`
- `色々` merged into `色色`; `色色` converted to a compound
- `見る` normalized to `見`; Dict A refs updated to `li:見`
- `言う` merged into `言ふ`; `へ.言ふ` restored in Dict A
- `辺` split into `辺` (`へ`) and `辺り` (`あたり`)
- `おろし` renamed to `颪`; `山颪` component refs updated
- `さつき` merged into `五月`

### Held

- `澪標`: user chose to skip for now
- `結果`: user chose not to treat `かくなわ` as a kana-normalization issue
- `衛る`: reviewed but left unchanged
- `躊躇`: reviewed; no `十六夜` entry exists in this repo, left unchanged
- `うらびる`: reviewed but left unchanged
- `がに`: reviewed; user chose not to rename to `かに`
- `さす`: reviewed; user judged the form as causative and left unchanged

### Caveats

- `check_lemma.py` can overcount poem tokens when one lemma ID is a prefix of
  another, such as `辺` vs `辺り`.
- TEI RNG validation via remote URL may fail in restricted environments; when
  that happens, at least run `xmllint --noout` for well-formedness.
