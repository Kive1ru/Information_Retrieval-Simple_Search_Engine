# 15786064(Zijian Chen), 13713641(Qingshuang Su), 70518431(Lingxin Li), 90277259(Jiahao(Kylin) Guo)
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import json
from collections import defaultdict
import os
import math
from simhash import Simhash


indexer_dict = defaultdict(dict)
numPage = 0
docID = 0
docUrl = dict()
unique_url = set()
unique_word = 0
splitCount = 0
comparehash = set()

def tokenize(content):
    stemmer = SnowballStemmer("english")
    return [stemmer.stem(word) for word in word_tokenize(content) if word.isalnum()]


def indexer(content, types, docID):
    global Posting
    global indexer_dict
    if types == 1:  # bold and strong
        for token in content:
            if not token in indexer_dict:
                indexer_dict[token][docID] = 1.5
            elif not docID in indexer_dict[token]:
                indexer_dict[token][docID] = 1.5
            else:
                indexer_dict[token][docID] += 1.5       
    elif types == 2: # heading
        for token in content:
            if not token in indexer_dict:
                indexer_dict[token][docID] = 2
            elif not docID in indexer_dict[token]:
                indexer_dict[token][docID] = 2
            else:
                indexer_dict[token][docID] += 2
    elif types == 3: # title
        for token in content:
            if not token in indexer_dict:
                indexer_dict[token][docID] = 2.5
            elif not docID in indexer_dict[token]:
                indexer_dict[token][docID] = 2.5
            else:
                indexer_dict[token][docID] += 2.5
    else: # frequency
        for token in content:
            if not token in indexer_dict:
                indexer_dict[token][docID] = 1
            elif not docID in indexer_dict[token]:
                indexer_dict[token][docID] = 1
            else:
                indexer_dict[token][docID] += 1


def simhash_diff(hash_1, hash_2):  #simhash comparison function from #https://algonotes.readthedocs.io/en/latest/Simhash.html
    """calcuate the difference from two simhash values.
    """
    x = (hash_1 ^ hash_2) & ((1 << 64) - 1)
    ans = 0
    while x:
        ans += 1
        x &= x - 1
    return ans


def readjson(file_path):
    global docID
    global numPage
    global splitCount
    f = open(file_path)
    js = json.load(f)
    soup = BeautifulSoup(js['content'], 'html.parser')
    if len(soup.get_text()) <= 75000:
        pagehash = Simhash(soup.get_text())
        button = False
        if not comparehash: #add the first hashvalue to comparehash
            comparehash.add(pagehash.value)
        else:
            for i in comparehash:
                if simhash_diff(pagehash.value,i) <= 3:
                    button = True
        if not button:
            comparehash.add(pagehash.value)
            docID += 1
            splitCount += 1
            docUrl[docID] = js['url']
            for b in soup.find_all(['b', 'strong']):
                indexer(tokenize(b.get_text()), 1, docID)
            for h in soup.find_all(['h1', 'h2', 'h3']):
                indexer(tokenize(h.get_text()), 2, docID)
            for t in soup.find_all('title'):
                indexer(tokenize(t.get_text()), 3, docID)
            indexer(tokenize(soup.get_text()), 0, docID)
    numPage += 1


          
def get_files(root):
    files = os.listdir(root)
    paths = []
    for f in files:
        absolute_path = os.path.join(root,f)
        if os.path.isdir(absolute_path):
            paths.extend(get_files(absolute_path))
        else:
            if absolute_path.endswith('.json'):
                if not absolute_path.endswith('docID.json'):
                    paths.append(absolute_path)
    return paths


def storeIndexer(root):
    global indexer_dict
    global docUrl
    global unique_word
    directory = "TEST"
    path = os.path.join(root, directory)
    if not os.path.exists(path):
        os.mkdir(path)
    docID_path = os.path.join(path, "docID.json")
    with open(docID_path, "w") as dd:
        json.dump(docUrl, dd, indent = 5)
    for key, value in indexer_dict.items():
        subdir = key[0]
        tPath = os.path.join(path, subdir)
        if not os.path.exists(tPath):
            os.mkdir(tPath)
        if key == "aux":
            tfilename = os.path.join(tPath, "aux_.json")
        else:
            tfilename = os.path.join(tPath, key + ".json")
        if not os.path.isfile(tfilename):
            with open(tfilename, "w", encoding = 'utf-8') as idx1:
                json.dump(value, idx1, indent=4)
        else:
            with open(tfilename, "r", encoding = 'utf-8') as idx2:
                indexers = json.load(idx2)
            os.remove(tfilename)
            with open(tfilename, "w", encoding = 'utf-8') as idx3:
                indexers.update(value)
                json.dump(indexers, idx3, indent=4)
    unique_word += len(indexer_dict.keys())
    indexer_dict = defaultdict(dict)


def grade(path):
    global docUrl
    with open(path, "r", encoding = 'utf-8') as idx4:
        termDict = json.load(idx4)
    for doc in termDict:
        termDict[doc] = (1 + math.log(termDict[doc])) * math.log(len(docUrl.keys()) / len(termDict))
    os.remove(path)
    with open(path, "w", encoding = 'utf-8') as idx5:
        json.dump(termDict, idx5, indent=4)


def report(storeRoot):
    global numPage
    global docID
    global unique_word
    reportTxt = os.path.join(storeRoot, 'report.txt')
    with open(reportTxt,"a") as rp:
        rp.write (f"The number of pages in the dataset: {numPage}")
        rp.write("\n")
        rp.write (f"The number of indexed documents: {docID}")
        rp.write("\n")
        rp.write (f"unique words: {unique_word}")
        rp.write("\n")

     
def run(root, storeRoot):
    global splitCount
    file_paths = get_files(root)
    splitCount = 0
    for p in file_paths:
        print(p)
        readjson(p)
        if splitCount == 14000:
            storeIndexer(storeRoot)
            splitCount = 0
    storeIndexer(storeRoot)
    print('finish Dividing')
    index_path = os.path.join(storeRoot, 'TEST')
    result_paths = get_files(index_path)
    print('start tf-idf')
    for p in result_paths:
        print(p)
        grade(p)
    report(storeRoot)
    print('finish')


if __name__ == '__main__':
    root = 'B:\CS 121\Assignment3M3\DEV'
    storeRoot = 'B:\CS 121\Assignment3M3'
    run(root, storeRoot)

