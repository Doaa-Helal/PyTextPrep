
import unittest
from unittest.mock import patch
from PyTextPrep.src.Steps import Cleaning as cleaning

class TestLowercase(unittest.TestCase):

    def test_basic_text(self):
        self.assertEqual(cleaning.lowercase("Hello WORLD"), "hello world")

    def test_casefold(self):
        self.assertEqual(cleaning.lowercase("Straße"), "strasse")

    def test_empty_text(self):
        self.assertEqual(cleaning.lowercase(""), "")

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            cleaning.lowercase(123)


class TestNormalizeWhitespace(unittest.TestCase):

    def test_multiple_spaces(self):
        self.assertEqual(
            cleaning.normalize_whitespace("hello     world"),
            "hello world"
        )

    def test_tabs_and_newlines(self):
        self.assertEqual(
            cleaning.normalize_whitespace("hello\t\nworld"),
            "hello world"
        )

    def test_leading_and_trailing_spaces(self):
        self.assertEqual(
            cleaning.normalize_whitespace("   hello world   "),
            "hello world"
        )

    def test_empty_text(self):
        self.assertEqual(cleaning.normalize_whitespace(""), "")

    def test_only_whitespace(self):
        self.assertEqual(cleaning.normalize_whitespace("   \n\t "), "")

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            cleaning.normalize_whitespace(None)


class TestRemoveURLs(unittest.TestCase):

    def test_http_url(self):
        result = cleaning.remove_urls("Visit http://example.com today")
        self.assertNotIn("http://example.com", result)

    def test_https_url(self):
        result = cleaning.remove_urls("Visit https://example.com today")
        self.assertNotIn("https://example.com", result)

    def test_www_url(self):
        result = cleaning.remove_urls("Visit www.example.com today")
        self.assertNotIn("www.example.com", result)

    def test_custom_replacement(self):
        result = cleaning.remove_urls(
            "Visit https://example.com today",
            replace_with="[URL]"
        )
        self.assertIn("[URL]", result)

    def test_trailing_punctuation(self):
        result=cleaning.remove_urls("go to https://a.io/x?y=1.")
        self.assertEqual(result,"go to ." )

    def test_empty_text(self):
        self.assertEqual(cleaning.remove_urls(""), "")

    def test_no_url(self):
        text = "This is a normal sentence."
        self.assertEqual(cleaning.remove_urls(text), text)

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            cleaning.remove_urls(123)

    def test_broken_urls(self):
        result=cleaning.remove_urls("not a url: http:/broken")
        self.assertEqual(result,"not a url: http:/broken" )

class TestRemoveEmails(unittest.TestCase):

    def test_basic_email(self):
        result = cleaning.remove_emails("Contact me at test@example.com")
        self.assertNotIn("test@example.com", result)

    def test_multiple_emails(self):
        result = cleaning.remove_emails(
            "test@example.com and hello@gmail.com"
        )
        self.assertNotIn("test@example.com", result)
        self.assertNotIn("hello@gmail.com", result)

    def test_custom_replacement(self):
        result = cleaning.remove_emails(
            "Contact test@example.com",
            replace_with="[EMAIL]"
        )
        self.assertIn("[EMAIL]", result)

    def test_empty_text(self):
        self.assertEqual(cleaning.remove_emails(""), "")

    def test_no_email(self):
        text = "This is a normal sentence."
        self.assertEqual(cleaning.remove_emails(text), text)

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            cleaning.remove_emails(None)

    def test_custom_email(self):
        result=cleaning.remove_emails("write to ali@iti.gov.eg today")
        self.assertEqual(result,"write to  today")


class TestRemovePunctuation(unittest.TestCase):

    def test_remove_ascii_punctuation(self):
        result = cleaning.remove_punctuation("Hello, world!")
        self.assertEqual(result, "Hello  world ")

    def test_remove_apostrophes(self):
        result = cleaning.remove_punctuation("rock'n'roll!!")
        self.assertEqual(result, "rocknroll  ")

    def test_keep_emojis(self):
        result = cleaning.remove_punctuation("Hello 😀!")
        self.assertIn("😀", result)
        self.assertNotIn("!", result)

    def test_remove_emojis(self):
        result = cleaning.remove_punctuation(
            "Hello 😀!",
            keep_emojis=False
        )
        self.assertNotIn("😀", result)
        self.assertNotIn("!", result)

    def test_empty_text(self):
        self.assertEqual(cleaning.remove_punctuation(""), "")

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            cleaning.remove_punctuation(123)


