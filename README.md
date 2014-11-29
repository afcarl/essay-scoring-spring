Installation
========================

This code uses Python. Linux environment is needed for the code to run smoothly.

Setting up the environment

**Create Python environment** 
```
virtualenv --no-site-packages env
```

**Activate the environment**
```
source env/bin/activate
```

**Install requirements**
```
pip install -r requirements.txt
```

**Download wikipedia n-grams**
```
./features/wikipedia/download.sh
```

After downloading you must create a database ```wiki``` in PostgreSQL.

And then configure file ```features/wiki_ngram_coverage.py```

```
conn = psycopg2.connect("dbname='wiki' user='postgres' host='localhost' port=5432 password='XXXX'")
```

Change the user and password to be able to use wikipedia coverage features

Importing data
========================

1. Put xml files in data/xml/training/ and data/xml/validation
2. Run script

```
python 1_import_raw_data.py
```

It will combine and transform the XML files into CSV format.


Creating models
========================

Run script

```
python 2_model_generic.py
```

Ensembling models
========================

Run script

```
python 3_create_ensemble.py
```

Exporting the results
========================

Run script

```
python 4_export_results.py
```
