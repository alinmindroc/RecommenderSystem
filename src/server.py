import ujson
import flask
import requests
from flask_cors import CORS
import elasticsearchddl
import prefixtree

commonWords = ["to","of","in","for","on","with","at","by","from","up","the","and","a","that","I","it","not","he","as","you","this","but","his","they","her","she","or","an","will","my","one","all","would","there","their"]

with open("../chidict.json") as f:
    chiDict = ujson.load(f)

with open("../cstree.json") as f:
    chiTrie = prefixtree.PrefixTree()
    chiTrie.loadFromJson(ujson.load(f))

with open("../mvdict.json") as f:
    mvDict = ujson.load(f)

with open("../mvtree.json") as f:
    mvTrie = prefixtree.PrefixTree()
    mvTrie.loadFromJson(ujson.load(f))

def getBigramCandidates(word):
    if word in chiDict:
        #keep only words which appear at least once at the right of the requested word
        rightWords = filter(lambda x: x[1]["o12"] > 0, list(chiDict[word].items()))
        #keep only uncommon words as bigram candidates
        rightWords = filter(lambda x: x[0] not in commonWords, rightWords)
        return map(
            lambda x: x[0],
	    sorted(rightWords, key = lambda x: (x[1]["o11"] > 1, -x[1]["o21"])))
    else:
        return []

def getCollocationCandidates(word):
    if word in mvDict:
        #keep only words which appear at least once at the right of the requested word
        rightWords = filter(lambda x: x[1]["o12"] > 0, list(chiDict[word].items()))

        #keep only uncommon words as bigram candidates
        rightWords = filter(lambda x: x[0] not in commonWords, rightWords)
        return map(
            lambda x: x[0],
	    sorted(rightWords, key = lambda x: (x[1]["o11"] > 1, -x[1]["o21"])))
    else:
        return []

app = flask.Flask(__name__, static_url_path='/home/mindroc/work/ngrams')
CORS(app)

@app.route('/<path:path>')
def send_js(path):
    return flask.send_from_directory('static', path)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route("/api/chi")
def chi():
    word = flask.request.args.get('word')
    w1 = word.split()[0]

    if len(word.split()) > 1:
    	w2 = word.split()[1]
    	recomm = filter(
       		lambda x: x.startswith(w2),
                getBigramCandidates(w1))
    else:
        recomm = getBigramCandidates(w1)

    return flask.jsonify(results = list(map(lambda x: w1 + ' ' + x, recomm))[:10])

@app.route("/api/prefixChi")
def prefix_chi():
    word = flask.request.args.get('word')

    prefixCandidates = list(filter(
        lambda x: len(x) > 2,
        map(lambda x: x[0], chiTrie.getRecommendations(word))))[:10]

    return flask.jsonify(results = prefixCandidates)

@app.route("/api/prefixMv")
def prefix_mv():
    word = flask.request.args.get('word')

    prefixCandidates = list(filter(
        lambda x: len(x) > 2,
        map(lambda x: x[0], mvTrie.getRecommendations(word))))[:10]

    return flask.jsonify(results = prefixCandidates)

@app.route("/api/mv")
def mv():
    word = flask.request.args.get('word')
    w1 = word.split()[0]

    if len(word.split()) > 1:
    	w2 = word.split()[1]
    	recomm = filter(
       		lambda x: x.startswith(w2),
                getCollocationCandidates(w1))
    else:
        recomm = getCollocationCandidates(w1)

    return flask.jsonify(results = list(map(lambda x: w1 + ' ' + x, recomm))[:10])

@app.route("/api/searchBigrams")
def searchBigrams():
    query = flask.request.args.get('query')
    articleList = elasticsearchddl.ElasticsearchDDL().searchByBigram("test-index", query)['hits']['hits']

    def getHighlight(doc):
        res = {'text': doc['_source']['text']}
        if 'highlight' in doc:
            res['highlight'] = doc['highlight']
            res['highlight']['text'] = [' '.join(sentence for sentence in res['highlight']['text'])]

        return res

    articleList = list(map(getHighlight, articleList))

    return flask.jsonify(results = articleList)

@app.route("/api/searchCollocs")
def searchCollocs():
    [term1, term2] = flask.request.args.get('query').split()
    articleList = elasticsearchddl.ElasticsearchDDL().searchByCollocation("test-index", term1, term2)['hits']['hits']

    def getHighlight(doc):
        res = {'text': doc['_source']['text']}
        if 'highlight' in doc:
            res['highlight'] = doc['highlight']
            res['highlight']['text'] = [' '.join(sentence for sentence in res['highlight']['text'])]

        return res

    articleList = list(map(getHighlight, articleList))[:5]

    return flask.jsonify(results = articleList)

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True,host='0.0.0.0')

