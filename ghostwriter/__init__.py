"""Ghostwriter package."""

__version__ = "0.1.0"

from .cli import main
from .wrapper import main as interactive

__all__ = ["main", "interactive"]
