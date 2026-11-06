import re
import string
import unicodedata
from .utils import *
from ..registry import register_step


@register_step("lowercase")
@requires_str
def lowercase(txt:str) ->str:
    """
    Convert all uppercase characters in the input text to lowercase.

    Args:
        txt (str): The text to convert.

    Returns:
        str: The input text converted to lowercase.

    Raises:
        TypeError: If txt is not a string.

    Examples:
        >>> lowercase("Doaa Helal")
        'doaa helal'
    """
    return txt.casefold()


@register_step("normalize_whitespace")
@requires_str
def normalize_whitespace(txt:str)->str:
    """
    Normalize whitespace by replacing consecutive whitespace characters
    with a single space.

    Args:
        txt (str): The text whose whitespace needs to be normalized.

    Returns:
        str: The text with normalized whitespace.

    Raises:
        TypeError: If txt is not a string.

    Examples:
        >>> normalize_whitespace("  Doaa      Helal")
        'Doaa Helal'
    """  
    cleaned = WHITESPACE_pattern.sub(" ",txt).strip()
    return cleaned

@register_step("remove_urls")
@requires_str
def remove_urls(txt:str,replace_with:str="")->str:
    """
    Remove URLs from the input text.

    Args:
        txt (str): The text containing URLs.
        replace_with (str): The string used to replace each URL.
            Defaults to an empty string.

    Returns:
        str: The input text with URLs replaced.

    Raises:
        TypeError: If txt is not a string.

    Examples:
        >>> remove_urls("Visit https://www.google.com/ for more info")
        'Visit  for more info'
        >>> remove_urls("Visit https://google.com", replace_with="[URL]")
        'Visit [URL]'
    """        
    cleaned=URLS_pattern.sub(replace_with,txt)
    return cleaned


@register_step("remove_emails")
@requires_str
def remove_emails(txt,replace_with="")->str:
    """
    Remove email addresses from the input text.

    Args:
        txt (str): The text containing email addresses.
        replace_with (str): The string used to replace each email address.
            Defaults to an empty string.

    Returns:
        str: The input text with email addresses replaced.

    Raises:
        TypeError: If txt is not a string.

    Examples:
        >>> remove_emails("My email is doaa@gmail.com")
        'My email is '
        >>> remove_emails("Contact doaa@gmail.com", replace_with="[EMAIL]")
        'Contact [EMAIL]'
    """   
    cleaned=EMAIL_pattern.sub(replace_with,txt)
    return cleaned


@register_step("remove_punctuation")
@requires_str
def remove_punctuation(txt:str, keep_emojis=True)->str:
    """
    Remove punctuation characters from the input text.

    Apostrophes are deleted rather than replaced with spaces.
    Other ASCII punctuation characters are replaced with spaces.
    Emojis are preserved by default.

    Args:
        txt (str): The text from which punctuation will be removed.
        keep_emojis (bool): Whether to preserve emojis.
            Defaults to True.

    Returns:
        str: The input text with punctuation removed.

    Raises:
        TypeError: If txt is not a string.

    Examples:
        >>> remove_punctuation("HI, How are you?")
        'HI  How are you '
        >>> remove_punctuation("Hello!!! 😊", keep_emojis=True)
        'Hello    😊'
    """     
    txt=txt.replace("'","")
    
    if not keep_emojis:
        txt = re.sub(r'[^\w\s]', ' ', txt)
    else:
        punctuation_len = len(string.punctuation)
        translation_table = str.maketrans(string.punctuation, ' ' * punctuation_len)
        txt = txt.translate(translation_table)
    return txt


@register_step("normalize_repeating_chars")
@requires_str
def normalize_repeating_chars(txt:str, keep=2)->str:
    """
    Reduce consecutive repetitions of the same character.

    Runs of three or more consecutive identical characters are reduced
    to the specified number of occurrences. Doubled characters are preserved.

    Args:
        txt (str): The text to process.
        keep (int): The number of consecutive occurrences to retain.
            Defaults to 2.

    Returns:
        str: The text with excessive character repetitions reduced.

    Raises:
        TypeError: If txt is not a string.

    Examples:
        >>> normalize_repeating_chars("Doaaaa")
        'Doaa'
        >>> normalize_repeating_chars("Soooo cool", keep=1)
        'So cool'
    """     
    if isinstance(keep,int) and keep>=0 :
        repl = r'\1' * keep
        return REPEATING_pattern.sub( repl, txt)
    else:
        raise ValueError("Keep param must be an integer with a value greater than or equal 0")


