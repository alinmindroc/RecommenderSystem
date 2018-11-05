# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2017, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

import sys
from os import listdir
from os.path import isfile, isdir, join
import re
from nltk import sent_tokenize
from cleantext import CleanText
import static
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor
import csv

cachedStopWords_en = static.stopWordsEN()
ct = CleanText()

#this part is for reading the file


def readCSVFile(filename):
    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ",")     
        h = next(spamreader) # get rid of the header
        return [row for row in spamreader]

def processCsvElement(elem):
    document = {}
    sentences = []
    if len(elem) == 2:
        document["title"] = elem[0].replace('\n', ' ')    
        cleanText, hashtags, attags = ct.cleanText(elem[1].replace('\n', ' '))
        document["text"] = cleanText.lower()
        sentences = [ct.removePunctuation(sentence.lower()) for sentence in sent_tokenize(cleanText)]
    return (document, sentences)


def readCsvFiles(uri):
    filelist = []

    for mypath in uri:
        if isdir(mypath):
            filelist += [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
        elif isfile(mypath):
            filelist.append(mypath)

    if filelist:
        no_threads = int(cpu_count()-1)
        documents = []
        index = []
        fullTexts = []

        with ProcessPoolExecutor(max_workers=no_threads) as worker:
            for result in worker.map(readCSVFile, filelist):
                if result:
                    documents.extend(result)

        with ProcessPoolExecutor(max_workers=no_threads) as worker:
            for result in worker.map(processCsvElement, documents):
                if result:
                    index.append(result[0])
                    fullTexts.extend(result[1])
        sentences = [re.findall('\w+', line) for line in fullTexts]
        words = [word for sentence in sentences for word in sentence]
        return sentences, words, index


def processTxtElement(file):
    with open(file) as inFile:
        document = {}
        sentences = []
        data = inFile.read().replace('\n', ' ')
        cleanText, hashtags, attags = ct.cleanText(data)
        document["title"] = "N/A"
        document["text"] = cleanText.lower()
        sentences = [ct.removePunctuation(sentence.lower()) for sentence in sent_tokenize(cleanText)]
        return (document, sentences)

def readTxtFiles(uri):
    filelist = []

    for mypath in uri:
        if isdir(mypath):
            filelist += [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
        elif isfile(mypath):
            filelist.append(mypath)

    if filelist:
        no_threads = int(cpu_count()-1)
        fullTexts = []
        index = []

        with ProcessPoolExecutor(max_workers=no_threads) as worker:
            for result in worker.map(processTxtElement, filelist):
                if result:
                    index.append(result[0])
                    fullTexts.extend(result[1])

        sentences = [re.findall('\w+', line) for line in fullTexts]
        words = [word for sentence in sentences for word in sentence]
        return sentences, words, index

if __name__ == "__main__":
    fileType = sys.argv[1] # txt, csv
    uri = sys.argv[2:]
    if fileType == "txt":
        readTxtFiles(uri)
    elif fileType == "csv":
        readCsvFiles(uri)



