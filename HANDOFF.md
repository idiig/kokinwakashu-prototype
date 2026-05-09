# Handoff Notes

This file is for agent-to-agent communication only.

- Put session-specific change summaries here.
- Put held / deferred entries here.
- Put temporary validation or tooling caveats here.
- Do not move stable project rules here; those belong in `AGENTS.md`.

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

- Continue `issues-compound.txt` from 心地 (line 140) onward

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
