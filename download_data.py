import glob
import os
import pandas as pd
import requests


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
