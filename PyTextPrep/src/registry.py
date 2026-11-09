"""
Step Registry Module.

This module provides a centralized registry for managing text
preprocessing functions.

It allows preprocessing functions to register themselves using
the register_step decorator and provides utilities to retrieve
individual steps or list all registered steps.
"""
from typing import Callable, Any

STEP_REGISTRY: dict[str, Callable] = {}


def register_step(name: str | None = None):
    """
    Decorator for registering a preprocessing function.
    The decorated function is stored in the global STEP_REGISTRY
    dictionary using its specified name or its original function name.
    Args:
        name (str | None): Optional custom name for the registered step.
            If None, the function's __name__ is used.
            Defaults to None.
    Returns:
        Callable: A decorator that registers the function and returns
            the original function unchanged.
    Raises:
        ValueError: If the registration name is empty, contains only
            whitespace, or is already registered.

    Example:
        The decorator can also use the function's original name:

        >>> @register_step()
        ... def remove_urls(text: str) -> str:
        ...     return text
    """
    def decorator(func: Callable) -> Callable:
        step_name = name or func.__name__

        if not isinstance(step_name, str) or not step_name.strip():
            raise ValueError("Step name must be a non-empty string.")

        if step_name in STEP_REGISTRY:
            raise ValueError(
                f"A step named '{step_name}' is already registered."
            )

        STEP_REGISTRY[step_name] = func

        return func

    return decorator


def get_step(name: str) -> Callable:
    """
    Retrieve a registered preprocessing function by its name.
    Args:
        name (str): Name of the registered preprocessing step.
    Returns:
        Callable: The function associated with the requested name.
    Raises:
        KeyError: If the requested step is not registered.

    Example:
        >>> @register_step("lowercase")
        ... def lowercase(text):
        ...     return text.casefold()

        >>> func = get_step("lowercase")
        >>> func("HELLO")
        'hello'
    """
    if name not in STEP_REGISTRY:
        raise KeyError(f"Step '{name}' is not registered.")

    return STEP_REGISTRY[name]


def get_registered_steps() -> list[str]:
    """
    Retrieve the names of all registered preprocessing steps.
    The returned names are sorted alphabetically.
    Returns:
        list[str]: Alphabetically sorted registered step names.
    Example:
        >>> get_registered_steps()
        ['lowercase', 'remove_urls', 'remove_whitespace']
    """
    return sorted(STEP_REGISTRY.keys())
