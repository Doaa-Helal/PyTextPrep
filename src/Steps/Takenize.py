from ..registry import register_step
from utils import *
import re

@register_step("word_tokenize")
def word_tokenize(text):
    validate_string(text)
    return text.split()

@register_step("sent_tokenize")
def sent_tokenize(text: str) -> list[str]:
    validate_string(text)
    if not text:
        return []

    abbreviations = ["Dr.","Mr.","Mrs.","e.g.","i.e.","etc."]
    placeholder = "\u0000"
    for abbreviation in abbreviations:
        protected = abbreviation.replace(".", placeholder)
        text = re.sub(re.escape(abbreviation),protected,text,flags=re.IGNORECASE)
        
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])',text)
    sentences = [sentence.replace(placeholder, ".").strip()for sentence in sentences]

    return [sentence for sentence in sentences if sentence]

