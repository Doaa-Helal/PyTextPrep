# PyTextPrep

PyTextPrep is a small, extensible Python library for preparing text before
analysis or machine-learning workflows. It provides reusable cleaning,
filtering, tokenization, morphology, spelling, and n-gram steps.

## Ready to download package

You can now download the package using: 
```shell
pip install -i https://test.pypi.org/simple/ pytextprep-doaahelal==0.1.2
```

## Current project layout

The source code is currently used directly from the repository:

```text
PyTextPrep/
├── PyTextPrep/src/
│   ├── text.py        # Fluent Text wrapper
│   ├── pipeline.py    # Configurable Pipeline
│   ├── registry.py    # Step registration and lookup
│   └── Steps/         # Built-in text-processing steps
├── tests/             # Unit tests
└── data/              # Runtime dictionaries and corpora
```

Run examples from the repository root so that the `PyTextPrep` package is on
Python's import path. Python 3.10 or newer is recommended because the source
uses modern type-annotation syntax.

## Quick start

### Fluent `Text` API

`Text` stores a string and exposes registered processing steps as methods.
Each step updates the value and returns the same `Text` instance, so steps can
be chained:

```python
from PyTextPrep.src.text import Text

cleaned = (
    Text("  Visit https://example.com NOW!!!  ")
    .remove_urls()
    .lowercase()
    .remove_punctuation()
    .normalize_whitespace()
)

print(cleaned.value)
# visit now
```

The wrapped value is also available through `str()` and `repr()`:

```python
print(str(cleaned))  # visit now
print(repr(cleaned)) # Text('visit now')
```

`Text` requires a string at construction time and raises `TypeError` for
non-string input. An unknown step raises `AttributeError`.

### Reusable `Pipeline`

Use `Pipeline` when the same sequence should be applied to many texts or when
step parameters should be declared up front:

```python
from PyTextPrep.src.pipeline import Pipeline

pipeline = Pipeline([
    ("lowercase", {}),
    ("remove_urls", {"replace_with": "[URL]"}),
    ("normalize_whitespace", {}),
])

print(pipeline.transform("Visit HTTPS://example.com  NOW"))
# visit [URL] now

print(pipeline.transform_batch(["HELLO", "PYTHON"]))
# ['hello', 'python']
```

Set `return_tokens=True` to return tokens after transformation:

```python
tokens = pipeline.transform("HELLO WORLD", return_tokens=True)
print(tokens)  # ['hello', 'world']
```

`Pipeline` validates step names and parameters when it is created. It also
checks the return type of each step during transformation. The
`porter_stemmer` step returns a list of stems; other pipeline steps must return
strings.

## Built-in steps

All built-in steps are registered automatically when
`PyTextPrep.src.pipeline` or `PyTextPrep.src.text` is imported.

### Cleaning

| Step | Parameters | Purpose |
| --- | --- | --- |
| `lowercase()` | — | Convert text to lowercase using `casefold()` |
| `normalize_whitespace()` | — | Collapse whitespace and trim the result |
| `remove_urls()` | `replace_with=""` | Remove URLs |
| `remove_emails()` | `replace_with=""` | Remove email addresses |
| `remove_punctuation()` | `keep_emojis=True` | Remove punctuation |
| `normalize_repeating_chars()` | `keep=2` | Reduce repeated characters |
| `remove_html()` | — | Remove HTML tags |
| `remove_mentions()` | — | Remove `@mentions` |
| `remove_hashtags()` | `keep_word=False` | Remove hashtags or only `#` |
| `remove_digits()` | — | Remove numeric digits |
| `handle_emojis()` | `mode="remove"` | Remove emojis or convert them to text |

### Filtering

| Step | Parameters | Purpose |
| --- | --- | --- |
| `remove_stopwords()` | — | Remove stopwords while preserving negations |
| `expand_contractions()` | — | Expand contractions such as `don't` |

### Tokenization

| Step | Parameters | Result |
| --- | --- | --- |
| `word_tokenize()` | — | Whitespace-separated word list |
| `sent_tokenize()` | — | Sentence list based on sentence-ending punctuation |

### Morphology and normalization

| Step | Parameters | Result |
| --- | --- | --- |
| `porter_stemmer()` | — | List of Porter stems |
| `lemmatize()` | — | Text with words converted to base forms |
| `normalize_arabic()` | `taa_marbuta=False` | Normalize Arabic letters and diacritics |
| `remove_accents()` | — | Remove Latin accent marks |
| `ngrams()` | `n` | List of word n-gram tuples |
| `char_ngrams()` | `n` | List of character n-grams |
| `normalize_slang()` | `table=None` | Replace slang using the built-in or supplied table |
| `correct_spelling()` | — | Correct words using the frequency dictionary |

Steps that return lists, such as `word_tokenize`, `sent_tokenize`,
`porter_stemmer`, `ngrams`, and `char_ngrams`, are generally best called
directly or used as the final operation in a pipeline. `Text` is intended
primarily for chains of string-to-string steps.

## Calling steps directly

The step functions can also be imported from their modules:

```python
from PyTextPrep.src.Steps.Cleaning import normalize_whitespace
from PyTextPrep.src.Steps.Morphology import ngrams

print(normalize_whitespace("  hello   world  "))
# hello world

print(ngrams("one two three", 2))
# [('one', 'two'), ('two', 'three')]
```

## Adding a custom step

Register a function with `register_step`. Import the module containing the
registration before constructing a `Text` object or `Pipeline`:

```python
from PyTextPrep.src.registry import register_step
from PyTextPrep.src.text import Text

@register_step("remove_dashes")
def remove_dashes(text: str) -> str:
    return text.replace("-", " ")

result = Text("well-known").remove_dashes().value
print(result)  # well known
```

The registry rejects empty or duplicate names. Registered step names can be
inspected with:

```python
from PyTextPrep.src.registry import get_registered_steps

print(get_registered_steps())
```

## Runtime resources

Some steps load bundled resources from `data/` or
`PyTextPrep/src/Resources/`, including:

- English stopwords
- Contraction mappings
- Slang mappings
- Word-frequency data for spelling correction
- WordNet data for lemmatization

Keep these resource directories available when using the corresponding
steps.

## Testing

Run the unit-test suite from the repository root:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

The tests cover cleaning, filtering, morphology, tokenization, pipelines, and
step registration.

## License

See [LICENSE](LICENSE) for licensing information.