class TestNormalizeRepeatingChars(unittest.TestCase):

    def test_default_keep(self):
        result = cleaning.normalize_repeating_chars("soooo")
        self.assertEqual(result, "soo")

    def test_keep_one(self):
        result = cleaning.normalize_repeating_chars("sooooo", keep=1)
        self.assertEqual(result, "so")

    def test_keep_three(self):
        result = cleaning.normalize_repeating_chars("sooooo", keep=3)
        self.assertEqual(result, "sooo")

    def test_preserve_double_characters(self):
        result = cleaning.normalize_repeating_chars("good book")
        self.assertEqual(result, "good book")

    def test_keep_zero(self):
        result = cleaning.normalize_repeating_chars("soooo", keep=0)
        self.assertEqual(result, "s")

    def test_negative_keep(self):
        with self.assertRaises(ValueError):
            cleaning.normalize_repeating_chars("hello", keep=-1)

    def test_invalid_keep_type(self):
        with self.assertRaises(ValueError):
            cleaning.normalize_repeating_chars("hello", keep=1.5)

    def test_empty_text(self):
        self.assertEqual(cleaning.normalize_repeating_chars(""), "")

    def test_invalid_text_type(self):
        with self.assertRaises(TypeError):
            cleaning.normalize_repeating_chars(123)


class TestRemoveHTML(unittest.TestCase):

    def test_remove_html_tags(self):
        result = cleaning.remove_html("<p>Hello World</p>")
        self.assertNotIn("<p>", result)
        self.assertNotIn("</p>", result)
        self.assertIn("Hello World", result)

    def test_nested_html_tags(self):
        result = cleaning.remove_html(
            "<div><p>Hello <b>World</b></p></div>"
        )
        self.assertNotIn("<", result)
        self.assertNotIn(">", result)
        self.assertIn("Hello", result)
        self.assertIn("World", result)

    def test_empty_text(self):
        self.assertEqual(cleaning.remove_html(""), "")

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            cleaning.remove_html(None)


class TestRemoveMentions(unittest.TestCase):

    def test_remove_mention(self):
        result = cleaning.remove_mentions("Hello @doaa")
        self.assertNotIn("@doaa", result)

    def test_multiple_mentions(self):
        result = cleaning.remove_mentions("@user1 hello @user2")
        self.assertNotIn("@user1", result)
        self.assertNotIn("@user2", result)

    def test_no_mentions(self):
        text = "Hello world"
        self.assertEqual(cleaning.remove_mentions(text), text)

    def test_empty_text(self):
        self.assertEqual(cleaning.remove_mentions(""), "")

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            cleaning.remove_mentions(123)


class TestRemoveHashtags(unittest.TestCase):

    def test_remove_hashtag_and_word(self):
        result = cleaning.remove_hashtags("I love #Python")
        self.assertNotIn("#Python", result)

    def test_keep_hashtag_word(self):
        result = cleaning.remove_hashtags(
            "I love #Python",
            keep_word=True
        )
        self.assertNotIn("#", result)
        self.assertIn("Python", result)

    def test_multiple_hashtags(self):
        result = cleaning.remove_hashtags("#Python is #awesome")
        self.assertNotIn("#Python", result)
        self.assertNotIn("#awesome", result)

    def test_empty_text(self):
        self.assertEqual(cleaning.remove_hashtags(""), "")

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            cleaning.remove_hashtags(None)


class TestRemoveDigits(unittest.TestCase):

    def test_remove_digits(self):
        result = cleaning.remove_digits("I have 2 apples")
        self.assertEqual(result, "I have  apples")

    def test_remove_multiple_digits(self):
        result = cleaning.remove_digits("Python 3.10 was released in 2021")
        self.assertNotIn("3", result)
        self.assertNotIn("1", result)
        self.assertNotIn("0", result)
        self.assertNotIn("2", result)

    def test_no_digits(self):
        text = "Hello world"
        self.assertEqual(cleaning.remove_digits(text), text)

    def test_empty_text(self):
        self.assertEqual(cleaning.remove_digits(""), "")

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            cleaning.remove_digits(123)


class TestHandleEmojis(unittest.TestCase):

    @patch.object(cleaning, "is_emoji")
    def test_remove_emojis(self, mock_is_emoji):
        mock_is_emoji.side_effect = lambda char: char == "😀"

        result = cleaning.handle_emojis("Hello 😀 world")

        self.assertEqual(result, "Hello world")

    @patch.object(cleaning, "is_emoji")
    def test_convert_emojis_to_text(self, mock_is_emoji):
        mock_is_emoji.side_effect = lambda char: char == "😀"

        result = cleaning.handle_emojis(
            "Hello 😀",
            mode="text"
        )

        self.assertEqual(result, "Hello :grinning_face:")

    @patch.object(cleaning, "is_emoji")
    def test_multiple_emojis(self, mock_is_emoji):
        mock_is_emoji.side_effect = lambda char: char in ("😀", "😂")

        result = cleaning.handle_emojis("Hello 😀 😂")

        self.assertEqual(result, "Hello")

    def test_invalid_mode(self):
        with self.assertRaises(ValueError):
            cleaning.handle_emojis("Hello 😀", mode="invalid")

    def test_empty_text(self):
        self.assertEqual(cleaning.handle_emojis(""), "")

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            cleaning.handle_emojis(123)


if __name__ == "__main__":
    unittest.main(verbosity=2)
