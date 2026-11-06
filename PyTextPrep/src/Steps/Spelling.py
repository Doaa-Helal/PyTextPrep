import string

class CorrectSpelling:
    """
    Correct spelling mistakes using Peter Norvig's edit-distance approach.

    The algorithm generates candidate words with an edit distance of one
    and selects the candidate with the highest frequency from a
    predefined word-frequency dictionary.

    Methods:
        __call__: Correct spelling mistakes in a word or text.
        _edit1: Generate all possible words with an edit distance of one.
        correct_word: Correct a single word using the frequency dictionary.
    """
    def __init__(self):
        pass
    def __call__(self, word:str,freq:dict):
        """
    Correct spelling mistakes in a word or a text containing multiple words.

    Args:
        word (str): The input word or text to correct.
        freq (dict): A dictionary mapping words to their occurrence frequencies.

    Returns:
        str: The corrected word or text.

    Raises:
        TypeError: If word is not a string.

    Examples:
        >>> corrector("speling", {"spelling": 100, "speaking": 50})
        'spelling'
        >>> corrector("helo world", {"hello": 100, "world": 200})
        'hello world'
        """
        ans=[]
        if len(word.split())==1:
            return self.correct_word(word,freq)
        else:
            for w in word.split():
                ans.append(self.correct_word(w,freq))

        return " ".join(ans)

    def _edit1(self,word:str):
        """
        Generate all possible words with an edit distance of one.

        The function generates candidates through four operations:
            - Deletion: Remove one character.
            - Transposition: Swap two adjacent characters.
            - Replacement: Replace one character with another letter.
            - Insertion: Insert a letter at any position.

        Args:
            word (str): The input word.

        Returns:
            set[str]: A set containing all generated candidate words.

        Raises:
            TypeError: If word is not a string.

        Examples:
            >>> corrector._edit1("at")
            {'a', 't', 'ta', 'bat', 'cat', ...}
        """
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


    def correct_word(self,word: str,frequencies:dict) -> str:
        """
        Correct a single potentially misspelled word using a frequency dictionary.

        Args:
            word (str): The word to correct.
            frequencies (dict): A dictionary mapping words to their frequencies.

        Returns:
            str: The corrected word, or the original word if no valid
                correction is found.

        Examples:
            >>> corrector.correct_word("programing", {"programming": 100})
            'programming'
            
        """
        if word in frequencies:
            return word

        candidates = self._edit1(word)

        valid_candidates = candidates.intersection(frequencies.keys())

        if not valid_candidates:
            return word

        best_candidate = min(valid_candidates,key=lambda candidate: (-frequencies[candidate], candidate))

        return best_candidate   


