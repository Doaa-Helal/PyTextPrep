
import unittest
from unittest.mock import patch
from  PyTextPrep.src.Steps import Morphology as morphology


class TestPorterStemmer(unittest.TestCase):

    def test_basic_stemming(self):
        test_cases = {
            "caresses": "caress",
            "ponies": "poni",
            "ties": "ti",
            "agreed": "agre",
            "disabled": "disabl",
            "matting": "mat",
            "mating": "mate",
            "meeting": "meet",
            "relational": "relat",
            "conditional": "condit",
            "adjustment": "adjust",
        }

        for word, expected in test_cases.items():
            with self.subTest(word=word):
                self.assertEqual(
                    morphology.stemmer.stem(word),
                    expected
                )

    def test_case_insensitivity(self):
        self.assertEqual(
            morphology.stemmer.stem("RUNNING"),
            morphology.stemmer.stem("running")
        )

    def test_short_words(self):
        self.assertEqual(morphology.stemmer.stem("is"), "is")
        self.assertEqual(morphology.stemmer.stem("a"), "a")

    def test_empty_word(self):
        self.assertEqual(morphology.stemmer.stem(""), "")

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            morphology.stemmer.stem(123)


class TestPorterStemFunction(unittest.TestCase):

    def test_stem_sentence(self):
        result = morphology.porter_stemmer(
            "The cats are playing"
        )

        self.assertEqual(result, ["the", "cat", "ar", "plai"])

    def test_empty_text(self):
        self.assertEqual(morphology.porter_stemmer(""), [])

    def test_multiple_spaces(self):
        result = morphology.porter_stemmer("cats    dogs")
        self.assertEqual(result, ["cat", "dog"])

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            morphology.porter_stemmer(123)


class TestLemmatize(unittest.TestCase):

    @patch.object(morphology, "load_wordnet")
    @patch.object(morphology, "singularize")
    def test_wordnet_lookup(self, mock_singularize, mock_wordnet):
        mock_wordnet.return_value = {
            "children": "child",
            "mice": "mouse"
        }

        result = morphology.lemmatize("children mice")

        self.assertEqual(result, "child mouse")
        mock_singularize.assert_not_called()

    @patch.object(morphology, "load_wordnet")
    @patch.object(morphology, "singularize")
    def test_singularize_fallback(
        self, mock_singularize, mock_wordnet
    ):
        mock_wordnet.return_value = {}
        mock_singularize.side_effect = lambda word: {
            "cars": "car",
            "books": "book"
        }.get(word, word)

        result = morphology.lemmatize("cars books")

        self.assertEqual(result, "car book")

    @patch.object(morphology, "load_wordnet", return_value={})
    def test_empty_text(self, mock_wordnet):
        self.assertEqual(morphology.lemmatize(""), "")

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            morphology.lemmatize(123)


class TestNormalizeArabic(unittest.TestCase):

    def test_remove_diacritics(self):
        self.assertEqual(
            morphology.normalize_arabic("أَحْمَد"),
            "احمد"
        )

    def test_normalize_alef(self):
        self.assertEqual(
            morphology.normalize_arabic("آكل أكل إسلام"),
            "اكل اكل اسلام"
        )

    def test_normalize_alef_maksura(self):
        self.assertEqual(
            morphology.normalize_arabic("على"),
            "علي"
        )

    def test_taa_marbuta(self):
        self.assertEqual(
            morphology.normalize_arabic(
                "مدرسة",
                taa_marbuta=True
            ),
            "مدرسه"
        )

    def test_preserve_taa_marbuta_by_default(self):
        self.assertEqual(
            morphology.normalize_arabic("مدرسة"),
            "مدرسة"
        )

    def test_empty_text(self):
        self.assertEqual(morphology.normalize_arabic(""), "")

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            morphology.normalize_arabic(123)


