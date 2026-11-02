import json
from pathlib import Path
from collections import Counter

def is_emoji(char: str) -> bool:
    
    code = ord(char)

    return (
        0x1F300 <= code <= 0x1FAFF
        or 0x2600 <= code <= 0x27BF
    )


def load_stopwords() -> set[str]:
    resource = Path(__file__).resolve().parents[2] / "Resources" / "english_stopwords.txt"

    with resource.open(encoding="utf-8") as file:
        return {
            word.strip().lower()
            for word in file
            if word.strip()
        }




def load_contractions() -> dict[str, str]:

    resource = (
        Path(__file__).resolve().parents[2] / "Resources" / "contraction_mapping.json")

    with resource.open("r", encoding="utf-8") as file:
        contractions = json.load(file)

    return {
        contraction.lower(): expansion
        for contraction, expansion in contractions.items()
    }

def load_slang()-> dict[str,str]:
    resource = Path(__file__).resolve().parents[2] / "Resources" / "SlangText2.csv"
    
    slang_dataset=dict()
   
    with resource.open(encoding="utf-8") as f:
        for word in f:
            slang_dataset[word.split(",")[0].replace("\n","")]=" ".join(word.split(",")[1:]).replace("\n","")
                
    return slang_dataset



def word_freq_loader() -> dict[str, int]:
    resource = Path(__file__).resolve().parents[2] / "Resources" / "unigram_freq.csv"
    
    word_freq_dataset = dict()
   
    with resource.open(encoding="utf-8") as f:
        next(f) 
        for word in f:
            parts = word.strip().split(",")
            if len(parts) == 2:
                word_freq_dataset[parts[0]] = int(parts[1])
                
    return word_freq_dataset


