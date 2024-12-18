import glob
import os
import pandas as pd
import requests
from acdh_tei_pyutils.tei import TeiReader


print("downloads single tei files from phaidra")
url_stub = "https://services.phaidra.univie.ac.at/api/object/{}/download"


for volume, x in enumerate(glob.glob("./csv/*.csv"), start=1):
    df = pd.read_csv(x)
    for i, row in df.iterrows():
        f_name = f"tn_bd{volume}-{i + 1:03}.xml"
        url = url_stub.format(row["pid"])
        save_path = os.path.join("data", "editions", f_name)
        response = requests.get(url)
        with open(save_path, "wb") as file:
            file.write(response.content)


print("and now make well formed xml files out of it")

files = sorted(glob.glob("data/editions/*.xml"))
for filename in files:
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
        better_content = (
            content.replace(
                'xml:id="https://pid.phaidra.org/vocabulary',
                'key="https://pid.phaidra.org/vocabulary',
            )
            .replace(' xml:id=""', "")
            .replace(" & ", " &amp;")
            .replace("< ", " &lt; ")
        )
    with open(filename, "w", encoding="utf-8") as file:
        file.write(better_content)

for x in files:
    try:
        doc = TeiReader(x)
    except Exception as e:
        print(x, e)
