
"""
Text Module.

This module provides a fluent, object-oriented interface for applying
registered text preprocessing operations through method chaining.

The Text class stores the current text internally and dynamically
retrieves preprocessing functions from the central step registry.
"""
from inspect import signature
from .registry import get_step
from . import Steps


class Text:
    """
    A text wrapper that supports fluent preprocessing and method chaining.

    The class stores a string internally and allows registered
    preprocessing functions to be applied directly as methods.

    Each operation updates the stored text and returns the same
    Text instance, allowing multiple operations to be chained.

    Args:
        text (str): Initial text to be processed.

    Raises:
        TypeError: If the provided text is not a string.

    Example:
        >>> text = (
        ...     Text("HELLO!!! Visit https://example.com")
        ...     .lowercase()
        ...     .remove_urls()
        ...     .remove_punctuation()
        ... )
        >>> text.value
        'hello visit'
    """
    def __init__(self, text: str):
        """
        Initialize a Text instance.
        Args:
            text (str): Initial text value.
        Raises:
            TypeError: If text is not a string.
        """
        if not isinstance(text, str) :
            raise TypeError( f"Expected str, got {type(text).__name__}" )
        self._value = text
    @property
    def value(self) -> str:
        return self._value
    
    def __getattr__(self, name: str):
        try:
            func = get_step(name)
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' has no method '{name}'") 

        def method(*args, **kwargs):
            parameters = signature(func).parameters
            if "language" in parameters:
                kwargs.setdefault("language", "en")
            self._value = func(self._value,*args,**kwargs)
            return self
        return method

    def __str__(self):
        return self._value

    def __repr__(self):
        return f"Text({self._value!r})"
