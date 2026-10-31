import re
import string
import unicodedata
from utils import *

def lower_case(txt:str):
    return txt.lower()

def normalize_whitespace(txt:str):
    cleaned = re.sub(r'\s+', ' ', txt)
    return cleaned

def remove_urls(txt:str,replace_with:str):
    urls_pattern=r"https?://[^\s.,!?;:)\]]+|www\.[^\s.,!?;:)\]]+"
    cleaned=re.sub(urls_pattern,replace_with,txt)
    return cleaned

def remove_emails(txt,replace_with):
    email_pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    cleaned=re.sub(email_pattern,replace_with,txt)
    return cleaned

def remove_punctuation(txt:str, keep_emojis=True):
    txt=txt.replace("'","")
    
    if not keep_emojis:
        txt = re.sub(r'[^\w\s]', ' ', txt)
    else:
        punctuation_len = len(string.punctuation)
        translation_table = str.maketrans(string.punctuation, ' ' * punctuation_len)
        txt = txt.translate(translation_table)


def normalize_repeating_chars(txt, keep=2):
    pattern = r'(.)\1{2,}'
    repl = r'\1' * keep
    return re.sub(pattern, repl, txt)

def remove_html(txt):
    txt=strip_tags(txt)
    return txt

def remove_mentions(txt):
    pattern=r"(?<![\w@])@[A-Za-z0-9_]+"
    return re.sub(pattern,"",txt)

def remove_hashtags(text, keep_word=False):
    if keep_word:
        pattern=r"#(?=[A-Za-z0-9_]+)"
    else:    
        pattern=r"(?<!\w)#[A-Za-z0-9_]+"
    return re.sub(pattern,"",text)

def remove_digits(txt):
    pattern=r"[+-]?\d+(?:\.\d+)?"
    return re.sub(pattern,"",txt)




def handle_emojis(text: str, mode: str = "remove") -> str:
   
    if mode not in ("remove", "text"):
        raise ValueError("mode must be either 'remove' or 'text'")

    if not text:
        return ""

    result = []

    for char in text:

        # Handle invisible Unicode characters
        if char in ("\ufe0f", "\u200d"):
            continue

        if is_emoji(char):

            if mode == "remove":
                result.append(" ")

            elif mode == "text":
                try:
                    name = unicodedata.name(char).lower()
                    name = name.replace(" ", "_")
                    result.append(f":{name}:")
                except ValueError:
                    result.append(" ")

        else:
            result.append(char)

    return re.sub(r"\s+", " ", "".join(result)).strip()



    
