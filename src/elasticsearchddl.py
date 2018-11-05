from elasticsearch import Elasticsearch
from datetime import datetime

class ElasticsearchDDL(object):
    def __init__(self, host='localhost', port='9200'):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def createIndex(self, indexname):
        self.es.indices.create(index=indexname)

    def deleteIndex(self, indexname):
        self.es.indices.delete(index=indexname)

    def bulkInsert(self, indexname, doctype, data, no):
        datadim = len(data)
        bulk_data = []
        i = 0
        for elem in data:
            data_dict = {
                "id": i, 
                "title": elem["title"],
                "text": elem["text"]
            }
            op_dict = {
                "index": {
                    "_index": indexname,
                    "_type": doctype,
                    "_id": data_dict["id"]
                }
            }
            bulk_data.append(op_dict)
            bulk_data.append(data_dict)
            if i % no == 0 or i == datadim - 1:
                self.es.bulk(index=indexname, body=bulk_data, refresh=True)
                bulk_data = []
            i += 1


    def searchByCollocation(self, indexname, w1, w2):
        res = self.es.search(
            index = indexname,
            body =
            {
                "query": {
                    "span_near" : {
                        "clauses": [
                            { "span_term" : { "text" : "statistics" }},
                            { "span_term" : { "text" : "demonstrated" }}
                        ],
                        "slop" : 6,
                        "in_order" : True}
                    },
                    "highlight": {"fields": {"text": {}}}
            },
            size = 5)

        return res

    def selectByQuery(self, indexname, query={}):
        res = self.es.search(index = indexname, body={"query": {"match_all": query}})
        return res

    def selectOneByID(self, indexname, doctype, id):
        result = self.es.get(index=indexname, doc_type=doctype, id=id)['_source']

    def indexEsists(self, indexname):
        return self.es.indices.exists(index=indexname)

if __name__ == "__main__":
    import sys
    import utils

    fileType = sys.argv[1]
    files = sys.argv[2:]

    if fileType == "csv":
        sentences, words, data = utils.readCsvFiles(files)
        es = ElasticsearchDDL()
        if es.indexEsists("test-index"):
            es.deleteIndex("test-index")

        es.createIndex(indexname="test-index")

        es.bulkInsert(indexname="test-index", doctype="_doc", data=data, no=10000)
        

        res = es.selectByQuery(indexname="test-index")
        print(res)

        res = es.selectOneByID(indexname="test-index", doctype="_doc", id=100)
        print(res)


        res = es.searchByCollocation(indexname="test-index", w1="statistics", w2="demonstrated")
        print(res)
        
        es.deleteIndex("test-index")
        