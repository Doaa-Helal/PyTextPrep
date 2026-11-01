import string

class CorrectSpelling:
    def __init__(self):
        pass
    def __call__(self, word,freq):
        ans=[]
        if len(word.split())==1:
            return self.correct_word(word,freq)
        else:
            for w in word.split():
                ans.append(self.correct_word(w,freq))

        return " ".join(ans)

    def _edit1(self,word:str):
        if not isinstance(word, str):
            raise TypeError(f"expected str, got {type(word).__name__}")
        
        word = word.casefold()
        if not word:
            return set()
        
        letters = string.ascii_lowercase
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1) ]

        deletes = [left + right[1:] for left, right in splits if right]
        transposes = [ left + right[1] + right[0] + right[2:] for left, right in splits if len(right) > 1]
        replaces = [ left + char + right[1:] for left, right in splits if right for char in letters   ]
        inserts = [left + char + right for left, right in splits for char in letters]

        return set(deletes + transposes + replaces + inserts)     


    def correct_word(self,word: str,frequencies) -> str:
      
        if word in frequencies:
            return word

        candidates = self._edit1(word)

        valid_candidates = candidates.intersection(frequencies.keys())

        if not valid_candidates:
            return word

        best_candidate = min(valid_candidates,key=lambda candidate: (-frequencies[candidate], candidate))

        return best_candidate   


