from ..registry import register_step
from .utils import *
import re


@register_step("word_tokenize")
@requires_str
def word_tokenize(text):
    """
    Split text into individual words using whitespace as the delimiter.

    Args:
        text (str): The input text to tokenize.

    Returns:
        list[str]: A list containing the words in the input text.
                   Returns an empty list if the input is empty.

    Raises:
        TypeError: If the input is not a string.
    
    """
    return text.split()


@register_step("sent_tokenize")
@requires_str
def sent_tokenize(text: str) -> list[str]:
    """
    Split text into sentences based on sentence-ending punctuation.

    Args:
        text (str): The input text to split into sentences.

    Returns:
        list[str]: A list of sentences. Returns an empty list if the
                   input is empty.

    Raises:
        TypeError: If the input is not a string.  
    """
    if not text:
        return []

    abbreviations = ["Dr.","Mr.","Mrs.","e.g.","i.e."]
    placeholder = "\u0000"
    for abbreviation in abbreviations:
        protected = abbreviation.replace(".", placeholder)
        text = re.sub(re.escape(abbreviation),protected,text,flags=re.IGNORECASE)
        
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])',text)
    sentences = [sentence.replace(placeholder, ".").strip()for sentence in sentences]

    return [sentence for sentence in sentences if sentence]

