import json
from pathlib import Path

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

