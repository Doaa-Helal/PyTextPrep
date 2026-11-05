import re

URLS_pattern=re.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")
EMAIL_pattern=re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
MENTION_pattern=re.compile(r"(?<![\w@])@[A-Za-z0-9_]+")
DIGIT_pattern=re.compile(r"[+-]?\d+(?:\.\d+)?")
WHITESPACE_pattern=re.compile(r'\s+')
REPEATING_pattern =re.compile( r'(.)\1{2,}')
keep_HASHTAG_words_pattern=re.compile(r"#(?=[A-Za-z0-9_]+)")
remove_HASHTAG_pattern=re.compile(r"(?<!\w)#[A-Za-z0-9_]+")
