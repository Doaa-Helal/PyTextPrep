from .utils import *
from ..registry import register_step


@register_step("remove_stopwords")
@requires_str
def remove_stopwords(text:str,language="en")-> str:
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
    stopwords=load_stopwords(language)
    EN_NEGATIONS = {"not", "no", "nor"}
    AR_NEGATION = ["لا", "لم", "لن", "لما", "لات","ليس", "ليست", "ليسا", "ليستا", "ليسوا","لسن", "لست", "لستم", "لستما", "لستن", "لسنا","ما", "غير", "عدم", "بلا", "بدون", "دون","كلا", "كلّا","أبدا", "ابدا", "أبداً", "ابداً","قط","مطلقا", "مطلقاً","إطلاقا", "اطلاقا", "إطلاقاً","البتة"]
    AR_NEGATION_SET = frozenset(AR_NEGATION)
    EN_NEGATION_SET=frozenset(EN_NEGATIONS)
    
    if language=="ar":
        NEGATIONS=AR_NEGATION_SET
    else:
        NEGATIONS=EN_NEGATION_SET
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

