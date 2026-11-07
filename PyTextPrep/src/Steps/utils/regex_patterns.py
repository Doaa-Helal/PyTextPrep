import re

URLS_pattern=re.compile(
    r"""(?ix)
    (?<![@\w.-])                                         # not preceded by @, word char, dot or dash
    (?:
        (?:https?|ftp)://[^\s<>"']*[^\s<>"'.,;:!?]       # with scheme
        |
        (?:
            (?:www\.)?                                   # optional www.
            (?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+  # domain labels
            [a-z]{2,24}                                  # TLD
            (?::\d{2,5})?                                # optional port
            (?:/[^\s<>"']*[^\s<>"'.,;:!?])?              # optional path
            (?![\w@-])                                   # not followed by @, word char or dash
        )
    )
    """
)
EMAIL_pattern=re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
MENTION_pattern=re.compile(r"(?<![\w@])@[A-Za-z0-9_]+")
DIGIT_pattern=re.compile(r"[+-]?\d+(?:\.\d+)?")
WHITESPACE_pattern=re.compile(r'\s+')
REPEATING_pattern =re.compile( r'(.)\1{2,}')
keep_HASHTAG_words_pattern=re.compile(r"#(?=[A-Za-z0-9_]+)")
remove_HASHTAG_pattern=re.compile(r"(?<!\w)#[A-Za-z0-9_]+")
