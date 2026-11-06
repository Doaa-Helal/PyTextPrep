
import unittest
from unittest.mock import patch
from PyTextPrep.src.Steps import Filtering as filtering


class TestRemoveStopwords(unittest.TestCase):

    @patch.object(filtering,"load_stopwords",return_value={"the", "is", "a", "an", "and", "in", "of"})
    def test_remove_basic_stopwords(self, mock_loader):
        result = filtering.remove_stopwords("the cat is in the house")

        self.assertEqual(result, "cat house")
        mock_loader.assert_called_once()

    @patch.object(filtering,"load_stopwords",return_value={"the", "is", "a", "an", "and"})
    def test_preserve_negations(self, mock_loader):
        result = filtering.remove_stopwords("I do not like this")
        self.assertEqual(result, "I do not like this")

    @patch.object(filtering,"load_stopwords",return_value={"no", "not", "nor", "the"})
    def test_preserve_all_negations(self, mock_loader):
        result = filtering.remove_stopwords("no not nor the")
        self.assertEqual(result, "no not nor")

    @patch.object(filtering,"load_stopwords",return_value={"the", "is", "and"})
    def test_case_insensitive_removal(self, mock_loader):
        result = filtering.remove_stopwords("THE Cat IS Sleeping")
        self.assertEqual(result, "Cat Sleeping")

    @patch.object(filtering,"load_stopwords",return_value={"the", "is", "and"})
    def test_empty_text(self, mock_loader):
        self.assertEqual(filtering.remove_stopwords(""), "")

    @patch.object(filtering,"load_stopwords",return_value=set())
    def test_no_stopwords(self, mock_loader):
        text = "the cat is sleeping"
        self.assertEqual(filtering.remove_stopwords(text), text)

    @patch.object(filtering,"load_stopwords",return_value={"the", "is"})
    def test_multiple_spaces(self, mock_loader):
        result = filtering.remove_stopwords("the   cat   is   sleeping")
        self.assertEqual(result, "cat sleeping")

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            filtering.remove_stopwords(123)

    @patch.object(filtering,"load_stopwords",return_value={"the", "is"})
    def test_case_insesitive(self,mock_loader):
        result=filtering.remove_stopwords("THE end")
        self.assertEqual(result, "end")
    


class TestExpandContractions(unittest.TestCase):

    @patch.object(filtering,"load_contractions",return_value={"can't": "cannot" ,"won't": "will not" ,"i'm": "i am" ,"you're": "you are" ,"they're": "they are"})
    def test_expand_basic_contractions(self, mock_loader):
        result = filtering.expand_contractions(
            "I can't believe you're here"
        )
        self.assertEqual(result, "I cannot believe you are here")
        mock_loader.assert_called_once()

    @patch.object(filtering,"load_contractions",
        return_value={
            "can't": "cannot",
            "don't": "do not",
            "isn't": "is not",
            "'re":"are"
        }
    )
    def test_multiple_contractions(self, mock_loader):
        result = filtering.expand_contractions(
            "I can't and don't think it isn't true"
        )
        result2=filtering.expand_contractions("They 're here") 
        self.assertEqual(result,"I cannot and do not think it is not true")
        self.assertEqual(result2,"They are here")

    @patch.object(filtering,"load_contractions",return_value={"can't": "cannot"})
    def test_case_insensitive_lookup(self, mock_loader):
        result = filtering.expand_contractions("I CAN'T do that")
        self.assertEqual(result, "I cannot do that")

    @patch.object(filtering,"load_contractions",return_value={"can't": "cannot"})
    def test_unknown_contraction(self, mock_loader):
        text = "I won't change this"
        self.assertEqual(filtering.expand_contractions(text),text)

    @patch.object(filtering,"load_contractions",return_value={})
    def test_empty_dictionary(self, mock_loader):
        text = "I can't do this"
        self.assertEqual(filtering.expand_contractions(text),text)

    @patch.object(filtering,"load_contractions",return_value={"can't": "cannot"})
    def test_empty_text(self, mock_loader):
        self.assertEqual(filtering.expand_contractions(""), "")

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            filtering.expand_contractions(None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
