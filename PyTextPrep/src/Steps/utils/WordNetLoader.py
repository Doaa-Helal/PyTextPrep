from pathlib import Path


def singularize(word: str) -> str:

    if word.endswith("ies"):
        return word[:-3] + "y"
    
    if word.endswith("sses"):
        return word[:-2]

    if word.endswith(("ches", "shes", "xes", "zes")):
        return word[:-2]

    if word.endswith(("ss", "us", "is")):
        return word

    if word.endswith("s"):
        return word[:-1]

    return word

def load_wordnet() -> set[str]:
    resource = Path(__file__).resolve().parents[2] / "Resources" / "wordnet"

    files = list(resource.glob("*.exc"))
    lemma_dataset=dict()
    for file in files:
        with file.open(encoding="utf-8") as f:
            for word in f:
                lemma_dataset[word.split()[0]]=word.split()[1]
                
    return lemma_dataset
