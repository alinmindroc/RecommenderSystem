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
            if i % no == 0 or i == datadim:
                self.es.bulk(index=indexname, body=bulk_data, refresh=True)
                bulk_data = []


    def searchByCollocation(self, indexname, w1, w2):
        res = self.es.search(
            index = indexname,
            body =
            {
                "query": {
                    "span_near" : {
                        "clauses": [
                            { "span_term" : { "text" : w1 }},
                            { "span_term" : { "text" : w2 }}
                        ],
                        "slop" : 6,
                        "in_order" : True,
                        "collect_payloads" : True}
                    },
                "highlight": {"fields": {"text": {}}}
            },
            size = 5)['hits']['hits']

        res.sort(key = lambda x: -x['_score'])

        return res

    def selectByQuery(self, indexname, query={}):
        res = self.es.search(index = indexname, body={"query": {"match_all": query}})
        return res

    def selectOneByID(self, indexname, doctype, id):
        result = es.get(index=indexname, doc_type=doctype, id=id)['_source']



if __name__ == "__main__":
    import sys
    import utils

    fileType = sys.argv[1]
    files = sys.argv[2:]

    if fileType == "csv":
        sentences, words, data = utils.readCsvFiles(files)
        es = ElasticsearchDDL()
        # try:
        #     es.deleteIndex("test-index")
        # except:
        #     pass

        try:
            es.createIndex(indexname="test-index")
        except:
            pass

        try:
            es.bulkInsert(indexname="test-index", doctype="_doc", data=data, no=10000)
        except:
            pass
        
        # try:
        #     res = es.selectByQuery(indexname="test-index")
        #     print(res)
        # except:
        #     pass

        res = es.selectOneByID(indexname="test-index", doctype="_doc", id=100)
        print(res)


        # try:
        #     res = es.searchByCollocation(indexname="test-index", w1="decompositions", w2="graphs")
        #     print(res)
        # except:
        #     pass

        # try:
        #     es.deleteIndex("test-index")
        # except:
        #     pass