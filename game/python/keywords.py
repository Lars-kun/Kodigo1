import pke # type: ignore
import string
import nltk # type: ignore
nltk.download('stopwords')
from nltk.corpus import stopwords # type: ignore

import sys
import json
import os

def keywords(text, n):
    out = []

    extractor = pke.unsupervised.MultipartiteRank()
    extractor.load_document(input=text, language='en')
    pos = {'PROPN', 'NOUN', 'VERB'}
    stoplist = list(string.punctuation)
    stoplist += stopwords.words('english')
    extractor.candidate_selection(pos=pos)
    # 4. build the Multipartite graph and rank candidates using random walk,
    #    alpha controls the weight adjustment mechanism, see TopicRank for
    #    threshold/method parameters.
    try:
        extractor.candidate_weighting(alpha=1.1,
                                      threshold=0.75,
                                      method='average')
    except:
        return out

    keyphrases = extractor.get_n_best(n)

    for key in keyphrases:
        out.append(key[0])

    return out

fn = sys.argv[1]
extract_type = sys.argv[2]

base_path = os.getcwd()
relative_path = f"kodigo\\game\\python\\temp\\{fn}.json"
fp = os.path.join(base_path, relative_path)#f"D:\\renpy-8.1.3-sdk\\kodigo\\game\\python\\docs\\{fn}.json"# #
    
#read the json file
with open(fp, 'r') as file:
    quiz = json.load(file)

if extract_type == "bulk":
    if quiz["ranked_sentences"]:
        text = quiz["ranked_sentences"]
    else:
        text = quiz["notes"]
    
    n = len(quiz["sentences"]) + 40
    keywords = keywords(text, n)

    quiz["keywords"] = keywords 
elif extract_type == "last":
    sent = quiz["sentences"][-1]
    answer = keywords(sent, 1)[0]
    quiz["answers"][-1] = answer

#save the updated data back to json
with open(fp, 'w') as file:
    json.dump(quiz, file)



