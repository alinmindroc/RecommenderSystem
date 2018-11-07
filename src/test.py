# coding: utf-8

"""
 *
 * Copyright (C) 2018 Ciprian-Octavian Truică <ciprian.truica@cs.pub.ro>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
"""

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

    # save mean-variance dictionary to file
    mv.saveToFile("mvdict.json")
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

    # save prefix tree build with mean-variance to file
    pt.saveToFile("mvtree.json")

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

    # save chi-squared dictionary to file
    cs.saveToFile("chidict.json")

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

    # save prefix tree build with chi-squared to file
    pt.saveToFile("cstree.json")

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

    print(list(s1)[0])
    w1, w2 = list(s1)[0][0].split(" ")
    print(w1, w2)

    res = es.searchByCollocation(indexname="test-index", w1=w1, w2=w2)
    print(res)
