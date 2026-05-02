"""
Check compound entries in lemma-index.xml:
For each compound, try to decompose its pron text using readings from reading-index.xml.
Supports: exact match, rendaku (voicing of first char), verbal stem (strip final る).
Report OK (unique), Ambiguous (multiple), or Failed (no match).
"""
from lxml import etree
from itertools import product

NS = "http://www.tei-c.org/ns/1.0"
T = lambda tag: f"{{{NS}}}{tag}"
XML_NS = "http://www.w3.org/XML/1998/namespace"

RENDAKU = str.maketrans(
    'かきくけこさしすせそたちつてとはひふへほ',
    'がぎぐげござじずぜぞだぢづでどばびぶべぼ'
)


def reading_variants(reading):
    """All phonological forms to try for a reading."""
    variants = [reading]
    # verbal stem: strip final る (一段動詞 連用形)
    if reading.endswith('る'):
        variants.append(reading[:-1])
    # adjective stem: strip final い (形容詞 語幹)
    if reading.endswith('い') and len(reading) > 1:
        variants.append(reading[:-1])
    return variants


def build_lemma_to_homs(reading_index_path):
    """Build map: lemma_id -> [(reading, hom_id), ...]"""
    tree = etree.parse(reading_index_path)
    result = {}
    for hom in tree.findall(f".//{T('hom')}"):
        hom_id = hom.get(f"{{{XML_NS}}}id")
        if not hom_id or "." not in hom_id:
            continue
        reading = hom_id.split(".", 1)[0]
        ref = hom.find(T("ref"))
        if ref is None:
            continue
        target = ref.get("target", "")
        if target.startswith("li:"):
            lemma_id = target[3:]
            result.setdefault(lemma_id, []).append((reading, hom_id))
    return result


def find_decompositions(pron, components, lemma_to_homs):
    """
    Try to match component readings left-to-right against pron.
    Priority: exact > stem (strip る) > rendaku.
    Returns list of best-priority matched combos: [(reading, hom_id, actual_form, rendaku), ...]
    or None if a component has no homs at all.
    """
    candidates = []
    for lemma_id in components:
        homs = lemma_to_homs.get(lemma_id, [])
        if not homs:
            return None
        candidates.append(homs)

    # Collect all results with their priority (lower = better)
    # priority: 0=exact, 1=stem, 2=rendaku, 3=stem+rendaku
    all_results = []  # [(priority_sum, combo)]

    def recurse(pos, idx, current, priority_sum):
        if idx == len(candidates):
            if pos == len(pron):
                all_results.append((priority_sum, tuple(current)))
            return
        for reading, hom_id in candidates[idx]:
            variants = reading_variants(reading)
            for vi, variant in enumerate(variants):
                stem_penalty = vi  # 0 for base, 1 for stem
                # exact match
                if pron[pos:pos + len(variant)] == variant:
                    current.append((reading, hom_id, variant, False))
                    recurse(pos + len(variant), idx + 1, current, priority_sum + stem_penalty)
                    current.pop()
                    continue
                # rendaku match
                if variant:
                    voiced = variant[0].translate(RENDAKU) + variant[1:]
                    if voiced != variant and pron[pos:pos + len(voiced)] == voiced:
                        current.append((reading, hom_id, voiced, True))
                        recurse(pos + len(voiced), idx + 1, current, priority_sum + stem_penalty + 2)
                        current.pop()

    recurse(0, 0, [], 0)

    if not all_results:
        return []

    # Return only results with the best (lowest) priority
    best_priority = min(p for p, _ in all_results)
    best = [combo for p, combo in all_results if p == best_priority]
    # Deduplicate
    seen = set()
    unique = []
    for combo in best:
        key = tuple((hom_id, actual) for _, hom_id, actual, _ in combo)
        if key not in seen:
            seen.add(key)
            unique.append(combo)
    return unique


def main():
    lemma_path = "lemma-index.xml"
    reading_path = "reading-index.xml"

    lemma_to_homs = build_lemma_to_homs(reading_path)

    tree = etree.parse(lemma_path)

    ok = []
    ambiguous = []
    failed = []

    for entry in tree.findall(f".//{T('entry')}[@type='compound']"):
        entry_id = entry.get(f"{{{XML_NS}}}id", "?")

        pron_el = entry.find(f".//{T('form')}[@type='lemma']/{T('pron')}")

        # Skip already-decomposed entries (pron contains <w> children)
        if pron_el is not None and pron_el.find(T('w')) is not None:
            ok.append((entry_id, "".join(pron_el.itertext()), []))
            continue

        pron = pron_el.text.strip() if pron_el is not None and pron_el.text else ""

        compound_form = entry.find(f"{T('form')}[@type='compound']")
        if compound_form is None:
            continue
        components = []
        for ref in compound_form.findall(T("ref")):
            target = ref.get("target", "")
            if target.startswith("#"):
                components.append(target[1:])

        if not pron or not components:
            failed.append((entry_id, pron, components, "missing pron or components", []))
            continue

        result = find_decompositions(pron, components, lemma_to_homs)

        if result is None:
            missing = [c for c in components if c not in lemma_to_homs]
            failed.append((entry_id, pron, components, "component not in reading-index", missing))
        elif len(result) == 0:
            failed.append((entry_id, pron, components, "no matching decomposition",
                           {c: lemma_to_homs.get(c, []) for c in components}))
        elif len(result) == 1:
            ok.append((entry_id, pron, result[0]))
        else:
            ambiguous.append((entry_id, pron, result))

    print(f"=== OK ({len(ok)}) ===")
    for entry_id, pron, combo in ok:
        if not combo:
            print(f"  {entry_id}: {pron} [already decomposed]")
            continue
        parts = []
        for reading, hom_id, actual, is_rendaku in combo:
            label = f"ri:{hom_id}"
            if is_rendaku:
                label += " [rendaku]"
            if actual != reading:
                label += f" [stem: {reading}→{actual}]"
            parts.append(label)
        print(f"  {entry_id}: {pron} → {' + '.join(parts)}")

    print(f"\n=== Ambiguous ({len(ambiguous)}) ===")
    for entry_id, pron, combos in ambiguous:
        print(f"  {entry_id}: {pron}")
        for combo in combos:
            parts = [f"ri:{hom_id}({'rendaku' if r else ''})" for _, hom_id, _, r in combo]
            print(f"    → {' + '.join(parts)}")

    print(f"\n=== Failed ({len(failed)}) ===")
    for entry_id, pron, components, reason, detail in failed:
        print(f"  {entry_id}: {pron} | {reason}")
        if isinstance(detail, list):
            for c in components:
                homs = lemma_to_homs.get(c, [])
                tag = "(not found)" if not homs else str([h for _, h in homs])
                print(f"    {c} → {tag}")
        elif isinstance(detail, dict):
            for c, homs in detail.items():
                tag = "(not found)" if not homs else str([h for _, h in homs])
                print(f"    {c} → {tag}")


if __name__ == "__main__":
    main()
