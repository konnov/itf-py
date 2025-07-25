"""
Python library to parse and emit Apalache ITF traces.
"""

from .itf import (
    ITFState,
    ITFTrace,
    state_from_json,
    state_to_json,
    trace_from_json,
    trace_to_json,
    value_from_json,
    value_to_json,
)

__version__ = "0.2.1"
__all__ = [
    "ITFState",
    "ITFTrace",
    "value_to_json",
    "value_from_json",
    "state_to_json",
    "state_from_json",
    "trace_to_json",
    "trace_from_json",
]
