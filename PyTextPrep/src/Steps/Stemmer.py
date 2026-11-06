class PorterStemmer:
    """
    Implement the original Porter Stemming algorithm for English words.

    The Porter Stemmer reduces words to their stems by applying a sequence
    of suffix-removal and replacement rules. It consists of five main
    steps, including substeps for handling plurals, verb endings, and
    final character adjustments.

    The implementation uses helper methods to determine consonants,
    calculate the measure (m) of a word, detect vowels and consonant
    patterns, and apply suffix transformations.

    The algorithm is rule-based and does not require external libraries.

    Examples:
        >>> stemmer = PorterStemmer()
        >>> stemmer.stem("caresses")
        'caress'
    """
    def __init__(self):
        self.VOWELS=['a','e','i','o','u','A','E','I','O','U']

    def _is_consonant(self,char:str):
        """
        Check if a char at  is a consonant or not
        """
        return char  not in self.VOWELS
        

    def measure(self, word:str):
        """
        Calculate the number of VC sequences (m).
        """
        ans=[]
        for idx,char in enumerate(word):
            if self._is_consonant(char):
                ans.append("c")
            else:
                ans.append("v")
        seq="".join(ans)
        return seq.count("vc")
    
    def has_vowel(self, word:str):
        """
        Check whether a word contains at least one vowel.
        """

        return any(
            not self._is_consonant(char)
            for char in word
        )

    def ends_with_double_consonant(self, word:str):
        """
        Check whether a word ends with two identical consonants.
        This condition is used in Step 1b when processing words
        ending in 'ed' or 'ing'.
        """
        return (len(word) >= 2 and word[-1] == word[-2] and self._is_consonant(word[-1]))
    
    def ends_with_cvc(self, word):
        """
        Check whether a word ends with a consonant-vowel-consonant pattern.

        The final consonant must not be 'w', 'x', or 'y'.

        This condition is used in Step 1b and Step 5a to determine
        whether an 'e' should be added or retained.
        """
        if len(word) < 3:
            return False
        return (
            self._is_consonant(word[-3])
            and not self._is_consonant(word[-2])
            and self._is_consonant(word[-1])
            and word[-1] not in "wxy"
        )
    
    def step1a(self, word:str):
        """
        Handle plural suffixes.

        Apply the following transformations:

        Step 1a has these rules:
        - sses → ss
        - ies → i
        - ss → ss
        - s → remove
        """
        if word.endswith("sses"):
            word = word[:-2]

        elif word.endswith("ies"):
            word = word[:-2]

        elif word.endswith("ss"):
            pass

        elif word.endswith("s"):
            word = word[:-1]

        return word
    
    def step1b(self, word:str):
        """
        Remove 'eed', 'ed', and 'ing' suffixes according to the algorithm.

        For 'eed', the suffix is replaced with 'ee' if the remaining
        stem has a measure greater than zero.

        For 'ed' and 'ing', the suffix is removed only if the remaining
        stem contains a vowel. The resulting word is then processed
        by the Step 1b cleanup rules.

        """
        if word.endswith("eed"):
            stem = word[:-3]

            if self.measure(stem) > 0:
                word = stem + "ee"

        elif word.endswith("ed"):
            stem = word[:-2]

            if self.has_vowel(stem):
                word = stem
                word = self._step1b_cleanup(word)

        elif word.endswith("ing"):
            stem = word[:-3]

            if self.has_vowel(stem):
                word = stem
                word = self._step1b_cleanup(word)

        return word
    
    def _step1b_cleanup(self, word:str):
        """
        Apply additional rules after removing 'ed' or 'ing'.

        The cleanup rules are:
            - Append 'e' to words ending in 'at', 'bl', or 'iz'.
            - Remove the final consonant from a double consonant,
              except when it is 'l', 's', or 'z'.
            - Append 'e' if the word has measure 1 and ends with CVC.
        """
        if word.endswith(("at", "bl", "iz")):
            word += "e"

        elif self.ends_with_double_consonant(word):
            if word[-1] not in "lsz":
                word = word[:-1]

        elif self.measure(word) == 1 and self.ends_with_cvc(word):
            word += "e"

        return word
    
    def step1c(self, word:str):
        """
        Replace a terminal 'y' with 'i' when the stem contains a vowel.
        """
        if word.endswith("y"):
            stem = word[:-1]

            if self.has_vowel(stem):
                word = stem + "i"

        return word

    def _replace_suffix(self, word:str, replacements:dict, min_measure:int):
        """
        Replace a matching suffix when the remaining stem satisfies
        the specified measure condition.

        Suffixes are checked in the order provided by the replacements
        dictionary. A replacement is applied only when the measure
        of the remaining stem is greater than min_measure.
        """
        for suffix, replacement in replacements.items():
            if word.endswith(suffix):
                stem = word[:-len(suffix)]
                if self.measure(stem) > min_measure:
                    return stem + replacement
                return word
        return word
    
    def step2(self, word:str):
        """
        Replace longer derivational suffixes with shorter forms.
        """
        replacements = {
            "ational": "ate",
            "tional": "tion",
            "enci": "ence",
            "anci": "ance",
            "izer": "ize",
            "abli": "able",
            "alli": "al",
            "entli": "ent",
            "eli": "e",
            "ousli": "ous",
            "ization": "ize",
            "ation": "ate",
            "ator": "ate",
            "alism": "al",
            "iveness": "ive",
            "fulness": "ful",
            "ousness": "ous",
            "aliti": "al",
            "iviti": "ive",
            "biliti": "ble",
            "logi": "log"
        }

        return self._replace_suffix(word, replacements, min_measure=0)
    
    def step3(self, word:str):
        """Apply additional derivational suffix transformations."""
        replacements = {
            "icate": "ic",
            "ative": "",
            "alize": "al",
            "iciti": "ic",
            "ical": "ic",
            "ful": "",
            "ness": ""
        }
        return self._replace_suffix(word, replacements, min_measure=0)

    def step4(self, word:str):
        """
        Remove selected suffixes when the remaining stem has a
        measure greater than one."""
        suffixes = (
            "al", "ance", "ence", "er", "ic",
            "able", "ible", "ant", "ement",
            "ment", "ent", "ou", "ism", "ate",
            "iti", "ous", "ive", "ize"
        )
        for suffix in suffixes:
            if word.endswith(suffix):
                stem = word[:-len(suffix)]

                if self.measure(stem) > 1:
                    return stem

                return word

        if word.endswith("ion"):
            stem = word[:-3]

            if stem.endswith(("s", "t")) and self.measure(stem) > 1:
                return stem

        return word

    def step5(self, word:str):
        """
        Perform final adjustments to the stem.

        Step 5 consists of two rules:
            - Step 5a: Remove a final 'e' when the remaining stem
              has measure greater than one, or measure equal to one
              and does not end in CVC.
            - Step 5b: Remove one 'l' from a final 'll' when the
              word has a measure greater than one.
        """
        if word.endswith("e"):
            stem = word[:-1]
            m = self.measure(stem)
            if m > 1 or (m == 1 and not self.ends_with_cvc(stem)):
                word = stem

        if word.endswith("ll") and self.measure(word) > 1:
            word = word[:-1]

        return word
 
    def stem(self, word:str):
        """
        Apply the complete Porter Stemming algorithm to an English word.

        The word is converted to lowercase using casefold(), then
        processed through the five main steps in their required order:
            1. Step 1a, 1b, and 1c: Remove plural and common verb endings.
            2. Step 2: Replace longer derivational suffixes.
            3. Step 3: Apply additional suffix transformations.
            4. Step 4: Remove selected suffixes.
            5. Step 5: Perform final character adjustments.

        Words containing two or fewer characters are returned unchanged
        after case normalization.
        """
        if not isinstance(word,str):
            raise TypeError(f"expected str got {type(word).__name__}")
        word = word.casefold()
        if len(word) <= 2:
            return word
        word = self.step1a(word)
        word = self.step1b(word)
        word = self.step1c(word)
        word = self.step2(word)
        word = self.step3(word)
        word = self.step4(word)
        word = self.step5(word)

        return word


