import json
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any, Dict, List, Optional


@dataclass
class ITFState:
    """A single state in an ITF trace as a Python object."""

    meta: Dict[str, Any]
    values: Dict[str, Any]


@dataclass
class ITFTrace:
    """An ITF trace as a Python object."""

    meta: Dict[str, Any]
    params: List[str]
    vars: List[str]
    states: List[ITFState]
    loop: Optional[int]


@dataclass
class ITFUnserializable:
    """A placeholder for unserializable values."""

    value: str


def value_of_itf(val: Any) -> Any:
    """Decode a Python value from its ITF JSON representation"""
    if isinstance(val, dict):
        if "#bigint" in val:
            return int(val["#bigint"])
        elif "#tup" in val:
            return tuple(value_of_itf(v) for v in val["#tup"])
        elif "#set" in val:
            return frozenset(value_of_itf(v) for v in val["#set"])
        elif "#map" in val:
            return {value_of_itf(k): value_of_itf(v) for (k, v) in val["#map"]}
        elif "#unserializable" in val:
            return ITFUnserializable(value=val["#unserializable"])
        else:
            return SimpleNamespace(**{k: value_of_itf(v) for k, v in val.items()})
    elif isinstance(val, list):
        return [value_of_itf(v) for v in val]
    else:
        return val  # int, str, bool, or unserializable


def itf_of_value(val: Any) -> Any:
    """Encode a Python value to its ITF JSON representation"""
    if isinstance(val, bool):
        return val
    elif isinstance(val, int):
        return {"#bigint": str(val)}
    elif isinstance(val, tuple):
        return {"#tup": [itf_of_value(v) for v in val]}
    elif isinstance(val, frozenset):
        return {"#set": [itf_of_value(v) for v in val]}
    elif isinstance(val, dict):
        return {"#map": [[itf_of_value(k), itf_of_value(v)] for k, v in val.items()]}
    elif isinstance(val, list):
        return [itf_of_value(v) for v in val]
    elif hasattr(val, "__dict__"):
        return {k: itf_of_value(v) for k, v in val.__dict__.items()}
    elif isinstance(val, str):
        return val
    else:
        return ITFUnserializable(value=str(val))


def state_of_itf(raw_state: Dict[str, Any]) -> ITFState:
    """Decode a single ITFState from its ITF JSON representation"""
    state_meta = raw_state["#meta"] if "#meta" in raw_state else {}
    values = {k: value_of_itf(v) for k, v in raw_state.items() if k != "#meta"}
    return ITFState(meta=state_meta, values=values)


def itf_of_state(state: ITFState) -> Dict[str, Any]:
    """Encode a single ITFState to its ITF JSON representation"""
    result = {"#meta": state.meta}
    for k, v in state.values.items():
        result[k] = itf_of_value(v)
    return result


def trace_of_itf(data: Dict[str, Any]) -> ITFTrace:
    """Decode an ITFTrace from its ITF JSON representation"""
    meta = data["#meta"] if "#meta" in data else {}
    params = data.get("params", [])
    vars_ = data["vars"]
    loop = data.get("loop", None)
    states = [state_of_itf(s) for s in data["states"]]
    return ITFTrace(meta=meta, params=params, vars=vars_, states=states, loop=loop)


def load_itf(json_str: str) -> ITFTrace:
    """Load an ITF trace from a JSON string"""
    data = json.loads(json_str)
    return trace_of_itf(data)
