from typing import Any, Iterable
from collections.abc import Mapping
from inspect import signature
from difflib import get_close_matches
from .registry import STEP_REGISTRY, get_step
from .Steps import *
from .exceptions import *


class Pipeline:
    def __init__(self, steps: list[tuple[str, dict[str, Any]]]):
        self._steps = []

        for step_name, params in steps:
            self._validate_step_name(step_name)
            self._validate_params(step_name, params)

            func = get_step(step_name)

            self._steps.append({
                "name": step_name,
                "func": func,
                "params": params.copy()
            })


    @staticmethod
    def _validate_step_name(step_name: str) -> None:
        if not isinstance(step_name, str):
            raise TypeError("Step name must be a string.")

        if step_name not in STEP_REGISTRY:
            suggestions = get_close_matches(
                step_name,
                STEP_REGISTRY.keys(),
                n=3,
                cutoff=0.6
            )

            message = f"Unknown step: '{step_name}'."
            if suggestions:
                message += f" Did you mean: {', '.join(suggestions)}?"
            raise UnknownStepError(message)

    @staticmethod
    def _validate_params(step_name: str,params: dict[str, Any]) -> None:
       

        if not isinstance(params, Mapping):
            raise TypeError(
                f"Parameters for '{step_name}' must be a dictionary."
            )

        func = get_step(step_name)

        try:
            sig = signature(func)
            sig.bind("sample text", **params)

        except TypeError as error:
            raise InvalidStepParamsError(f"Invalid parameters for step '{step_name}': {error}") from error

    @property
    def steps(self) -> list[str]:
        
        return [step["name"] for step in self._steps]


    def transform(self,text: str,return_tokens: bool = False) -> str | list[str]:
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}" )

        if not isinstance(return_tokens, bool):
            raise TypeError("return_tokens must be a bool.")

        result = text
        for step in self._steps:
            func = step["func"]
            params = step["params"]
            result = func(result, **params)

            if step["name"] == "porter_stemmer":
                if not isinstance(result, list):
                    raise TypeError(
                        f"Step '{step['name']}' must return list, "
                        f"got {type(result).__name__}"
                    )

            else:
                if not isinstance(result, str):
                    raise TypeError(
                        f"Step '{step['name']}' must return str, "
                        f"got {type(result).__name__}")

        if return_tokens:
            tokenizer = STEP_REGISTRY.get("word_tokenize")

            if tokenizer is not None:
                return tokenizer(result)

            return result.split()

        return result

    def transform_batch(self,texts: Iterable[str],return_tokens: bool = False) -> list[str] | list[list[str]]:
        if isinstance(texts, str):
            raise TypeError("Expected an iterable of strings, not a single string."  )

        results = []

        for text in texts:
            results.append(self.transform(text, return_tokens=return_tokens))

        return results


    def __repr__(self) -> str:
        step_names = " -> ".join(self.steps)
        return f"Pipeline({step_names})"

