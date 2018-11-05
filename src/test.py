# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2017, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

import sys
import re
import ujson    
import utils
import static
from chisquared import ChiSquared
from meanvariance import MeanVariance
from prefixtree import PrefixTree
import time
from elasticsearchddl import ElasticsearchDDL


cachedStopWords_en = static.stopWordsEN()

def testWord(word):
    if word in cachedStopWords_en or not re.sub(r'\w*\d\w*', '', word) or len(word) < 3:
        return False
    return True

if __name__ == '__main__':
    fileType = sys.argv[1]
    topK = int(sys.argv[2])    
    files = sys.argv[3:]

    if fileType == "txt":
        sentences, words, data = utils.readTxtFiles(files)
    elif fileType == "csv":
        sentences, words, data = utils.readCsvFiles(files)

    # mean-variance
    print("********************************")
    print("*         Mean-Variance        *")
    print("********************************")

    start = time.time()
    mv = MeanVariance(sentences)
    mv.build()
    mvDict = mv.getMVDict()
    stop = time.time()
    print("Mean-Variance build time (s):", (stop - start))

    # test get collocations
    # print(mv.getCollocsCandidates("kid"))

    # get top 20 
    start = time.time()
    d = {}
    for w1 in mvDict:
        for w2 in mvDict[w1]:
            # do not take into account stopwords, words with length <3 and words that contain numbers
            if testWord(w1) and testWord(w2):
                d[str(w1) + " " + str(w2)] = mvDict[w1][w2]["variance"]
            
    
    s1 = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    print(s1[0:topK])
    stop = time.time()
    print("Mean-Variance get top " + str(topK) + " collocations time (s):", (stop - start))

    # get bottom 20 
    start = time.time()
    d = {}
    for w1 in mvDict:
        for w2 in mvDict[w1]:
            # do not take into account stopwords, words with length <3 and words that contain numbers
            if testWord(w1) and testWord(w2):
                d[str(w1) + " " + str(w2)] = mvDict[w1][w2]["variance"]

    s2 = [(k, d[k]) for k in sorted(d, key=d.get, reverse=False)]
    print(s2[0:topK])
    stop = time.time()
    print("Mean-Variance get bottom " + str(topK) + " collocations time (s):", (stop - start))

    # # get Arthur
    # d = {}
    # for w2 in mvDict['arthur']:
    #     if testWord(w2):
    #         d["arthur " + str(w2)] = mvDict['arthur'][w2]["variance"]
    # sa = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    # print(sa)
    
    # # get Ford
    # d = {}
    # for w2 in mvDict['ford']:
    #     if testWord(w2):
    #         d["ford " + str(w2)] = mvDict['ford'][w2]["variance"]
    # sf = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    # print(sf)

    # # get Zaphod
    # d = {}
    # for w2 in mvDict['zaphod']:
    #     if testWord(w2):
    #         d["zaphod " + str(w2)] = mvDict['zaphod'][w2]["variance"]
    # sz = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    # print(sz)

    start = time.time()
    pt = PrefixTree(wordsDict=mvDict)
    pt.buildPrefixTree()
    stop = time.time()
    print("Mean-Variance build prefix tree time (s):", (stop - start))
    print(pt.getRecommendations("k"))

    # Chi-Squared 
    print("********************************")
    print("*          Chi-Squared         *")
    print("********************************")

    start = time.time()

    cs = ChiSquared(sentences)
    cs.build()
    chiDict = cs.getChiDict()

    stop = time.time()
    print("Chi-Squared build time (s):", (stop - start))

    # test get collocations
    # print(cs.getCollocsCandidates("kid"))

    # get top 20 
    start = time.time()
    d = {}
    for w1 in chiDict:
        for w2 in chiDict[w1]:
            # do not take into account stopwords, words with length <3 and words that contain numbers
            if testWord(w1) and testWord(w2):
                d[str(w1) + " " + str(w2)] = chiDict[w1][w2]["chisquared"]
            
    s1 = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    print(s1[0:topK])
    stop = time.time()
    print("Chi-Squared get top " + str(topK) + " collocations time (s):", (stop - start))
    
    # get bottom 20 
    start = time.time()
    d = {}
    for w1 in chiDict:
        for w2 in chiDict[w1]:
            # do not take into account stopwords, words with length <3 and words that contain numbers
            if testWord(w1) and testWord(w2):
                d[str(w1) + " " + str(w2)] = chiDict[w1][w2]["chisquared"]

    s2 = [(k, d[k]) for k in sorted(d, key=d.get, reverse=False)]
    print(s2[0:topK])
    stop = time.time()
    print("Chi-Squared get bottom " + str(topK) + " collocations time (s):", (stop - start))

    # # get Arthur
    # d = {}
    # for w2 in chiDict['arthur']:
    #     if testWord(w2):
    #         d["arthur " + str(w2)] = chiDict['arthur'][w2]["chisquared"]
    # sa = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    # print(sa)
    
    # # get Ford
    # d = {}
    # for w2 in chiDict['ford']:
    #     if testWord(w2):
    #         d["ford " + str(w2)] = chiDict['ford'][w2]["chisquared"]
    # sf = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    # print(sf)

    # # get Zaphod
    # d = {}
    # for w2 in chiDict['zaphod']:
    #     if testWord(w2):
    #         d["zaphod " + str(w2)] = chiDict['zaphod'][w2]["chisquared"]
    # sz = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    # print(sz)

    start = time.time()
    pt = PrefixTree(wordsDict=chiDict)
    pt.buildPrefixTree()
    stop = time.time()
    print("Chi-Squared build prefix tree time (s):", (stop - start))

    print(pt.getRecommendations("k"))

    print("********************************")
    print("*        Elasticsearch         *")
    print("********************************")

    es = ElasticsearchDDL()

    if es.indexEsists("test-index"):
        es.deleteIndex("test-index")

    es.createIndex(indexname="test-index")

    es.bulkInsert(indexname="test-index", doctype="_doc", data=data, no=10000)
        

    res = es.selectByQuery(indexname="test-index")
    print(res)

    res = es.selectOneByID(indexname="test-index", doctype="_doc", id=1)
    print(res)

    w1, w2 = list(s1)[3].split(" ")
    res = es.searchByCollocation(indexname="test-index", w1=w1, w2=w2)
    print(res)
        
    es.deleteIndex("test-index")