"""
Apply <w lemmaRef="ri:..."> decomposition to <pron> of compound entries in lemma-index.xml.
- Surface text: actual form in compound (including rendaku)
- lemmaRef: ri:<hom_id> (canonical, non-dakuon reading)
Only modifies entries where decomposition is unambiguously OK.
"""
from lxml import etree

NS = "http://www.tei-c.org/ns/1.0"
T = lambda tag: f"{{{NS}}}{tag}"
XML_NS = "http://www.w3.org/XML/1998/namespace"

RENDAKU = str.maketrans(
    'かきくけこさしすせそたちつてとはひふへほ',
    'がぎぐげござじずぜぞだぢづでどばびぶべぼ'
)


def reading_variants(reading):
    variants = [reading]
    if reading.endswith('る'):
        variants.append(reading[:-1])
    if reading.endswith('い') and len(reading) > 1:
        variants.append(reading[:-1])
    return variants


def build_lemma_to_homs(reading_index_path):
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


def find_decomposition(pron, components, lemma_to_homs):
    """Return unique best-priority decomposition or None."""
    candidates = []
    for lemma_id in components:
        homs = lemma_to_homs.get(lemma_id, [])
        if not homs:
            return None
        candidates.append(homs)

    all_results = []

    def recurse(pos, idx, current, priority_sum):
        if idx == len(candidates):
            if pos == len(pron):
                all_results.append((priority_sum, tuple(current)))
            return
        for reading, hom_id in candidates[idx]:
            for vi, variant in enumerate(reading_variants(reading)):
                stem_penalty = vi
                if pron[pos:pos + len(variant)] == variant:
                    current.append((hom_id, variant, False))
                    recurse(pos + len(variant), idx + 1, current, priority_sum + stem_penalty)
                    current.pop()
                    continue
                if variant:
                    voiced = variant[0].translate(RENDAKU) + variant[1:]
                    if voiced != variant and pron[pos:pos + len(voiced)] == voiced:
                        current.append((hom_id, voiced, True))
                        recurse(pos + len(voiced), idx + 1, current, priority_sum + stem_penalty + 2)
                        current.pop()

    recurse(0, 0, [], 0)
    if not all_results:
        return None
    best_priority = min(p for p, _ in all_results)
    best = list({tuple((h, a) for h, a, _ in combo): combo
                 for p, combo in all_results if p == best_priority}.values())
    return best[0] if len(best) == 1 else None


def apply_pron_decomposition(lemma_path, reading_path, dry_run=False):
    lemma_to_homs = build_lemma_to_homs(reading_path)
    tree = etree.parse(lemma_path)

    applied = skipped_fail = skipped_already = 0

    for entry in tree.findall(f".//{T('entry')}[@type='compound']"):
        entry_id = entry.get(f"{{{XML_NS}}}id", "?")

        pron_el = entry.find(f"{T('form')}[@type='lemma']/{T('pron')}")
        if pron_el is None:
            continue
        # Skip already decomposed
        if pron_el.find(T('w')) is not None:
            skipped_already += 1
            continue

        pron_text = pron_el.text.strip() if pron_el.text else ""

        compound_form = entry.find(f"{T('form')}[@type='compound']")
        if compound_form is None:
            skipped_fail += 1
            continue
        components = []
        for ref in compound_form.findall(T("ref")):
            t = ref.get("target", "")
            if t.startswith("#"):
                components.append(t[1:])

        if not pron_text or not components:
            skipped_fail += 1
            continue

        combo = find_decomposition(pron_text, components, lemma_to_homs)
        if combo is None:
            skipped_fail += 1
            continue

        # Build new pron element
        if not dry_run:
            pron_el.text = None
            for child in list(pron_el):
                pron_el.remove(child)
            for i, (hom_id, surface, _) in enumerate(combo):
                w = etree.SubElement(pron_el, T('w'))
                w.set("lemmaRef", f"ri:{hom_id}")
                w.text = surface
                w.tail = None
            pron_el.tail = pron_el.tail  # preserve
        applied += 1
        if dry_run:
            parts = " + ".join(f"<w lemmaRef='ri:{h}'>{s}</w>" for h, s, _ in combo)
            print(f"  {entry_id}: {pron_text} → {parts}")

    print(f"\nApplied: {applied}, Already done: {skipped_already}, Failed/skipped: {skipped_fail}")

    if not dry_run and applied > 0:
        tree.write(lemma_path, encoding="UTF-8", xml_declaration=True, pretty_print=False)
        print(f"Written to {lemma_path}")


if __name__ == "__main__":
    import sys
    dry_run = "--dry-run" in sys.argv
    apply_pron_decomposition("lemma-index.xml", "reading-index.xml", dry_run=dry_run)
