from rdflib import Graph
from tqdm import tqdm
import pandas as pd

print("scraps person-skos-collection and creates a listperson.xml")
collection_graph = Graph()
collection_graph.parse("skos/MEYV-0NCM.rdf")

items = []
for subject, predicate, object in tqdm(collection_graph.triples((None, None, None))):
    uri = f"{str(object)}.ttl"
    g = Graph()
    try:
        g.parse(uri)
    except Exception as e:
        print(uri, e)
        continue
    item = {
        "ids": [],
        "label": ""
    }
    for s, p, o in g.triples((None, None, None)):
        if str(p) == "http://www.w3.org/2004/02/skos/core#prefLabel":
            item["label"] = str(o)
        if str(p) == "http://www.w3.org/2004/02/skos/core#relatedMatch":
            item["ids"].append(str(o))
    items.append(item)


df = pd.DataFrame(items)
df.to_csv("persons.csv", index=False)
