from typing import Any, Iterable
from collections.abc import Mapping
from inspect import signature
from difflib import get_close_matches
from .registry import STEP_REGISTRY, get_step
from .Steps import *
from .exceptions import *


class Pipeline:
    """
    A configurable text preprocessing pipeline.
    A pipeline executes a sequence of registered preprocessing steps
    in the specified order. Each step can receive custom parameters.
    Args:
        steps (list[tuple[str, dict[str, Any]]]):
            A list of tuples, where each tuple contains:
                - The registered step name.
                - A dictionary of parameters for that step.

    Raises:
        TypeError:
            If a step name is not a string or its parameters are not
            provided as a Mapping.
        UnknownStepError:
            If a step is not registered.
        InvalidStepParamsError:
            If the supplied parameters do not match the step's signature.

    Example:
        >>> pipeline = Pipeline([
        ...     ("lowercase", {}),
        ...     ("remove_urls", {}),
        ...     ("remove_punctuation", {})
        ... ])
        >>> pipeline.transform("HELLO! Visit https://example.com")
        'hello visit'
    """

    def __init__(self, steps: list[tuple[str, dict[str, Any]]]):
        """
        Initialize the pipeline and validate its preprocessing steps.

        Each step is retrieved from the global step registry, and its
        parameters are validated against its function signature before
        the pipeline is constructed.

        Args:
            steps: Ordered list of preprocessing steps and their parameters.

        Raises:
            TypeError: If the step name or parameters have an invalid type.
            UnknownStepError: If a requested step is not registered.
            InvalidStepParamsError: If the parameters are invalid.
        """
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
        """
        Validate that a preprocessing step exists in the registry.

        If the requested step is unknown, similar registered step names
        are suggested using fuzzy matching.

        Args:
            step_name: Name of the preprocessing step.

        Raises:
            TypeError: If step_name is not a string.
            UnknownStepError: If the step is not registered.
        """
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
        """
        Validate the parameters supplied to a preprocessing step.

        The function signature is inspected to ensure that the provided
        arguments are compatible with the registered function.

        Args:
            step_name: Name of the preprocessing step.
            params: Dictionary or Mapping containing step parameters.

        Raises:
            TypeError: If params is not a Mapping.
            InvalidStepParamsError: If the parameters do not match
                the function signature.
        """      

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
        """
        Get the names of the preprocessing steps in execution order.

        Returns:
            list[str]: Ordered names of the pipeline steps.

        Example:
            >>> pipeline.steps
            ['lowercase', 'remove_urls', 'remove_punctuation']
        """        
        return [step["name"] for step in self._steps]


    def transform(self,text: str,return_tokens: bool = False) -> str | list[str]:
        """
        Apply all preprocessing steps to a single text input.
        Each step is executed sequentially, using the output of the
        previous step as its input. The return type of each step is
        validated during execution.
        Args:
            text: Input text to preprocess.
        Returns:
            str | list[str]:
                The processed text as a string, or a list of tokens
                when return_tokens is True.

        Raises:
            TypeError: If text is not a string, return_tokens is not
                a boolean, or a preprocessing step returns an
                unexpected type.

        Example:
            >>> pipeline = Pipeline([
            ...     ("lowercase", {}),
            ...     ("remove_punctuation", {})
            ... ])
            >>> pipeline.transform("HELLO WORLD!")
            'hello world'
        """
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
        """
        Apply the preprocessing pipeline to multiple text inputs.
        Each text is processed independently using transform(), while
        preserving the original order of the inputs.

        Args:
            texts: Iterable containing the input strings to preprocess.
                Generators and other iterable objects are supported.
        Returns:
            list[str] | list[list[str]]:
                A list containing the processed results for each input.
        Raises:
            TypeError: If texts is a single string, or if any individual
                input is not a string.

        Example:
            >>> pipeline = Pipeline([("lowercase", {})])
            >>> pipeline.transform_batch(["HELLO", "WORLD"])
            ['hello', 'world']
            >>> pipeline.transform_batch(
            ...     ["HELLO WORLD", "GOOD MORNING"],
            ...     return_tokens=True
            ... )
            [['hello', 'world'], ['good', 'morning']]
        """
        if isinstance(texts, str):
            raise TypeError("Expected an iterable of strings, not a single string."  )

        results = []

        for text in texts:
            results.append(self.transform(text, return_tokens=return_tokens))

        return results


    def __repr__(self) -> str:
        step_names = " -> ".join(self.steps)
        return f"Pipeline({step_names})"

