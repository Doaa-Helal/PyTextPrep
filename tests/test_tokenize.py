import unittest
from PyTextPrep.src.Steps import Tokenize as tokenize


class TestWordTokenize(unittest.TestCase):

    def test_basic_tokenization(self):
        result = tokenize.word_tokenize("I love Python programming")
        self.assertEqual(result,["I", "love", "Python", "programming"])

    def test_multiple_spaces(self):
        result = tokenize.word_tokenize("I   love    Python")
        self.assertEqual(result, ["I", "love", "Python"])

    def test_tabs_and_newlines(self):
        result = tokenize.word_tokenize("I\tlove\nPython")
        self.assertEqual(result, ["I", "love", "Python"])

    def test_empty_text(self):
        self.assertEqual(tokenize.word_tokenize(""), [])

    def test_only_whitespace(self):
        self.assertEqual(tokenize.word_tokenize("   \n\t "), [])

    def test_preserve_punctuation(self):
        result = tokenize.word_tokenize("Hello, world!")
        self.assertEqual(result, ["Hello,", "world!"])

    def test_preserve_apostrophes(self):
        result = tokenize.word_tokenize("I don't like it")
        self.assertEqual(result, ["I", "don't", "like", "it"])

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            tokenize.word_tokenize(123)


class TestSentTokenize(unittest.TestCase):

    def test_basic_sentences(self):
        text = "Hello world. How are you? I am fine!"
        result = tokenize.sent_tokenize(text)
        self.assertEqual(result,["Hello world.","How are you?","I am fine!"] )

    def test_single_sentence(self):
        text = "I love Python."
        self.assertEqual(tokenize.sent_tokenize(text),["I love Python."])

    def test_multiple_spaces_between_sentences(self):
        text = "Hello world.   How are you?"
        self.assertEqual(tokenize.sent_tokenize(text),["Hello world.", "How are you?"])

    def test_newlines_between_sentences(self):
        text = "Hello world.\nHow are you?"
        self.assertEqual(tokenize.sent_tokenize(text),["Hello world.", "How are you?"])

    def test_dr_abbreviation(self):
        text = "Dr. Smith is here. He is a doctor."
        self.assertEqual(tokenize.sent_tokenize(text),["Dr. Smith is here.", "He is a doctor."])

    def test_mr_abbreviation(self):
        text = "Mr. John arrived. He is waiting."
        self.assertEqual(tokenize.sent_tokenize(text),["Mr. John arrived.", "He is waiting."])

    def test_mrs_abbreviation(self):
        text = "Mrs. Smith arrived. She is waiting."
        self.assertEqual(tokenize.sent_tokenize(text),["Mrs. Smith arrived.", "She is waiting."])

    def test_eg_abbreviation(self):
        text = "I like fruits, e.g. apples and oranges. They are healthy."
        self.assertEqual(tokenize.sent_tokenize(text),["I like fruits, e.g. apples and oranges.","They are healthy."])

    def test_ie_abbreviation(self):
        text = "He is a programmer, i.e. he writes code. He enjoys it."
        self.assertEqual(tokenize.sent_tokenize(text),["He is a programmer, i.e. he writes code.","He enjoys it."])

    def test_etc_abbreviation(self):
        text = "I bought apples, oranges, etc. They are fresh."
        self.assertEqual(tokenize.sent_tokenize(text),["I bought apples, oranges, etc.","They are fresh."])

    def test_decimal_numbers(self):
        text = "Pi is 3.14. Use e.g. this one!"
        self.assertEqual(tokenize.sent_tokenize(text),["Pi is 3.14.", "Use e.g. this one!"])

    def test_split_before_number(self):
        text = "The result is excellent. 95 students passed."
        self.assertEqual(tokenize.sent_tokenize(text),["The result is excellent.","95 students passed."])

    def test_empty_text(self):
        self.assertEqual(tokenize.sent_tokenize(""), [])

    def test_only_whitespace(self):
        self.assertEqual(tokenize.sent_tokenize("   \n\t "), [])

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            tokenize.sent_tokenize(None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
