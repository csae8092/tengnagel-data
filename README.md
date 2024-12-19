# tengnagel-data
data from https://tengnagel.univie.ac.at/

## folder csv

cvs manually populated from clicking through
https://tengnagel.univie.ac.at/ -> one of the volumes; https://tengnagel.univie.ac.at/manuscript/9737q -> one of the letters; https://tengnagel.univie.ac.at/view/o:2107725 -> go to it's collection (This object is in collection) -> https://phaidra.univie.ac.at/detail/o:2107662 -> show memebers; https://phaidra.univie.ac.at/search?page=1&pagesize=10&collection=o:2107662 -> check all and click download

url to download single tei: https://services.phaidra.univie.ac.at/api/object/o:2109781/download

## (re)create data

to (re)fetch the data run follwoing script
```bash
python download_data.py
python create_listperson.py
```
