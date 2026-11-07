
from inspect import signature
from .registry import get_step
from . import Steps


class Text:
    def __init__(self, text: str):
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
