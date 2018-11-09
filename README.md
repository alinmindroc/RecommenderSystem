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