@register_step("remove_html")
@requires_str
def remove_html(txt:str)->str:
    """
    Remove HTML tags from the input text.

    Args:
        txt (str): The text containing HTML tags.

    Returns:
        str: The input text with HTML tags removed.

    Raises:
        TypeError: If txt is not a string.

    Examples:
        >>> remove_html("<p>Hello World</p>")
        'Hello World'
        >>> remove_html("<b>Doaa</b> Helal")
        'Doaa Helal'
    """     
    txt=strip_tags(txt)
    return txt


@register_step("remove_mentions")
@requires_str
def remove_mentions(txt:str)->str:
    """
    Remove social media mentions from the input text.

    Args:
        txt (str): The text containing mentions.

    Returns:
        str: The input text with mentions removed.

    Raises:
        TypeError: If txt is not a string.

    Examples:
        >>> remove_mentions("Hello @doaa")
        'Hello '
        >>> remove_mentions("@user1 is talking to @user2")
        ' is talking to '
    """
    
    return MENTION_pattern.sub("",txt)


@register_step("remove_hashtags")
@requires_str
def remove_hashtags(txt:str, keep_word=False)->str:
    """
    Remove hashtags or hashtag symbols from the input text.

    Args:
        txt (str): The text containing hashtags.
        keep_word (bool): If True, remove only the hashtag symbol
            and preserve the hashtag word. If False, remove the
            entire hashtag. Defaults to False.

    Returns:
        str: The input text with hashtags processed according to keep_word.

    Raises:
        TypeError: If txt is not a string.

    Examples:
        >>> remove_hashtags("I love #Python")
        'I love '
        >>> remove_hashtags("I love #Python", keep_word=True)
        'I love Python'
    """
    if keep_word:
        cleaned=keep_HASHTAG_words_pattern.sub("",txt)
    else:    
        cleaned=remove_HASHTAG_pattern.sub("",txt)
    return cleaned


@register_step("remove_digits")
@requires_str
def remove_digits(txt:str)->str:
    """
    Remove numeric digits from the input text.

    Args:
        txt (str): The text containing digits.

    Returns:
        str: The input text with digits removed.

    Raises:
        TypeError: If txt is not a string.

    Examples:
        >>> remove_digits("Python 3 is great")
        'Python  is great'
        >>> remove_digits("I have 123 apples")
        'I have  apples'
    """     

    return DIGIT_pattern.sub("",txt)



@register_step("handle_emojis")
@requires_str
def handle_emojis(txt: str, mode: str = "remove") -> str:
    """
    Handle emojis in the input text according to the selected mode.

    In 'remove' mode, emojis are replaced with spaces.
    In 'text' mode, emojis are replaced with their Unicode names
    formatted as colon-separated text.

    Args:
        txt (str): The text containing emojis.
        mode (str): The emoji handling mode. Supported values are:
            - 'remove': Replace emojis with spaces.
            - 'text': Replace emojis with their Unicode names.
            Defaults to 'remove'.

    Returns:
        str: The processed text with emojis handled according to mode.
            Consecutive whitespace characters are collapsed into one space,
            and leading/trailing whitespace is removed.

    Raises:
        TypeError: If txt is not a string.
        ValueError: If mode is not 'remove' or 'text'.

    Examples:
        >>> handle_emojis("Hello 😊")
        'Hello'
        >>> handle_emojis("Hello 😊", mode="text")
        'Hello :smiling_face_with_smiling_eyes:'
    """
     
    if mode not in ("remove", "text"):
        raise ValueError("mode must be either 'remove' or 'text'")

    if not txt:
        return ""

    result = []

    for char in txt:
        if char in ("\ufe0f", "\u200d"):
            continue

        if is_emoji(char):

            if mode == "remove":
                result.append(" ")

            elif mode == "text":
                try:
                    name = unicodedata.name(char).lower()
                    name = name.replace(" ", "_")
                    result.append(f":{name}:")
                except ValueError:
                    result.append(" ")

        else:
            result.append(char)

    return re.sub(r"\s+", " ", "".join(result)).strip()



    
