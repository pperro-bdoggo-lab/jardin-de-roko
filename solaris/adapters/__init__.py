"""Adaptadores de generación."""

from __future__ import annotations

from solaris.adapters.api import ApiAdapter
from solaris.adapters.base import ModelAdapter
from solaris.adapters.hybrid import HybridAdapter
from solaris.adapters.local import LocalAdapter
from solaris.adapters.stub import StubAdapter

__all__ = [
    "ApiAdapter",
    "HybridAdapter",
    "LocalAdapter",
    "ModelAdapter",
    "StubAdapter",
]
