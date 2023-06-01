"""markup_prompter root package."""

try:
    from markup_prompter import _version

    __version__ = _version.__version__
except Exception:
    __version__ = ""
