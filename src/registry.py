
from typing import Callable, Any

STEP_REGISTRY: dict[str, Callable] = {}


def register_step(name: str | None = None):

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
 
    if name not in STEP_REGISTRY:
        raise KeyError(f"Step '{name}' is not registered.")

    return STEP_REGISTRY[name]


def get_registered_steps() -> list[str]:
   
    return sorted(STEP_REGISTRY.keys())
