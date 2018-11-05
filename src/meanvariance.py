# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2017, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

class MeanVariance(object):
    def __init__(self, sentences, ws = 5):
        self.sentences = sentences
        self.ws = ws # window size
        self.mvDict = {}

    def getCollocsCandidates(self, w, order=True):
        return sorted(list(self.mvDict[w].items()), key=lambda x: x[1]['variance'], reverse=order)

    def build(self):
        for line in self.sentences:
            lineSize = len(line)
            for i in range(lineSize):
                w1 = line[i]

                maxWindow = min(i + 1 + self.ws, lineSize)
                for j in range(i + 1, maxWindow):
                    w2 = line[j]
                    # compute the distance between the words
                    dist = j - i
                    if w1 not in self.mvDict:
                        self.mvDict[w1] = {}
                    if w2 not in self.mvDict[w1]:
                        self.mvDict[w1][w2] = { 'dist': [dist] }
                    else:
                        self.mvDict[w1][w2]['dist'].append(dist)
                            
        for w1 in self.mvDict:
            for w2 in self.mvDict[w1]:
                dList = self.mvDict[w1][w2]['dist']
                listLen = float(len(dList))
                mean = float(sum(dList))/listLen
                self.mvDict[w1][w2]['size'] = listLen
                self.mvDict[w1][w2]['mean'] = mean
                # self.mvDict[w1][w2]['variance'] = float(sum(map(lambda x: (x - mean)**2, dList))) / max(float((listLen - 1)), 1)
                self.mvDict[w1][w2]['variance'] = float(sum([(dist - mean)**2 for dist in dList])) / max(float((listLen - 1)), 1)

    def getMVDict(self):
        return self.mvDict

# this part is just for individual testing
if __name__ == "__main__":
    import sys
    import re
    import ujson
    import utils
    import static

    cachedStopWords_en = static.stopWordsEN()
    fileType = sys.argv[1]
    files = sys.argv[2:]
    if fileType == "txt":
        sentences, words = utils.readTxtFiles(files)
    
    print("********************************")
    print("*         Mean-Variance        *")
    print("********************************")
    mv = MeanVariance(sentences)
    mv.build()
    mvDict = mv.getMVDict()

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

    # with open("bigramDict", "w") as f:
    #     print "writing to bigramDict..."
    #     ujson.dump(big, f)
