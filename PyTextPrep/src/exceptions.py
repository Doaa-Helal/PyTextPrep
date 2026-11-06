class UnknownStepError(Exception):
    """Raised when the user entered a step into the pipeline that don't exist."""
    pass

class InvalidStepParamsError(Exception):
    """Raised when the user enter the params of a function incorrectly"""
    pass