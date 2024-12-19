import os
import ast
import pandas as pd
import lxml.etree as ET
from rdflib import Graph
from tqdm import tqdm
from acdh_tei_pyutils.tei import TeiReader


print("scrapes person-skos-collection and creates a listperson.xml")
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
    item = {"ids": [], "label": ""}
    for s, p, o in g.triples((None, None, None)):
        if str(p) == "http://www.w3.org/2004/02/skos/core#prefLabel":
            item["label"] = str(o)
        if str(p) == "http://www.w3.org/2004/02/skos/core#relatedMatch":
            item["ids"].append(str(o))
    items.append(item)


df = pd.DataFrame(items)
df.to_csv("persons.csv", index=False)
template = """
<TEI xmlns="http://www.tei-c.org/ns/1.0">
   <teiHeader>
      <fileDesc>
         <titleStmt>
            <title type="main">Personenverzeichnis</title>
            <respStmt>
               <persName><surname>Petrolini</surname><forename>Chiara</forename></persName>
               <resp>Data acquisition</resp>
            </respStmt>
            <respStmt>
               <persName><surname>Wallnig</surname><forename>Thomas</forename></persName>
               <resp>Data curation</resp>
            </respStmt>
         </titleStmt>
         <editionStmt>
            <edition>The Tengnagel Correspondence Data</edition>
            <principal><forename>Thomas</forename><surname>Wallnig</surname></principal>
            <funder ref="https://www.fwf.ac.at/forschungsradar/10.55776/P30511">FWF P
               30511</funder>
         </editionStmt>
         <publicationStmt>
            <publisher><orgName>Phaidra</orgName><ref target="https://phaidra.univie.ac.at/"
                  >https://phaidra.univie.ac.at/</ref></publisher>
            <date type="first" when="2024">2024</date>
            <pubPlace>Vienna</pubPlace>
            <availability status="free">
               <licence target="https://creativecommons.org/licenses/by-sa/4.0/">Creative
                  Commons Attribution-Sharealike 4.0 International (CC BY-SA 4.0)</licence>
            </availability>
            <idno>o:2107731</idno>
            <idno type="URI">https://phaidra.univie.ac.at/o:2107731</idno>
         </publicationStmt>
         <sourceDesc>
            <ab>created with create_listperson.py</ab>
         </sourceDesc>
      </fileDesc>
   </teiHeader>
  <text>
      <body>
         <listPerson/>
      </body>
  </text>
</TEI>
"""
doc = TeiReader(template)
listperson = doc.any_xpath(".//tei:listPerson")[0]
df = pd.read_csv("persons.csv")
for i, row in df.iterrows():
    entity_id = f"person__{i + 1:04}"
    ids = ast.literal_eval(row["ids"])
    person = ET.Element("{http://www.tei-c.org/ns/1.0}person")
    person.attrib["{http://www.w3.org/XML/1998/namespace}id"] = entity_id
    listperson.append(person)
    persname = ET.Element("{http://www.tei-c.org/ns/1.0}persName")
    try:
        persname.text = row["label"]
    except:  # noqa:
        persname.text = "Unbekannt"
    person.append(persname)
    for x in ids:
        if "wikidata" in x:
            type = "wikidata"
        elif "viaf" in x:
            type = "viaf"
        elif "cerl" in x:
            type = "cerl"
        else:
            type = "other"
        idno = ET.Element("{http://www.tei-c.org/ns/1.0}idno")
        idno.attrib["type"] = type
        idno.text = x
        person.append(idno)
doc.tree_to_file(os.path.join("data", "indices", "listperson.xml"))
