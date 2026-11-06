from .utils import *
from ..registry import register_step


@register_step("remove_stopwords")
@requires_str
def remove_stopwords(text:str)-> str:
    """
    Remove stopwords from the input text.

    Args:
        text (str): The input text from which stopwords will be removed.

    Returns:
        str: The input text without stopwords.

    Raises:
        TypeError: If text is not a string.

    Examples:
        >>> remove_stopwords("This is a simple example")
        'simple example'
    """
    stopwords=load_stopwords()
    NEGATIONS = {"not", "no", "nor"}
    ans=[]
    for word in text.split():
        x=word.casefold()
        if x in stopwords and word not in NEGATIONS:
            continue
        else:
            ans.append(word)
    return " ".join(ans)


@register_step("expand_contractions")
@requires_str
def expand_contractions(text:str)->str:
    """
    Expand contractions in the input text using a predefined
    contractions dictionary.
    Each recognized contraction is replaced with its expanded form.

    Args:
        text (str): The input text containing contractions.

    Returns:
        str: The input text with recognized contractions expanded.

    Raises:
        TypeError: If text is not a string.

    Examples:
        >>> expand_contractions("I don't know")
        'I do not know'
    """
    contractions_dict=load_contractions()
    ans=[]
    for word in text.split():
        if word.lower() in contractions_dict:
            ans.append(contractions_dict[word.lower()])
        else:
            ans.append(word)
    return " ".join(ans)

