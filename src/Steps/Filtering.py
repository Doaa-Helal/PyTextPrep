from .utils import *
from ..registry import register_step

@register_step("remove_stopwords")
def remove_stopwords(text):
    stopwords=load_stopwords()
    ans=[]
    for word in text.split():
        if word.lower() in stopwords:
            continue
        else:
            ans.append(word)
    return " ".join(ans)

@register_step("expand_contractions")
def expand_contractions(text):
    contractions_dict=load_contractions()
    ans=[]
    for word in text.split():
        if word.lower() in contractions_dict:
            ans.append(contractions_dict[word.lower()])
        else:
            ans.append(word)
    return " ".join(ans)

