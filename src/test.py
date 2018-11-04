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
    files = sys.argv[1:]
    sentences, words = utils.readFile(files)

    # mean-variance
    print("********************************")
    print("*         Mean-Variance        *")
    print("********************************")

    start = time.time() * 1000

    mv = MeanVariance(sentences)
    mv.build()
    mvDict = mv.getMVDict()

    stop = time.time() * 1000
    print("Mean-Variance time:", (stop - start))

    # test get collocations
    # print(mv.getCollocsCandidates("kid"))

    # sort
    d = {}
    for w1 in mvDict:
        for w2 in mvDict[w1]:
            # do not take into account stopwords
            if w1 not in cachedStopWords_en and w2 not in cachedStopWords_en:
                d[str(w1) + " " + str(w2)] = mvDict[w1][w2]["variance"]
            
    # get top 20 
    s1 = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    print(s1[0:20])

    # get bottom 20 
    s2 = [(k, d[k]) for k in sorted(d, key=d.get, reverse=False)]
    print(s2[0:20])

    pt = PrefixTree(wordsDict=mvDict)
    pt.buildPrefixTree()
    print(pt.getRecommendations("k"))

    # Chi-Squared 
    print("********************************")
    print("*          Chi-Squared         *")
    print("********************************")

    start = time.time() * 1000

    cs = ChiSquared(sentences)
    cs.build()
    chiDict = cs.getChiDict()

    stop = time.time() * 1000
    print("Chi-Squared time:", (stop - start))

    # test get collocations
    # print(cs.getCollocsCandidates("kid"))

    # sort
    d = {}
    for w1 in chiDict:
        for w2 in chiDict[w1]:
            # do not take into account stopwords
            if w1 not in cachedStopWords_en and w2 not in cachedStopWords_en:
                d[str(w1) + " " + str(w2)] = chiDict[w1][w2]["chisquared"]
            
            
    # get top 20 
    s1 = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    print(s1[0:20])
    
    # get bottom 20 
    s2 = [(k, d[k]) for k in sorted(d, key=d.get, reverse=False)]
    print(s2[0:20])

    pt = PrefixTree(wordsDict=chiDict)
    pt.buildPrefixTree()
    print(pt.getRecommendations("k"))
    # trie = pt.getPrefixTree()