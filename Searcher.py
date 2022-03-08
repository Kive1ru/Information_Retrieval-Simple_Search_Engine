#15786064(Zijian Chen), 13713641(Qingshuang Su), 70518431(Lingxin Li), 90277259(Jiahao(Kylin) Guo)
import os
import json
import time
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer


docid = dict()


def read_docID(root):  # load the docID dict 
    global docid
    json_file = os.path.join(root, 'docID.json')
    with open(json_file, 'r', encoding='utf-8') as d:
        docid = json.load(d)


def Load_json(query_token):  # get the dict item of sepecific token term
    global root
    if query_token == "aux":
        dir_file = os.path.join(root, query_token[0])
        json_file = os.path.join(dir_file, query_token + '_.json')
    else:
        dir_file = os.path.join(root, query_token[0])
        json_file = os.path.join(dir_file, query_token + '.json')
    try:
        with open(json_file, 'r', encoding='utf-8') as idx:
            indexes = json.loads(idx.read())
        return indexes
    except:
        return {}


def tokenize(content): # tokenize query
    stemmer = SnowballStemmer("english")
    return [stemmer.stem(word) for word in word_tokenize(content) if word.isalnum()]


def Query_search(query):  # get a list of query terms associated with their postings
    relst = []
    query_lst = tokenize(query)
    for qtoken in query_lst:
        query_dic = Load_json(qtoken)
        relst.append(query_dic)
    relst = sorted(relst, key = lambda x: len(x))
    return relst


def Merge_query(query_lst): # find intersection among query terms' postings
    common_posting = defaultdict(int)
    sortID = []
    if query_lst:
        comEle = query_lst[0].copy()
        for query in query_lst:
            comEle = {x:0 for x in comEle if x in query}
        for ele in comEle:
            for query in query_lst:
                common_posting[ele] += query[ele]
        sortID = sorted(common_posting.keys(), key = lambda x: -common_posting[x])
    return sortID


def RankTop(sortPost): # print the top 5 urls
    global docid
    check = 0
    relst = []
    while check < len(sortPost):
        if check == 5:
            break
        print(docid[sortPost[check]])
        relst.append(docid[sortPost[check]])
        check += 1
    return relst


def run(root): # text user interface of the search engine
    count = 0
    while True:
        query = input("Query (ENTER Key to exit):\n")
        start = time.process_time()
        if query == "":
            print("EXIT THE SEARCH ENGINE")
            break
        if count == 0:
            read_docID(root)
            count += 1
        resultUrl = Merge_query((Query_search(query)))
        end = time.process_time()
        if not resultUrl:
            print("")
            print("No result found")
        else:
            print(f"\nSearch time: {end - start} seconds. Total {len(resultUrl)} Urls are found.")
            if len(resultUrl) >= 5:
                print("Top 5 results:")
            else:
                print(f"Top {len(resultUrl)} results (results found are less than 5):")
            RankTop(resultUrl)
            print("")


def UInterface(query):
    start = time.process_time()
    resultUrl = Merge_query((Query_search(query)))
    infolst = []
    if not resultUrl:
        infolst.append("No result found")
    else:
        end = time.process_time()
        infolst.append(f"\nSearch time: {end - start} seconds. Total {len(resultUrl)} Urls are found.")
        if len(resultUrl) >= 5:
            infolst.append("Top 5 results:")
        else:
            infolst.append(f"Top {len(resultUrl)} results (results found are less than 5):")
        infolst.extend(RankTop(resultUrl))
    return infolst, format(end-start,'.3f')


if __name__ == '__main__':
    root = 'B:\CS 121\Assignment3M3\TEST'
    run(root)

