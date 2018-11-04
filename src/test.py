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


cachedStopWords_en = static.stopWordsEN()

if __name__ == '__main__':
    topK = int(sys.argv[1])
    files = sys.argv[2:]
    sentences, words = utils.readFile(files)

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
            # do not take into account stopwords
            if w1 not in cachedStopWords_en and w2 not in cachedStopWords_en:
                d[str(w1) + " " + str(w2)] = mvDict[w1][w2]["variance"]
            
    
    s1 = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    print(s1[0:    print(pt.getRecommendations("k"))])
    stop = time.time()
    print("Mean-Variance get top + " topK " + collocations (s):", (stop - start))

    # get bottom 20 
    start = time.time()
    d = {}
    for w1 in mvDict:
        for w2 in mvDict[w1]:
            # do not take into account stopwords
            if w1 not in cachedStopWords_en and w2 not in cachedStopWords_en:
                d[str(w1) + " " + str(w2)] = mvDict[w1][w2]["variance"]

    s2 = [(k, d[k]) for k in sorted(d, key=d.get, reverse=False)]
    print(s2[0:])
    stop = time.time()
    print("Mean-Variance get bottom + " topK " + collocations (s):", (stop - start))

    start = time.time()
    pt = PrefixTree(wordsDict=mvDict)
    pt.buildPrefixTree()
    print(pt.getRecommendations("k"))
    stop = time.time()
    print("Mean-Variance build prefix tree (s)):", (stop - start))

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
            # do not take into account stopwords
            if w1 not in cachedStopWords_en and w2 not in cachedStopWords_en:
                d[str(w1) + " " + str(w2)] = chiDict[w1][w2]["chisquared"]
            
    s1 = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    print(s1[0:topK])
    stop = time.time()
    print("Chi-Squared get top + " topK " + collocations time (s):", (stop - start))
    
    # get bottom 20 
    start = time.time()
    d = {}
    for w1 in chiDict:
        for w2 in chiDict[w1]:
            # do not take into account stopwords
            if w1 not in cachedStopWords_en and w2 not in cachedStopWords_en:
                d[str(w1) + " " + str(w2)] = chiDict[w1][w2]["chisquared"]

    s2 = [(k, d[k]) for k in sorted(d, key=d.get, reverse=False)]
    print(s2[0:topK])
    stop = time.time()
    print("Chi-Squared get bottom + " topK " + collocations time (s):", (stop - start))

    start = time.time()
    pt = PrefixTree(wordsDict=chiDict)
    pt.buildPrefixTree()
    stop = time.time()
    print("Chi-Squared build prefix tree (s)):", (stop - start))

    print(pt.getRecommendations("k"))

    