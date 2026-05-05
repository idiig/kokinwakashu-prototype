# Handoff Notes

This file is for agent-to-agent communication only.

- Put session-specific change summaries here.
- Put held / deferred entries here.
- Put temporary validation or tooling caveats here.
- Do not move stable project rules here; those belong in `AGENTS.md`.

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
