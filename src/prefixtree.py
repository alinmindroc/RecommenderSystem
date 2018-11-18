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

class PrefixTree(object):
    def __init__(self, wordsDict = None):
        if wordsDict:
            self.wordsDict = wordsDict
            self.words = self.wordsDict.keys()
        self.tree = dict()
        self.end = '_end_'

    def buildPrefixTree(self):
        self.tree = dict()
        crt_dict = self.tree

        for word in self.words:
            crt_dict = self.tree
            for letter in word:
                crt_dict = crt_dict.setdefault(letter, {})
            crt_dict[self.end] = len(self.wordsDict[word])

    def getPrefixTree(self):
        return self.tree

    # exists in tree: oprig name in_trie
    def exists(self, word, is_prefix=False):
        crt_dict = self.tree
        for letter in word:
            if letter in crt_dict:
                crt_dict = crt_dict[letter]
            else:
                return False
        else:#no letter found
            if self.end in crt_dict:
                return True
            else:
                return is_prefix

    def dfs(self, tree,  crt_suffix, all_suffixes):
        if type(tree) is int:
            all_suffixes.append([crt_suffix, tree])
            return
        for k in tree.keys():
            if k != self.end:
                self.dfs(tree[k], crt_suffix + k, all_suffixes)
            else:
                self.dfs(tree[k], crt_suffix, all_suffixes)

    # original name get_recommendations
    def getRecommendations(self, prefix):
        if not self.exists(prefix, is_prefix=True):
            return []

        crt_dict = self.tree
        for letter in prefix:
            crt_dict = crt_dict[letter]

        res = []
        self.dfs(crt_dict, '', res)
        return sorted(map(lambda x: (prefix + x[0], x[1]), res), key = lambda x: -x[1])

    def saveToFile(self, filename):
        import ujson
        with open(filename, 'w') as f:
            ujson.dump(self.tree, f)

    def loadFromJson(self, jsonContent):
        self.tree = jsonContent

# this part is just for individual testing
if __name__ == '__main__':
    import sys
    import re
    import ujson
    import utils
    from chisquared import ChiSquared
    from meanvariance import MeanVariance

    fileType = sys.argv[1]
    files = sys.argv[2:]
    if fileType == "txt":
        sentences, words = utils.readTxtFiles(files)

    # Chi-Squared
    cs = ChiSquared(sentences)
    cs.build()
    chiDict = cs.getChiDict()

    pt = PrefixTree(wordsDict=chiDict)
    pt.buildPrefixTree()
    print(pt.getRecommendations("k"))
    # trie = pt.getPrefixTree()

    # mean-variance
    mv = MeanVariance(sentences)
    mv.build()
    mvDict = mv.getMVDict()

    pt = PrefixTree(wordsDict=mvDict)
    pt.buildPrefixTree()
    print(pt.getRecommendations("k"))

    
    # with open('trie.json', 'w') as f:
    #   ujson.dump(trie, f)

