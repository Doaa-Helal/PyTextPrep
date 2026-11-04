from .utils import *
from ..registry import register_step
from .Spelling import CorrectSpelling
import unicodedata
import re

@requires_str
@register_step("lemmatize")
def lemmatize(text):  
    wordnet=load_wordnet()
    words=text.strip().split()
    ans=[]
    for word in words:
        if word in wordnet:
            ans.append(wordnet[word])
            print(wordnet[word])
        else:
            word=singularize(word)
            ans.append(word)
    return " ".join(ans)

@requires_str
@register_step("normalize_arabic")
def normalize_arabic(text: str, taa_marbuta: bool = False) -> str:
    text = re.sub(r'[\u064B-\u0652\u0670\u0640]', '', text)
    text = re.sub(r'[\u0622\u0623\u0625\u0671]', '\u0627', text)
    text = text.replace('\u0649', '\u064A')
    if taa_marbuta:
        text = text.replace('\u0629', '\u0647')
        
    return text

@requires_str
@register_step("remove_accents")
def remove_accents(text):
    normalized = unicodedata.normalize("NFKD", text)
    clean_text = normalized.encode("ascii", "ignore").decode("ascii")
    return clean_text

@requires_str
@register_step("ngrams")
def ngrams(tokens, n):
    step = n - 1
    ans=[]
    for i in range(0,len(tokens),step):
        gram=tokens[i:i+n]
        if len(gram)==n:
            ans.append(tuple(gram))
    return ans

@requires_str
@register_step("char_ngrams")
def char_ngrams(word, n):
    ans=[]
    for i in range(0,len(word)-n+1):
        gram=word[i:i+n]
        print(gram)
        if len(gram)==n:
            ans.append(gram)
    return ans

@requires_str
@register_step("normalize_slang")
def normalize_slang(text, table=None):
    slang_dict=None
    if table:
        slang_dict=table
    else:
        slang_dict=load_slang()
    ans=[]
    for word in text.split():
        if word in slang_dict:
            ans.append(slang_dict[word])
        else:
            ans.append(word)
    return " ".join(ans)

@requires_str
@register_step("correct_spelling")  
def correct_spelling(text):
    freq=word_freq_loader()
    correct=CorrectSpelling()
    ans=correct(text,freq)
    return ans

