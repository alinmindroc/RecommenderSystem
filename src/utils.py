import sys
from os import listdir
from os.path import isfile, isdir, join
import re
from nltk import sent_tokenize
from cleantext import CleanText
import static
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor

cachedStopWords_en = static.stopWordsEN()
ct = CleanText()

def processElement(file):
    with open(file) as inFile:
        data = inFile.read().replace('\n', ' ')
        cleanText, hashtags, attags = ct.cleanText(data)
        return list(map(lambda x: ct.removePunctuation(x.lower()), sent_tokenize(cleanText)))

def readFile(uri):
    filelist = []

    for mypath in uri:
        if isdir(mypath):
            filelist += [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
        elif isfile(mypath):
            filelist.append(mypath)

    if filelist:
        no_threads = int(cpu_count()-1)
        fullTexts = []

        with ProcessPoolExecutor(max_workers=no_threads) as worker:
            for result in worker.map(processElement, filelist):
                if result:
                    fullTexts.extend(result)
        # single thread version
        # for file in filelist:
        #     with open(file) as inFile:
        #         data = inFile.read().replace('\n', ' ')
        #         cleanText, hashtags, attags = ct.cleanText(data)
        #         fullTexts.extend(list(map(lambda x: ct.removePunctuation(x.lower()), sent_tokenize(cleanText))))
        sentences = [list(map(lambda x: x, re.findall('\w+', line))) for line in fullTexts]
        words = [word for sentence in sentences for word in sentence]
        return sentences, words

if __name__ == "__main__":
    uri = sys.argv[1:]
    readFile(uri)


