from inspect import signature
from .registry import get_step
from . import Steps

class TextCleaner:
    """
    Object-oriented interface for the registered text preprocessing steps.
    Args:
        language (str): Language used by language-dependent preprocessing
            steps. Defaults to "en".
    """
    def __init__(self, language: str = "en"):
        if not isinstance(language, str) and language not in ["en","ar"] :
            raise TypeError("language must be one of these values ['en','ar']")
        self.language = language

    def __getattr__(self, name: str):
        """
        Dynamically retrieve a preprocessing function from the registry.
        Args:
            name (str): Registered preprocessing step name.
        """
        try:
            func = get_step(name)
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' has no method '{name}'") 

        def method(text: str, **kwargs):
            parameters = signature(func).parameters

            if "language" in parameters:
                kwargs.setdefault("language", self.language)

            return func(text, **kwargs)

        return method

    def __repr__(self) -> str:
        return f"TextCleaner(language='{self.language}')"
