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

from stop_words import get_stop_words
from nltk.corpus import stopwords

# ate parametters
grammar ={
         "P1":  "P1: {<NN.*>}",
         "P2":  "P2: {<NN.*> (<IN|RP|TO>)? <NN.*>}",
         "P3":  "P3: {<JJ.*> (<IN|RP|TO>)? <NN.*>}",
         "P4":  "P4: {<NN.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*>}",
         "P5":  "P5: {<JJ.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*>}",
         "P6":  "P6: {<NN.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*>}",
         "P7":  "P7: {<JJ.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*>}",
         "P8":  "P8: {<NN.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*>}",
         "P9":  "P9: {<JJ.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*>}",
        "P10": "P10: {<NN.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*>}",
        "P11": "P11: {<NN.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*>}",
        "P12": "P12: {<JJ.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*>}",
        "P13": "P13: {<JJ.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*>}",
        "P14": "P14: {<NN.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*>}",
        "P15": "P15: {<NN.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*>}",
        "P16": "P16: {<JJ.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*>}",
        "P17": "P17: {<NN.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*>}",
        "P18": "P18: {<NN.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*>}",
        "P19": "P19: {<NN.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*>}",
        "P20": "P20: {<JJ.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*>}",
        "P21": "P21: {<JJ.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*>}",
        "P22": "P22: {<JJ.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*>}",
        "P23": "P23: {<NN.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*>}",
        "P24": "P24: {<NN.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*>}",
        "P25": "P25: {<JJ.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <NN.*>}",
        "P26": "P26: {<JJ.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*>}",
        "P27": "P27: {<JJ.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <JJ.*> (<IN|RP|TO>)? <NN.*>}",

}

#dictionary for special characters utf-8 to ascii
specialchar_dic={
    "’": "'",
    "„": "\"",
    "“": "\"",
    "”": "\"",
    "«": "<<",
    "»": ">>",
    "…": "...",
    "—": "-",
    "¡": "!",
    "¿": "?",
    "©": " "
}

#dictionary of contractions
contractions_dict = { 
"ain't": "am not; are not; is not; has not; have not",
"aren't": "are not; am not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had / he would",
"he'd've": "he would have",
"he'll": "he shall / he will",
"he'll've": "he shall have / he will have",
"he's": "he has / he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how has / how is / how does",
"I'd": "I had / I would",
"I'd've": "I would have",
"I'll": "I shall / I will",
"I'll've": "I shall have / I will have",
"I'm": "I am",
"I've": "I have",
"isn't": "is not",
"it'd": "it had / it would",
"it'd've": "it would have",
"it'll": "it shall / it will",
"it'll've": "it shall have / it will have",
"it's": "it has / it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she had / she would",
"she'd've": "she would have",
"she'll": "she shall / she will",
"she'll've": "she shall have / she will have",
"she's": "she has / she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as / so is",
"that'd": "that would / that had",
"that'd've": "that would have",
"that's": "that has / that is",
"there'd": "there had / there would",
"there'd've": "there would have",
"there's": "there has / there is",
"they'd": "they had / they would",
"they'd've": "they would have",
"they'll": "they shall / they will",
"they'll've": "they shall have / they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we had / we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what shall / what will",
"what'll've": "what shall have / what will have",
"what're": "what are",
"what's": "what has / what is",
"what've": "what have",
"when's": "when has / when is",
"when've": "when have",
"where'd": "where did",
"where's": "where has / where is",
"where've": "where have",
"who'll": "who shall / who will",
"who'll've": "who shall have / who will have",
"who's": "who has / who is",
"who've": "who have",
"why's": "why has / why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you had / you would",
"you'd've": "you would have",
"you'll": "you shall / you will",
"you'll've": "you shall have / you will have",
"you're": "you are",
"you've": "you have"
}

def contractionsEN():
    contractions_en2 = { 
    "'s": " is",
    "'ve": " have",
    "'d": " had",
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he had",
    "he'd've": "he would have",
    "he'll": "he shall",
    "he'll've": "he shall have",
    "he's": "he has",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how has",
    "i'd": "i had",
    "i'd've": "i would have",
    "i'll": "i shall",
    "i'll've": "i shall have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it had",
    "it'd've": "it would have",
    "it'll": "it shall",
    "it'll've": "it shall have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she had",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that had",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when has",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where has",
    "where've": "where have",
    "who'll": "who shall",
    "who'll've": "who will have",
    "who's": "who has",
    "who've": "who have",
    "why's": "why has",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you had",
    "you'd've": "you would have",
    "you'll": "you shall",
    "you'll've": "you shall have",
    "you're": "you are",
    "you've": "you have"
    }

    contractions_en = {}
    # for key in contractions_en2.iterkeys():
    for key in contractions_en2:
        contractions_en[key.capitalize()] = contractions_en2[key]#.capitalize()
        contractions_en[key] = contractions_en2[key]
    return contractions_en

