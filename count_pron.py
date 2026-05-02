from lxml import etree
NS = "http://www.tei-c.org/ns/1.0"
T = lambda t: f"{{{NS}}}{t}"
tree = etree.parse("lemma-index.xml")
total = plain = decomposed = 0
for entry in tree.findall(f".//{T('entry')}[@type='compound']"):
    pron = entry.find(f"{T('form')}[@type='lemma']/{T('pron')}")
    if pron is None: continue
    total += 1
    if pron.find(T('w')) is not None:
        decomposed += 1
    else:
        plain += 1
print(f"Total: {total}, Plain: {plain}, Decomposed: {decomposed}")
