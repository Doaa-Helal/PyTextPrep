from .utils import *
from ..registry import register_step
from .Spelling import CorrectSpelling
import unicodedata
import re


@register_step("lemmatize")
@requires_str
def lemmatize(text:str)->str:  
    """
    Convert words in the input text to their base forms (lemmas).

    The function first checks the WordNet dictionary for known lemmas.
    If a word is not found, it applies a singularization rule.

    Args:
        text (str): The input text to lemmatize.

    Returns:
        str: The input text with words converted to their base forms.

    Raises:
        TypeError: If text is not a string.

    Examples:
        >>> lemmatize("children")
        'child'
        >>> lemmatize("cars")
        'car'
    """
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

@register_step("normalize_arabic")
@requires_str
def normalize_arabic(text: str, taa_marbuta: bool = False) -> str:
    """
    Normalize Arabic text by removing diacritics and tatweel,
    and standardizing different forms of Arabic letters.

    The function normalizes Alef variants to Alef, converts Alef
    Maksura to Yeh, and optionally converts Taa Marbuta to Heh.

    Args:
        text (str): The Arabic text to normalize.
        taa_marbuta (bool): If True, convert Taa Marbuta (ة) to Heh (ه).
            Defaults to False.

    Returns:
        str: The normalized Arabic text.

    Raises:
        TypeError: If text is not a string.

    Examples:
        >>> normalize_arabic("أَحْمَد")
        'احمد'
        >>> normalize_arabic("مدرسة", taa_marbuta=True)
        'مدرسه'
    """
    text = re.sub(r'[\u064B-\u0652\u0670\u0640]', '', text)
    text = re.sub(r'[\u0622\u0623\u0625\u0671]', '\u0627', text)
    text = text.replace('\u0649', '\u064A')
    if taa_marbuta:
        text = text.replace('\u0629', '\u0647')
        
    return text


@register_step("remove_accents")
@requires_str
def remove_accents(text:str)->str:
    """
    Remove accent marks from the input text.

    The function applies Unicode NFKD normalization and removes
    characters that cannot be encoded in ASCII.

    Args:
        text (str): The input text containing accented characters.

    Returns:
        str: The text with accents removed.

    Raises:
        TypeError: If text is not a string.

    Examples:
        >>> remove_accents("café")
        'cafe'
        >>> remove_accents("naïve")
        'naive'
    """
    normalized = unicodedata.normalize("NFKD", text)
    clean_text = normalized.encode("ascii", "ignore").decode("ascii")
    return clean_text


@register_step("ngrams")
@requires_str
def ngrams(tokens:list, n:int)-> list[tuple]:
    """
    Generate n-grams from a sequence of tokens.

    An n-gram is a consecutive sequence of n tokens.
    Each generated n-gram is returned as a tuple.

    Args:
        tokens (list): The input sequence of tokens.
        n (int): The number of tokens in each n-gram.

    Returns:
        list[tuple]: A list containing the generated n-grams.

    Raises:
        TypeError: If tokens is not a string.

    Examples:
        >>> ngrams("I love natural language processing", 2)
        [('I', 'love'), ('natural', 'language'), ('processing',)]
    """
    step = n - 1
    ans=[]
    for i in range(0,len(tokens),step):
        gram=tokens[i:i+n]
        if len(gram)==n:
            ans.append(tuple(gram))
    return ans


@register_step("char_ngrams")
@requires_str
def char_ngrams(word:str, n:int)->list[str]:
    """
    Generate character n-grams from the input word.

    A character n-gram is a consecutive sequence of n characters.

    Args:
        word (str): The input word or text.
        n (int): The number of characters in each n-gram.

    Returns:
        list[str]: A list containing the generated character n-grams.

    Raises:
        TypeError: If word is not a string.

    Examples:
        >>> char_ngrams("hello", 2)
        ['he', 'el', 'll', 'lo']
        >>> char_ngrams("hello", 3)
        ['hel', 'ell', 'llo']
    """
    ans=[]
    for i in range(0,len(word)-n+1):
        gram=word[i:i+n]
        print(gram)
        if len(gram)==n:
            ans.append(gram)
    return ans


@register_step("normalize_slang")
@requires_str
def normalize_slang(text:str, table:dict=None)-> str:
    """
    Normalize slang words in the input text using a predefined
    or user-provided slang dictionary.

    Each recognized slang word is replaced with its standard form.

    Args:
        text (str): The input text containing slang words.
        table (dict, optional): A dictionary mapping slang words
            to their standard forms. If None, the default slang
            dictionary is loaded. Defaults to None.

    Returns:
        str: The input text with recognized slang words normalized.

    Raises:
        TypeError: If text is not a string.

    Examples:
        >>> normalize_slang("u r gr8", {"u": "you", "r": "are", "gr8": "great"})
        'you are great'
    """
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


@register_step("correct_spelling")  
@requires_str
def correct_spelling(text:str)->str:
    """
    Correct spelling mistakes in the input text using a
    word-frequency dictionary and an edit-distance-based algorithm.

    The function identifies misspelled words and replaces them
    with the most probable candidates from the frequency dictionary.

    Args:
        text (str): The input text containing potentially misspelled words.

    Returns:
        str: The input text with spelling mistakes corrected.

    Raises:
        TypeError: If text is not a string.

    Examples:
        >>> correct_spelling("I love progrmming")
        'I love programming'
    """
    freq=word_freq_loader()
    correct=CorrectSpelling()
    ans=correct(text,freq)
    return ans