class TestRemoveAccents(unittest.TestCase):

    def test_remove_accents(self):
        self.assertEqual(
            morphology.remove_accents("café"),
            "cafe"
        )

    def test_multiple_accents(self):
        self.assertEqual(
            morphology.remove_accents("naïve résumé"),
            "naive resume"
        )

    def test_unaccented_text(self):
        self.assertEqual(
            morphology.remove_accents("hello world"),
            "hello world"
        )

    def test_empty_text(self):
        self.assertEqual(morphology.remove_accents(""), "")

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            morphology.remove_accents(123)


class TestNgrams(unittest.TestCase):

    def test_bigrams(self):
        result = morphology.ngrams(
            "I love natural language processing",
            2
        )

        expected = [
            ("I", "love"),
            ("love", "natural"),
            ("natural", "language"),
            ("language", "processing")
        ]

        self.assertEqual(result, expected)

    def test_trigrams(self):
        result = morphology.ngrams(
            "I love natural language processing",
            3
        )

        expected = [
            ("I", "love", "natural"),
            ("love", "natural", "language"),
            ("natural", "language", "processing")
        ]

        self.assertEqual(result, expected)

    def test_n_larger_than_token_count(self):
        result = morphology.ngrams("hello world", 3)
        self.assertEqual(result, [])

    def test_single_token(self):
        result = morphology.ngrams("hello", 1)
        self.assertEqual(result, [("hello",)])

    def test_empty_text(self):
        self.assertEqual(morphology.ngrams("", 2), [])

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            morphology.ngrams(123, 2)


class TestCharNgrams(unittest.TestCase):

    def test_bigrams(self):
        self.assertEqual(
            morphology.char_ngrams("hello", 2),
            ["he", "el", "ll", "lo"]
        )

    def test_trigrams(self):
        self.assertEqual(
            morphology.char_ngrams("hello", 3),
            ["hel", "ell", "llo"]
        )

    def test_n_larger_than_word(self):
        self.assertEqual(
            morphology.char_ngrams("hi", 3),
            []
        )

    def test_single_character_ngrams(self):
        self.assertEqual(
            morphology.char_ngrams("cat", 1),
            ["c", "a", "t"]
        )

    def test_empty_word(self):
        self.assertEqual(morphology.char_ngrams("", 2), [])

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            morphology.char_ngrams(123, 2)


class TestNormalizeSlang(unittest.TestCase):

    def test_custom_slang_dictionary(self):
        result = morphology.normalize_slang(
            "u r gr8",
            {"u": "you", "r": "are", "gr8": "great"}
        )

        self.assertEqual(result, "you are great")

    def test_default_slang_dictionary(self):
        with patch.object(
            morphology,
            "load_slang",
            return_value={"u": "you"}
        ):
            result = morphology.normalize_slang("u")

        self.assertEqual(result, "you")

    def test_unknown_slang(self):
        result = morphology.normalize_slang(
            "hello world",
            {"u": "you"}
        )

        self.assertEqual(result, "hello world")

    def test_empty_text(self):
        self.assertEqual(
            morphology.normalize_slang("", {"u": "you"}),
            ""
        )

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            morphology.normalize_slang(123)


class TestCorrectSpelling(unittest.TestCase):

    @patch.object(morphology, "word_freq_loader")
    def test_correct_misspelled_word(self, mock_loader):
        mock_loader.return_value = {
            "programming": 1000
        }

        result = morphology.correct_spelling("progrmming")

        self.assertEqual(result, "programming")

    @patch.object(morphology, "word_freq_loader")
    def test_correct_sentence(self, mock_loader):
        mock_loader.return_value = {
            "programming": 1000
        }

        result = morphology.correct_spelling(
            "I love progrmming"
        )

        self.assertEqual(result, "I love programming")

    @patch.object(morphology, "word_freq_loader")
    def test_empty_text(self, mock_loader):
        mock_loader.return_value = {}

        self.assertEqual(morphology.correct_spelling(""), "")

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            morphology.correct_spelling(123)


if __name__ == "__main__":
    unittest.main(verbosity=2)
