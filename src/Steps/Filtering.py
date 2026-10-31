from utils import *

def remove_stopwords(text, custom_words=None, extra_only=False):
    stopwords=load_stopwords()
    ans=[]
    for word in text.split():
        if word.lower() in stopwords:
            continue
        else:
            ans.append(word)
    return " ".join(ans)


def expand_contractions(text):
    contractions_dict=load_contractions()
    ans=[]
    for word in text.split():
        if word.lower() in contractions_dict:
            ans.append(contractions_dict[word.lower()])
        else:
            ans.append(word)
    return " ".join(ans)

