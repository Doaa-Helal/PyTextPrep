import re

def word_tokenize(text):
    return text.split()

def sent_tokenize(text: str) -> list[str]:
 
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

