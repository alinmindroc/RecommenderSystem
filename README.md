# Collocation detector for recommander systems

This code was written using python3.
You will also need an Elasticsearch server running either localy of in the Cloud.

To the the system locally, from the root directory issue the following command:

`python3 test.py filetype top dataset [dataset]`

- filetype is the file type, currently supports csv (with 2 collumns title and text) or txt. 
- top is the number for extracting the top and bottom collocations
- dataset is the file name of path to files

E.g.:

`python3 src/test.py txt 20 datasets/hitchhiker.txt`
`python3 src/test.py csv 20 datasets/arxiv1.csv`

### Python packages:
* nltk
* stop_words

### Running the demo web app:
The demo application gathers all sentences in a given text and bulk inserts them into an ElasticSearch index. The chi-squared and mean-variance methods can be tested then by querying the index with generated word pairs.

- run src/test.py as mentioned previously. This will populate a local elasticsearch cluster with sentences and generate the prefix trees and dictionaries containing chi-squared and variance scores for all word pairs
- run server.py, which will open a web interface at http://0.0.0.0:5000/