def contractionsFR():
    contractions_fr2 = {
        "l'": "la ",
        "c'": "ce ",
        "j'": "je ",
        "m'": "me ",
        "n'": "ne ",
        "s'": "se ",
        "t'": "te ",
        "d'": "de ",
        "qu'": "que ",
        "puisqu'": "puisque ",
        "lorsqu'": "lorsque",
        "-t-": " te ",
        "-y-": " y ",
        "-d'": " de ",
        "-de": " de"
    }

    contractions_fr = {}
    # for key in contractions_fr2.iterkeys():
    for key in contractions_fr2:
        contractions_fr[key.capitalize()] = contractions_fr2[key]#.capitalize()
        contractions_fr[key] = contractions_fr2[key]
    return contractions_fr

def stopWordsEN():
    sw_stop_words = get_stop_words('en')
    sw_nltk = stopwords.words('english')
    sw_mallet = ['a', 'able', 'about', 'above', 'according', 'accordingly', 'across', 'actually', 'after', 'afterwards', 'again', 'against', 'all', 'allow', 'allows', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'another', 'any', 'anybody', 'anyhow', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apart', 'appear', 'appreciate', 'appropriate', 'are', 'around', 'as', 'aside', 'ask', 'asking', 'associated', 'at', 'available', 'away', 'awfully', 'b', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'best', 'better', 'between', 'beyond', 'both', 'brief', 'but', 'by', 'c', 'came', 'can', 'cannot', 'cant', 'cause', 'causes', 'certain', 'certainly', 'changes', 'clearly', 'co', 'com', 'come', 'comes', 'concerning', 'consequently', 'consider', 'considering', 'contain', 'containing', 'contains', 'corresponding', 'could', 'course', 'currently', 'd', 'definitely', 'described', 'despite', 'did', 'different', 'do', 'does', 'doing', 'done', 'down', 'downwards', 'during', 'e', 'each', 'edu', 'eg', 'eight', 'either', 'else', 'elsewhere', 'enough', 'entirely', 'especially', 'et', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'exactly', 'example', 'except', 'f', 'far', 'few', 'fifth', 'first', 'five', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'forth', 'four', 'from', 'further', 'furthermore', 'g', 'get', 'gets', 'getting', 'given', 'gives', 'go', 'goes', 'going', 'gone', 'got', 'gotten', 'greetings', 'h', 'had', 'happens', 'hardly', 'has', 'have', 'having', 'he', 'hello', 'help', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'hi', 'him', 'himself', 'his', 'hither', 'hopefully', 'how', 'howbeit', 'however', 'i', 'ie', 'if', 'ignored', 'immediate', 'in', 'inasmuch', 'inc', 'indeed', 'indicate', 'indicated', 'indicates', 'inner', 'insofar', 'instead', 'into', 'inward', 'is', 'it', 'its', 'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kept', 'know', 'knows', 'known', 'l', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', 'like', 'liked', 'likely', 'little', 'look', 'looking', 'looks', 'ltd', 'm', 'mainly', 'many', 'may', 'maybe', 'me', 'mean', 'meanwhile', 'merely', 'might', 'more', 'moreover', 'most', 'mostly', 'much', 'must', 'my', 'myself', 'n', 'name', 'namely', 'nd', 'near', 'nearly', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'new', 'next', 'nine', 'no', 'nobody', 'non', 'none', 'noone', 'nor', 'normally', 'not', 'nothing', 'novel', 'now', 'nowhere', 'o', 'obviously', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'own', 'p', 'particular', 'particularly', 'per', 'perhaps', 'placed', 'please', 'plus', 'possible', 'presumably', 'probably', 'provides', 'q', 'que', 'quite', 'qv', 'r', 'rather', 'rd', 're', 'really', 'reasonably', 'regarding', 'regardless', 'regards', 'relatively', 'respectively', 'right', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'second', 'secondly', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sensible', 'sent', 'serious', 'seriously', 'seven', 'several', 'shall', 'she', 'should', 'since', 'six', 'so', 'some', 'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specified', 'specify', 'specifying', 'still', 'sub', 'such', 'sup', 'sure', 't', 'take', 'taken', 'tell', 'tends', 'th', 'than', 'thank', 'thanks', 'thanx', 'that', 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 'theres', 'thereupon', 'these', 'they', 'think', 'third', 'this', 'thorough', 'thoroughly', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'twice', 'two', 'u', 'un', 'under', 'unfortunately', 'unless', 'unlikely', 'until', 'unto', 'up', 'upon', 'us', 'use', 'used', 'useful', 'uses', 'using', 'usually', 'uucp', 'v', 'value', 'various', 'very', 'via', 'viz', 'vs', 'w', 'want', 'wants', 'was', 'way', 'we', 'welcome', 'well', 'went', 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'willing', 'wish', 'with', 'within', 'without', 'wonder', 'would', 'would', 'x', 'y', 'yes', 'yet', 'you', 'your', 'yours', 'yourself', 'yourselves', 'z', 'zero']
    return list(set(sw_stop_words + sw_nltk + sw_mallet))