"""
Python library to parse and emit Apalache ITF traces.
"""

from .itf import (
    State,
    Trace,
    itf_variant,
    state_from_json,
    state_to_json,
    trace_from_json,
    trace_to_json,
    value_from_json,
    value_to_json,
)

__version__ = "0.2.1"
__all__ = [
    "State",
    "Trace",
    "itf_variant",
    "state_from_json",
    "state_to_json",
    "trace_from_json",
    "trace_to_json",
    "value_from_json",
    "value_to_json",
]
